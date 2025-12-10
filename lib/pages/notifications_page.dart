import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';
import '../services/api_service.dart';

class NotificationsPage extends StatefulWidget {
  const NotificationsPage({super.key});

  @override
  State<NotificationsPage> createState() => _NotificationsPageState();
}

class _NotificationsPageState extends State<NotificationsPage> {
  final storage = const FlutterSecureStorage();
  bool _isLoading = true;
  List<Map<String, dynamic>> _notifications = [];
  List<Map<String, dynamic>> _generatedNotifications = [];
  String? _errorMessage;
  int _unreadCount = 0;

  @override
  void initState() {
    super.initState();
    loadNotifications();
    generateStockNotifications();
  }

  Future<void> generateStockNotifications() async {
    try {
      final token = await storage.read(key: 'auth_token');
      if (token == null) return;

      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/optimasi'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        final List<dynamic> bahanList = jsonResponse['data'] ?? [];

        final generated = <Map<String, dynamic>>[];
        final now = DateTime.now();

        for (var bahan in bahanList) {
          final status = bahan['status'] as String? ?? '';
          final nama = bahan['nama'] as String? ?? 'Unknown';
          final currentStock =
              (bahan['current_stock'] as num?)?.toDouble() ?? 0.0;
          final stokOptimal =
              (bahan['stok_optimal'] as num?)?.toDouble() ?? 0.0;

          String? notifType;
          String? message;
          IconData icon = Icons.info_rounded;
          Color iconColor = Colors.blue;

          if (status == 'Kritis') {
            notifType = 'persediaan_kritis';
            message =
                '$nama dalam kondisi kritis (stok: $currentStock). Segera pesan ulang!';
            icon = Icons.warning_rounded;
            iconColor = const Color(0xFFDC2626);
          } else if (status == 'Kurang') {
            notifType = 'persediaan_rendah';
            message =
                '$nama mendekati batas minimum (stok: $currentStock). Pertimbangkan memesan ulang.';
            icon = Icons.info_rounded;
            iconColor = const Color(0xFFF97316);
          } else if (status == 'Optimal') {
            notifType = 'persediaan_optimal';
            message = '$nama dalam kondisi optimal (stok: $currentStock).';
            icon = Icons.check_circle_rounded;
            iconColor = const Color(0xFF7C3AED);
          }

          if (notifType != null) {
            generated.add({
              'id': 'gen_${bahan['bahan_id']}_${now.millisecondsSinceEpoch}',
              'tipe': notifType,
              'judul': '$status - $nama',
              'pesan': message ?? '',
              'status': 'unread',
              'created_at': now.toIso8601String(),
              'icon': icon,
              'iconColor': iconColor,
              'bahan_id': bahan['bahan_id'],
              'isGenerated': true,
            });
          }
        }

        setState(() {
          _generatedNotifications = generated;
        });
      }
    } catch (e) {
      debugPrint('Error generating notifications: $e');
    }
  }

  Future<void> loadNotifications() async {
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

      final response = await http.get(
        Uri.parse('${ApiService.baseUrl}/notifications'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () => throw TimeoutException('Connection timeout'),
      );

      if (response.statusCode == 200) {
        final jsonResponse = jsonDecode(response.body);
        final List<dynamic> notifList = jsonResponse['data'] ?? [];

        final processed = <Map<String, dynamic>>[];
        for (var notif in notifList) {
          processed.add({
            ...notif,
            'icon': _getIconForType(notif['tipe'] as String?),
            'iconColor': _getColorForType(notif['tipe'] as String?),
            'isGenerated': false,
          });
        }

        // Combine API notifications + generated ones
        final combined = [
          ...processed,
          ..._generatedNotifications,
        ];

        // Sort by created_at (newest first)
        combined.sort((a, b) {
          final dateA = DateTime.parse(a['created_at'] as String? ?? '');
          final dateB = DateTime.parse(b['created_at'] as String? ?? '');
          return dateB.compareTo(dateA);
        });

        setState(() {
          _notifications = combined;
          _unreadCount = combined.where((n) => n['status'] == 'unread').length;
          _isLoading = false;
        });

        debugPrint('✅ Loaded ${_notifications.length} notifications');
      } else {
        setState(() {
          _errorMessage = 'Gagal mengambil notifikasi';
          _isLoading = false;
        });
      }
    } catch (e) {
      debugPrint('❌ Error loading notifications: $e');
      setState(() {
        _errorMessage = 'Terjadi kesalahan: $e';
        _isLoading = false;
      });
    }
  }

  IconData _getIconForType(String? type) {
    switch (type) {
      case 'persediaan_kritis':
        return Icons.warning_rounded;
      case 'persediaan_rendah':
        return Icons.info_rounded;
      case 'persediaan_optimal':
        return Icons.check_circle_rounded;
      case 'pesanan_ulang':
        return Icons.local_shipping_rounded;
      case 'stok_optimal':
        return Icons.trending_up;
      case 'prediksi_tinggi':
        return Icons.auto_graph;
      default:
        return Icons.notifications_rounded;
    }
  }

  Color _getColorForType(String? type) {
    switch (type) {
      case 'persediaan_kritis':
        return const Color(0xFFDC2626);
      case 'persediaan_rendah':
        return const Color(0xFFF97316);
      case 'persediaan_optimal':
        return const Color(0xFF7C3AED);
      case 'pesanan_ulang':
        return const Color(0xFF5B5BF5);
      default:
        return Colors.grey;
    }
  }

  String _formatDate(String dateString) {
    try {
      final date = DateTime.parse(dateString);
      final now = DateTime.now();
      final diff = now.difference(date);

      if (diff.inMinutes < 1) {
        return 'Baru saja';
      } else if (diff.inMinutes < 60) {
        return '${diff.inMinutes} menit yang lalu';
      } else if (diff.inHours < 24) {
        return '${diff.inHours} jam yang lalu';
      } else if (diff.inDays < 7) {
        return '${diff.inDays} hari yang lalu';
      } else {
        return DateFormat('dd MMM yyyy', 'id_ID').format(date);
      }
    } catch (e) {
      return dateString;
    }
  }

  void _markAsRead(String notificationId) {
    setState(() {
      _notifications = _notifications.map((n) {
        if (n['id'] == notificationId) {
          return {...n, 'status': 'read'};
        }
        return n;
      }).toList();
      _unreadCount =
          _notifications.where((n) => n['status'] == 'unread').length;
    });
  }

  void _deleteNotification(String notificationId) {
    setState(() {
      _notifications.removeWhere((n) => n['id'] == notificationId);
      _unreadCount =
          _notifications.where((n) => n['status'] == 'unread').length;
    });
  }

  void _deleteAllNotifications() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Hapus Semua Notifikasi?'),
        content: const Text(
            'Semua notifikasi akan dihapus. Tindakan ini tidak dapat dibatalkan.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Batal'),
          ),
          TextButton(
            onPressed: () {
              setState(() {
                _notifications = [];
                _unreadCount = 0;
              });
              Navigator.pop(context);
            },
            child:
                const Text('Hapus Semua', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
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
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Notifikasi',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                              color: Colors.black,
                            ),
                          ),
                        ],
                      ),
                    ),
                    GestureDetector(
                      onTap: loadNotifications,
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
                    const SizedBox(width: 8),
                    GestureDetector(
                      onTap: _deleteAllNotifications,
                      child: Icon(
                        Icons.delete_rounded,
                        color: Colors.grey[600],
                        size: 24,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            // Unread badge
            if (_unreadCount > 0)
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                color: const Color(0xFFFEEDED),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: const Color(0xFFDC2626),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        '$_unreadCount Belum Dibaca',
                        style: const TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

            // Notifications list
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
                        onPressed: loadNotifications,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFFA855F7),
                        ),
                        child: const Text('Coba Lagi'),
                      ),
                    ],
                  ),
                ),
              )
            else if (_notifications.isEmpty)
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.6,
                child: const Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.notifications_none,
                          color: Colors.grey, size: 48),
                      SizedBox(height: 16),
                      Text(
                        'Tidak ada notifikasi',
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
                  children: [
                    ..._notifications.asMap().entries.map((entry) {
                      final index = entry.key;
                      final notif = entry.value;
                      final isUnread = notif['status'] == 'unread';

                      return Padding(
                        padding: EdgeInsets.only(
                            bottom:
                                index == _notifications.length - 1 ? 0 : 12),
                        child: _buildNotificationCard(
                          notif: notif,
                          isUnread: isUnread,
                          onRead: () =>
                              _markAsRead(notif['id'] as String? ?? ''),
                          onDelete: () =>
                              _deleteNotification(notif['id'] as String? ?? ''),
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

  Widget _buildNotificationCard({
    required Map<String, dynamic> notif,
    required bool isUnread,
    required VoidCallback onRead,
    required VoidCallback onDelete,
  }) {
    final icon = notif['icon'] as IconData?;
    final iconColor = notif['iconColor'] as Color?;
    final judul = notif['judul'] as String? ?? '';
    final pesan = notif['pesan'] as String? ?? '';
    final timestamp = notif['created_at'] as String? ?? '';

    return GestureDetector(
      onTap: isUnread ? onRead : null,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: isUnread ? const Color(0xFFFEEDED) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isUnread ? const Color(0xFFDC2626) : const Color(0xFFE5E7EB),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header dengan icon dan title
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: (iconColor ?? Colors.grey).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    icon ?? Icons.notifications_rounded,
                    color: iconColor ?? Colors.grey,
                    size: 20,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              judul,
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: Colors.black,
                              ),
                            ),
                          ),
                          if (isUnread)
                            Container(
                              width: 8,
                              height: 8,
                              decoration: const BoxDecoration(
                                color: Color(0xFFDC2626),
                                shape: BoxShape.circle,
                              ),
                            ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        _formatDate(timestamp),
                        style: const TextStyle(
                          fontSize: 12,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),

            // Message
            Text(
              pesan,
              style: const TextStyle(
                fontSize: 13,
                color: Colors.black87,
                height: 1.5,
              ),
            ),
            const SizedBox(height: 12),

            // Action buttons
            Row(
              children: [
                if (isUnread)
                  Expanded(
                    child: OutlinedButton(
                      onPressed: onRead,
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 8),
                        side: const BorderSide(
                            color: Color(0xFFDC2626), width: 1.5),
                      ),
                      child: const Text(
                        'Tandai Dibaca',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: Color(0xFFDC2626),
                        ),
                      ),
                    ),
                  )
                else
                  const Spacer(),
                const SizedBox(width: 8),
                GestureDetector(
                  onTap: onDelete,
                  child: Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.grey[100],
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child:
                        const Icon(Icons.close, color: Colors.grey, size: 18),
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
