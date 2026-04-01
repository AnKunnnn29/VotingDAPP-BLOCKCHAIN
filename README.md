# 🗳️ DApp Voting System - Hệ thống bỏ phiếu phi tập trung

Ứng dụng Python mô phỏng hệ thống bỏ phiếu phi tập trung (Decentralized Voting DApp) dựa trên blockchain và smart contract.

## ✨ Tính năng chính

### 🔐 Bảo mật & Mật mã
- **Chữ ký số RSA**: Mỗi cử tri có cặp khóa công khai/riêng tư
- **Xác thực lá phiếu**: Mỗi phiếu được ký số và xác minh
- **Blockchain bất biến**: Lưu trữ phiếu bầu trong sổ cái phi tập trung
- **Hash linking**: Mỗi block liên kết với block trước đó

### 🔄 Smart Contract State Machine
Quy trình bỏ phiếu tuân theo state machine:
```
Start → ValidateVoter → Vote → Count → DeclareWinner → Done
```

### ⛓️ Hai chế độ Blockchain
- **Permissionless**: Mọi cử tri có thể bỏ phiếu (giống Ethereum)
- **Permissioned**: Chỉ cử tri đã xác thực mới được bỏ phiếu (giống Hyperledger)

### 👥 Hai vai trò người dùng

#### Cử tri
- Đăng nhập và xác thực danh tính
- Xem danh sách ứng viên
- Bỏ phiếu cho 1 ứng viên (chỉ 1 lần)
- Xem trạng thái phiếu trên blockchain
- Xem kết quả sau khi công bố

#### Quản trị viên
- Tạo cuộc bầu cử mới
- Quản lý ứng viên (thêm/sửa/xóa)
- Quản lý cử tri và xác thực
- Điều khiển state machine
- Kiểm phiếu và công bố kết quả
- Xem blockchain ledger
- Kiểm tra tính toàn vẹn blockchain

## 🛠️ Công nghệ sử dụng

- **Python 3.8+**
- **PySide6**: Giao diện GUI hiện đại
- **cryptography**: Mật mã RSA và chữ ký số
- **SQLite**: Lưu trữ dữ liệu
- **matplotlib**: Biểu đồ kết quả

## 📦 Cài đặt

### 1. Clone hoặc tải project

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
python main.py
```

## 🚀 Hướng dẫn sử dụng

### Lần đầu chạy
Ứng dụng sẽ tự động tạo 20 cử tri mẫu (ID từ 1-20):
- Cử tri 1-10: Đã xác thực
- Cử tri 11-20: Chưa xác thực

### Đăng nhập

#### Đăng nhập với vai trò Quản trị viên
- Chọn vai trò: "Quản trị viên"
- Nhập mã: `admin`

#### Đăng nhập với vai trò Cử tri
- Chọn vai trò: "Cử tri"
- Nhập mã: Số từ 1-20 (ví dụ: `1`, `5`, `15`)

### Quy trình bầu cử (Admin)

1. **Tạo cuộc bầu cử**
   - Vào tab "📋 Cuộc bầu cử"
   - Click "➕ Tạo cuộc bầu cử mới"
   - Nhập thông tin và chọn chế độ blockchain

2. **Thêm ứng viên**
   - Vào tab "🎯 Ứng viên"
   - Click "➕ Thêm ứng viên"
   - Nhập tên và mô tả ứng viên

3. **Quản lý cử tri**
   - Vào tab "👥 Cử tri"
   - Thêm cử tri mới hoặc xác thực cử tri hiện có

4. **Chuyển trạng thái**
   - Vào tab "📋 Cuộc bầu cử"
   - Click các nút theo thứ tự:
     - 1️⃣ Xác thực cử tri
     - 2️⃣ Mở bỏ phiếu
     - (Cử tri bỏ phiếu)
     - 3️⃣ Kiểm phiếu
     - 4️⃣ Công bố
     - 5️⃣ Kết thúc

5. **Xem kết quả**
   - Vào tab "📊 Kết quả"
   - Click "📊 Xem biểu đồ" để xem biểu đồ

### Quy trình bỏ phiếu (Cử tri)

1. Đăng nhập với mã cử tri
2. Xem danh sách ứng viên
3. Chọn 1 ứng viên
4. Click "🗳️ Bỏ phiếu"
5. Xác nhận
6. Click "📊 Xem trạng thái phiếu" để xem phiếu trên blockchain
7. Sau khi admin công bố, click "📈 Xem kết quả"

## 🏗️ Kiến trúc hệ thống

### Cấu trúc thư mục
```
voting-dapp/
├── main.py                 # Entry point
├── models/                 # Data models
│   ├── voter.py           # Voter model
│   ├── proposal.py        # Proposal model
│   └── election.py        # Election model
├── blockchain/            # Blockchain implementation
│   ├── block.py          # Block structure
│   └── blockchain.py     # Blockchain ledger
├── services/             # Business logic
│   ├── crypto_service.py    # Cryptography
│   ├── voting_service.py    # Voting operations
│   ├── auth_service.py      # Authentication
│   └── election_service.py  # Election management
├── database/             # Data persistence
│   └── db_manager.py    # SQLite manager
├── ui/                   # User interface
│   ├── main_window.py   # Main window
│   ├── login_dialog.py  # Login dialog
│   ├── voter_view.py    # Voter interface
│   ├── admin_view.py    # Admin interface
│   └── styles.py        # Modern stylesheet
└── utils/               # Utilities
    └── constants.py     # Constants
