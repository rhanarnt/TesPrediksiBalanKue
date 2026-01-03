import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class InputDataPage extends StatefulWidget {
  const InputDataPage({super.key});

  @override
  State<InputDataPage> createState() => _InputDataPageState();
}

class _InputDataPageState extends State<InputDataPage> {
  final _jumlahController = TextEditingController();
  final _bahanBaruController = TextEditingController();
  final _storage = const FlutterSecureStorage();
  String _selectedUnit = 'Kilogram (kg)';
  String? _selectedFile;
  bool _isLoading = false;
  bool _isLoadingBahan = true;

  // Bahan selection
  List<Map<String, dynamic>> _bahanList = [];
  int? _selectedBahanId;
  String? _selectedBahanName;

  // Available units with mapping from backend format
  final Map<String, String> _unitMapping = {
    'gram': 'Gram (g)',
    'g': 'Gram (g)',
    'kilogram': 'Kilogram (kg)',
    'kg': 'Kilogram (kg)',
    'liter': 'Liter (L)',
    'l': 'Liter (L)',
    'mililiter': 'Mililiter (ml)',
    'ml': 'Mililiter (ml)',
    'butir': 'Butir',
    'bungkus': 'Bungkus',
  };

  final List<String> _availableUnits = [
    'Gram (g)',
    'Kilogram (kg)',
    'Liter (L)',
    'Mililiter (ml)',
    'Butir',
    'Bungkus',
  ];

  // Convert backend unit format to display format
  String _normalizeUnit(String? unit) {
    if (unit == null || unit.isEmpty) {
      return 'Kilogram (kg)';
    }
    final normalized = _unitMapping[unit.toLowerCase().trim()];
    return normalized ?? 'Kilogram (kg)';
  }

  @override
  void initState() {
    super.initState();
    _loadBahanList();
  }

