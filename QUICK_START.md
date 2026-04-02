# Hướng dẫn nhanh - Quick Start

## Cài đặt và chạy (3 bước)

### Bước 1: Cài đặt thư viện
```bash
install_requirements.bat
```
Hoặc:
```bash
pip install -r requirements.txt
```

### Bước 2: Chạy ứng dụng
```bash
run_app.bat
```
Hoặc:
```bash
python main.py
```

### Bước 3: Đăng nhập

#### Đăng nhập Admin:
1. Chọn "Quản trị viên"
2. Nhập: `admin`
3. Click "Đăng nhập"

#### Đăng nhập Cử tri:
1. Chọn "Cử tri"
2. Nhập CCCD: `001123456789` (hoặc 002, 003... đến 020)
3. Click "📸 Quét khuôn mặt"
4. Đăng ký khuôn mặt lần đầu (nhấn SPACE để chụp)
5. Quét lại để xác thực
6. Click "Đăng nhập"

## Tính năng chính

### Admin có thể:
- ✅ Tạo và quản lý cuộc bầu cử
- ✅ Thêm đề xuất/ứng viên
- ✅ Xem kết quả và thống kê
- ✅ Xem blockchain và xác thực
- ✅ Quản lý cử tri

### Cử tri có thể:
- ✅ Xem danh sách cuộc bầu cử
- ✅ Bỏ phiếu (với xác thực khuôn mặt)
- ✅ Xem kết quả
- ✅ Xác minh phiếu bầu trên blockchain

## Chế độ hiển thị

Ứng dụng tự động mở **FULL SCREEN** (maximized) khi chạy.

Để thoát full screen:
- Nhấn nút minimize/restore trên thanh tiêu đề
- Hoặc nhấn `Alt + Enter` (nếu dùng true fullscreen)

## Dữ liệu mẫu

Hệ thống tự động tạo 20 cử tri với CCCD:
- 001123456789
- 002123456789
- 003123456789
- ...
- 020123456789

## Yêu cầu

- ✅ Python 3.8+
- ✅ Webcam (cho nhận diện khuôn mặt)
- ✅ Windows 10/11
- ✅ Kết nối internet (chỉ khi cài đặt)

## Khắc phục nhanh

**Lỗi: Module not found**
```bash
pip install -r requirements.txt
```

**Lỗi: Webcam không hoạt động**
- Kiểm tra Settings > Privacy > Camera
- Cho phép ứng dụng truy cập camera

**Lỗi: Font không hiển thị**
- Cập nhật Windows
- Font mặc định: Segoe UI (có sẵn trên Windows)

## Liên hệ

Nếu gặp vấn đề, xem thêm:
- `HUONG_DAN_CAI_DAT.md` - Hướng dẫn chi tiết
- `HUONG_DAN_DANG_NHAP_KHUON_MAT.md` - Hướng dẫn xác thực
- `README.md` - Tài liệu đầy đủ
