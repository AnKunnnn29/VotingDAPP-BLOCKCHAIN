"""Login dialog for voter and admin authentication"""
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QComboBox, QMessageBox,
                               QFormLayout, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LoginDialog(QDialog):
    """Dialog for user login"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_role = None
        self.user_id = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("Đăng nhập - DApp Voting System")
        self.setMinimumWidth(550)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("🗳️ Hệ thống bỏ phiếu phi tập trung")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Form layout for better alignment
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Role selection
        role_label = QLabel("Vai trò:")
        role_label.setObjectName("infoLabel")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Cử tri", "Quản trị viên"])
        self.role_combo.setMinimumHeight(45)
        form_layout.addRow(role_label, self.role_combo)
        
        # ID input
        id_label = QLabel("Mã số:")
        id_label.setObjectName("infoLabel")
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Nhập mã cử tri (1-100) hoặc 'admin'")
        self.id_input.setMinimumHeight(45)
        form_layout.addRow(id_label, self.id_input)
        
        form_widget.setLayout(form_layout)
        layout.addWidget(form_widget)
        
        layout.addSpacing(15)
        
        # Info label
        info = QLabel("💡 Cử tri: nhập số từ 1-100\n💡 Admin: nhập 'admin'")
        info.setObjectName("infoLabel")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)
        
        layout.addSpacing(15)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        login_btn = QPushButton("Đăng nhập")
        login_btn.setMinimumHeight(50)
        login_btn.setMinimumWidth(150)
        login_btn.clicked.connect(self.handle_login)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("dangerButton")
        cancel_btn.setMinimumHeight(50)
        cancel_btn.setMinimumWidth(150)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(login_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def handle_login(self):
        """Handle login button click"""
        role = self.role_combo.currentText()
        user_input = self.id_input.text().strip()
        
        if not user_input:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã số")
            return
        
        if role == "Quản trị viên":
            if user_input.lower() == "admin":
                self.user_role = "Admin"
                self.user_id = 0
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Mã quản trị viên không đúng")
        else:
            try:
                voter_id = int(user_input)
                if 1 <= voter_id <= 100:
                    self.user_role = "Voter"
                    self.user_id = voter_id
                    self.accept()
                else:
                    QMessageBox.warning(self, "Lỗi", "Mã cử tri phải từ 1-100")
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Mã cử tri phải là số")
