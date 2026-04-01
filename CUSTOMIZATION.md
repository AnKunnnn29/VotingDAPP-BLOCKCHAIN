# 🎨 Hướng dẫn Customization

## 1. Thay đổi màu sắc

### File: `ui/styles.py`

```python
# Thay đổi màu primary
QPushButton {
    background-color: #9C27B0;  # Purple thay vì Blue
}

# Thay đổi màu success
QPushButton#successButton {
    background-color: #00BCD4;  # Cyan thay vì Green
}
```

### Màu sắc gợi ý
- **Blue**: #2196F3 (Professional)
- **Purple**: #9C27B0 (Creative)
- **Green**: #4CAF50 (Eco-friendly)
- **Orange**: #FF9800 (Energetic)
- **Red**: #F44336 (Bold)

## 2. Thêm ứng viên mặc định

### File: `demo_setup.py`

```python
proposals_data = [
    ("Ứng viên 1", "Mô tả 1"),
    ("Ứng viên 2", "Mô tả 2"),
    ("Ứng viên 3", "Mô tả 3"),
    ("Ứng viên 4", "Mô tả 4"),  # Thêm ứng viên mới
]
```

## 3. Thay đổi số lượng cử tri mặc định

### File: `demo_setup.py`

```python
# Tạo 50 voters thay vì 20
for i in range(1, 51):
    # ...
    verified=(i <= 25)  # 25 voters verified
```

## 4. Thêm trường dữ liệu mới

### Ví dụ: Thêm email cho Voter

#### Bước 1: Update model
**File: `models/voter.py`**
```python
@dataclass
class Voter:
    # ... existing fields
    email: Optional[str] = None  # Thêm field mới
```

#### Bước 2: Update database
**File: `database/db_manager.py`**
```python
# Trong init_database()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS voters (
        ...
        email TEXT,  -- Thêm column mới
        ...
    )
''')

# Update add_voter()
cursor.execute('''
    INSERT INTO voters (..., email)
    VALUES (..., ?)
''', (..., voter.email))
```

#### Bước 3: Update UI
**File: `ui/admin_view.py`**
```python
# Trong AddVoterDialog
self.email_input = QLineEdit()
layout.addRow("Email:", self.email_input)
```

## 5. Thay đổi thuật toán hash

### File: `blockchain/block.py`

```python
import hashlib

# Thay SHA-256 bằng SHA-512
def calculate_hash(self):
    block_string = json.dumps(...)
    return hashlib.sha512(block_string.encode()).hexdigest()
```

## 6. Thêm loại bỏ phiếu mới

### Ví dụ: Ranked Choice Voting

#### Bước 1: Update Voter model
```python
@dataclass
class Voter:
    # ...
    ranked_choices: List[int] = None  # [1st, 2nd, 3rd choice]
```

#### Bước 2: Update voting logic
```python
def cast_ranked_vote(voter, choices):
    # Validate choices
    # Sign vote
    # Add to blockchain
    pass
```

## 7. Thêm biểu đồ mới

### File: `ui/admin_view.py`

```python
def show_pie_chart(self):
    """Show pie chart instead of bar chart"""
    proposals = self.voting_service.db_manager.get_all_proposals()
    names = [p.candidate_name for p in proposals]
    votes = [p.vote_count for p in proposals]
    
    plt.figure(figsize=(8, 8))
    plt.pie(votes, labels=names, autopct='%1.1f%%')
    plt.title('Kết quả bầu cử')
    plt.show()
```

## 8. Thêm export kết quả

### File: `services/election_service.py`

```python
import csv

def export_results_to_csv(self, filename: str):
    """Export results to CSV file"""
    proposals = self.db_manager.get_all_proposals()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Ứng viên', 'Số phiếu'])
        for p in proposals:
            writer.writerow([p.id, p.candidate_name, p.vote_count])
```

## 9. Thêm logging

### File: `main.py`

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voting_dapp.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

## 10. Thêm notification system

### File: `ui/main_window.py`

```python
from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtGui import QIcon

def setup_notifications(self):
    """Setup system tray notifications"""
    self.tray_icon = QSystemTrayIcon(self)
    self.tray_icon.setIcon(QIcon("icon.png"))
    self.tray_icon.show()

def notify(self, title, message):
    """Show notification"""
    self.tray_icon.showMessage(title, message)
```

## 11. Thêm multi-language support

### File: `utils/i18n.py` (mới)

