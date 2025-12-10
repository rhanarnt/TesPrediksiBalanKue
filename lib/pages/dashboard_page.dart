import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../services/api_service.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => DashboardPageState();
}

class DashboardPageState extends State<DashboardPage> {
  final storage = const FlutterSecureStorage();
  bool _isLoading = true;
  List<Map<String, dynamic>> _bahanList = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    loadBahanData();
  }

  Future<void> loadBahanData() async {
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

      // Retry logic untuk handle Windows server issues
      http.Response? response;
      int retries = 0;
      const maxRetries = 3;

      while (retries < maxRetries && response == null) {
        try {
          response = await http.get(
            Uri.parse('${ApiService.baseUrl}/stock-records'),
            headers: {
              'Authorization': 'Bearer $token',
              'Content-Type': 'application/json',
            },
          ).timeout(
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

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        final bahanData = List<Map<String, dynamic>>.from(responseData['data']);

        // Reverse untuk menampilkan data terbaru di atas
        bahanData.sort((a, b) => DateTime.parse(b['tanggal'] as String)
            .compareTo(DateTime.parse(a['tanggal'] as String)));

        setState(() {
          _bahanList = bahanData;
          _isLoading = false;
        });

        debugPrint('✅ Loaded ${_bahanList.length} stock records from API');
      } else if (response.statusCode == 401) {
        setState(() {
          _errorMessage = 'Sesi Anda telah berakhir. Silakan login lagi.';
          _isLoading = false;
        });
        // Redirect to login
        if (mounted) {
          Navigator.pushReplacementNamed(context, '/login');
        }
      } else {
        setState(() {
          _errorMessage =
              'Gagal mengambil data: ${response?.statusCode ?? "Unknown"}';
          _isLoading = false;
        });
      }
    } catch (e) {
      debugPrint('❌ Error loading bahan: $e');
      setState(() {
        _errorMessage = 'Error: ${e.toString()}';
        _isLoading = false;
      });
    }
  }

  int _countLowStock() {
    // Count items yang stok minimum belum terpenuhi
    // Untuk sekarang, kita asumsikan jika tidak ada data tentang current stock,
    // return 0. Di fase selanjutnya, ini akan diupdate dengan real data
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          // Header with BakeSmart logo and notification
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
                  Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      color: const Color(0xFFA855F7),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: const Icon(
                      Icons.shopping_bag_rounded,
                      color: Colors.white,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 8),
                  const Text(
                    'BakeSmart',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: Colors.black,
                    ),
                  ),
                  const Spacer(),
                  GestureDetector(
                    onTap: () => Navigator.pushNamed(context, '/notifications'),
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

          // Loading State
          if (_isLoading)
            Padding(
              padding: const EdgeInsets.all(32.0),
              child: Column(
                children: [
                  const CircularProgressIndicator(
                    valueColor:
                        AlwaysStoppedAnimation<Color>(Color(0xFFA855F7)),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Memuat data stok...',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),

          // Error State
          if (_errorMessage != null)
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Card(
                color: Colors.red[50],
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Column(
                    children: [
                      Text(
                        _errorMessage!,
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.red[700],
                        ),
                      ),
                      const SizedBox(height: 8),
                      ElevatedButton.icon(
                        onPressed: loadBahanData,
                        icon: const Icon(Icons.refresh),
                        label: const Text('Coba Lagi'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.red[700],
                          foregroundColor: Colors.white,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),

          // Ringkasan Stok
          if (!_isLoading && _errorMessage == null)
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Ringkasan Stok',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _buildSummaryCard(
                          icon: Icons.inventory_2_rounded,
                          iconColor: const Color(0xFF7C3AED),
                          iconBgColor: const Color(0xFF7C3AED),
                          title: 'Total Item',
                          value: '${_bahanList.length} Bahan',
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _buildSummaryCard(
                          icon: Icons.error_rounded,
                          iconColor: const Color(0xFFDC2626),
                          iconBgColor: const Color(0xFFDC2626),
                          title: 'Stok Rendah',
                          value: '${_countLowStock()} Item',
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  _buildSummaryCard(
                    icon: Icons.schedule_rounded,
                    iconColor: const Color(0xFFF59E0B),
                    iconBgColor: const Color(0xFFF59E0B),
                    title: 'Daftar Bahan',
                    value: 'Lihat Detail',
                  ),
                ],
              ),
            ),

          // Data Input Terbaru
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Data Input Terbaru',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 16),
                if (_bahanList.isEmpty)
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: const Color(0xFFE5E7EB)),
                    ),
                    child: const Center(
                      child: Text(
                        'Belum ada data input',
                        style: TextStyle(
                          fontSize: 14,
                          color: Color(0xFF9CA3AF),
                        ),
                      ),
                    ),
                  )
                else
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: _bahanList.length > 5 ? 5 : _bahanList.length,
                    itemBuilder: (context, index) {
                      final item = _bahanList[index];
                      return _buildStockRecordCard(item);
                    },
                  ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Tren Penjualan
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Tren Penjualan',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE5E7EB)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Penjualan Bulanan',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF6B7280),
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Performa penjualan dalam 6 bulan terakhir.',
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFF9CA3AF),
                          height: 1.4,
                        ),
                      ),
                      const SizedBox(height: 20),
                      _buildBarChart(),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Prediksi Permintaan
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Prediksi Permintaan',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFE5E7EB)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Prediksi Permintaan Mingguan',
                        style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w500,
                          color: Color(0xFF6B7280),
                        ),
                      ),
                      const SizedBox(height: 4),
                      const Text(
                        'Perbandingan aktual vs prediksi permintaan bahan utama.',
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFF9CA3AF),
                          height: 1.4,
                        ),
                      ),
                      const SizedBox(height: 20),
                      _buildLineChart(),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Peringatan Terbaru
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Peringatan Terbaru',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 16),
                // Alert 1: Stok Rendah
                _buildAlertCard(
                  icon: Icons.error_rounded,
                  iconColor: const Color(0xFFDC2626),
                  borderColor: const Color(0xFFDC2626),
                  backgroundColor: const Color(0xFFFEE2E2),
                  title: 'Stok Rendah',
                  message: 'Tepung Terigu mendekati habis. Sisa 5 kg.',
                  timestamp: '2 jam lalu',
                  buttonText: 'Lihat Detail',
                  buttonColor: const Color(0xFFDC2626),
                ),
                const SizedBox(height: 12),
                // Alert 2: Prediksi Permintaan
                _buildAlertCard(
                  icon: Icons.trending_up_rounded,
                  iconColor: const Color(0xFFF59E0B),
                  borderColor: const Color(0xFFF59E0B),
                  backgroundColor: const Color(0xFFFEF3C7),
                  title: 'Prediksi Permintaan',
                  message: 'Permintaan roti tawar meningkat 15% minggu ini.',
                  timestamp: 'Kemarin',
                  buttonText: 'Lihat Detail',
                  buttonColor: const Color(0xFFF59E0B),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  static Widget _buildSummaryCard({
    required IconData icon,
    required Color iconColor,
    required Color iconBgColor,
    required String title,
    required String value,
  }) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE5E7EB)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: iconBgColor.withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: iconColor, size: 20),
          ),
          const SizedBox(height: 10),
          Text(
            title,
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: Color(0xFF6B7280),
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: Colors.black,
            ),
          ),
        ],
      ),
    );
  }

  static Widget _buildAlertCard({
    required IconData icon,
    required Color iconColor,
    required Color borderColor,
    required Color backgroundColor,
    required String title,
    required String message,
    required String timestamp,
    required String buttonText,
    required Color buttonColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(8),
        border: Border(left: BorderSide(color: borderColor, width: 4)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: iconColor, size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                    color: iconColor,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  message,
                  style: const TextStyle(
                    fontSize: 12,
                    color: Color(0xFF6B7280),
                    height: 1.4,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  timestamp,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF9CA3AF),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          TextButton(
            onPressed: () {},
            style: TextButton.styleFrom(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            ),
            child: Text(
              buttonText,
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: buttonColor,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStockRecordCard(Map<String, dynamic> record) {
    final nama = record['nama_bahan'] ?? 'Bahan Tidak Diketahui';
    final jumlah = record['jumlah'] ?? 0;
    final unit = record['unit'] ?? '';
    final tipe = record['tipe'] ?? 'masuk';
    final tanggal = record['tanggal'] != null
        ? DateTime.parse(record['tanggal']).toString().substring(0, 16)
        : 'Tanggal Tidak Ada';

    final tipeColor = tipe == 'masuk'
        ? const Color(0xFF10B981)
        : tipe == 'keluar'
            ? const Color(0xFFDC2626)
            : const Color(0xFFF59E0B);

    final tipeLabel = tipe == 'masuk'
        ? '📥 Masuk'
        : tipe == 'keluar'
            ? '📤 Keluar'
            : '⚠️  Penyesuaian';

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFE5E7EB)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: tipeColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Center(
              child: Text(
                tipe == 'masuk'
                    ? '⬆️'
                    : tipe == 'keluar'
                        ? '⬇️'
                        : '⚖️',
                style: const TextStyle(fontSize: 18),
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  nama,
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: Colors.black,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: tipeColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        tipeLabel,
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                          color: tipeColor,
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      tanggal,
                      style: const TextStyle(
                        fontSize: 11,
                        color: Color(0xFF9CA3AF),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(width: 8),
          Text(
            '$jumlah $unit',
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w700,
              color: tipeColor,
            ),
          ),
        ],
      ),
    );
  }

  // Custom Bar Chart untuk Tren Penjualan
  static Widget _buildBarChart() {
    final barData = [1800, 2800, 2300, 2900, 1800, 3300];
    final labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'];
    final maxValue = barData.reduce((a, b) => a > b ? a : b).toDouble();

    return SizedBox(
      height: 200,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: List.generate(
          barData.length,
          (index) {
            final percentage = barData[index] / maxValue;
            return Column(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Container(
                  width: 32,
                  height: 140 * percentage,
                  decoration: BoxDecoration(
                    color: const Color(0xFF5B5BF5),
                    borderRadius: const BorderRadius.vertical(
                      top: Radius.circular(4),
                    ),
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  labels[index],
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: Color(0xFF6B7280),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  // Custom Line Chart untuk Prediksi Permintaan
  static Widget _buildLineChart() {
    return SizedBox(
      height: 150,
      child: Stack(
        children: [
          // Grid background
          Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: List.generate(
              5,
              (index) => Container(
                width: double.infinity,
                height: 1,
                color: const Color(0xFFE5E7EB),
              ),
            ),
          ),
          // Line chart
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: CustomPaint(
              size: const Size(double.infinity, 150),
              painter: LineChartPainter(),
            ),
          ),
          // Labels
          Positioned(
            bottom: 8,
            left: 0,
            right: 0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                'Minggu 1',
                'Minggu 2',
                'Minggu 3',
                'Minggu 4',
                'Minggu 5',
              ]
                  .map(
                    (label) => Text(
                      label,
                      style: const TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w500,
                        color: Color(0xFF6B7280),
                      ),
                    ),
                  )
                  .toList(),
            ),
          ),
        ],
      ),
    );
  }
}

// Custom painter untuk line chart
class LineChartPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = const Color(0xFF5B5BF5)
      ..strokeWidth = 2
      ..strokeCap = StrokeCap.round;

    // Data points for line chart (normalized to canvas size)
    final points = [
      Offset(size.width * 0.1, size.height * 0.6),
      Offset(size.width * 0.3, size.height * 0.5),
      Offset(size.width * 0.5, size.height * 0.45),
      Offset(size.width * 0.7, size.height * 0.35),
      Offset(size.width * 0.9, size.height * 0.25),
    ];

    // Draw line
    for (int i = 0; i < points.length - 1; i++) {
      canvas.drawLine(points[i], points[i + 1], paint);
    }

    // Draw circles at points
    final circlePaint = Paint()
      ..color = const Color(0xFF5B5BF5)
      ..style = PaintingStyle.fill;

    for (var point in points) {
      canvas.drawCircle(point, 4, circlePaint);
    }

    // Draw filled area under line
    final pathPaint = Paint()
      ..color = const Color(0xFF5B5BF5).withValues(alpha: 0.15)
      ..style = PaintingStyle.fill;

    final path = Path();
    path.moveTo(points[0].dx, points[0].dy);
    for (int i = 1; i < points.length; i++) {
      path.lineTo(points[i].dx, points[i].dy);
    }
    path.lineTo(size.width, size.height);
    path.lineTo(0, size.height);
    path.close();

    canvas.drawPath(path, pathPaint);
  }

  @override
  bool shouldRepaint(LineChartPainter oldDelegate) => false;
}
