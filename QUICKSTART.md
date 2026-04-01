# 🚀 Hướng dẫn nhanh - DApp Voting System

## Cài đặt nhanh

```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Chạy ứng dụng
python main.py
```

## Demo nhanh (5 phút)

### Bước 1: Đăng nhập Admin
- Vai trò: **Quản trị viên**
- Mã số: **admin**

### Bước 2: Tạo cuộc bầu cử
1. Tab "📋 Cuộc bầu cử"
2. Click "➕ Tạo cuộc bầu cử mới"
3. Nhập:
   - Tiêu đề: `Bầu cử Tổng thống 2026`
   - Mô tả: `Bầu chọn tổng thống nhiệm kỳ 2026-2030`
   - Chế độ: `Permissionless`
4. Click "Tạo"

### Bước 3: Thêm ứng viên
1. Tab "🎯 Ứng viên"
2. Click "➕ Thêm ứng viên" (thêm 3 ứng viên):
   - Ứng viên A: `Nguyễn Văn A` - `Ứng viên có kinh nghiệm 20 năm`
   - Ứng viên B: `Trần Thị B` - `Ứng viên trẻ năng động`
   - Ứng viên C: `Lê Văn C` - `Ứng viên cải cách`

### Bước 4: Mở bỏ phiếu
1. Tab "📋 Cuộc bầu cử"
2. Click theo thứ tự:
   - **1️⃣ Xác thực cử tri**
   - **2️⃣ Mở bỏ phiếu**

### Bước 5: Đăng xuất và bỏ phiếu
1. Click "🚪 Đăng xuất"
2. Đăng nhập lại:
   - Vai trò: **Cử tri**
   - Mã số: **1**
3. Chọn ứng viên A
4. Click "🗳️ Bỏ phiếu"
5. Xác nhận
6. Click "📊 Xem trạng thái phiếu" để xem phiếu trên blockchain

### Bước 6: Bỏ thêm phiếu
Lặp lại bước 5 với các cử tri khác:
- Cử tri 2 → Vote cho B
- Cử tri 3 → Vote cho A
- Cử tri 4 → Vote cho C
- Cử tri 5 → Vote cho A

### Bước 7: Kiểm phiếu và công bố
1. Đăng xuất, đăng nhập lại với **admin**
2. Tab "📋 Cuộc bầu cử"
3. Click theo thứ tự:
   - **3️⃣ Kiểm phiếu**
   - **4️⃣ Công bố**
   - **5️⃣ Kết thúc**

### Bước 8: Xem kết quả
1. Tab "📊 Kết quả"
2. Click "📊 Xem biểu đồ"

### Bước 9: Kiểm tra Blockchain
1. Tab "⛓️ Blockchain"
2. Xem tất cả blocks
3. Click "🔍 Kiểm tra tính toàn vẹn"

## 🎯 Các tính năng để test

### Test 1: Double Voting Prevention
1. Cử tri 1 bỏ phiếu
2. Đăng xuất
3. Đăng nhập lại với cử tri 1
4. Thử bỏ phiếu lần 2 → **Bị chặn** ✅

### Test 2: Permissioned Mode
1. Admin tạo election với mode "Permissioned"
2. Cử tri 15 (chưa verified) thử bỏ phiếu → **Bị chặn** ✅
3. Admin xác thực cử tri 15
4. Cử tri 15 bỏ phiếu lại → **Thành công** ✅

### Test 3: State Machine
1. Admin ở state "Start"
2. Thử chuyển thẳng sang "Count" → **Bị chặn** ✅
3. Phải đi theo thứ tự: Start → ValidateVoter → Vote → Count

### Test 4: Blockchain Integrity
1. Bỏ vài phiếu
2. Kiểm tra blockchain → **Valid** ✅
3. Dùng DB Browser sửa data trong bảng blockchain
4. Kiểm tra lại → **Invalid** ✅

### Test 5: Digital Signature
1. Cử tri bỏ phiếu
2. Xem trạng thái phiếu → Có signature
3. Hệ thống đã verify signature trước khi ghi vào blockchain ✅

## 💡 Tips

- **Cử tri 1-10**: Đã được xác thực sẵn
- **Cử tri 11-20**: Chưa xác thực, cần admin verify
- **Admin password**: `admin`
- **Xem blockchain**: Tab "⛓️ Blockchain" trong admin view
- **Xem biểu đồ**: Tab "📊 Kết quả" → Click "📊 Xem biểu đồ"

## ⚠️ Lưu ý

- Đây là ứng dụng demo/học thuật
- Không sử dụng cho bầu cử thực tế
- Private keys được lưu trong database (không an toàn cho production)
- Blockchain chạy local, không có network layer

## 🐛 Troubleshooting

### Lỗi "No module named 'PySide6'"
```bash
pip install PySide6
```

### Lỗi "No module named 'cryptography'"
```bash
pip install cryptography
```

### Database bị lỗi
```bash
# Xóa database và chạy lại
rm voting_dapp.db
python main.py
```

### Muốn reset toàn bộ dữ liệu
Xóa file `voting_dapp.db` và chạy lại ứng dụng.

---

**Chúc bạn khám phá thú vị với DApp Voting System!** 🎉