```

### Luồng dữ liệu

```
UI Layer
    ↓
Service Layer (Business Logic)
    ↓
Blockchain Layer ← Crypto Service
    ↓
Database Layer (SQLite)
```

## 🔒 Mô phỏng Blockchain

### Block Structure
Mỗi block chứa:
- `index`: Vị trí trong chain
- `timestamp`: Thời gian tạo
- `voter_id`: ID cử tri
- `proposal_id`: ID ứng viên
- `signature`: Chữ ký số
- `previous_hash`: Hash của block trước
- `hash`: Hash của block hiện tại

### Tính toàn vẹn
- Mỗi block liên kết với block trước qua `previous_hash`
- Thay đổi bất kỳ dữ liệu nào sẽ làm hash không khớp
- Có thể kiểm tra tính toàn vẹn toàn bộ chain

## 🎯 Phản ánh lý thuyết DApp Voting

### 1. Smart Contract State Machine
- Quy trình bỏ phiếu tuân theo state machine nghiêm ngặt
- Mỗi hành động chỉ được thực hiện ở đúng trạng thái

### 2. Cryptographic Identity
- Mỗi cử tri có cặp khóa RSA 2048-bit
- Phiếu bầu được ký số bằng private key
- Xác thực bằng public key

### 3. Immutable Ledger
- Mỗi phiếu được ghi vào blockchain
- Không thể sửa đổi sau khi ghi
- Có thể audit toàn bộ lịch sử

### 4. Permissionless vs Permissioned
- **Permissionless**: Phi tập trung cao, ai cũng tham gia được
- **Permissioned**: Tốc độ cao hơn, chỉ người được phép

### 5. Transparency & Auditability
- Mọi phiếu đều công khai trên blockchain
- Có thể kiểm tra tính toàn vẹn bất kỳ lúc nào
- Kết quả minh bạch và có thể xác minh

## ⚠️ Giới hạn & Trade-offs

### Scalability
- Với số lượng cử tri lớn (hàng triệu), cần tối ưu hóa
- Blockchain size tăng theo số phiếu

### Security vs Usability
- Private key cần được bảo vệ cẩn thận
- Mất private key = mất quyền bỏ phiếu

### Decentralization vs Performance
- Permissionless: Phi tập trung cao nhưng chậm hơn
- Permissioned: Nhanh hơn nhưng kém phi tập trung

### Smart Contract Bugs
- Lỗi trong logic state machine có thể ảnh hưởng kết quả
- Cần audit kỹ lưỡng trước khi triển khai thật

## 📊 Demo Data

Ứng dụng đi kèm với dữ liệu mẫu:
- 20 cử tri (ID 1-20)
- 10 cử tri đầu đã được xác thực
- Có thể thêm ứng viên và tạo cuộc bầu cử mới

## 🎨 Giao diện

Ứng dụng sử dụng Material Design với:
- Màu sắc hiện đại (Blue primary, Green success, Red danger)
- Typography rõ ràng
- Icons trực quan
- Tables và forms dễ sử dụng
- Responsive layout

## 🔧 Troubleshooting

### Lỗi import PySide6
```bash
pip install --upgrade PySide6
```

### Lỗi cryptography
```bash
pip install --upgrade cryptography
```

### Database bị lỗi
Xóa file `voting_dapp.db` và chạy lại ứng dụng

## 📝 License

Đây là ứng dụng demo/học thuật cho mục đích giáo dục.

## 👨‍💻 Tác giả

Được xây dựng như một ứng dụng mẫu để minh họa các khái niệm:
- Blockchain và distributed ledger
- Smart contract state machine
- Digital signatures và cryptography
- Decentralized application (DApp)
- Modern Python GUI development

---

**Lưu ý**: Đây là ứng dụng demo, không nên sử dụng cho bầu cử thực tế mà không có audit bảo mật đầy đủ.
