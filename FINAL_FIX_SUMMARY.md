# Sửa lỗi cuối cùng - Cử tri không thể bỏ phiếu

## Vấn đề

Cử tri 1 đã vote ở election cũ, khi vào election mới:
- Hiển thị "✅ Đã bỏ phiếu" 
- Nút "Bỏ phiếu" bị vô hiệu hóa
- Không thể chọn ứng viên để vote

## Nguyên nhân

Trong `VoterView`:

1. **Hiển thị trạng thái sai**: 
   - Code kiểm tra `voter.voted` (trạng thái chung)
   - Không kiểm tra voter đã vote cho election HIỆN TẠI chưa

2. **Logic enable/disable button sai**:
   ```python
   # Code cũ - SAI
   if selected_rows and not self.voter.voted:
       self.vote_btn.setEnabled(True)
   ```
   - Chỉ kiểm tra `voter.voted` chung
   - Không phân biệt election nào

## Giải pháp

### 1. Thêm biến theo dõi trạng thái cho election hiện tại

```python
def __init__(self, ...):
    self.current_election = None
    self.has_voted_current_election = False  # Trạng thái cho election hiện tại
```

### 2. Tạo hàm kiểm tra trạng thái cho election hiện tại

```python
def update_voter_status_for_current_election(self):
    """Update voter status specifically for current election"""
    if self.voter.voted and self.voter.selected_proposal_id:
        # Lấy proposals của election hiện tại
        proposals = self.voting_service.db_manager.get_all_proposals(self.current_election.id)
        proposal_ids = [p.id for p in proposals]
        
        # Kiểm tra selected_proposal_id có trong election hiện tại không
        self.has_voted_current_election = self.voter.selected_proposal_id in proposal_ids
    else:
        self.has_voted_current_election = False
    
    # Cập nhật label hiển thị
    if self.has_voted_current_election:
        status = "✅ Đã bỏ phiếu (cuộc bầu cử này)"
    elif self.voter.voted:
        status = "⏳ Chưa bỏ phiếu (cuộc bầu cử này)"  # Đã vote election khác
    else:
        status = "⏳ Chưa bỏ phiếu"
```

### 3. Cập nhật logic enable/disable button

```python
def on_proposal_selected(self):
    """Handle proposal selection"""
    selected_rows = self.proposals_table.selectedItems()
    # Kiểm tra has_voted_current_election thay vì voter.voted
    if selected_rows and not self.has_voted_current_election:
        self.selected_proposal_id = int(selected_rows[0].text())
        self.vote_btn.setEnabled(True)
    else:
        self.vote_btn.setEnabled(False)
```

### 4. Gọi hàm cập nhật khi load proposals

```python
def load_proposals(self):
    # ... load proposals ...
    
    # Cập nhật trạng thái cho election hiện tại
    self.update_voter_status_for_current_election()
```

## Kết quả

### Trước khi sửa:
- Cử tri 1 đã vote election 3 → Hiển thị "Đã bỏ phiếu"
- Vào election 5 → Vẫn hiển thị "Đã bỏ phiếu"
- Nút bỏ phiếu bị disable → KHÔNG THỂ VOTE

### Sau khi sửa:
- Cử tri 1 đã vote election 3 → Hiển thị "Đã bỏ phiếu (cuộc bầu cử này)" khi ở election 3
- Vào election 5 → Hiển thị "⏳ Chưa bỏ phiếu (cuộc bầu cử này)"
- Nút bỏ phiếu được enable → CÓ THỂ VOTE

## Các trường hợp

### Trường hợp 1: Cử tri chưa vote bao giờ
- `voter.voted = False`
- `has_voted_current_election = False`
- Hiển thị: "⏳ Chưa bỏ phiếu"
- Nút bỏ phiếu: ENABLED

### Trường hợp 2: Cử tri đã vote election khác
- `voter.voted = True`
- `voter.selected_proposal_id = 1` (thuộc election 3)
- Election hiện tại: 5 (proposals: 5, 6)
- `has_voted_current_election = False` (vì 1 không trong [5,6])
- Hiển thị: "⏳ Chưa bỏ phiếu (cuộc bầu cử này)"
- Nút bỏ phiếu: ENABLED

### Trường hợp 3: Cử tri đã vote election hiện tại
- `voter.voted = True`
- `voter.selected_proposal_id = 5` (thuộc election 5)
- Election hiện tại: 5 (proposals: 5, 6)
- `has_voted_current_election = True` (vì 5 trong [5,6])
- Hiển thị: "✅ Đã bỏ phiếu (cuộc bầu cử này)"
- Nút bỏ phiếu: DISABLED

## Lưu ý

- Logic backend (`voting_service.py`) đã đúng từ đầu
- Vấn đề chỉ ở UI (VoterView) không cập nhật đúng trạng thái
- Giải pháp không cần thay đổi database hay backend
- Chỉ cần cập nhật logic hiển thị ở frontend
