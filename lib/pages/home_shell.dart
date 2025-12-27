import 'package:flutter/material.dart';
import 'dashboard_page.dart';
import 'input_data_page.dart';
import 'prediksi_page.dart';
import 'optimasi_stok_page.dart';
import 'notifications_page.dart';

class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int _currentIndex = 0;
  late final GlobalKey<DashboardPageState> _dashboardKey;

  late final List<Widget> _pages;

  @override
  void initState() {
    super.initState();
    _dashboardKey = GlobalKey<DashboardPageState>();
    _pages = [
      DashboardPage(key: _dashboardKey),
      const InputDataPage(),
      const PrediksiPage(),
      const OptimiasiStokPage(),
      const NotificationsPage(),
    ];
  }

  void _refreshDashboard() {
    _dashboardKey.currentState?.loadBahanData();
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) {
        if (didPop) return;
        // Prevent back navigation from HomeShell
        // This will keep user in the app instead of going back
      },
      child: Scaffold(
        body: _pages[_currentIndex],
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) {
            if (index == 1) {
              // When tapping Input Data, push it to get result
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const InputDataPage()),
              ).then((result) {
                // If data was added (result == true), refresh dashboard and optimasi
                if (result == true && mounted) {
                  _refreshDashboard();
                  setState(() => _currentIndex = 0);
                }
              });
            } else {
              setState(() => _currentIndex = index);
            }
          },
          type: BottomNavigationBarType.fixed,
          backgroundColor: Colors.white,
          elevation: 8,
          selectedItemColor: const Color(0xFFA855F7),
          unselectedItemColor: Colors.grey,
          selectedLabelStyle: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w600,
          ),
          unselectedLabelStyle: const TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w500,
          ),
          items: [
            BottomNavigationBarItem(
              icon: Icon(
                Icons.dashboard_rounded,
                size: 24,
              ),
              label: 'Dasboard',
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.cloud_upload_outlined,
                size: 24,
              ),
              label: 'Input Data',
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.trending_up,
                size: 24,
              ),
              label: 'Prediksi',
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.balance,
                size: 24,
              ),
              label: 'Optimasi',
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.notifications_rounded,
                size: 24,
              ),
              label: 'Peringatan',
            ),
          ],
        ),
      ),
    );
  }
}