```python
TRANSLATIONS = {
    'en': {
        'login': 'Login',
        'vote': 'Vote',
        'logout': 'Logout',
    },
    'vi': {
        'login': 'Đăng nhập',
        'vote': 'Bỏ phiếu',
        'logout': 'Đăng xuất',
    }
}

def translate(key, lang='vi'):
    return TRANSLATIONS[lang].get(key, key)
```

## 12. Thêm database backup

### File: `database/db_manager.py`

```python
import shutil
from datetime import datetime

def backup_database(self):
    """Backup database to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backup_{timestamp}.db"
    shutil.copy2(self.db_path, backup_file)
    return backup_file
```

## 13. Thêm vote weight visualization

### File: `ui/voter_view.py`

```python
# Hiển thị weight của voter
weight_label = QLabel(f"⚖️ Quyền biểu quyết: {voter.weight}")
weight_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
```

## 14. Thêm time-locked voting

### File: `services/election_service.py`

```python
from datetime import datetime

def can_vote_now(self, election):
    """Check if voting is open based on time"""
    now = datetime.now()
    
    if election.start_time and now < election.start_time:
        return False, "Chưa đến giờ bỏ phiếu"
    
    if election.end_time and now > election.end_time:
        return False, "Đã hết giờ bỏ phiếu"
    
    return True, "OK"
```

## 15. Thêm vote delegation

### Ví dụ: Voter có thể ủy quyền vote cho người khác

```python
@dataclass
class Voter:
    # ...
    delegated_to: Optional[int] = None  # ID of delegate
    delegation_signature: Optional[str] = None

def delegate_vote(self, voter, delegate_id):
    """Delegate voting right to another voter"""
    # Verify delegate exists
    # Sign delegation
    # Update voter
    pass
```

## 16. Thêm real-time updates

### Sử dụng QTimer

```python
from PySide6.QtCore import QTimer

class VoterView(QWidget):
    def __init__(self, ...):
        super().__init__()
        # ...
        
        # Auto refresh every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_proposals)
        self.timer.start(5000)  # 5000ms = 5s
```

## 17. Thêm search và filter

### File: `ui/admin_view.py`

```python
# Thêm search box
self.search_input = QLineEdit()
self.search_input.setPlaceholderText("🔍 Tìm kiếm...")
self.search_input.textChanged.connect(self.filter_table)

def filter_table(self, text):
    """Filter table by search text"""
    for row in range(self.voters_table.rowCount()):
        name = self.voters_table.item(row, 1).text()
        should_show = text.lower() in name.lower()
        self.voters_table.setRowHidden(row, not should_show)
```

## 18. Thêm dark mode

### File: `ui/styles.py`

```python
DARK_STYLE = """
QMainWindow {
    background-color: #212121;
}

QLabel {
    color: #FFFFFF;
}

QPushButton {
    background-color: #424242;
    color: #FFFFFF;
}

QTableWidget {
    background-color: #303030;
    color: #FFFFFF;
}
"""

# Trong main_window.py
def toggle_dark_mode(self):
    if self.dark_mode:
        self.setStyleSheet(MAIN_STYLE)
    else:
        self.setStyleSheet(DARK_STYLE)
    self.dark_mode = not self.dark_mode
```

## 19. Thêm statistics dashboard

### File: `ui/admin_view.py`

```python
def create_stats_tab(self):
    """Create statistics dashboard"""
    widget = QWidget()
    layout = QVBoxLayout()
    
    # Stats cards
    total_voters = len(self.voting_service.db_manager.get_all_voters())
    voted_count = sum(1 for v in voters if v.voted)
    turnout = (voted_count / total_voters * 100) if total_voters > 0 else 0
    
    stats_html = f"""
    <h2>📊 Thống kê</h2>
    <p>👥 Tổng cử tri: {total_voters}</p>
    <p>✅ Đã bỏ phiếu: {voted_count}</p>
    <p>📈 Tỷ lệ tham gia: {turnout:.1f}%</p>
    """
    
    stats_label = QLabel(stats_html)
    layout.addWidget(stats_label)
    
    widget.setLayout(layout)
    return widget
```

## 20. Thêm unit tests

### File: `tests/test_voting.py` (mới)

```python
import unittest
from services.voting_service import VotingService
from database.db_manager import DatabaseManager
from blockchain.blockchain import Blockchain

class TestVoting(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.blockchain = Blockchain()
        self.service = VotingService(self.db, self.blockchain)
    
    def test_cast_vote(self):
        # Test voting logic
        pass
    
    def test_double_voting(self):
        # Test double voting prevention
        pass

if __name__ == '__main__':
    unittest.main()
```

---

**Tip**: Sau mỗi thay đổi, chạy lại app để test:
```bash
python main.py
```
