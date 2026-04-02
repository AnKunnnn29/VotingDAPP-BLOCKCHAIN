# HƯỚNG DẪN SỬ DỤNG TÍNH NĂNG BẢO MẬT NÂNG CAO

## 📋 TỔNG QUAN

Hệ thống đã được nâng cấp với 4 tính năng bảo mật chính:

1. **Advanced Face Recognition** - Nhận diện khuôn mặt nâng cao với Deep Learning
2. **Liveness Detection** - Phát hiện người thật (chống ảnh in, video)
3. **Anonymous Token** - Token ẩn danh để tách biệt danh tính và phiếu bầu
4. **Zero-Knowledge Proof (ZKP)** - Chứng minh hợp lệ mà không tiết lộ danh tính

---

## 1. ADVANCED FACE RECOGNITION + LIVENESS DETECTION

### 1.1. Cài Đặt Thư Viện

```bash
# Cài đặt thư viện bổ sung
pip install face-recognition dlib scipy

# Lưu ý: dlib cần CMake và Visual Studio Build Tools trên Windows
# Nếu gặp lỗi, cài đặt từ wheel:
pip install dlib-19.24.0-cp310-cp310-win_amd64.whl
```

### 1.2. Sử Dụng Trong Code

```python
from services.face_recognition_service_advanced import FaceRecognitionServiceAdvanced

# Khởi tạo service
face_service = FaceRecognitionServiceAdvanced()

# Đăng ký khuôn mặt (với liveness detection)
success = face_service.register_face(
    cccd="123456789012",
    name="Nguyễn Văn A"
)

# Quy trình đăng ký:
# 1. Nhấp nháy mắt 2-3 lần (5 giây)
# 2. Quay đầu sang trái, sau đó sang phải (5 giây)
# 3. Nhấn SPACE để chụp ảnh

# Xác thực khuôn mặt (với liveness detection)
is_match, confidence = face_service.verify_face(cccd="123456789012")

if is_match:
    print(f"✅ Xác thực thành công! Độ tin cậy: {confidence:.2%}")
else:
    print(f"❌ Xác thực thất bại! Độ tin cậy: {confidence:.2%}")
```

### 1.3. So Sánh Với Phiên Bản Cũ

| Tính năng | Phiên bản cũ | Phiên bản mới |
|-----------|--------------|---------------|
| Thuật toán | Correlation | Deep Learning (128-D) |
| Độ chính xác | 60-70% | 95-99% |
| Liveness Detection | ❌ Không | ✅ Có (blink + movement) |
| Chống ảnh in | ❌ Không | ✅ Có |
| Chống video | ❌ Không | ✅ Có (cơ bản) |
| Threshold | 0.6 (60%) | 0.4 (40% distance) |

### 1.4. Lưu Ý

- Cần webcam hoạt động tốt
- Ánh sáng đủ (không quá tối hoặc quá sáng)
- Khuôn mặt nhìn thẳng vào camera
- Thực hiện đúng các bước liveness detection

---

## 2. ANONYMOUS TOKEN SYSTEM

### 2.1. Kiến Trúc

```
┌─────────────────────────────────────────────────────────────┐
│                    IDENTITY DATABASE                        │
│  (Riêng biệt, bảo mật cao)                                 │
│                                                             │
│  CCCD: 123456789012  →  Token: abc123...                   │
│  CCCD: 123456789013  →  Token: def456...                   │
│  CCCD: 123456789014  →  Token: ghi789...                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (Sau bầu cử: XÓA)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    VOTING DATABASE                          │
│  (Không có thông tin cá nhân)                              │
│                                                             │
│  Token: abc123...  →  Used: True                           │
│  Token: def456...  →  Used: True                           │
│  Token: ghi789...  →  Used: False                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      BLOCKCHAIN                             │
│  (Chỉ có token, không có CCCD)                             │
│                                                             │
│  Block #1: Token=abc123... → Proposal=5                    │
│  Block #2: Token=def456... → Proposal=3                    │
└─────────────────────────────────────────────────────────────┘
```

