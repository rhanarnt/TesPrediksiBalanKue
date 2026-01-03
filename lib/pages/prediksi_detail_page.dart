import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../services/api_service.dart';

class PrediksiDetailPage extends StatefulWidget {
  final int? bahanId;
  final String? bahanName;

  const PrediksiDetailPage({
    super.key,
    this.bahanId,
    this.bahanName,
  });

  @override
  State<PrediksiDetailPage> createState() => _PrediksiDetailPageState();
}

class _PrediksiDetailPageState extends State<PrediksiDetailPage> {
  final _storage = const FlutterSecureStorage();

  bool _isLoading = true;
  Map<String, dynamic>? _predictionData;
  Map<String, dynamic>? _bahanData;
  String? _errorMessage;
  bool _showAllMaterials = false;
  List<Map<String, dynamic>> _allPredictions = [];

  @override
  void initState() {
    super.initState();
    if (widget.bahanId != null) {
      _loadDetailPrediction();
    } else {
      _loadBatchPredictions();
    }
  }

  Future<void> _loadDetailPrediction() async {
    try {
      final token = await _storage.read(key: 'auth_token');
      if (token == null) {
        setState(() {
          _errorMessage = 'Token tidak ditemukan. Silakan login lagi';
          _isLoading = false;
        });
        return;
      }

      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/prediksi-detail/${widget.bahanId}'),
        headers: {'Authorization': 'Bearer $token'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        setState(() {
          _predictionData = result['data'];
          _bahanData = result['bahan'];
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Gagal memuat prediksi: ${response.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: $e';
        _isLoading = false;
      });
    }
  }

  Future<void> _loadBatchPredictions() async {
    try {
      final token = await _storage.read(key: 'auth_token');
      if (token == null) {
        setState(() {
          _errorMessage = 'Token tidak ditemukan. Silakan login lagi';
          _isLoading = false;
        });
        return;
      }

      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/prediksi-batch'),
        headers: {'Authorization': 'Bearer $token'},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        setState(() {
          _allPredictions =
              List<Map<String, dynamic>>.from(result['data'] ?? []);
          _showAllMaterials = true;
          _isLoading = false;
        });
      } else {
        setState(() {
          _errorMessage = 'Gagal memuat prediksi: ${response.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'Error: $e';
        _isLoading = false;
      });
    }
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toUpperCase()) {
      case 'HIGH':
        return Colors.red;
      case 'MEDIUM':
        return Colors.orange;
      case 'LOW':
        return Colors.yellow;
      default:
        return Colors.green;
    }
  }

  Icon _getActionIcon(String action) {
    switch (action.toUpperCase()) {
      case 'URGENT_ORDER':
        return const Icon(Icons.error, color: Colors.red);
      case 'EXPEDITED_ORDER':
        return const Icon(Icons.warning, color: Colors.orange);
      case 'REGULAR_ORDER':
        return const Icon(Icons.shopping_cart, color: Colors.blue);
      case 'MONITOR':
        return const Icon(Icons.visibility, color: Colors.green);
      default:
        return const Icon(Icons.info);
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
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: const Icon(Icons.arrow_back,
                          color: Colors.black, size: 24),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Text(
                        'Prediksi Bahan Baku',
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: Colors.black,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Content
            if (_isLoading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(32),
                  child: CircularProgressIndicator(),
                ),
              )
            else if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.all(16),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.red[50],
                    border: Border.all(color: Colors.red),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Error',
                        style: TextStyle(
                          color: Colors.red,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(_errorMessage!),
                    ],
                  ),
                ),
              )
            else if (_showAllMaterials && _allPredictions.isNotEmpty)
              _buildBatchView()
            else if (_predictionData != null && _bahanData != null)
              _buildDetailView()
            else
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(32),
                  child: Text('Tidak ada data prediksi'),
                ),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailView() {
    final prediction = _predictionData!;
    final bahan = _bahanData!;
    final recommendation = prediction['recommendation'] ?? {};
    final actionPlan = prediction['action_plan'] ?? [];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Material Info
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
                Text(
                  bahan['nama'] ?? 'Unknown',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 12),
                _buildInfoRow('Stok Saat Ini',
                    '${bahan['current_stock']} ${bahan['unit']}'),
                _buildInfoRow('Stok Minimum',
                    '${bahan['stok_minimum']} ${bahan['unit']}'),
                _buildInfoRow('Stok Optimal',
                    '${bahan['stok_optimal']} ${bahan['unit']}'),
                _buildInfoRow('Harga per Unit',
                    'Rp ${(bahan['harga_per_unit'] as num?)?.toStringAsFixed(0) ?? '0'}'),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Prediction Stats
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
                  'Prediksi Permintaan',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: Colors.black,
                  ),
                ),
                const SizedBox(height: 12),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildStatCard(
                      'Per Hari',
                      '${(prediction['predicted_daily_demand'] as num?)?.toStringAsFixed(1) ?? '0'} unit',
                      Colors.blue,
                    ),
                    _buildStatCard(
                      'Per Bulan',
                      '${(prediction['predicted_monthly_demand'] as num?)?.toStringAsFixed(0) ?? '0'} unit',
                      Colors.green,
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                _buildInfoRow(
                  'Estimated Cost',
                  'Rp ${(prediction['estimated_cost'] as num?)?.toStringAsFixed(0) ?? '0'}',
                ),
                _buildInfoRow(
                  'Confidence',
                  '${(prediction['confidence'] as num?)?.toStringAsFixed(1) ?? '0'}%',
                ),
                if (prediction['days_until_stockout'] != null)
                  _buildInfoRow(
                    'Hari hingga Stok Habis',
                    '${(prediction['days_until_stockout'] as num?)?.toStringAsFixed(1) ?? 'N/A'} hari',
                  ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Recommendation
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.amber[50],
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.amber),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.lightbulb, color: Colors.amber[700]),
                    const SizedBox(width: 8),
                    const Text(
                      'Rekomendasi',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _getPriorityColor(recommendation['priority'] ?? '')
                        .withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color:
                          _getPriorityColor(recommendation['priority'] ?? ''),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        recommendation['message'] ?? 'No recommendation',
                        style: TextStyle(
                          color: _getPriorityColor(
                              recommendation['priority'] ?? ''),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Priority: ${recommendation['priority'] ?? 'N/A'}',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Action Plan
          if (actionPlan.isNotEmpty)
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
                    'Rencana Aksi',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                      color: Colors.black,
                    ),
                  ),
                  const SizedBox(height: 12),
                  ListView.separated(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: actionPlan.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 8),
                    itemBuilder: (_, index) {
                      final action = actionPlan[index] as Map<String, dynamic>;
                      return Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.grey[50],
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.grey[200]!),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                _getActionIcon(action['action'] ?? ''),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        action['description'] ?? '',
                                        style: const TextStyle(
                                          fontWeight: FontWeight.w600,
                                        ),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        action['timeline'] ?? '',
                                        style: TextStyle(
                                          fontSize: 12,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildBatchView() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Geser untuk melihat prediksi per bahan baku',
            style: TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w400,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 12),
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _allPredictions.length,
            separatorBuilder: (_, __) => const SizedBox(height: 12),
            itemBuilder: (_, index) {
              final pred = _allPredictions[index];
              final recommendation = pred['recommendation'] ?? {};
              final bahanId = pred['bahan_id'] ?? index + 1;
              final bahanNama = pred['bahan_nama'] ?? 'Unknown';
              final currentStock = pred['current_stock'] ?? 0;
              final daysUntilStockout = pred['days_until_stockout'] ?? 0;
              final priority = recommendation['priority'] ?? 'MEDIUM';

              return GestureDetector(
                onTap: () {
                  // Navigate to detail view
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(
                      builder: (context) => PrediksiDetailPage(
                        bahanId: bahanId,
                        bahanName: bahanNama,
                      ),
                    ),
                  );
                },
                child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: Colors.grey[200]!,
                      width: 1,
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.05),
                        blurRadius: 4,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Header: Nama dan Status
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(
                              bahanNama,
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                                fontSize: 15,
                                color: Colors.black,
                              ),
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            decoration: BoxDecoration(
                              color:
                                  _getPriorityColor(priority).withOpacity(0.15),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              priority == 'HIGH'
                                  ? '[H]'
                                  : priority == 'MEDIUM'
                                      ? '[M]'
                                      : '[L]',
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                                color: _getPriorityColor(priority),
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),

                      // Stok dengan Icon
                      Row(
                        children: [
                          const Icon(Icons.inventory_2,
                              size: 18, color: Colors.amber),
                          const SizedBox(width: 8),
                          Text(
                            '${currentStock.toStringAsFixed(1)} kg',
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                              color: Colors.black,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),

                      // Durasi
                      Text(
                        'Cukup untuk ${daysUntilStockout.toStringAsFixed(1)} hari',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.grey[600],
                        ),
                      ),
                      const SizedBox(height: 12),

                      // Divider
                      Container(
                        height: 1,
                        color: Colors.grey[200],
                      ),
                      const SizedBox(height: 12),

                      // Tombol Lihat Detail
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Demand: ${(pred['predicted_monthly_demand'] as num?)?.toStringAsFixed(0) ?? '0'} unit/bln',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey[600],
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          Row(
                            children: [
                              const Text(
                                'Lihat Detail',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Colors.blue,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              const SizedBox(width: 4),
                              const Icon(
                                Icons.arrow_forward,
                                size: 14,
                                color: Colors.blue,
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: TextStyle(
              color: Colors.grey[600],
              fontSize: 13,
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color),
      ),
      child: Column(
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }
}
