import 'package:flutter/material.dart';
import 'pages/login_page.dart';
import 'pages/home_shell.dart';
import 'pages/prediksi_detail_page.dart';
import 'pages/notifications_page.dart';

void main() {
  runApp(const PrediksiStokApp());
}

class PrediksiStokApp extends StatelessWidget {
  const PrediksiStokApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BakeSmart',
      theme: ThemeData(
        colorScheme: const ColorScheme.light(
            primary: Color(0xFFA855F7), secondary: Color(0xFFD97706)),
        primaryColor: const Color(0xFFA855F7),
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.white,
      ),
      home: const LoginPage(),
      routes: {
        '/login': (context) => const LoginPage(),
        '/dashboard': (context) => const HomeShell(),
        '/prediksi-detail': (context) => const PrediksiDetailPage(),
        '/notifications': (context) => const NotificationsPage(),
      },
      debugShowCheckedModeBanner: false,
    );
  }
}
