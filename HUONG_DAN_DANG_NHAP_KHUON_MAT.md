# Hướng dẫn đăng nhập bằng CCCD và khuôn mặt

## Tính năng mới

Hệ thống đã được nâng cấp với tính năng xác thực 2 lớp:
1. **CCCD (Căn cước công dân)**: Nhập số CCCD 12 chữ số
2. **Nhận diện khuôn mặt**: Quét khuôn mặt qua webcam

## Quy trình đăng nhập cho Cử tri

### Bước 1: Chọn vai trò
- Chọn "Cử tri" trong dropdown

### Bước 2: Nhập CCCD
- Nhập số CCCD 12 chữ số
- Ví dụ: 001123456789, 002123456789, ...

### Bước 3: Quét khuôn mặt

#### Lần đầu tiên (Đăng ký khuôn mặt):
1. Click nút "📸 Quét khuôn mặt"
2. Hệ thống sẽ hỏi có muốn đăng ký khuôn mặt không
3. Click "Yes" để đăng ký
4. Webcam sẽ mở:
   - Đặt khuôn mặt vào khung hình
   - Đảm bảo ánh sáng đủ
   - Nhìn thẳng vào camera
   - Nhấn **SPACE** để chụp
   - Nhấn **ESC** để hủy
5. Sau khi đăng ký thành công, quét lại lần nữa để xác thực

#### Lần sau (Xác thực):
1. Click nút "📸 Quét khuôn mặt"
2. Webcam sẽ mở
3. Đặt khuôn mặt vào khung hình
4. Nhấn **SPACE** để xác thực
5. Hệ thống sẽ hiển thị kết quả:
   - ✅ Xác thực thành công: Độ tin cậy > 60%
   - ❌ Xác thực thất bại: Độ tin cậy < 60%

### Bước 4: Đăng nhập
- Sau khi xác thực khuôn mặt thành công
- Nút "🚀 Đăng nhập" sẽ được kích hoạt
- Click để đăng nhập vào hệ thống

## Quy trình đăng nhập cho Quản trị viên

### Bước 1: Chọn vai trò
- Chọn "Quản trị viên" trong dropdown

### Bước 2: Nhập mã
- Nhập "admin" (không phân biệt hoa thường)

### Bước 3: Đăng nhập
- Click nút "🚀 Đăng nhập"

## Lưu ý quan trọng

### Về CCCD:
- Phải đúng 12 chữ số
- Phải đã được đăng ký trong hệ thống
- Mỗi CCCD chỉ đăng ký 1 khuôn mặt

### Về nhận diện khuôn mặt:
- Cần webcam hoạt động tốt
- Ánh sáng đủ, không quá tối hoặc quá sáng
- Nhìn thẳng vào camera
- Không đeo khẩu trang, kính đen
- Khuôn mặt phải rõ ràng, không bị che khuất

### Về bảo mật:
- Dữ liệu khuôn mặt được lưu mã hóa
- Mỗi lần đăng nhập cần xác thực lại
- Không thể sử dụng ảnh để đăng nhập (hệ thống phát hiện khuôn mặt thật)

## Khắc phục sự cố

### Webcam không mở:
```
- Kiểm tra webcam đã kết nối
- Cho phép ứng dụng truy cập camera
- Đóng các ứng dụng khác đang dùng webcam
```

### Không phát hiện khuôn mặt:
```
- Di chuyển gần camera hơn
- Cải thiện ánh sáng
- Nhìn thẳng vào camera
- Đảm bảo khuôn mặt không bị che
```

### Xác thực thất bại:
```
- Thử lại với ánh sáng tốt hơn
- Đảm bảo cùng điều kiện với lúc đăng ký
- Nếu vẫn lỗi, liên hệ admin để đăng ký lại
```

### CCCD không tìm thấy:
```
- Kiểm tra lại số CCCD
- Liên hệ quản trị viên để đăng ký
```

## Dữ liệu mẫu

Hệ thống có 20 cử tri mẫu với CCCD:
- Cử tri 1: **001123456789**
- Cử tri 2: **002123456789**
- Cử tri 3: **003123456789**
- ...
- Cử tri 20: **020123456789**

Bạn có thể sử dụng bất kỳ CCCD nào để test hệ thống.

## Demo nhanh

1. Chạy ứng dụng: `python main.py`
2. Chọn "Cử tri"
3. Nhập CCCD: `001123456789`
4. Click "📸 Quét khuôn mặt"
5. Đăng ký khuôn mặt lần đầu
6. Quét lại để xác thực
7. Đăng nhập thành công!
