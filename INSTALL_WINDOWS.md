# 💻 Hướng dẫn cài đặt trên Windows

## Yêu cầu hệ thống
- Windows 10/11
- Python 3.8 trở lên
- 2GB RAM trở lên
- 500MB dung lượng trống

## Bước 1: Kiểm tra Python

Mở Command Prompt hoặc PowerShell và chạy:
```bash
python --version
```

Nếu chưa có Python, tải tại: https://www.python.org/downloads/

**Lưu ý**: Khi cài Python, nhớ tick "Add Python to PATH"

## Bước 2: Tải project

Giải nén project vào thư mục, ví dụ:
```
D:\Projects\voting-dapp\
```

## Bước 3: Mở Command Prompt tại thư mục project

Cách 1: Shift + Right click trong thư mục → "Open PowerShell window here"

Cách 2: Mở Command Prompt và cd vào thư mục:
```bash
cd D:\Projects\voting-dapp
```

## Bước 4: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Nếu gặp lỗi, thử:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Cài đặt từng package riêng (nếu cần)
```bash
pip install PySide6==6.6.1
pip install cryptography==41.0.7
pip install matplotlib==3.8.2
```

## Bước 5: Chạy ứng dụng

### Cách 1: Chạy trực tiếp
```bash
python main.py
```

### Cách 2: Setup demo data trước
```bash
python demo_setup.py
python main.py
```

## Bước 6: Đăng nhập

### Đăng nhập Admin
- Vai trò: Quản trị viên
- Mã số: `admin`

### Đăng nhập Cử tri
- Vai trò: Cử tri
- Mã số: `1` đến `20`

## Troubleshooting

### Lỗi: "No module named 'PySide6'"
```bash
pip install PySide6
```

### Lỗi: "No module named 'cryptography'"
```bash
pip install cryptography
```

### Lỗi: "Microsoft Visual C++ 14.0 is required"
Tải và cài đặt: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Lỗi: "pip is not recognized"
Python chưa được thêm vào PATH. Cài lại Python và tick "Add to PATH"

### Lỗi: Database locked
Đóng tất cả instances của app và chạy lại

### Muốn reset dữ liệu
```bash
del voting_dapp.db
python main.py
```

## Kiểm tra cài đặt thành công

Sau khi chạy `python main.py`, bạn sẽ thấy:
1. Cửa sổ đăng nhập hiện ra
2. Giao diện màu xanh hiện đại
3. Có thể đăng nhập với admin hoặc voter

## Cấu trúc sau khi chạy

```
voting-dapp/
├── voting_dapp.db          # Database (tự động tạo)
├── __pycache__/            # Python cache (tự động tạo)
├── models/__pycache__/
├── services/__pycache__/
└── ... (các file code)
```

## Chạy demo nhanh

```bash
# Setup demo data với 20 voters và 3 candidates
python demo_setup.py

# Chạy app
python main.py

# Login as admin → Setup election → Open voting
# Login as voter 1 → Vote
# Login as admin → Count → Declare → Done
```

## Gỡ cài đặt

Để gỡ bỏ hoàn toàn:
```bash
# Xóa dependencies
pip uninstall PySide6 cryptography matplotlib -y

# Xóa thư mục project
rmdir /s voting-dapp
```

---

**Nếu gặp vấn đề, hãy kiểm tra:**
1. Python version >= 3.8
2. pip đã được cập nhật
3. Có quyền ghi file trong thư mục
4. Không có antivirus chặn Python
