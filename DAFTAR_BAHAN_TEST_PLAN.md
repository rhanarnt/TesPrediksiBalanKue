# Test Plan: Daftar Bahan Fix Verification

## Quick Test (1-2 minutes)

### Prerequisites

- App running on emulator (should still be running from rebuild)
- User logged in as admin@bakesmart.com
- Dashboard visible

### Test Steps

1. **Verify Dashboard Daftar Bahan Section**

   - [ ] Navigate to Dashboard
   - [ ] Scroll down to "Daftar Bahan" section
   - [ ] Confirm section displays
   - [ ] Confirm NO ERROR panel appears
   - [ ] Verify 5 or fewer stock records showing

2. **Verify Each Stock Record Card**

   - [ ] Check each card has proper styling (white bg, border, shadow)
   - [ ] Confirm icon shows (arrow down for "masuk", arrow up for "keluar", etc.)
   - [ ] Confirm type badge shows: "Masuk", "Keluar", or "Penyesuaian"
   - [ ] Confirm date/time displays
   - [ ] Confirm item name displays

3. **Verify No Errors**
   - [ ] Check Flutter console output (should have no red errors)
   - [ ] Check emulator logs (should have no crash messages)
   - [ ] Try scrolling the list (should be smooth)

### Expected Results

- ✅ Dashboard loads without errors
- ✅ "Daftar Bahan" section displays 5 stock records
- ✅ Each record shows proper capitalization (type is "Masuk", not "masuk")
- ✅ Type badges are colored correctly:
  - Green for "Masuk" (incoming)
  - Red for "Keluar" (outgoing)
  - Orange for "Penyesuaian" (adjustment)
- ✅ No console errors or crash messages

## If Error Still Appears

1. Try **Hot Reload** (press 'R' in terminal):

   ```
   R Hot reload.
   ```

2. If error persists, try **Hot Restart** (press 'R' again):

   ```
   R Hot restart.
   ```

3. If still failing, do full rebuild:
   ```bash
   flutter clean && flutter pub get && flutter run -d emulator-5554
   ```

## Validation Checklist

- [ ] App starts without crashes
- [ ] Login successful
- [ ] Dashboard loads
- [ ] "Daftar Bahan" section visible
- [ ] No "NoSuchMethodError" message
- [ ] Stock records display correctly
- [ ] Type capitalization correct (e.g., "Masuk" not "masuk")
- [ ] Styling matches dashboard design
- [ ] No red errors in console
