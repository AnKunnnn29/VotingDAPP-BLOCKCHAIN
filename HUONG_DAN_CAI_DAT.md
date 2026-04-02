# Hướng dẫn cài đặt hệ thống bầu cử Blockchain

## Yêu cầu hệ thống
- Python 3.8 trở lên
- Webcam (cho tính năng nhận diện khuôn mặt)
- Windows 10/11

## Các bước cài đặt

### 1. Cài đặt Python
Tải và cài đặt Python từ: https://www.python.org/downloads/

Lưu ý: Chọn "Add Python to PATH" khi cài đặt

### 2. Cài đặt thư viện

#### Cách 1: Sử dụng file batch (Khuyến nghị)
```bash
install_requirements.bat
```

#### Cách 2: Cài đặt thủ công
```bash
pip install -r requirements.txt
```

### 3. Khởi tạo cơ sở dữ liệu
```bash
python demo_setup.py
```

### 4. Chạy ứng dụng
```bash
python main.py
```

## Thư viện được cài đặt

- **PySide6**: Framework giao diện người dùng
- **cryptography**: Mã hóa và chữ ký số
- **matplotlib**: Vẽ biểu đồ thống kê
- **opencv-python**: Xử lý hình ảnh và nhận diện khuôn mặt
- **numpy**: Tính toán số học
- **Pillow**: Xử lý ảnh

## Khắc phục sự cố

### Lỗi: "pip không được nhận dạng"
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Lỗi: "Không tìm thấy webcam"
- Kiểm tra webcam đã được kết nối
- Cho phép ứng dụng truy cập camera trong Settings > Privacy > Camera

### Lỗi font
- Hệ thống sử dụng font "Segoe UI" có sẵn trên Windows
- Nếu gặp lỗi hiển thị, cập nhật Windows

## Dữ liệu mẫu

Hệ thống tự động tạo 20 cử tri mẫu với CCCD:
- Cử tri 1: CCCD 001123456789
- Cử tri 2: CCCD 002123456789
- ...
- Cử tri 20: CCCD 020123456789

Admin: Nhập "admin" khi đăng nhập với vai trò Quản trị viên