### 2.2. Sử Dụng

```python
from services.anonymous_token_service import AnonymousTokenService

# Khởi tạo service
token_service = AnonymousTokenService()

# Tạo anonymous token cho cử tri
token = token_service.generate_anonymous_token(
    cccd="123456789012",
    election_id=1
)
print(f"Token: {token}")  # abc123def456...

# Kiểm tra token hợp lệ
is_valid = token_service.verify_token(token, election_id=1)

# Đánh dấu token đã sử dụng (sau khi bỏ phiếu)
token_service.mark_token_used(token)

# Kiểm tra token đã dùng chưa
is_used = token_service.is_token_used(token)

# SAU BẦU CỬ: Xóa identity mapping (QUAN TRỌNG!)
token_service.revoke_identity_mapping(election_id=1)

# Sau khi revoke, không thể trace token về CCCD nữa
cccd = token_service.get_cccd_by_token(token, election_id=1)
# cccd = None (Privacy protected!)
```

### 2.3. Quy Trình Bỏ Phiếu Với Token

```python
from services.voting_service_enhanced import VotingServiceEnhanced

# Khởi tạo
voting_service = VotingServiceEnhanced(db_manager, blockchain)

# Set privacy mode = 'token'
voting_service.set_privacy_mode('token')

# Bước 1: Cử tri đăng nhập (xác thực khuôn mặt)
voter = authenticate_voter_with_face(cccd="123456789012")

# Bước 2: Tạo anonymous token
success, message = voting_service.prepare_voter_for_election(voter, election)

# Bước 3: Bỏ phiếu với token (không dùng voter_id)
success, message = voting_service.cast_vote(voter, proposal_id=5, election=election)

# Blockchain lưu: Token + Proposal (KHÔNG có CCCD/voter_id)

# Bước 4: Sau bầu cử, revoke identity mapping
voting_service.finalize_election(election)
# → Từ giờ KHÔNG THỂ trace votes về voters!
```

### 2.4. Thống Kê

```python
# Xem thống kê
stats = token_service.get_statistics(election_id=1)

print(f"Total tokens: {stats['total_tokens']}")
print(f"Used tokens: {stats['used_tokens']}")
print(f"Identity mappings exist: {stats['identity_mappings_exist']}")
print(f"Privacy protected: {stats['privacy_protected']}")
```

---

## 3. ZERO-KNOWLEDGE PROOF (ZKP) VOTING

### 3.1. Concept

Zero-Knowledge Proof cho phép:
- Chứng minh bạn là cử tri hợp lệ
- KHÔNG tiết lộ voter_id
- Ngăn double voting bằng nullifier
- Hoàn toàn ẩn danh

### 3.2. Sử Dụng

```python
from services.zkp_service import ZKPVotingSystem

# Khởi tạo
zkp_system = ZKPVotingSystem()

# Danh sách cử tri đã đăng ký
registered_voters = [1, 2, 3, 4, 5]

# Bỏ phiếu ẩn danh
success, message = zkp_system.cast_anonymous_vote(
    voter_id=1,           # Sẽ được ẩn trong proof
    proposal_id=5,
    election_id=1,
    registered_voters=registered_voters
)

if success:
    print("✅ Bỏ phiếu ẩn danh thành công!")
    print("⚠️ Blockchain KHÔNG chứa voter_id")
    print("⚠️ Chỉ có nullifier (không thể trace)")

# Thử bỏ phiếu lần 2 (double voting)
success2, message2 = zkp_system.cast_anonymous_vote(
    voter_id=1,           # Cùng voter
    proposal_id=3,        # Proposal khác
    election_id=1,
    registered_voters=registered_voters
)
# → Thất bại: "Nullifier đã được sử dụng"

# Xem kết quả
results = zkp_system.get_results(election_id=1)
print(f"Total votes: {results['total_votes']}")
print(f"Results: {results['results']}")
print(f"Privacy preserved: {results['privacy_preserved']}")
```

