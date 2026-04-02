# BÁO CÁO TỔNG KẾT DỰ ÁN: HỆ THỐNG BỎ PHIẾU PHI TẬP TRUNG (VOTING DAPP)

## 1. TỔNG QUAN DỰ ÁN
Dự án là một ứng dụng phần mềm mô phỏng hệ thống bỏ phiếu phi tập trung dựa trên công nghệ Blockchain và Smart Contract. Được xây dựng trên nền tảng Python (với PySide6 cho giao diện người dùng), hệ thống minh họa cách thức tổ chức một cuộc bầu cử minh bạch, bất biến và có tính bảo mật cao, từ việc đăng ký cử tri đến quá trình bỏ phiếu và kiểm phiếu.

## 2. KIẾN TRÚC HỆ THỐNG
Hệ thống được thiết kế theo mô hình phân lớp rõ ràng nhằm dễ dàng bảo trì và mở rộng:

- **UI Layer (Giao diện người dùng):** Sử dụng `PySide6` để xây dựng giao diện trực quan, kết hợp kiến trúc View-Controller tách biệt. Có hai phân hệ chính: Admin (Quản trị viên) và Voter (Cử tri).
- **Service Layer (Xử lý nghiệp vụ):** Các file `.py` nằm ở thư mục `services/` điều phối toàn bộ luồng logic của ứng dụng. Bao gồm quản lý bầu cử (`election_service.py`), mã hóa chữ ký (`crypto_service.py`), quản lý bầu cử nâng cao có bảo mật (`voting_service_enhanced.py`).
- **Blockchain Layer:** Mô phỏng mạng lưới phân tán. Mỗi lá phiếu là một `Block` được liên kết với khối trước bởi hàm băm mật mã học (Hash Linking), đảm bảo dữ liệu không bị thay đổi sau khi ghi nhận.
- **Database Layer:** Dữ liệu off-chain (như danh sách cử tri, mapping danh tính) được lưu trữ tại SQLite.

## 3. TÍNH NĂNG CHÍNH VÀ QUY TRÌNH BỎ PHIẾU

### 3.1 Chức năng Quản lý (Dành cho Quản trị viên)
- Khởi tạo cuộc bầu cử và điều khiển quá trình theo một vòng đời nghiêm ngặt (Start → ValidateVoter → Vote → Count → DeclareWinner → Done).
- Quản lý ứng cử viên và cử tri. Có cả 2 dạng: Permissionless (Ai cũng được bầu) và Permissioned (Cần được quyền).
- Kiểm tra tính toàn vẹn của chuỗi khối (Ledger Audit) để phát hiện sự gian lận.

### 3.2 Quy trình Bỏ phiếu (Dành cho Cử tri)
- Xác thực danh tính (e-KYC).
- Chọn ứng viên và thực hiện bỏ phiếu ẩn danh.
- Theo dõi trạng thái lá phiếu trên sổ cái công khai (Public Ledger).

## 4. CÁC TÍNH NĂNG BẢO MẬT NÂNG CAO (MỚI CẬP NHẬT)
Gần đây, dự án đã được tích hợp bộ công nghệ bảo mật chuyên sâu để hướng tới tiêu chuẩn thực tế:

1. **Nhận diện khuôn mặt & Liveness Detection (`face_recognition_service_advanced.py`)**
   - Sự dụng Deep Learning (128-D encoding) để đạt độ chính xác trên 95%.
   - Liveness Detection yêu cầu người dùng nháy mắt hoặc quay đầu để chống lại hành vi gian lận qua hình ảnh không chuyển động hoặc video deepfake thô sơ.

2. **Cơ chế Token Ẩn danh (Anonymous Token System)**
   - Hệ thống phát hành Token một lần dựa trên CCCD nhưng lưu tách biệt giữa Identity Database và Voting Database.
   - Quá trình bỏ phiếu lưu Token lên Blockchain. Sau khi hoàn thành, Identity Mapping bị phá hủy, khiến hệ thống hoàn toàn ẩn danh. Ngay cả hệ thống cũng không thể truy ngược từ phiếu bầu ra danh tính.

3. **Zero-Knowledge Proof (ZKP - Công nghệ Không tri thức)**
   - Cho phép hệ thống chứng minh cử tri đã thao tác hợp lệ mà *không* cần tiết lộ ID của họ trên Blockchain.
   - Kết hợp sử dụng khái niệm `Nullifier` trong mật mã để vừa ngăn chặn gian lận "Bỏ phiếu kép" (Double voting) vừa đảm bảo không để lộ dấu vết giao dịch của cá nhân.

## 5. ĐÁNH GIÁ VÀ KẾT LUẬN

**Ưu điểm của hệ thống:**
- Giải quyết triệt để vấn đề Sybil Attack, đảm bảo tính duy nhất qua nhận diện sinh trắc học.
- Bảo mật quyền riêng tư của cử tri (ẩn danh tuyệt đối) qua Token & ZKP.
- Thiết kế hiện đại, mô phỏng chân thực quy trình Smart Contract thông qua mô hình chuyển tiếp trạng thái.

**Hướng phát triển trong tương lai:**
- Gắn kết với các hệ thống mã hóa đồng dạng (Homomorphic Encryption) tại khâu tính phiếu để hệ triệt tiêu hoàn toàn khả năng lộ thông tin sớm.
- Thay vì cơ sở dữ liệu giả lập, có thể viết lại Smart Contract thật bằng Solidity và triển khai lên EVM.
- Hỗ trợ lưu trữ khóa mã hóa qua Hardware Security Module (HSM).

