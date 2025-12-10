import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/app_header.dart';
import '../widgets/primary_button.dart';

class PermintaanBahanPage extends StatefulWidget {
  const PermintaanBahanPage({super.key});

  @override
  State<PermintaanBahanPage> createState() => _PermintaanBahanPageState();
}

class _PermintaanBahanPageState extends State<PermintaanBahanPage> {
  final kuantitasController = TextEditingController(text: '500');
  DateTime? selectedDate = DateTime(2025, 11, 25);
  String? selectedBahan = 'Gula Pasir';
  bool isSubmitting = false;

  final List<String> bahanList = [
    'Tepung Terigu',
    'Gula Pasir',
    'Telur',
    'Mentega',
    'Susu',
  ];

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate ?? DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null && picked != selectedDate) {
      setState(() {
        selectedDate = picked;
      });
    }
  }

  void _submitPermintaan() async {
    if (selectedBahan == null ||
        kuantitasController.text.isEmpty ||
        selectedDate == null) {
      _showErrorSnackbar('Isi semua field terlebih dahulu');
      return;
    }

    setState(() => isSubmitting = true);

    try {
      final payload = {
        'nama_bahan': selectedBahan,
        'kuantitas': kuantitasController.text,
        'tanggal': selectedDate?.toIso8601String(),
      };

      debugPrint('📤 Mengirim permintaan: $payload');

      final ok = await ApiService.submitPermintaan(payload);

      if (!mounted) return;

      if (ok) {
        _showSuccessSnackbar('Permintaan bahan berhasil dikirim ✓');
        kuantitasController.text = '500';
        setState(() => selectedBahan = 'Gula Pasir');
        setState(() => selectedDate = DateTime(2025, 11, 25));
      } else {
        _showErrorSnackbar('Gagal mengirim permintaan');
      }
    } catch (e) {
      if (!mounted) return;
      _showErrorSnackbar('Error: $e');
    } finally {
      if (mounted) {
        setState(() => isSubmitting = false);
      }
    }
  }

  void _showErrorSnackbar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  void _showSuccessSnackbar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.green),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const AppHeader(title: 'Permintaan Bahan'),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Nama Bahan',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Container(
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey[300]!),
                borderRadius: BorderRadius.circular(8),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: DropdownButton<String>(
                isExpanded: true,
                underline: const SizedBox(),
                value: selectedBahan,
                items: bahanList
                    .map((bahan) =>
                        DropdownMenuItem(value: bahan, child: Text(bahan)))
                    .toList(),
                onChanged: (value) => setState(() => selectedBahan = value),
              ),
            ),
            const SizedBox(height: 20),
            const Text('Kuantitas',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            TextField(
              controller: kuantitasController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                hintText: 'Contoh: 500',
                border:
                    OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
            const SizedBox(height: 20),
            const Text('Tanggal Permintaan',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            GestureDetector(
              onTap: () => _selectDate(context),
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey[300]!),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.calendar_today, color: Colors.grey),
                    const SizedBox(width: 12),
                    Text(
                      selectedDate == null
                          ? 'Pilih tanggal'
                          : '${selectedDate!.day} ${_getMonthName(selectedDate!.month)} ${selectedDate!.year}',
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 32),
            PrimaryButton(
              label: isSubmitting ? 'Mengirim...' : 'Kirim Permintaan',
              onPressed: isSubmitting ? () {} : _submitPermintaan,
            ),
          ],
        ),
      ),
    );
  }

  String _getMonthName(int month) {
    const months = [
      'Januari',
      'Februari',
      'Maret',
      'April',
      'Mei',
      'Juni',
      'Juli',
      'Agustus',
      'September',
      'Oktober',
      'November',
      'Desember',
    ];
    return months[month - 1];
  }

  @override
  void dispose() {
    kuantitasController.dispose();
    super.dispose();
  }
}
