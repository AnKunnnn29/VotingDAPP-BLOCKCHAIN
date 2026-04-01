# Cải tiến giao diện cử tri

## 1. Thêm thông tin cuộc bầu cử hiện tại

### Vấn đề
- Cử tri không biết đang tham gia cuộc bầu cử nào
- Không biết trạng thái của cuộc bầu cử

### Giải pháp
Thêm GroupBox "🗳️ Thông tin cuộc bầu cử" hiển thị:
- Tiêu đề cuộc bầu cử
- Trạng thái cuộc bầu cử với màu sắc:
  - **Xanh lá (#10b981)**: "Vote (Đang bỏ phiếu)" - có thể vote
  - **Cam (#f59e0b)**: Các trạng thái khác - chưa thể vote
  - **Xám (#94a3b8)**: "Done (Đã kết thúc)" - đã kết thúc

### Code
```python
# Election info
self.election_info_group = QGroupBox("🗳️ Thông tin cuộc bầu cử")
self.election_title_label = QLabel("📌 {election.title}")
self.election_state_label = QLabel("Trạng thái: {election.state}")
```

## 2. Sửa view_vote_status - Chỉ hiển thị phiếu của election hiện tại

### Vấn đề
- Khi xem trạng thái phiếu, hiển thị phiếu của election cũ
- Gây nhầm lẫn cho cử tri

### Giải pháp
Kiểm tra proposal có thuộc election hiện tại không:

```python
def view_vote_status(self):
    election = self.election_service.get_current_election()
    
    # Kiểm tra đã vote cho election hiện tại chưa
    if not self.has_voted_current_election:
        return "Bạn chưa bỏ phiếu cho cuộc bầu cử này"
    
    # Lấy status từ blockchain
    status = self.voting_service.get_voter_vote_status(self.voter)
    
    # Verify proposal thuộc election hiện tại
    if proposal.election_id == election.id:
        # Hiển thị thông tin
    else:
        return "Bạn chưa bỏ phiếu cho cuộc bầu cử này"
```

### Kết quả
- Nếu chưa vote election hiện tại → Thông báo "Bạn chưa bỏ phiếu"
- Nếu đã vote election hiện tại → Hiển thị thông tin phiếu
- Thêm tên cuộc bầu cử vào thông báo để rõ ràng hơn

## 3. Hiển thị rõ quyền bầu cử

### Vấn đề
- Label "Xác thực" không rõ ý nghĩa
- Không biết có được phép bỏ phiếu không

### Giải pháp
Đổi label thành "Quyền bầu cử" với 2 trạng thái rõ ràng:

**Có quyền:**
```
✅ Có quyền bầu cử
Màu: Xanh lá (#10b981)
```

**Chưa có quyền:**
```
❌ Chưa được xác thực
Màu: Đỏ (#ef4444)
```

### Code
```python
verified_text = QLabel("Quyền bầu cử:")
if self.voter.verified:
    verified = "✅ Có quyền bầu cử"
    verified_style = "color: #10b981;"
else:
    verified = "❌ Chưa được xác thực"
    verified_style = "color: #ef4444;"
self.verified_label.setStyleSheet(verified_style)
```

## Tổng kết các cải tiến

### Giao diện mới có:

1. **Thông tin cuộc bầu cử**
   - Tiêu đề
   - Trạng thái với màu sắc phân biệt

2. **Thông tin cử tri**
   - Mã cử tri
   - Quyền biểu quyết
   - Trạng thái bỏ phiếu (cho election hiện tại)
   - Quyền bầu cử (verified status) với màu sắc

3. **Xem trạng thái phiếu**
   - Chỉ hiển thị phiếu của election hiện tại
   - Thông báo rõ ràng nếu chưa vote
   - Hiển thị tên cuộc bầu cử

### Màu sắc sử dụng

- **Xanh lá (#10b981)**: Tích cực (có quyền, đang vote, đã vote)
- **Đỏ (#ef4444)**: Tiêu cực (không có quyền)
- **Cam (#f59e0b)**: Cảnh báo (trạng thái chờ)
- **Xám (#94a3b8)**: Trung tính (đã kết thúc)

### Trải nghiệm người dùng

**Trước:**
- Không biết đang ở cuộc bầu cử nào
- Xem trạng thái phiếu → thấy phiếu cũ → nhầm lẫn
- Không rõ có quyền vote không

**Sau:**
- Thấy rõ tên và trạng thái cuộc bầu cử
- Xem trạng thái phiếu → chỉ thấy phiếu của election hiện tại
- Biết rõ có quyền bầu cử hay không (màu xanh/đỏ)
