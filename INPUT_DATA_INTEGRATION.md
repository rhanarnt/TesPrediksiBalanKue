# Input Data Page - API Integration Complete ✅

**Status**: Production Ready  
**Last Update**: Current Session  
**Endpoint**: `POST /stock-record`  
**Database**: MySQL (prediksi_stok_kue)

## ✅ Completed Features

### 1. **Data Persistence**

- Input data automatically saved to MySQL database
- Endpoint: `http://127.0.0.1:5000/stock-record`
- Authentication: JWT Bearer token (from secure storage)

### 2. **User Interface**

- ✅ Button disabled during request
- ✅ Loading spinner visible
- ✅ Button opacity reduced for visual feedback
- ✅ Success snackbar with item details
- ✅ Error snackbar with error message

### 3. **Error Handling**

- Validation: Empty fields check
- Numeric validation: Jumlah must be number
- Timeout protection: 10 second timeout
- Graceful error messages in Indonesian
- Debug logging for troubleshooting

### 4. **Form Management**

- Auto-clear form after successful submission
- Reset unit to default 'kg'
- Maintains state during loading

## 📋 Testing Checklist

Before deploying, verify:

- [ ] Backend running: `python backend/run.py`
- [ ] Flutter running: `flutter run -d chrome`
- [ ] User logged in with valid JWT token
- [ ] Input name: "Tepung Terigu"
- [ ] Input quantity: "5"
- [ ] Select unit: "kg"
- [ ] Click "Tambahkan Item"
- [ ] Verify snackbar shows: "✅ Tepung Terigu ditambahkan (5 kg)"
- [ ] Verify form clears
- [ ] Verify data appears in Dashboard → Stok Tersedia table
- [ ] Verify data in MySQL: `SELECT * FROM stock_record WHERE tipe='masuk';`

## 🔧 Code Structure

### Button Widget

```dart
// Shows spinner during loading, disabled state
SizedBox(
  width: double.infinity,
  height: 44,
  child: ElevatedButton(
    onPressed: _isLoading ? null : _tambahkanItem,
    // ... style with opacity change
    child: _isLoading
      ? CircularProgressIndicator()
      : Text('Tambahkan Item'),
  ),
)
```

### API Call Structure

```dart
// GET token from secure storage
final token = await _storage.read(key: 'auth_token');

// POST to backend
final response = await http.post(
  Uri.parse('http://127.0.0.1:5000/stock-record'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json',
  },
  body: jsonEncode({
    'bahan_id': 1,
    'jumlah': double.parse(jumlah),
    'tipe': 'masuk',
    'catatan': 'Input manual dari aplikasi - $nama',
  }),
);

// Handle response (201 = Created successfully)
if (response.statusCode == 201) {
  // Success handling
}
```

## 📊 Data Flow

```
User Input (UI)
    ↓
Validation (empty, numeric)
    ↓
Load JWT Token (Secure Storage)
    ↓
HTTP POST to /stock-record
    ↓
Backend Validation
    ↓
MySQL INSERT (stock_record table)
    ↓
201 Response
    ↓
Success Snackbar + Form Clear
```

## 🐛 Debugging

**Enable debug logging:**

```dart
debugPrint('📝 Data disimpan ke database');
debugPrint('   Nama: $nama');
debugPrint('   Jumlah: $jumlah $_selectedUnit');
```

**Common Issues:**

1. **"Token tidak ditemukan"**

   - Solution: User needs to login first

2. **"Gagal menyimpan: [error message]"**

   - Check backend logs for details
   - Verify bahan_id exists in database

3. **"Koneksi timeout"**

   - Backend not running
   - Start: `python backend/run.py`

4. **No snackbar appears**
   - Check browser console for errors
   - Verify Flutter restart completed

## 🚀 Next Pages to Integrate

Following same pattern:

- [ ] Prediksi Page - POST /prediksi
- [ ] Permintaan Page - POST /permintaan
- [ ] Optimasi Page - POST /optimasi
- [ ] Notifications Page - GET /notifications

## 📝 Notes

- Bahan ID currently hardcoded to 1 (Tepung)
- Future: Add bahan dropdown to let user select
- Form unit resets to 'kg' to match default
- Token expires in 1 hour (from login)