  Future<void> _loadBahanList() async {
    try {
      final token = await _storage.read(key: 'auth_token');

      if (token == null) {
        setState(() {
          _isLoadingBahan = false;
        });
        return;
      }

      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/stok'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        final bahanData =
            List<Map<String, dynamic>>.from(jsonResponse['data'] ?? []);

        setState(() {
          _bahanList = bahanData;
          _isLoadingBahan = false;
          // Set default selected bahan
          if (_bahanList.isNotEmpty) {
            _selectedBahanId = _bahanList[0]['id'] as int?;
            _selectedBahanName = _bahanList[0]['nama'] as String?;
            // Normalize unit from backend format to display format
            String bahanUnit = _bahanList[0]['unit'] as String? ?? '';
            _selectedUnit = _normalizeUnit(bahanUnit);
          }
        });
      } else {
        setState(() {
          _isLoadingBahan = false;
        });
      }
    } catch (e) {
      debugPrint('Error loading bahan: $e');
      setState(() {
        _isLoadingBahan = false;
      });
    }
  }

  @override
  void dispose() {
    _jumlahController.dispose();
    _bahanBaruController.dispose();
    super.dispose();
  }

  void _showErrorSnackbar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _showSuccessSnackbar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.green,
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _showDialogBahanBaru() {
    _bahanBaruController.clear();
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Buat Bahan Baru'),
          content: TextField(
            controller: _bahanBaruController,
            decoration: InputDecoration(
              hintText: 'Nama bahan (contoh: Bawang Merah)',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            maxLines: 1,
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Batal'),
            ),
            ElevatedButton(
              onPressed: () {
                final namaBahan = _bahanBaruController.text.trim();
                if (namaBahan.isEmpty) {
                  _showErrorSnackbar('Nama bahan tidak boleh kosong');
                  return;
                }
                Navigator.pop(context);
                _tambahkanBahanBaru(namaBahan);
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF5B5BF5),
              ),
              child: const Text('Buat', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }

  Future<void> _tambahkanBahanBaru(String namaBahan) async {
    setState(() => _isLoading = true);

    try {
      final token = await _storage.read(key: 'auth_token');

      if (token == null) {
        _showErrorSnackbar('Token tidak ditemukan. Silakan login lagi');
        setState(() => _isLoading = false);
        return;
      }

      final response = await http
          .post(
            Uri.parse('${ApiService.baseUrl}/stok'),
            headers: {
              'Authorization': 'Bearer $token',
              'Content-Type': 'application/json',
            },
            body: jsonEncode({
              'nama': namaBahan,
              'unit': 'Kilogram (kg)', // Default unit
              'stok': 0,
            }),
          )
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 201 || response.statusCode == 200) {
        _showSuccessSnackbar('Bahan "$namaBahan" berhasil dibuat!');
        // Reload bahan list
        await _loadBahanList();
      } else {
        final errorBody = jsonDecode(response.body);
        _showErrorSnackbar(errorBody['message'] ?? 'Gagal membuat bahan baru');
      }
    } catch (e) {
      debugPrint('Error creating bahan: $e');
      _showErrorSnackbar('Error: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _tambahkanItem() async {
    final jumlah = _jumlahController.text.trim();

    if (_selectedBahanId == null) {
      _showErrorSnackbar('Pilih bahan terlebih dahulu');
      return;
    }

    if (jumlah.isEmpty) {
      _showErrorSnackbar('Jumlah tidak boleh kosong');
      return;
    }

    if (double.tryParse(jumlah) == null) {
      _showErrorSnackbar('Jumlah harus berupa angka');
      return;
    }

    setState(() => _isLoading = true);

    try {
      // Get token dari secure storage
      final token = await _storage.read(key: 'auth_token');

      if (token == null) {
        _showErrorSnackbar('Token tidak ditemukan. Silakan login lagi');
        return;
      }

      // Retry logic untuk handle Windows server issues
      http.Response? response;
      int retries = 0;
      const maxRetries = 3;

      while (retries < maxRetries && response == null) {
        try {
          response = await http
              .post(
                Uri.parse('${ApiService.baseUrl}/stock-record'),
                headers: {
                  'Authorization': 'Bearer $token',
                  'Content-Type': 'application/json',
                },
                body: jsonEncode({
                  'bahan_nama':
                      _selectedBahanName, // Send ingredient name to support auto-creation
                  'jumlah': double.parse(jumlah),
                  'unit': _selectedUnit,
                  'tipe': 'masuk', // Input = masuk
                  'catatan': 'Input manual dari aplikasi',
                }),
              )
              .timeout(
                const Duration(seconds: 10),
                onTimeout: () => throw TimeoutException('Request timeout'),
              );
        } on TimeoutException {
          retries++;
          if (retries >= maxRetries) rethrow;
          await Future.delayed(const Duration(seconds: 1));
        }
      }

      if (response == null) {
        throw Exception('Failed to get response after $maxRetries attempts');
      }

      if (response?.statusCode == 201) {
        final selectedBahan =
            _bahanList.firstWhere((b) => b['id'] == _selectedBahanId);
        final namaBahan = selectedBahan['nama'] as String? ?? 'Unknown';

        _showSuccessSnackbar(
            '✅ $namaBahan ditambahkan ($jumlah $_selectedUnit)');

        // Clear form
        _jumlahController.clear();
        setState(() {
          _selectedUnit = 'Kilogram (kg)';
          if (_bahanList.isNotEmpty) {
            _selectedBahanId = _bahanList[0]['id'] as int?;
            _selectedBahanName = _bahanList[0]['nama'] as String?;
          }
        });

        debugPrint('📝 Data disimpan ke database');
        debugPrint('   Nama: $namaBahan');
        debugPrint('   Jumlah: $jumlah $_selectedUnit');

        // Wait a moment then navigate back to dashboard with refresh
        await Future.delayed(const Duration(milliseconds: 500));
        if (mounted) {
          Navigator.pop(
              context, true); // Return true to indicate data was added
        }
      } else {
        final errorData = jsonDecode(response?.body ?? '{}');
        _showErrorSnackbar('Gagal menyimpan: ${errorData['error']}');
      }
    } on TimeoutException {
      _showErrorSnackbar('Koneksi timeout. Pastikan backend running.');
    } catch (e) {
      debugPrint('❌ Error: $e');
      _showErrorSnackbar('Error: ${e.toString()}');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _selectFile() {
    setState(() {
      _selectedFile = 'data_stok.csv';
    });
    _showSuccessSnackbar('File dipilih: data_stok.csv');
  }

  void _uploadCsv() {
    if (_selectedFile == null) {
      _showErrorSnackbar('Pilih file terlebih dahulu');
      return;
    }
    _showSuccessSnackbar('File CSV berhasil diunggah');
    setState(() => _selectedFile = null);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFAFAFA),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header with back button
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.white,
                border: Border(
                  bottom: BorderSide(color: Colors.grey[200]!),
                ),
              ),
              child: SafeArea(
                child: Row(
                  children: [
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: const Icon(Icons.arrow_back,
                          color: Colors.black, size: 24),
                    ),
                    const SizedBox(width: 16),
                    const Expanded(
                      child: Text(
                        'Input Data',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: Colors.black,
                        ),
                      ),
                    ),
                    GestureDetector(
                      onTap: () {},
                      child: Icon(
                        Icons.notifications_rounded,
                        color: Colors.grey[600],
                        size: 24,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Main content
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ========== ENTRI DATA MANUAL ==========
                  const Text(
                    'Entri Data Manual',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Nama Bahan
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'Nama Bahan',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          color: Colors.black,
                        ),
                      ),
                      GestureDetector(
                        onTap: _showDialogBahanBaru,
                        child: const Text(
                          '+ Buat Baru',
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF5B5BF5),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  if (_isLoadingBahan)
                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Center(
                        child: SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(
                              Color(0xFF5B5BF5),
                            ),
                          ),
                        ),
                      ),
                    )
                  else if (_bahanList.isEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 12),
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(8),
                        color: Colors.grey[50],
                      ),
                      child: const Center(
                        child: Text(
                          'Tidak ada bahan tersedia',
                          style: TextStyle(
                            fontSize: 13,
                            color: Color(0xFF9CA3AF),
                          ),
                        ),
                      ),
                    )
                  else
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12),
                      decoration: BoxDecoration(
                        border: Border.all(color: const Color(0xFFE5E7EB)),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: DropdownButton<int>(
                        value: _selectedBahanId,
                        isExpanded: true,
                        underline: const SizedBox(),
                        items: _bahanList.map((bahan) {
                          return DropdownMenuItem<int>(
                            value: bahan['id'] as int,
                            child: Text(
                              bahan['nama'] as String? ?? 'Unknown',
                              style: const TextStyle(
                                fontSize: 13,
                                color: Colors.black,
                              ),
                            ),
                          );
                        }).toList(),
                        onChanged: (value) {
                          if (value != null) {
                            final selectedBahan =
                                _bahanList.firstWhere((b) => b['id'] == value);
                            setState(() {
                              _selectedBahanId = value;
                              _selectedBahanName =
                                  selectedBahan['nama'] as String?;
                              // Normalize unit from backend format to display format
                              String bahanUnit =
                                  selectedBahan['unit'] as String? ?? '';
                              _selectedUnit = _normalizeUnit(bahanUnit);
                            });
                          }
                        },
                      ),
                    ),
                  const SizedBox(height: 16),

                  // Jumlah
                  const Text(
                    'Jumlah',
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextField(
                    controller: _jumlahController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: '500',
                      hintStyle: const TextStyle(
                        fontSize: 13,
                        color: Color(0xFFD1D5DB),
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFFE5E7EB),
                          width: 1,
                        ),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFFE5E7EB),
                          width: 1,
                        ),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFF5B5BF5),
                          width: 2,
                        ),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 12,
                      ),
                      filled: true,
                      fillColor: Colors.white,
                    ),
                    style: const TextStyle(
                      fontSize: 13,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Unit Dropdown
                  const Text(
                    'Unit',
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 8),
                  DropdownButtonFormField<String>(
                    value: _selectedUnit,
                    onChanged: (value) {
                      setState(() => _selectedUnit = value ?? 'Kilogram (kg)');
                    },
                    decoration: InputDecoration(
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFFE5E7EB),
                          width: 1,
                        ),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFFE5E7EB),
                          width: 1,
                        ),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: const BorderSide(
                          color: Color(0xFF5B5BF5),
                          width: 2,
                        ),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 14,
                        vertical: 12,
                      ),
                      filled: true,
                      fillColor: Colors.white,
                    ),
                    items: _availableUnits
                        .map((unit) => DropdownMenuItem(
                              value: unit,
                              child: Text(
                                unit,
                                style: const TextStyle(fontSize: 13),
                              ),
                            ))
                        .toList(),
                  ),
                  const SizedBox(height: 20),

                  // Tambahkan Item Button
                  SizedBox(
                    width: double.infinity,
                    height: 44,
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _tambahkanItem,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: _isLoading
                            ? const Color(0xFF5B5BF5).withValues(alpha: 0.6)
                            : const Color(0xFF5B5BF5),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        elevation: 0,
                      ),
                      child: _isLoading
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  Colors.white,
                                ),
                                strokeWidth: 2,
                              ),
                            )
                          : const Text(
                              'Tambahkan Item',
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                    ),
                  ),
                  const SizedBox(height: 32),

                  // ========== UNGGAH FILE DATA (CSV) ==========
                  const Text(
                    'Unggah File Data (CSV)',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Unggah file CSV yang berisi data penjualan atau stok Anda.',
                    style: TextStyle(
                      fontSize: 13,
                      color: Color(0xFF6B7280),
                      height: 1.5,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // File upload area
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 20,
                    ),
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: const Color(0xFFE5E7EB),
                        width: 1,
                      ),
                      borderRadius: BorderRadius.circular(8),
                      color: Colors.white,
                    ),
                    child: Column(
                      children: [
                        Container(
                          width: 48,
                          height: 48,
                          decoration: BoxDecoration(
                            color: const Color(0xFFF3F4F6),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Icon(
                            Icons.cloud_download_outlined,
                            color: Color(0xFF9CA3AF),
                            size: 24,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Text(
                          _selectedFile ?? 'Tidak ada file terpilih',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w500,
                            color: _selectedFile != null
                                ? Colors.black
                                : const Color(0xFF9CA3AF),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Pilih File and Unggah Data buttons row
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: _selectFile,
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(
                              color: Color(0xFFE5E7EB),
                              width: 1,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(8),
                            ),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(
                                Icons.download_rounded,
                                size: 18,
                                color: Color(0xFF5B5BF5),
                              ),
                              const SizedBox(width: 8),
                              const Text(
                                'Pilih File',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: Color(0xFF5B5BF5),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  // Unggah Data Button
                  SizedBox(
                    width: double.infinity,
                    height: 44,
                    child: ElevatedButton(
                      onPressed: _uploadCsv,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF5B5BF5),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        elevation: 0,
                      ),
                      child: const Text(
                        'Unggah Data',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w600,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
