# 🚀 HƯỚNG DẪN SỬ DỤNG NHANH

## ⚡ KHỞI ĐỘNG ỨNG DỤNG

```bash
python main.py
```

---

## 👤 ĐĂNG NHẬP CỬ TRI

1. **Chọn vai trò:** Cử tri
2. **Nhập mã cử tri:** 1 đến 20
3. **Bỏ phiếu** trong tab "Cuộc bầu cử hiện tại"
4. **Xem lịch sử** trong tab "Lịch sử bỏ phiếu"

**Cử tri mẫu:**
- ID 1-10: Đã xác thực (có thể bỏ phiếu Permissioned)
- ID 11-20: Chưa xác thực (chỉ bỏ phiếu Permissionless)

---

## 🔐 ĐĂNG NHẬP ADMIN

### Bước 1: Chọn vai trò
- Chọn "Quản trị viên"

### Bước 2: Nhập thông tin
```
Username: admin
Password: Admin@2024
```

### Bước 3: Xác thực 2FA
- Xem mã OTP trên console (terminal)
- Nhập mã OTP vào dialog
- Đăng nhập thành công!

**Ví dụ OTP trên console:**
```
==================================================
MÃ XÁC THỰC 2FA (OTP)
==================================================
Mã OTP: 123456
Hết hạn sau: 5 phút
==================================================
```

---

## 📋 CHỨC NĂNG ADMIN

### 1. Tạo cuộc bầu cử
- Tab "Cuộc bầu cử"
- Click "Tạo cuộc bầu cử mới"
- Nhập thông tin
- Chọn chế độ: Permissionless hoặc Permissioned

### 2. Thêm ứng viên
- Tab "Ứng viên"
- Click "Thêm ứng viên"
- Nhập tên và mô tả

### 3. Quản lý cử tri
- Tab "Cử tri"
- Xác thực cử tri (cho Permissioned mode)
- Đăng ký khuôn mặt

### 4. Chuyển trạng thái
- Tab "Cuộc bầu cử"
- Click các nút theo thứ tự:
  1. Xác thực cử tri
  2. Mở bỏ phiếu
  3. Kiểm phiếu
  4. Công bố
  5. Kết thúc

### 5. Xem kết quả
- Tab "Kết quả"
- Click "Xem biểu đồ"

---

## 🗳️ QUY TRÌNH BẦU CỬ HOÀN CHỈNH

### Admin:
1. Tạo cuộc bầu cử
2. Thêm ứng viên
3. Xác thực cử tri (nếu Permissioned)
4. Chuyển sang "Xác thực cử tri"
5. Chuyển sang "Mở bỏ phiếu"

### Cử tri:
6. Đăng nhập
7. Chọn ứng viên
8. Bỏ phiếu

### Admin:
9. Chuyển sang "Kiểm phiếu"
10. Chuyển sang "Công bố"
11. Chuyển sang "Kết thúc"
12. Xem kết quả

---

## 🆕 TÍNH NĂNG MỚI

### Cho Cử tri:
- ✅ **Lịch sử bỏ phiếu**: Xem tất cả cuộc bầu cử đã tham gia
- ✅ **Tất cả cuộc bầu cử**: Danh sách đầy đủ các cuộc bầu cử
- ✅ **Chi tiết block**: Nhấp đúp để xem thông tin blockchain
- ✅ **Xuất lịch sử**: Lưu ra file JSON

### Cho Admin:
- ✅ **Đăng nhập bảo mật**: Username + Password + 2FA
- ✅ **Rate limiting**: Khóa sau 5 lần sai
- ✅ **Audit log**: Ghi nhận mọi hành động
- ✅ **Session timeout**: Tự động đăng xuất sau 30 phút

---

## 🔧 KHẮC PHỤC SỰ CỐ

### Quên mật khẩu admin?
```python
# Chạy script reset password
from services.admin_auth_service import AdminAuthService
admin_auth = AdminAuthService()
admin_auth.reset_password(admin_id=1, new_password="NewP@ssw0rd2024")
```

### Database bị lỗi?
```bash
# Xóa database và chạy lại
rm voting_dapp.db
python main.py
```

### OTP không hiển thị?
- Kiểm tra console/terminal
- OTP hiển thị sau khi nhập đúng username + password

---

## 📞 HỖ TRỢ

**Tài liệu chi tiết:**
- `README.md` - Tổng quan
- `BAO_MAT_ADMIN.md` - Bảo mật admin
- `CHANGELOG_TINH_NANG_MOI.md` - Tính năng mới
- `DANH_GIA_TINH_NANG_CAN_BO_SUNG.md` - Đánh giá tính năng

**Lỗi thường gặp:**
- Không đăng nhập được → Kiểm tra username/password
- OTP sai → Kiểm tra console, OTP hết hạn sau 5 phút
- Không bỏ phiếu được → Kiểm tra trạng thái cuộc bầu cử
- Tài khoản bị khóa → Đợi 15 phút

---

**Version:** 2.0.0
**Cập nhật:** 2024-01-15
