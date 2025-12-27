import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';
import 'stok_detail_page.dart';

class OptimiasiStokPage extends StatefulWidget {
  const OptimiasiStokPage({super.key});

  @override
  State<OptimiasiStokPage> createState() => _OptimiasiStokPageState();
}

class _OptimiasiStokPageState extends State<OptimiasiStokPage> {
  final storage = const FlutterSecureStorage();
  bool _isLoading = true;
  List<Map<String, dynamic>> _optimasiList = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    loadOptimaiData();
  }

  Future<void> loadOptimaiData() async {
    try {
      setState(() {
        _isLoading = true;
        _errorMessage = null;
      });

      final token = await storage.read(key: 'auth_token');
      if (token == null) {
        setState(() {
          _errorMessage = 'Token tidak ditemukan. Silakan login lagi.';
          _isLoading = false;
        });
        return;
      }

      // Retry logic untuk handle network issues
      http.Response? response;
      int retries = 0;
      const maxRetries = 3;

      while (retries < maxRetries && response == null) {
        try {
          debugPrint('📤 Fetching optimasi data (attempt ${retries + 1})...');

          response = await http.get(
            Uri.parse('${ApiService.baseUrl}/optimasi'),
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer $token',
            },
          ).timeout(
            const Duration(seconds: 10),
            onTimeout: () => throw TimeoutException(
                'Koneksi timeout saat mengambil data optimasi'),
          );

          debugPrint('✅ Response status: ${response.statusCode}');
        } on TimeoutException {
          retries++;
          if (retries < maxRetries) {
            await Future.delayed(const Duration(seconds: 1));
          }
        }
      }

      if (response == null) {
        throw Exception(
            'Gagal terhubung ke server setelah $maxRetries percobaan');
      }

      if (response?.statusCode == 200) {
        final jsonResponse = jsonDecode(response?.body ?? '{}');
        final List<dynamic> bahanList = jsonResponse['data'] ?? [];

        setState(() {
          _optimasiList = List<Map<String, dynamic>>.from(bahanList);
          _isLoading = false;
        });

        debugPrint(
            '✅ Loaded ${_optimasiList.length} optimasi records from API');
      } else if (response?.statusCode == 401) {
        setState(() {
          _errorMessage = 'Token expired. Silakan login kembali.';
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Gagal mengambil data: ${response!.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      debugPrint('❌ Error loading optimasi: $e');
      setState(() {
        _errorMessage = 'Terjadi kesalahan: $e';
        _isLoading = false;
      });
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'Kritis':
        return Colors.red;
      case 'Kurang':
        return Colors.orange;
      case 'Optimal':
        return const Color(0xFF7C3AED);
      case 'Cukup':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFAFAFA),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header
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
                    const Expanded(
                      child: Text(
                        'Optimasi Stok',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: Colors.black,
                        ),
                      ),
                    ),
                    GestureDetector(
                      onTap: loadOptimaiData,
                      child: Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.grey[100],
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: const Icon(Icons.refresh,
                            color: Colors.black, size: 20),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Main content
            if (_isLoading)
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.6,
                child: const Center(
                  child: CircularProgressIndicator(
                    color: Color(0xFFA855F7),
                  ),
                ),
              )
            else if (_errorMessage != null)
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.6,
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline,
                          color: Colors.red, size: 48),
                      const SizedBox(height: 16),
                      Text(
                        _errorMessage!,
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 14,
                          color: Colors.grey,
                        ),
                      ),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: loadOptimaiData,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFFA855F7),
                        ),
                        child: const Text('Coba Lagi'),
                      ),
                    ],
                  ),
                ),
              )
            else if (_optimasiList.isEmpty)
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.6,
                child: const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.inbox, color: Colors.grey, size: 48),
                      SizedBox(height: 16),
                      Text(
                        'Belum ada data optimasi',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              )
            else
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Rekomendasi Tingkat Stok Header
                    const Text(
                      'Rekomendasi Tingkat Stok',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w700,
                        color: Colors.black,
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Pantau dan kelola tingkat stok bahan Anda dengan rekomendasi yang dioptimalkan untuk efisiensi.',
                      style: TextStyle(
                        fontSize: 13,
                        color: Color(0xFF6B7280),
                        height: 1.5,
                      ),
                    ),
                    const SizedBox(height: 20),

                    // Stock Items List
                    ..._optimasiList.asMap().entries.map((entry) {
                      final index = entry.key;
                      final item = entry.value;

                      return Padding(
                        padding: EdgeInsets.only(
                            bottom: index == _optimasiList.length - 1 ? 0 : 12),
                        child: _buildStockCard(
                          context: context,
                          bahanName: item['nama'] ?? 'Unknown',
                          currentStock:
                              '${item['current_stock']?.toStringAsFixed(1) ?? '0'} ${item['unit'] ?? ''}',
                          recommendedStock:
                              '${item['stok_optimal']?.toStringAsFixed(1) ?? '0'} ${item['unit'] ?? ''}',
                          status: item['status'] ?? 'Unknown',
                          statusColor: _getStatusColor(item['status'] ?? ''),
                          onDetailTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => StokDetailPage(bahan: item),
                              ),
                            );
                          },
                          bahanId: item['bahan_id'],
                        ),
                      );
                    }).toList(),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildStockCard({
    required BuildContext context,
    required String bahanName,
    required String currentStock,
    required String recommendedStock,
    required String status,
    required Color statusColor,
    required VoidCallback onDetailTap,
    required int bahanId,
  }) {
    return GestureDetector(
      onTap: onDetailTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: const Color(0xFFE5E7EB)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Top row: name and gear icon
            Row(
              children: [
                Expanded(
                  child: Text(
                    bahanName,
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                      color: Colors.black,
                    ),
                  ),
                ),
                GestureDetector(
                  onTap: onDetailTap,
                  child: Container(
                    width: 32,
                    height: 32,
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Icon(
                      Icons.settings_rounded,
                      color: Colors.grey[400],
                      size: 16,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Stock info rows
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Stok Saat Ini',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF9CA3AF),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        currentStock,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: Colors.black,
                        ),
                      ),
                    ],
                  ),
                ),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Rekomendasi Stok',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF9CA3AF),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        recommendedStock,
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: Color(0xFFA855F7),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Status and Button row
            Row(
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Status',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                        color: Color(0xFF9CA3AF),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: statusColor.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        status,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: statusColor,
                        ),
                      ),
                    ),
                  ],
                ),
                const Spacer(),
                Expanded(
                  child: SizedBox(
                    height: 36,
                    child: ElevatedButton(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content:
                                Text('Fitur pesan ulang sedang dikembangkan'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF5B5BF5),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(6),
                        ),
                        padding: EdgeInsets.zero,
                        elevation: 0,
                      ),
                      child: const Text(
                        'Pesan Ulang',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
