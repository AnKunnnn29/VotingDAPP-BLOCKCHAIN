"""Secure admin login dialog with 2FA"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QWidget,
                               QCheckBox, QGroupBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from services.admin_auth_service import AdminAuthService

class AdminLoginDialog(QDialog):
    """Secure admin login with username, password, and 2FA"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.admin_auth = AdminAuthService()
        self.admin_data = None
        self.pending_2fa = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Dang nhap Admin - Bao mat cao")
        self.setMinimumWidth(550)
        self.setMinimumHeight(650)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("DANG NHAP QUAN TRI VIEN")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 20pt;
            font-weight: 700;
            color: #60a5fa;
            padding: 15px;
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Xac thuc da lop voi 2FA")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 11pt;
            color: #94a3b8;
            padding: 8px;
        """)
        header_layout.addWidget(subtitle)
        
        layout.addLayout(header_layout)
        
        # Security info
        security_group = QGroupBox("Bao mat")
        security_layout = QVBoxLayout()
        
        security_info = QLabel(
            "- Mat khau duoc ma hoa SHA-256\n"
            "- 2FA (OTP) bat buoc\n"
            "- Khoa tai khoan sau 5 lan sai\n"
            "- Session timeout 30 phut\n"
            "- Audit log day du"
        )
        security_info.setStyleSheet("""
            font-size: 10pt;
            color: #10b981;
            padding: 12px;
            line-height: 1.8;
        """)
        security_layout.addWidget(security_info)
        security_group.setLayout(security_layout)
        layout.addWidget(security_group)
        
        # Login form
        form_group = QGroupBox("Thong tin dang nhap")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Username
        username_label = QLabel("Ten dang nhap:")
        username_label.setStyleSheet("font-weight: 600; color: #f8fafc; font-size: 11pt;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhap ten dang nhap...")
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 8px;
                background: #1e293b;
                color: #f8fafc;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Mat khau:")
        password_label.setStyleSheet("font-weight: 600; color: #f8fafc; font-size: 11pt;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nhap mat khau...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 8px;
                background: #1e293b;
                color: #f8fafc;
                font-size: 12pt;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        form_layout.addWidget(self.password_input)
        
        # Show password checkbox
        self.show_password_cb = QCheckBox("Hien thi mat khau")
        self.show_password_cb.setStyleSheet("color: #94a3b8; font-size: 10pt;")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        form_layout.addWidget(self.show_password_cb)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 2FA section (hidden initially)
        self.otp_group = QGroupBox("Xac thuc 2FA")
        otp_layout = QVBoxLayout()
        
        otp_info = QLabel("Ma OTP da duoc hien thi tren console.\nVui long nhap ma de hoan tat dang nhap.")
        otp_info.setStyleSheet("color: #f59e0b; padding: 8px; font-size: 10pt;")
        otp_info.setWordWrap(True)
        otp_layout.addWidget(otp_info)
        
        otp_label = QLabel("Ma OTP (6 chu so):")
        otp_label.setStyleSheet("font-weight: 600; color: #f8fafc; margin-top: 10px; font-size: 11pt;")
        otp_layout.addWidget(otp_label)
        
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Nhap ma OTP...")
        self.otp_input.setMaxLength(6)
        self.otp_input.setMinimumHeight(50)
        self.otp_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #334155;
                border-radius: 8px;
                background: #1e293b;
                color: #f8fafc;
                font-size: 16pt;
                font-weight: 700;
                letter-spacing: 8px;
                text-align: center;
            }
            QLineEdit:focus {
                border-color: #10b981;
            }
        """)
        self.otp_input.returnPressed.connect(self.verify_otp)
        otp_layout.addWidget(self.otp_input)
        
        self.otp_group.setLayout(otp_layout)
        self.otp_group.setVisible(False)
        layout.addWidget(self.otp_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_btn = QPushButton("Dang nhap")
        self.login_btn.setObjectName("successButton")
        self.login_btn.setMinimumHeight(50)
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setStyleSheet("""
            QPushButton {
                font-size: 13pt;
                font-weight: 700;
            }
        """)
        
        self.verify_btn = QPushButton("Xac thuc OTP")
        self.verify_btn.setObjectName("successButton")
        self.verify_btn.setMinimumHeight(50)
        self.verify_btn.clicked.connect(self.verify_otp)
        self.verify_btn.setVisible(False)
        self.verify_btn.setStyleSheet("""
            QPushButton {
                font-size: 13pt;
                font-weight: 700;
            }
        """)
        
        cancel_btn = QPushButton("Huy")
        cancel_btn.setObjectName("dangerButton")
        cancel_btn.setMinimumHeight(50)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.verify_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Default credentials info
        default_info = QLabel(
            "Tai khoan mac dinh:\n"
            "Username: admin\n"
            "Password: Admin@2024"
        )
        default_info.setStyleSheet("""
            font-size: 10pt;
            color: #64748b;
            padding: 15px;
            background: rgba(30, 41, 59, 0.5);
            border-radius: 8px;
            margin-top: 10px;
        """)
        default_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(default_info)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def toggle_password_visibility(self, state):
        """Toggle password visibility"""
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return
        
        # Step 1: Authenticate username and password
        success, admin_data, message = self.admin_auth.authenticate_step1(username, password)
        
        if not success:
            QMessageBox.critical(self, "Đăng nhập thất bại", message)
            return
        
        # Check if 2FA required
        if message == "REQUIRE_2FA":
            self.admin_data = admin_data
            self.pending_2fa = True
            
            # Show 2FA section
            self.otp_group.setVisible(True)
            self.login_btn.setVisible(False)
            self.verify_btn.setVisible(True)
            self.otp_input.setFocus()
            
            # Disable username/password inputs
            self.username_input.setEnabled(False)
            self.password_input.setEnabled(False)
            
            QMessageBox.information(self, "Xac thuc 2FA", 
                                   "Ma OTP da duoc hien thi tren console.\n"
                                   "Vui long kiem tra va nhap ma de tiep tuc.")
        else:
            # No 2FA, login successful
            self.admin_data = admin_data
            QMessageBox.information(self, "Thành công", message)
            self.accept()
    
    def verify_otp(self):
        """Verify OTP code"""
        if not self.pending_2fa or not self.admin_data:
            return
        
        otp = self.otp_input.text().strip()
        
        if len(otp) != 6 or not otp.isdigit():
            QMessageBox.warning(self, "Loi", "Ma OTP phai la 6 chu so")
            return
        
        # Step 2: Verify OTP
        success, message = self.admin_auth.authenticate_step2(
            self.admin_data['username'], otp, self.admin_data
        )
        
        if success:
            QMessageBox.information(self, "Thanh cong", 
                                   "Xac thuc thanh cong!\n"
                                   "Chao mung ban den voi he thong quan tri.")
            self.accept()
        else:
            QMessageBox.critical(self, "Xac thuc that bai", message)
            self.otp_input.clear()
            self.otp_input.setFocus()
    
    def get_admin_data(self):
        """Get authenticated admin data"""
        return self.admin_data