### 3.3. Tích Hợp Với Voting Service

```python
from services.voting_service_enhanced import VotingServiceEnhanced

# Khởi tạo
voting_service = VotingServiceEnhanced(db_manager, blockchain)

# Set privacy mode = 'zkp'
voting_service.set_privacy_mode('zkp')

# Bỏ phiếu (tự động dùng ZKP)
success, message = voting_service.cast_vote(voter, proposal_id=5, election=election)

# Xem kết quả ZKP
results = voting_service.get_election_results_zkp(election_id=1)
```

### 3.4. So Sánh Token vs ZKP

| Tính năng | Anonymous Token | Zero-Knowledge Proof |
|-----------|-----------------|----------------------|
| Độ phức tạp | Thấp | Cao |
| Tốc độ | Nhanh | Chậm hơn |
| Privacy | Tốt (sau revoke) | Tuyệt vời (ngay lập tức) |
| Trace về voter | Có thể (trước revoke) | Không thể |
| Double voting | Ngăn bằng token | Ngăn bằng nullifier |
| Blockchain size | Nhỏ | Lớn hơn (chứa proof) |
| Khuyến nghị | ✅ Cho production | ⚠️ Cho high-security |

---

## 4. DEMO SCRIPT

### 4.1. Chạy Demo

```bash
# Chạy demo đầy đủ
python demo_privacy_features.py

# Menu:
# 1. Advanced Face Recognition + Liveness Detection
# 2. Anonymous Token System
# 3. Zero-Knowledge Proof Voting
# 4. Full Workflow (Token + ZKP)
# 5. Chạy tất cả demos
```

### 4.2. Demo Từng Tính Năng

```python
# Demo 1: Face Recognition
from demo_privacy_features import demo_face_recognition_advanced
demo_face_recognition_advanced()

# Demo 2: Anonymous Token
from demo_privacy_features import demo_anonymous_token
demo_anonymous_token()

# Demo 3: ZKP Voting
from demo_privacy_features import demo_zkp_voting
demo_zkp_voting()

# Demo 4: Full Workflow
from demo_privacy_features import demo_full_workflow
demo_full_workflow()
```

---

## 5. TÍCH HỢP VÀO HỆ THỐNG CHÍNH

### 5.1. Cập Nhật main.py

```python
# Thêm import
from services.face_recognition_service_advanced import FaceRecognitionServiceAdvanced
from services.voting_service_enhanced import VotingServiceEnhanced

# Thay thế service cũ
# face_service = FaceRecognitionService()  # Cũ
face_service = FaceRecognitionServiceAdvanced()  # Mới

# voting_service = VotingService(db_manager, blockchain)  # Cũ
voting_service = VotingServiceEnhanced(db_manager, blockchain)  # Mới

# Set privacy mode
voting_service.set_privacy_mode('token')  # hoặc 'zkp'
```

### 5.2. Cập Nhật UI

```python
# Trong login dialog
from services.face_recognition_service_advanced import FaceRecognitionServiceAdvanced

class LoginDialogFace(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Dùng service mới
        self.face_service = FaceRecognitionServiceAdvanced()
        
    def verify_face(self):
        # Xác thực với liveness detection
        is_match, confidence = self.face_service.verify_face(self.cccd)
        if is_match:
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi", "Xác thực khuôn mặt thất bại")
```

### 5.3. Thêm Nút Finalize Election

```python
# Trong admin view
def finalize_election(self):
    """Finalize election và revoke identity mapping"""
    election = self.get_current_election()
    
    reply = QMessageBox.question(
        self,
        "Xác nhận",
        "Finalize election sẽ XÓA identity mapping.\n"
        "Sau đó KHÔNG THỂ trace votes về voters.\n"
        "Bạn có chắc chắn?",
        QMessageBox.Yes | QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        self.voting_service.finalize_election(election)
        QMessageBox.information(self, "Thành công", "Election đã được finalized!")
```

