import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;
  bool _isLoading = false;
  final storage = const FlutterSecureStorage();

  bool _isValidEmail(String email) {
    // Simple email validation to avoid complex regex issues
    return email.contains('@') && email.contains('.');
  }

  void _showErrorSnackbar(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  void _showSuccessSnackbar(String message) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.green,
        duration: const Duration(seconds: 2),
      ),
    );
  }

  Future<void> _login() async {
    // Validasi form
    if (!_formKey.currentState!.validate()) return;

    final email = _emailController.text.trim();
    final password = _passwordController.text;

    // Validasi email
    if (email.isEmpty || !_isValidEmail(email)) {
      _showErrorSnackbar('Format email tidak valid');
      return;
    }

    // Validasi password
    if (password.isEmpty || password.length < 6) {
      _showErrorSnackbar('Password minimal 6 karakter');
      return;
    }

    setState(() => _isLoading = true);

    try {
      debugPrint('🔄 Mencoba login dengan email: $email');

      // Nonaktifkan keyboard
      FocusScope.of(context).unfocus();

      // Retry logic untuk mengatasi Windows server issues
      http.Response? response;
      int retries = 0;
      const maxRetries = 3;

      while (retries < maxRetries && response == null) {
        try {
          debugPrint('📤 Attempt ${retries + 1}/$maxRetries...');

          response = await http
              .post(
            Uri.parse('${ApiService.baseUrl}/login'),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            body: jsonEncode({
              'email': email,
              'password': password,
            }),
          )
              .timeout(
            const Duration(seconds: 10),
            onTimeout: () {
              throw TimeoutException(
                  'Koneksi ke server timeout. Silakan coba lagi.');
            },
          );
        } on TimeoutException {
          retries++;
          if (retries >= maxRetries) {
            rethrow;
          }
          debugPrint('⏱️ Timeout, coba lagi... ($retries/$maxRetries)');
          await Future.delayed(const Duration(seconds: 1));
        }
      }

      if (response == null) {
        throw Exception('Failed to get response after $maxRetries attempts');
      }

      debugPrint('✅ Response Status: ${response.statusCode}');
      debugPrint('📥 Response Body: ${response.body}');

      if (!mounted) return;

      if (response.statusCode == 200) {
        // Parse response
        final responseData = jsonDecode(response.body);
        final token = responseData['token'];
        final user = responseData['user'];

        // Simpan token ke secure storage
        await storage.write(
          key: 'auth_token',
          value: token,
        );

        // Simpan user data (opsional)
        await storage.write(
          key: 'user_email',
          value: user['email'],
        );
        await storage.write(
          key: 'user_name',
          value: user['name'],
        );

        debugPrint('✅ Token saved to secure storage');
        debugPrint('✅ Login berhasil!');
        _showSuccessSnackbar('Login berhasil!');

        // Verify token was saved before navigating
        final verifyToken = await storage.read(key: 'auth_token');
        if (verifyToken == null) {
          debugPrint('❌ Failed to verify token saved');
          _showErrorSnackbar('Gagal menyimpan session. Coba lagi.');
          return;
        }

        debugPrint('✅ Token verified in storage');

        // Wait a moment to ensure storage is ready
        await Future.delayed(const Duration(milliseconds: 300));

        // Navigasi ke dashboard
        if (mounted) {
          Navigator.pushReplacementNamed(context, '/dashboard');
        }
      } else if (response.statusCode == 401) {
        _showErrorSnackbar('Email atau password salah');
      } else if (response.statusCode == 403) {
        _showErrorSnackbar('Akun Anda tidak aktif. Hubungi admin.');
      } else {
        final errorData = jsonDecode(response.body);
        final errorMsg = errorData['error'] ?? 'Login gagal';
        _showErrorSnackbar(errorMsg);
      }
    } on TimeoutException {
      if (!mounted) return;
      _showErrorSnackbar(
          'Koneksi timeout. Periksa apakah server berjalan.\nURL: ${ApiService.baseUrl}');
    } catch (e) {
      if (!mounted) return;
      debugPrint('❌ Error: $e');
      _showErrorSnackbar(
          'Terjadi kesalahan: ${e.toString()}\nURL: ${ApiService.baseUrl}');
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) {
        // Prevent back navigation from login page
        if (didPop) return;
      },
      child: Scaffold(
        backgroundColor: Colors.white,
        body: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Form(
              key: _formKey,
              child: Column(
                children: [
                  // Logo/Icon BakeSmart
                  const SizedBox(height: 60),
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      color: const Color(0xFFA855F7),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Icon(
                      Icons.cake,
                      color: Colors.white,
                      size: 48,
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Title
                  const Text(
                    'BakeSmart',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFFA855F7),
                    ),
                  ),
                  const SizedBox(height: 32),

                  // Subtitle
                  const Text(
                    'Selamat Datang di BakeSmart!',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Kelola bahan baku Anda dengan cerdas.',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 40),

                  // Email Label
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Email atau Nama Pengguna',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w500,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Email Field
                  TextFormField(
                    controller: _emailController,
                    decoration: InputDecoration(
                      hintText: 'Masukkan email atau nama pengguna',
                      prefixIcon:
                          const Icon(Icons.email_outlined, color: Colors.grey),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide:
                            const BorderSide(color: Colors.grey, width: 1),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                            color: Color(0xFFE5E7EB), width: 1),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                            color: Color(0xFFA855F7), width: 1),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 12),
                    ),
                    keyboardType: TextInputType.emailAddress,
                    textInputAction: TextInputAction.next,
                    autofillHints: const [AutofillHints.email],
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Email tidak boleh kosong';
                      }
                      if (!_isValidEmail(value)) {
                        return 'Masukkan email yang valid';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),

                  // Password Label
                  const Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      'Kata Sandi',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w500,
                        color: Colors.grey,
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Password Field
                  TextFormField(
                    controller: _passwordController,
                    obscureText: _obscurePassword,
                    decoration: InputDecoration(
                      hintText: 'Masukkan kata sandi Anda',
                      prefixIcon:
                          const Icon(Icons.lock_outline, color: Colors.grey),
                      suffixIcon: GestureDetector(
                        onTap: () {
                          setState(() => _obscurePassword = !_obscurePassword);
                        },
                        child: Icon(
                          _obscurePassword
                              ? Icons.visibility_off
                              : Icons.visibility,
                          color: Colors.grey,
                        ),
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide:
                            const BorderSide(color: Colors.grey, width: 1),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                            color: Color(0xFFE5E7EB), width: 1),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                            color: Color(0xFFA855F7), width: 1),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 12),
                    ),
                    textInputAction: TextInputAction.done,
                    onFieldSubmitted: (_) => _login(),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Password tidak boleh kosong';
                      }
                      if (value.length < 6) {
                        return 'Password minimal 6 karakter';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 24),

                  // Login Button
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _login,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFA855F7),
                        disabledBackgroundColor: Colors.grey[400],
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: _isLoading
                          ? const SizedBox(
                              width: 24,
                              height: 24,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                valueColor:
                                    AlwaysStoppedAnimation<Color>(Colors.white),
                              ),
                            )
                          : const Text(
                              'Masuk',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Forgot Password Link
                  GestureDetector(
                    onTap: () {
                      // TODO: Implement forgot password
                    },
                    child: const Text(
                      'Lupa Kata Sandi?',
                      style: TextStyle(
                        fontSize: 13,
                        color: Color(0xFFA855F7),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),

                  // Divider with "ATAU"
                  Row(
                    children: [
                      const Expanded(
                        child: Divider(
                          color: Color(0xFFE5E7EB),
                          thickness: 1,
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        child: Text(
                          'ATAU',
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey[600],
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                      const Expanded(
                        child: Divider(
                          color: Color(0xFFE5E7EB),
                          thickness: 1,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),

                  // Register Button
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: OutlinedButton(
                      onPressed: () {
                        // TODO: Navigate to register page
                      },
                      style: OutlinedButton.styleFrom(
                        side: const BorderSide(
                          color: Color(0xFFA855F7),
                          width: 1.5,
                        ),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                      ),
                      child: const Text(
                        'Daftar Akun Baru',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFFA855F7),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
