import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart' show kIsWeb, debugPrint;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

// Inisialisasi storage untuk token
const storage = FlutterSecureStorage();

class ApiService {
  // Untuk Android emulator, gunakan localhost dengan ADB reverse port forwarding
  static String get baseUrl {
    if (kIsWeb) {
      return 'http://127.0.0.1:5000'; // Web: localhost
    } else if (Platform.isAndroid) {
      return 'http://localhost:5000'; // Android emulator dengan ADB reverse
    } else {
      return 'http://127.0.0.1:5000'; // Desktop (Windows/Linux/macOS)
    }
  }

  static Future<Map<String, dynamic>> predict(
    Map<String, dynamic> input,
  ) async {
    try {
      final token = await storage.read(key: 'auth_token');

      final headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

      final uri = Uri.parse('$baseUrl/prediksi');
      debugPrint('🌐 API Request: POST $uri');
      debugPrint('📦 Request Data: $input');

      final response = await http
          .post(
            uri,
            headers: headers,
            body: jsonEncode(input),
          )
          .timeout(
            const Duration(seconds: 30),
            onTimeout: () =>
                throw TimeoutException('Koneksi timeout. Silakan coba lagi.'),
          );

      debugPrint('✅ Response Status: ${response.statusCode}');
      debugPrint('📥 Response Body: ${response.body}');

      final responseData = jsonDecode(response.body);

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return responseData;
      } else {
        throw Exception(
          responseData['error']?.toString() ??
              'Gagal mendapatkan prediksi: ${response.statusCode}',
        );
      }
    } on TimeoutException catch (e) {
      debugPrint('⏱️ Timeout: $e');
      rethrow;
    } on SocketException catch (e) {
      debugPrint('🔌 Socket Error: $e');
      throw Exception(
          'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.');
    } on FormatException catch (e) {
      debugPrint('📄 Format Error: $e');
      throw Exception('Terjadi kesalahan format data dari server.');
    } catch (e) {
      debugPrint('❌ Error in predict: $e');
      rethrow;
    }
  }

  static Future<Map<String, dynamic>> post(
      String endpoint, Map<String, dynamic> data) async {
    try {
      final token = await storage.read(key: 'auth_token');

      final headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

      // Hapus leading slash dari endpoint jika ada untuk menghindari double slash
      final cleanEndpoint =
          endpoint.startsWith('/') ? endpoint.substring(1) : endpoint;
      final uri = Uri.parse('$baseUrl/$cleanEndpoint');
      debugPrint('🌐 API Request: POST $uri');
      debugPrint('📦 Request Data: $data');

      final response = await http
          .post(
            uri,
            headers: headers,
            body: jsonEncode(data),
          )
          .timeout(
            const Duration(seconds: 30),
            onTimeout: () =>
                throw TimeoutException('Koneksi timeout. Silakan coba lagi.'),
          );

      debugPrint('✅ Response Status: ${response.statusCode}');
      debugPrint('📥 Response Body: ${response.body}');

      final responseData = jsonDecode(response.body);

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return responseData;
      } else {
        throw Exception(
          responseData['error']?.toString() ??
              'Request failed with status: ${response.statusCode}',
        );
      }
    } on TimeoutException catch (e) {
      debugPrint('⏱️ Timeout: $e');
      rethrow;
    } on SocketException catch (e) {
      debugPrint('🔌 Socket Error: $e');
      throw Exception(
          'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.');
    } on FormatException catch (e) {
      debugPrint('📄 Format Error: $e');
      throw Exception('Terjadi kesalahan format data dari server.');
    } catch (e) {
      debugPrint('❌ Error in ApiService.post: $e');
      throw Exception('Terjadi kesalahan: ${e.toString()}');
    }
  }

  static Future<bool> submitPermintaan(Map<String, dynamic> payload) async {
    try {
      final token = await storage.read(key: 'auth_token');

      final headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        if (token != null) 'Authorization': 'Bearer $token',
      };

      final uri = Uri.parse('$baseUrl/permintaan');
      debugPrint('🌐 API Request: POST $uri');
      debugPrint('📦 Request Payload: $payload');

      final response = await http
          .post(
            uri,
            headers: headers,
            body: jsonEncode(payload),
          )
          .timeout(
            const Duration(seconds: 30),
            onTimeout: () =>
                throw TimeoutException('Koneksi timeout. Silakan coba lagi.'),
          );

      debugPrint('✅ Response Status: ${response.statusCode}');
      debugPrint('📥 Response Body: ${response.body}');

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return true;
      } else {
        final responseData = jsonDecode(response.body);
        throw Exception(
          responseData['error']?.toString() ??
              'Gagal mengirim permintaan: ${response.statusCode}',
        );
      }
    } on TimeoutException {
      debugPrint('⏱️ Timeout saat mengirim permintaan');
      rethrow;
    } on SocketException {
      debugPrint('🔌 Koneksi terputus saat mengirim permintaan');
      rethrow;
    } on FormatException {
      debugPrint('📄 Format data tidak valid');
      rethrow;
    } catch (e) {
      debugPrint('❌ Error in submitPermintaan: $e');
      rethrow;
    }
  }
}
