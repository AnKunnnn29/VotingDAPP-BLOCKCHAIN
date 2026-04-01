# Hướng dẫn sử dụng hệ thống bầu cử

## Quy trình bầu cử

### 1. Admin tạo cuộc bầu cử mới

1. Đăng nhập với tài khoản admin (nhập "admin")
2. Nhấn nút "➕ Tạo cuộc bầu cử mới"
3. Nhập thông tin:
   - Tiêu đề cuộc bầu cử
   - Mô tả
   - Chế độ blockchain (Permissionless/Permissioned)
4. Nhấn "Tạo"

**Lưu ý**: Khi tạo cuộc bầu cử mới, tất cả cử tri đã vote ở cuộc bầu cử trước vẫn có thể tham gia cuộc bầu cử mới.

### 2. Admin thêm ứng viên

1. Chuyển sang tab "🎯 Ứng viên"
2. Nhấn "➕ Thêm ứng viên"
3. Nhập:
   - Tên ứng viên
   - Mô tả
4. Nhấn "OK"

**Quan trọng**: Phải có ít nhất 1 ứng viên trước khi chuyển sang bước tiếp theo.

### 3. Admin chuyển trạng thái election

Cuộc bầu cử phải đi qua các trạng thái theo thứ tự:

1. **Start** (Khởi tạo)
   - Trạng thái ban đầu
   - Thêm ứng viên ở trạng thái này

2. **ValidateVoter** (Xác thực cử tri)
   - Chuyển sang tab "👥 Cử tri"
   - Chọn cử tri và nhấn "✅ Xác thực"
   - Chỉ cử tri đã xác thực mới được bỏ phiếu

3. **Vote** (Bỏ phiếu) ⭐ QUAN TRỌNG
   - Nhấn nút "Chuyển sang Vote" ở tab "🏛️ Cuộc bầu cử"
   - **Cử tri CHỈ có thể bỏ phiếu khi election ở trạng thái này**

4. **Count** (Kiểm phiếu)
   - Hệ thống tự động đếm phiếu

5. **DeclareWinner** (Công bố kết quả)
   - Hệ thống tự động xác định người thắng

6. **Done** (Kết thúc)
   - Cuộc bầu cử hoàn tất
   - Có thể xem kết quả và biểu đồ

### 4. Cử tri bỏ phiếu

1. Đăng nhập với mã cử tri (1-100)
2. Kiểm tra thông tin cử tri:
   - Trạng thái: Chưa bỏ phiếu
   - Xác thực: Đã xác thực
3. Chọn ứng viên trong bảng
4. Nhấn "🗳️ Bỏ phiếu"
5. Xác nhận

**Lưu ý**: 
- Cử tri chỉ bỏ phiếu được khi election ở trạng thái "Vote"
- Mỗi cử tri chỉ bỏ phiếu 1 lần cho mỗi cuộc bầu cử
- Cử tri có thể tham gia nhiều cuộc bầu cử khác nhau

### 5. Xem kết quả

**Cử tri:**
- Nhấn "📈 Xem kết quả" (chỉ khi election ở trạng thái Done)
- Xem biểu đồ với phần trăm và số phiếu

**Admin:**
- Tab "📊 Kết quả": Xem bảng kết quả
- Nhấn "📊 Xem biểu đồ": Xem cả bar chart và pie chart

## Khắc phục sự cố

### Cử tri không thể bỏ phiếu

**Nguyên nhân 1**: Election không ở trạng thái "Vote"
- **Giải pháp**: Admin cần chuyển election sang trạng thái "Vote"

**Nguyên nhân 2**: Cử tri chưa được xác thực
- **Giải pháp**: Admin cần xác thực cử tri ở tab "👥 Cử tri"

**Nguyên nhân 3**: Cử tri đã bỏ phiếu cho cuộc bầu cử này rồi
- **Giải pháp**: Mỗi cử tri chỉ vote 1 lần, không thể vote lại

### Không có ứng viên nào hiển thị

**Nguyên nhân**: Chưa thêm ứng viên cho cuộc bầu cử hiện tại
- **Giải pháp**: Admin thêm ứng viên ở tab "🎯 Ứng viên"

### Cử tri đã vote ở election cũ không thể vote ở election mới

**Đã sửa**: Logic hiện tại cho phép cử tri tham gia nhiều cuộc bầu cử
- Hệ thống kiểm tra xem cử tri đã vote cho election HIỆN TẠI chưa
- Nếu chưa → cho phép vote
- Nếu rồi → từ chối

## Lưu ý quan trọng

1. **Thứ tự trạng thái**: Phải chuyển trạng thái theo đúng thứ tự
2. **Trạng thái Vote**: Cử tri CHỈ bỏ phiếu được ở trạng thái này
3. **Xác thực**: Cử tri phải được xác thực trước khi bỏ phiếu
4. **Một lần vote**: Mỗi cử tri chỉ vote 1 lần cho mỗi election
5. **Nhiều election**: Cử tri có thể tham gia nhiều cuộc bầu cử khác nhau
