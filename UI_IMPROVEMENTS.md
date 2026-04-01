# Cải tiến UI/UX

## Các cải tiến đã thực hiện

### 1. Cải thiện Typography và Spacing
- Giảm font size từ 11pt xuống 10pt cho text thông thường để dễ đọc hơn
- Tăng font size cho subtitle từ 14pt lên 16pt
- Thêm padding và margin đồng đều cho tất cả các thành phần
- Thêm label style mới `valueLabel` cho giá trị hiển thị

### 2. Cải thiện Table Display
- Thêm `alternatingRowColors` cho dễ phân biệt các hàng
- Ẩn vertical header để giao diện gọn gàng hơn
- Cải thiện selection highlighting với màu xanh đậm (#3b82f6)
- Thêm hover effect cho table items
- Tự động resize columns phù hợp với nội dung
- Tăng padding cho table cells (12px 8px)
- Set minimum height cho tables (200px cho voter, 300px cho admin)

### 3. Cải thiện Voter View
- Sử dụng grid layout cho thông tin cử tri với label và value riêng biệt
- Căn chỉnh đồng đều các label với `setMinimumWidth(150)`
- Thêm icon cho các group box (📋, 🎯)
- Tăng chiều cao nút bấm lên 40px
- Thêm spacing đồng đều giữa các thành phần (15px)
- Thêm margins cho layout (20px)

### 4. Biểu đồ kết quả (Charts)
- **Voter View**: Hiển thị biểu đồ ngang (horizontal bar chart) với:
  - Phần trăm và số phiếu trên mỗi thanh
  - Màu sắc đa dạng cho mỗi ứng viên
  - Dark theme phù hợp với UI chính
  - Hiển thị người chiến thắng với icon 🏆
  
- **Admin View**: Hiển thị 2 biểu đồ:
  - Biểu đồ ngang (bar chart) với phần trăm
  - Biểu đồ tròn (pie chart) với phân bổ phiếu
  - Hiển thị tổng số phiếu
  - Dialog size lớn hơn (900x700) để xem rõ hơn

### 5. Cải thiện Admin View
- Thêm spacing và margins cho tất cả các tabs
- Tăng chiều cao nút bấm lên 40px
- Cải thiện button styling với colors phù hợp:
  - Success button (xanh lá) cho Add
  - Danger button (đỏ) cho Delete
  - Default button (xanh dương) cho các action khác
- Cải thiện table layout với auto-resize columns

### 6. Selection Highlighting
- Màu selection rõ ràng hơn: #3b82f6 (xanh dương đậm)
- Text màu trắng (#ffffff) khi được chọn
- Font weight 600 (semi-bold) cho item được chọn
- Hover effect với opacity 0.2

## Màu sắc chính

- Background: #0f172a (dark blue)
- Secondary background: #1e293b
- Primary: #3b82f6 (blue)
- Success: #10b981 (green)
- Warning: #f59e0b (orange)
- Danger: #ef4444 (red)
- Text: #f8fafc (white)
- Secondary text: #94a3b8 (gray)
- Border: #334155

## Cách sử dụng

### Xem biểu đồ kết quả (Voter)
1. Đăng nhập với tài khoản cử tri
2. Nhấn nút "📈 Xem kết quả"
3. Biểu đồ sẽ hiển thị với phần trăm và số phiếu

### Xem biểu đồ kết quả (Admin)
1. Đăng nhập với tài khoản admin
2. Chuyển sang tab "📊 Kết quả"
3. Nhấn nút "📊 Xem biểu đồ"
4. Xem cả bar chart và pie chart

## Lưu ý
- Biểu đồ chỉ hiển thị khi cuộc bầu cử ở trạng thái "Done"
- Biểu đồ tự động tính phần trăm dựa trên tổng số phiếu
- Dark theme được áp dụng cho cả biểu đồ matplotlib
