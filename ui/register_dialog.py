"""Registration dialog for new voters"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QWidget)
from PySide6.QtCore import Qt
from database.db_manager import DatabaseManager
from services.crypto_service import CryptoService
from services.face_recognition_service import FaceRecognitionService
from models.voter import Voter

class RegisterDialog(QDialog):
    """Dialog for voter registration"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.crypto_service = CryptoService()
        self.face_service = FaceRecognitionService()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Đăng ký cử tri mới")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Header
        header_container = QWidget()
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(10)
        
        icon_label = QLabel("📝")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 42pt; padding: 8px;")
        header_layout.addWidget(icon_label)
        
        title = QLabel("Đăng ký cử tri mới")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16pt;
            font-weight: 700;
            color: #60a5fa;
            padding: 8px 0;
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Điền thông tin để tạo tài khoản")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 10pt;
            color: #94a3b8;
            padding: 3px;
        """)
        header_layout.addWidget(subtitle)
        
        header_container.setLayout(header_layout)
        layout.addWidget(header_container)
        
        # Form
        form_container = QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 41, 59, 0.6), stop:1 rgba(15, 23, 42, 0.8));
                border: 2px solid #1e293b;
                border-radius: 12px;
                padding: 25px;
            }
        """)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Full name
        name_label = QLabel("👤 Họ và tên")
        name_label.setStyleSheet("""
            font-size: 10pt;
            font-weight: 600;
            color: #60a5fa;
            padding: 3px 0;
        """)
        form_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập họ và tên đầy đủ")
        self.name_input.setMinimumHeight(42)
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 10pt;
                padding: 10px 14px;
            }
        """)
        form_layout.addWidget(self.name_input)
        
        # CCCD
        cccd_label = QLabel("🆔 Số CCCD")
        cccd_label.setStyleSheet("""
            font-size: 10pt;
            font-weight: 600;
            color: #60a5fa;
            padding: 3px 0;
        """)
        form_layout.addWidget(cccd_label)
        
        self.cccd_input = QLineEdit()
        self.cccd_input.setPlaceholderText("Nhập số CCCD (12 số)")
        self.cccd_input.setMinimumHeight(42)
        self.cccd_input.setMaxLength(12)
        self.cccd_input.setStyleSheet("""
            QLineEdit {
                font-size: 10pt;
                padding: 10px 14px;
            }
        """)
        form_layout.addWidget(self.cccd_input)
        
        # Register face button
        self.face_btn = QPushButton("📸 Đăng ký khuôn mặt")
        self.face_btn.setObjectName("warningButton")
        self.face_btn.setMinimumHeight(45)
        self.face_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        self.face_btn.clicked.connect(self.register_face)
        form_layout.addWidget(self.face_btn)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        form_layout.addWidget(self.status_label)
        
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)
        
        # Info
        info_box = QLabel("💡 Sau khi đăng ký, bạn có thể đăng nhập bằng CCCD và khuôn mặt")
        info_box.setAlignment(Qt.AlignCenter)
        info_box.setWordWrap(True)
        info_box.setStyleSheet("""
            color: #94a3b8;
            font-size: 9pt;
            padding: 12px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        """)
        layout.addWidget(info_box)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        register_btn = QPushButton("✅ Đăng ký")
        register_btn.setObjectName("successButton")
        register_btn.setMinimumHeight(45)
        register_btn.setMinimumWidth(160)
        register_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        register_btn.clicked.connect(self.handle_register)
        
        cancel_btn = QPushButton("❌ Hủy")
        cancel_btn.setObjectName("dangerButton")
        cancel_btn.setMinimumHeight(45)
        cancel_btn.setMinimumWidth(160)
        cancel_btn.setStyleSheet("""
            QPushButton {
                font-size: 10pt;
                font-weight: 700;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # State
        self.face_registered = False
    
    def register_face(self):
        """Register face for new voter"""
        name = self.name_input.text().strip()
        cccd = self.cccd_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên")
            return
        
        if not cccd or len(cccd) != 12 or not cccd.isdigit():
            QMessageBox.warning(self, "Lỗi", "Số CCCD phải có 12 chữ số")
            return
        
        # Check if CCCD already exists
        voters = self.db_manager.get_all_voters()
        for voter in voters:
            if voter.cccd == cccd:
                QMessageBox.warning(self, "Lỗi", 
                                  f"CCCD {cccd} đã được đăng ký.\n"
                                  "Vui lòng sử dụng CCCD khác hoặc đăng nhập.")
                return
        
        # Register face
        QMessageBox.information(
            self, "Hướng dẫn",
            "Webcam sẽ mở để đăng ký khuôn mặt.\n"
            "Nhấn SPACE để chụp, ESC để hủy."
        )
        
        if self.face_service.register_face(cccd, name):
            self.face_registered = True
            self.show_status("✅ Đã đăng ký khuôn mặt thành công!", "success")
        else:
            self.show_status("❌ Đăng ký khuôn mặt thất bại", "error")
    
    def show_status(self, message, status_type):
        """Show status message"""
        colors = {
            "success": ("background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981;"),
            "error": ("background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444;")
        }
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            font-size: 9pt;
            font-weight: 600;
            padding: 10px;
            border-radius: 8px;
            {colors.get(status_type, colors['success'])}
        """)
        self.status_label.show()
    
    def handle_register(self):
        """Handle registration"""
        name = self.name_input.text().strip()
        cccd = self.cccd_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên")
            return
        
        if not cccd or len(cccd) != 12 or not cccd.isdigit():
            QMessageBox.warning(self, "Lỗi", "Số CCCD phải có 12 chữ số")
            return
        
        if not self.face_registered:
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng ký khuôn mặt trước")
            return
        
        # Check if CCCD already exists
        voters = self.db_manager.get_all_voters()
        for voter in voters:
            if voter.cccd == cccd:
                QMessageBox.warning(self, "Lỗi", 
                                  f"CCCD {cccd} đã được đăng ký.\n"
                                  "Vui lòng sử dụng CCCD khác.")
                return
        
        # Create new voter
        private_key, public_key = self.crypto_service.generate_key_pair()
        voter = Voter(
            id=0,
            full_name=name,
            public_key=public_key,
            private_key=private_key,
            cccd=cccd,
            face_registered=True,
            weight=1,
            verified=False
        )
        
        self.db_manager.add_voter(voter)
        
        QMessageBox.information(
            self, "Thành công",
            f"Đăng ký thành công!\n\n"
            f"Tên: {name}\n"
            f"CCCD: {cccd}\n\n"
            f"Bạn có thể đăng nhập ngay bây giờ."
        )
        
        self.accept()