---

## 6. BEST PRACTICES

### 6.1. Bảo Mật

1. **Luôn revoke identity mapping sau bầu cử**
   ```python
   voting_service.finalize_election(election)
   ```

2. **Mã hóa token database**
   ```python
   # Trong production, mã hóa file anonymous_tokens.json
   # Sử dụng AES-256 hoặc lưu trong HSM
   ```

3. **Xóa log nhạy cảm**
   ```python
   # Không log CCCD, token, hoặc mapping
   # Chỉ log events (voted, not voted)
   ```

4. **Backup trước khi revoke**
   ```python
   # Backup identity mapping (encrypted) trước khi revoke
   # Chỉ để audit, không để trace votes
   ```

### 6.2. Performance

1. **Sử dụng Token mode cho production**
   - Nhanh hơn ZKP
   - Đủ privacy sau revoke
   - Dễ debug

2. **Chỉ dùng ZKP khi cần privacy tối đa**
   - Bầu cử nhạy cảm
   - Yêu cầu pháp lý cao
   - Có đủ tài nguyên

3. **Optimize face recognition**
   ```python
   # Giảm resolution nếu chậm
   resized = cv2.resize(face_img, (640, 480))
   
   # Cache face encodings
   # Không cần re-encode mỗi lần verify
   ```

### 6.3. User Experience

1. **Hướng dẫn rõ ràng cho liveness detection**
   - Video demo
   - Hình ảnh minh họa
   - Thông báo từng bước

2. **Fallback nếu liveness fail**
   ```python
   # Cho phép retry 3 lần
   # Hoặc fallback về phương pháp cũ (với cảnh báo)
   ```

3. **Thông báo về privacy**
   ```python
   # Hiển thị: "Phiếu bầu của bạn hoàn toàn ẩn danh"
   # "Sau bầu cử, không ai có thể biết bạn bầu cho ai"
   ```

---

## 7. TROUBLESHOOTING

### 7.1. Lỗi Cài Đặt dlib

```bash
# Windows: Tải wheel từ
# https://github.com/z-mahmud22/Dlib_Windows_Python3.x
pip install dlib-19.24.0-cp310-cp310-win_amd64.whl

# Linux:
sudo apt-get install cmake
pip install dlib

# Mac:
brew install cmake
pip install dlib
```

### 7.2. Lỗi Webcam

```python
# Kiểm tra webcam
import cv2
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam không hoạt động")
    # Thử index khác: 1, 2, ...
    cap = cv2.VideoCapture(1)
```

### 7.3. Lỗi Liveness Detection

```python
# Nếu blink detection không hoạt động
# Kiểm tra eye cascade
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)
if eye_cascade.empty():
    print("Eye cascade không load được")
```

### 7.4. Performance Issues

```python
# Giảm difficulty cho blockchain
blockchain = Blockchain(difficulty=2)  # Thay vì 4

# Giảm thời gian liveness detection
blink_count = self.detect_blinks(cap, duration=3)  # Thay vì 5

# Skip liveness cho testing
face_img = self.capture_face()  # Không có liveness
```

---

## 8. KẾT LUẬN

Hệ thống đã được nâng cấp với các tính năng bảo mật tiên tiến:

✅ **Face Recognition**: Deep learning + Liveness detection
✅ **Anonymous Token**: Tách biệt identity và votes
✅ **Zero-Knowledge Proof**: Privacy tối đa
✅ **Identity Revocation**: Xóa mapping sau bầu cử

**Khuyến nghị cho production**:
- Sử dụng Token mode (đủ privacy, performance tốt)
- Luôn revoke identity mapping sau bầu cử
- Backup encrypted trước khi revoke
- Test kỹ liveness detection với nhiều điều kiện ánh sáng

**Roadmap tiếp theo**:
- Homomorphic Encryption cho vote counting
- Multi-party computation cho tallying
- Hardware Security Module (HSM) cho key storage
- Audit trail với tamper-proof logging
