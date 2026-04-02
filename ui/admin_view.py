"""Admin view for managing elections and voters"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QGroupBox, QLineEdit, QTextEdit,
                               QDialog, QFormLayout, QComboBox, QTabWidget,
                               QHeaderView, QSpinBox)
from PySide6.QtCore import Qt, Signal
from services.voting_service import VotingService
from services.election_service import ElectionService
from services.auth_service import AuthService
from services.crypto_service import CryptoService
from models.voter import Voter
from models.proposal import Proposal
from models.election import Election
from blockchain.blockchain import Blockchain
from utils.constants import ElectionState, BlockchainMode
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class AdminView(QWidget):
    """View for administrators"""
    
    logout_signal = Signal()
    
    def __init__(self, voting_service: VotingService, 
                 election_service: ElectionService,
                 auth_service: AuthService,
                 blockchain: Blockchain):
        super().__init__()
        self.voting_service = voting_service
        self.election_service = election_service
        self.auth_service = auth_service
        self.blockchain = blockchain
        self.crypto_service = CryptoService()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🔧 Bảng điều khiển quản trị")
        header.setObjectName("titleLabel")
        layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_election_tab(), "📋 Cuộc bầu cử")
        tabs.addTab(self.create_proposals_tab(), "🎯 Ứng viên")
        tabs.addTab(self.create_voters_tab(), "👥 Cử tri")
        tabs.addTab(self.create_blockchain_tab(), "⛓️ Blockchain")
        tabs.addTab(self.create_results_tab(), "📊 Kết quả")
        layout.addWidget(tabs)
        
        # Logout button
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout_signal.emit)
        layout.addWidget(logout_btn)
        
        self.setLayout(layout)
    
    def create_election_tab(self):
        """Create election management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Current election info
        info_group = QGroupBox("📊 Thông tin cuộc bầu cử hiện tại")
        info_layout = QVBoxLayout()
        self.election_info_label = QLabel("Chưa có cuộc bầu cử")
        self.election_info_label.setWordWrap(True)
        info_layout.addWidget(self.election_info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # State machine visual indicator
        state_group = QGroupBox("🔄 Quy trình bầu cử (State Machine)")
        state_layout = QVBoxLayout()
        state_layout.setSpacing(15)
        
        # State flow diagram
        self.state_flow_label = QLabel(
            "Start → ValidateVoter → Vote → Count → DeclareWinner → Done"
        )
        self.state_flow_label.setObjectName("infoLabel")
        self.state_flow_label.setAlignment(Qt.AlignCenter)
        state_layout.addWidget(self.state_flow_label)
        
        # Current state indicator
        self.current_state_label = QLabel("Trạng thái hiện tại: Chưa có cuộc bầu cử")
        self.current_state_label.setObjectName("subtitleLabel")
        self.current_state_label.setAlignment(Qt.AlignCenter)
        self.current_state_label.setStyleSheet("padding: 10px; border-radius: 8px; background-color: #1e293b;")
        state_layout.addWidget(self.current_state_label)
        
        # State transition buttons
        state_buttons = QHBoxLayout()
        state_buttons.setSpacing(10)
        
        self.validate_btn = QPushButton("1️⃣ Xác thực\ncử tri")
        self.validate_btn.setMinimumHeight(60)
        self.validate_btn.clicked.connect(lambda: self.transition_state(ElectionState.VALIDATE_VOTER))
        
        self.vote_btn = QPushButton("2️⃣ Mở\nbỏ phiếu")
        self.vote_btn.setMinimumHeight(60)
        self.vote_btn.clicked.connect(lambda: self.transition_state(ElectionState.VOTE))
        
        self.count_btn = QPushButton("3️⃣ Kiểm\nphiếu")
        self.count_btn.setMinimumHeight(60)
        self.count_btn.clicked.connect(lambda: self.transition_state(ElectionState.COUNT))
        
        self.declare_btn = QPushButton("4️⃣ Công bố\nkết quả")
        self.declare_btn.setMinimumHeight(60)
        self.declare_btn.clicked.connect(lambda: self.transition_state(ElectionState.DECLARE_WINNER))
        
        self.done_btn = QPushButton("5️⃣ Kết thúc")
        self.done_btn.setMinimumHeight(60)
        self.done_btn.clicked.connect(lambda: self.transition_state(ElectionState.DONE))
        
        # Store buttons for easy access
        self.state_buttons = {
            ElectionState.START: None,  # No button for START
            ElectionState.VALIDATE_VOTER: self.validate_btn,
            ElectionState.VOTE: self.vote_btn,
            ElectionState.COUNT: self.count_btn,
            ElectionState.DECLARE_WINNER: self.declare_btn,
            ElectionState.DONE: self.done_btn
        }
        
        state_buttons.addWidget(self.validate_btn)
        state_buttons.addWidget(self.vote_btn)
        state_buttons.addWidget(self.count_btn)
        state_buttons.addWidget(self.declare_btn)
        state_buttons.addWidget(self.done_btn)
        state_layout.addLayout(state_buttons)
        
        state_group.setLayout(state_layout)
        layout.addWidget(state_group)
        
        # Create new election
        create_btn = QPushButton("➕ Tạo cuộc bầu cử mới")
        create_btn.setObjectName("successButton")
        create_btn.setMinimumHeight(50)
        create_btn.clicked.connect(self.create_new_election)
        layout.addWidget(create_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        
        self.update_election_info()
        return widget
    
    def create_proposals_tab(self):
        """Create proposals management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Proposals table
        self.proposals_table = QTableWidget()
        self.proposals_table.setColumnCount(4)
        self.proposals_table.setHorizontalHeaderLabels(["ID", "Ứng viên", "Mô tả", "Số phiếu"])
        self.proposals_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.proposals_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.proposals_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.proposals_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.proposals_table.setColumnWidth(1, 200)
        self.proposals_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.proposals_table.setAlternatingRowColors(True)
        self.proposals_table.verticalHeader().setVisible(False)
        self.proposals_table.setMinimumHeight(300)
        layout.addWidget(self.proposals_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_btn = QPushButton("➕ Thêm ứng viên")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_proposal)
        add_btn.setMinimumHeight(40)
        
        edit_btn = QPushButton("✏️ Sửa")
        edit_btn.clicked.connect(self.edit_proposal)
        edit_btn.setMinimumHeight(40)
        
        delete_btn = QPushButton("🗑️ Xóa")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_proposal)
        delete_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_proposals)
        refresh_btn.setMinimumHeight(40)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_proposals()
        return widget
    
    def create_voters_tab(self):
        """Create voters management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Voters table
        self.voters_table = QTableWidget()
        self.voters_table.setColumnCount(7)
        self.voters_table.setHorizontalHeaderLabels(["ID", "Họ tên", "CCCD", "Khuôn mặt", "Đã bỏ phiếu", "Đã xác thực", "Public Key"])
        self.voters_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.voters_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.voters_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.voters_table.setColumnWidth(1, 180)
        self.voters_table.setColumnWidth(2, 120)
        self.voters_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.voters_table.setAlternatingRowColors(True)
        self.voters_table.verticalHeader().setVisible(False)
        self.voters_table.setMinimumHeight(300)
        layout.addWidget(self.voters_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        add_btn = QPushButton("➕ Thêm cử tri")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_voter)
        add_btn.setMinimumHeight(40)
        
        verify_btn = QPushButton("✅ Xác thực")
        verify_btn.setObjectName("successButton")
        verify_btn.clicked.connect(self.verify_voter)
        verify_btn.setMinimumHeight(40)
        
        face_register_btn = QPushButton("📸 Đăng ký khuôn mặt")
        face_register_btn.setObjectName("warningButton")
        face_register_btn.clicked.connect(self.register_voter_face)
        face_register_btn.setMinimumHeight(40)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_voters)
        refresh_btn.setMinimumHeight(40)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(verify_btn)
        button_layout.addWidget(face_register_btn)
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_voters()
        return widget
    
    def create_blockchain_tab(self):
        """Create blockchain viewer tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Blockchain info
        info_layout = QHBoxLayout()
        self.chain_valid_label = QLabel()
        self.chain_length_label = QLabel()
        info_layout.addWidget(self.chain_valid_label)
        info_layout.addWidget(self.chain_length_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Blocks table
        self.blocks_table = QTableWidget()
        self.blocks_table.setColumnCount(6)
        self.blocks_table.setHorizontalHeaderLabels(
            ["Index", "Timestamp", "Voter ID", "Proposal ID", "Hash", "Previous Hash"]
        )
        self.blocks_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        layout.addWidget(self.blocks_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        verify_btn = QPushButton("🔍 Kiểm tra tính toàn vẹn")
        verify_btn.clicked.connect(self.verify_blockchain)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_blockchain)
        
        button_layout.addWidget(verify_btn)
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_blockchain()
        return widget
    
    def create_results_tab(self):
        """Create results and chart tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Ứng viên", "Số phiếu", "Tỷ lệ %"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        layout.addWidget(self.results_table)
        
        # Chart placeholder
        self.chart_label = QLabel("Biểu đồ sẽ hiển thị sau khi kiểm phiếu")
        self.chart_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.chart_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_results)
        
        chart_btn = QPushButton("📊 Xem biểu đồ")
        chart_btn.clicked.connect(self.show_chart)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(chart_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_results()
        return widget
    
    def update_election_info(self):
        """Update election information display"""
        election = self.election_service.get_current_election()
        if election:
            info_text = f"""
📋 Tiêu đề: {election.title}
📝 Mô tả: {election.description}
🔄 Trạng thái: {election.state}
⛓️ Chế độ: {election.blockchain_mode}
⏰ Bắt đầu: {election.start_time.strftime('%Y-%m-%d %H:%M:%S') if election.start_time else 'N/A'}
            """
            self.election_info_label.setText(info_text)
            
            # Update current state label with color
            state_display = {
                ElectionState.START: ("🟦 Start - Khởi tạo", "#3b82f6"),
                ElectionState.VALIDATE_VOTER: ("🟨 ValidateVoter - Xác thực cử tri", "#f59e0b"),
                ElectionState.VOTE: ("🟩 Vote - Đang bỏ phiếu", "#10b981"),
                ElectionState.COUNT: ("🟧 Count - Kiểm phiếu", "#f97316"),
                ElectionState.DECLARE_WINNER: ("🟪 DeclareWinner - Công bố kết quả", "#8b5cf6"),
                ElectionState.DONE: ("⬜ Done - Đã kết thúc", "#6b7280")
            }
            
            state_text, state_color = state_display.get(election.state, (election.state, "#3b82f6"))
            self.current_state_label.setText(f"Trạng thái hiện tại: {state_text}")
            self.current_state_label.setStyleSheet(
                f"padding: 15px; border-radius: 8px; background-color: {state_color}; color: #ffffff; font-weight: bold;"
            )
            
            # Reset all buttons to default style
            for btn in self.state_buttons.values():
                if btn:
                    btn.setStyleSheet("")
                    btn.setObjectName("")
            
            # Highlight current state button and next available button
            current_btn = self.state_buttons.get(election.state)
            if current_btn:
                current_btn.setStyleSheet(
                    f"background-color: {state_color}; color: #ffffff; font-weight: bold; border: 3px solid #ffffff;"
                )
            
            # Highlight next available button
            next_states = {
                ElectionState.START: ElectionState.VALIDATE_VOTER,
                ElectionState.VALIDATE_VOTER: ElectionState.VOTE,
                ElectionState.VOTE: ElectionState.COUNT,
                ElectionState.COUNT: ElectionState.DECLARE_WINNER,
                ElectionState.DECLARE_WINNER: ElectionState.DONE,
            }
            
            next_state = next_states.get(election.state)
            if next_state:
                next_btn = self.state_buttons.get(next_state)
                if next_btn:
                    next_btn.setStyleSheet(
                        "background-color: #3b82f6; color: #ffffff; font-weight: bold; border: 2px solid #60a5fa; animation: pulse 2s infinite;"
                    )
                    next_btn.setObjectName("successButton")
        else:
            self.election_info_label.setText("Chưa có cuộc bầu cử")
            self.current_state_label.setText("Trạng thái hiện tại: Chưa có cuộc bầu cử")
            self.current_state_label.setStyleSheet("padding: 10px; border-radius: 8px; background-color: #1e293b;")
    
    def transition_state(self, new_state: str):
        """Transition election state"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Chưa có cuộc bầu cử")
            return
        
        # Special handling for COUNT state
        if new_state == ElectionState.COUNT:
            success, message = self.election_service.transition_state(election, new_state)
            if success:
                proposals = self.election_service.count_votes(election, self.blockchain)
                QMessageBox.information(self, "Thành công", 
                    f"{message}\nĐã kiểm {len(proposals)} ứng viên")
                self.load_proposals()
                self.load_results()
            else:
                QMessageBox.warning(self, "Lỗi", message)
        
        # Special handling for DECLARE_WINNER state
        elif new_state == ElectionState.DECLARE_WINNER:
            success, message = self.election_service.transition_state(election, new_state)
            if success:
                winner = self.election_service.declare_winner(election)
                if winner:
                    QMessageBox.information(self, "Thành công", 
                        f"🏆 Người chiến thắng: {winner.candidate_name}\n"
                        f"Số phiếu: {winner.vote_count}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không xác định được người thắng")
            else:
                QMessageBox.warning(self, "Lỗi", message)
        
        else:
            success, message = self.election_service.transition_state(election, new_state)
            if success:
                QMessageBox.information(self, "Thành công", message)
            else:
                QMessageBox.warning(self, "Lỗi", message)
        
        self.update_election_info()
    
    def create_new_election(self):
        """Create a new election"""
        dialog = CreateElectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            election = self.election_service.create_election(
                dialog.title_input.text(),
                dialog.desc_input.toPlainText(),
                dialog.mode_combo.currentText()
            )
            QMessageBox.information(self, "Thành công", 
                f"Đã tạo cuộc bầu cử: {election.title}")
            self.update_election_info()
    
    def load_proposals(self):
        """Load proposals into table"""
        election = self.election_service.get_current_election()
        if not election:
            self.proposals_table.setRowCount(0)
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        self.proposals_table.setRowCount(len(proposals))
        
        for row, proposal in enumerate(proposals):
            self.proposals_table.setItem(row, 0, QTableWidgetItem(str(proposal.id)))
            self.proposals_table.setItem(row, 1, QTableWidgetItem(proposal.candidate_name))
            self.proposals_table.setItem(row, 2, QTableWidgetItem(proposal.description))
            self.proposals_table.setItem(row, 3, QTableWidgetItem(str(proposal.vote_count)))
    
    def add_proposal(self):
        """Add a new proposal"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Vui lòng tạo cuộc bầu cử trước")
            return
        
        dialog = AddProposalDialog(self)
        if dialog.exec() == QDialog.Accepted:
            proposal = Proposal(
                id=0,
                candidate_name=dialog.name_input.text(),
                description=dialog.desc_input.toPlainText(),
                election_id=election.id
            )
            proposal.id = self.voting_service.db_manager.add_proposal(proposal)
            QMessageBox.information(self, "Thành công", "Đã thêm ứng viên")
            self.load_proposals()
    
    def edit_proposal(self):
        """Edit selected proposal"""
        selected_rows = self.proposals_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        proposal_id = int(selected_rows[0].text())
        proposals = self.voting_service.db_manager.get_all_proposals()
        proposal = next((p for p in proposals if p.id == proposal_id), None)
        
        if proposal:
            dialog = AddProposalDialog(self, proposal)
            if dialog.exec() == QDialog.Accepted:
                proposal.candidate_name = dialog.name_input.text()
                proposal.description = dialog.desc_input.toPlainText()
                self.voting_service.db_manager.update_proposal(proposal)
                QMessageBox.information(self, "Thành công", "Đã cập nhật ứng viên")
                self.load_proposals()
    
    def delete_proposal(self):
        """Delete selected proposal"""
        selected_rows = self.proposals_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        proposal_id = int(selected_rows[0].text())
        reply = QMessageBox.question(self, "Xác nhận", 
            "Bạn có chắc muốn xóa ứng viên này?",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.voting_service.db_manager.delete_proposal(proposal_id)
            QMessageBox.information(self, "Thành công", "Đã xóa ứng viên")
            self.load_proposals()
    
    def load_voters(self):
        """Load voters into table"""
        voters = self.voting_service.db_manager.get_all_voters()
        self.voters_table.setRowCount(len(voters))
        
        for row, voter in enumerate(voters):
            self.voters_table.setItem(row, 0, QTableWidgetItem(str(voter.id)))
            self.voters_table.setItem(row, 1, QTableWidgetItem(voter.full_name))
            self.voters_table.setItem(row, 2, QTableWidgetItem(voter.cccd if voter.cccd else "Chưa có"))
            self.voters_table.setItem(row, 3, QTableWidgetItem("✅" if voter.face_registered else "❌"))
            self.voters_table.setItem(row, 4, QTableWidgetItem("✅" if voter.voted else "❌"))
            self.voters_table.setItem(row, 5, QTableWidgetItem("✅" if voter.verified else "❌"))
            self.voters_table.setItem(row, 6, QTableWidgetItem(voter.public_key[:50] + "..."))
    
    def add_voter(self):
        """Add a new voter"""
        dialog = AddVoterDialog(self)
        if dialog.exec() == QDialog.Accepted:
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(
                id=0,
                full_name=dialog.name_input.text(),
                public_key=public_key,
                private_key=private_key,
                weight=dialog.weight_input.value(),
                verified=False
            )
            voter.id = self.voting_service.db_manager.add_voter(voter)
            QMessageBox.information(self, "Thành công", 
                f"Đã thêm cử tri với ID: {voter.id}")
            self.load_voters()
    
    def verify_voter(self):
        """Verify selected voter"""
        selected_rows = self.voters_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cử tri")
            return
        
        voter_id = int(selected_rows[0].text())
        if self.auth_service.verify_voter(voter_id):
            QMessageBox.information(self, "Thành công", "Đã xác thực cử tri")
            self.load_voters()
    
    def register_voter_face(self):
        """Register face for selected voter"""
        from services.face_recognition_service import FaceRecognitionService
        
        selected_rows = self.voters_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cử tri")
            return
        
        voter_id = int(selected_rows[0].text())
        voter = self.voting_service.db_manager.get_voter_by_id(voter_id)
        
        if not voter:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy cử tri")
            return
        
        if not voter.cccd:
            QMessageBox.warning(self, "Lỗi", 
                              f"Cử tri {voter.full_name} chưa có số CCCD.\n"
                              "Vui lòng cập nhật CCCD trước khi đăng ký khuôn mặt.")
            return
        
        # Check if already registered
        face_service = FaceRecognitionService()
        if face_service.has_registered_face(voter.cccd):
            reply = QMessageBox.question(
                self, "Xác nhận",
                f"Cử tri {voter.full_name} (CCCD: {voter.cccd}) đã đăng ký khuôn mặt.\n"
                "Bạn có muốn đăng ký lại không?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
            face_service.delete_face(voter.cccd)
        
        # Register face
        QMessageBox.information(
            self, "Hướng dẫn",
            f"Chuẩn bị đăng ký khuôn mặt cho:\n"
            f"Tên: {voter.full_name}\n"
            f"CCCD: {voter.cccd}\n\n"
            "Webcam sẽ mở. Nhấn SPACE để chụp, ESC để hủy."
        )
        
        if face_service.register_face(voter.cccd, voter.full_name):
            voter.face_registered = True
            self.voting_service.db_manager.update_voter(voter)
            QMessageBox.information(
                self, "Thành công",
                f"Đã đăng ký khuôn mặt cho {voter.full_name}"
            )
            self.load_voters()
        else:
            QMessageBox.warning(
                self, "Lỗi",
                "Không thể đăng ký khuôn mặt. Vui lòng thử lại."
            )
    
    def load_blockchain(self):
        """Load blockchain into table"""
        blocks = self.voting_service.blockchain.get_all_blocks()
        self.blocks_table.setRowCount(len(blocks))
        
        for row, block in enumerate(blocks):
            self.blocks_table.setItem(row, 0, QTableWidgetItem(str(block.index)))
            self.blocks_table.setItem(row, 1, QTableWidgetItem(block.timestamp))
            self.blocks_table.setItem(row, 2, QTableWidgetItem(str(block.voter_id)))
            self.blocks_table.setItem(row, 3, QTableWidgetItem(str(block.proposal_id)))
            self.blocks_table.setItem(row, 4, QTableWidgetItem(block.hash[:50] + "..."))
            self.blocks_table.setItem(row, 5, QTableWidgetItem(block.previous_hash[:50] + "..."))
        
        # Update info
        is_valid = self.voting_service.blockchain.is_chain_valid()
        self.chain_valid_label.setText(
            f"✅ Blockchain hợp lệ" if is_valid else "❌ Blockchain không hợp lệ"
        )
        self.chain_length_label.setText(f"📦 Số block: {len(blocks)}")
    
    def verify_blockchain(self):
        """Verify blockchain integrity"""
        is_valid = self.voting_service.blockchain.is_chain_valid()
        if is_valid:
            QMessageBox.information(self, "Kết quả kiểm tra", 
                "✅ Blockchain hợp lệ và toàn vẹn")
        else:
            QMessageBox.warning(self, "Kết quả kiểm tra", 
                "❌ Blockchain đã bị thay đổi hoặc không hợp lệ")
    
    def load_results(self):
        """Load election results"""
        election = self.election_service.get_current_election()
        if not election:
            self.results_table.setRowCount(0)
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        proposals.sort(key=lambda p: p.vote_count, reverse=True)
        
        total_votes = sum(p.vote_count for p in proposals)
        
        self.results_table.setRowCount(len(proposals))
        for row, proposal in enumerate(proposals):
            self.results_table.setItem(row, 0, QTableWidgetItem(proposal.candidate_name))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(proposal.vote_count)))
            percentage = (proposal.vote_count / total_votes * 100) if total_votes > 0 else 0
            self.results_table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))
    
    def show_chart(self):
        """Show results chart with percentages"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
        from matplotlib.figure import Figure
        
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Không có cuộc bầu cử nào")
            return
            
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        if not proposals or all(p.vote_count == 0 for p in proposals):
            QMessageBox.information(self, "Thông báo", "Chưa có dữ liệu để hiển thị")
            return
        
        proposals.sort(key=lambda p: p.vote_count, reverse=True)
        total_votes = sum(p.vote_count for p in proposals)
        
        # Create dialog with chart
        dialog = QDialog(self)
        dialog.setWindowTitle("📊 Biểu đồ kết quả")
        dialog.setMinimumSize(900, 700)
        layout = QVBoxLayout()
        
        # Create matplotlib figure
        fig = Figure(figsize=(10, 7), facecolor='#1e293b')
        canvas = FigureCanvasQTAgg(fig)
        
        # Create subplots for bar chart and pie chart
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Prepare data
        names = [p.candidate_name for p in proposals]
        votes = [p.vote_count for p in proposals]
        percentages = [(v / total_votes * 100) if total_votes > 0 else 0 for v in votes]
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16']
        
        # Bar chart
        bars = ax1.barh(names, percentages, color=colors[:len(names)])
        ax1.set_xlabel('Phần trăm (%)', color='#f8fafc', fontsize=11, fontweight='bold')
        ax1.set_title('Kết quả theo phần trăm', color='#60a5fa', fontsize=14, fontweight='bold', pad=15)
        ax1.set_facecolor('#0f172a')
        ax1.tick_params(colors='#f8fafc', labelsize=9)
        ax1.spines['bottom'].set_color('#334155')
        ax1.spines['left'].set_color('#334155')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='x', alpha=0.2, color='#334155')
        
        # Add percentage labels
        for bar, pct, vote in zip(bars, percentages, votes):
            width = bar.get_width()
            ax1.text(width + 1, bar.get_y() + bar.get_height()/2, 
                    f'{pct:.1f}% ({vote})',
                    ha='left', va='center', color='#f8fafc', fontsize=9, fontweight='600')
        
        ax1.set_xlim(0, max(percentages) * 1.25 if percentages else 100)
        
        # Pie chart
        wedges, texts, autotexts = ax2.pie(votes, labels=names, autopct='%1.1f%%',
                                            colors=colors[:len(names)],
                                            startangle=90,
                                            textprops={'color': '#f8fafc', 'fontsize': 9})
        ax2.set_title('Phân bổ phiếu bầu', color='#60a5fa', fontsize=14, fontweight='bold', pad=15)
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('#0f172a')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        fig.tight_layout()
        layout.addWidget(canvas)
        
        # Add statistics
        stats_label = QLabel(f"📊 Tổng số phiếu: {total_votes}")
        stats_label.setObjectName("valueLabel")
        stats_label.setStyleSheet("color: #60a5fa; padding: 10px; font-size: 12pt;")
        layout.addWidget(stats_label)
        
        # Add close button
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setMinimumHeight(40)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec()

class CreateElectionDialog(QDialog):
    """Dialog for creating new election"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Tạo cuộc bầu cử mới")
        self.setFixedSize(500, 350)
        
        layout = QFormLayout()
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ví dụ: Bầu cử Tổng thống 2026")
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Mô tả chi tiết về cuộc bầu cử...")
        self.desc_input.setMaximumHeight(100)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([BlockchainMode.PERMISSIONLESS, BlockchainMode.PERMISSIONED])
        
        layout.addRow("Tiêu đề:", self.title_input)
        layout.addRow("Mô tả:", self.desc_input)
        layout.addRow("Chế độ blockchain:", self.mode_combo)
        
        # Info
        info = QLabel(
            "💡 Permissionless: Mọi cử tri có thể bỏ phiếu\n"
            "💡 Permissioned: Chỉ cử tri đã xác thực mới được bỏ phiếu"
        )
        info.setObjectName("infoLabel")
        layout.addRow(info)
        
        # Buttons
        button_layout = QHBoxLayout()
        create_btn = QPushButton("Tạo")
        create_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        self.setLayout(layout)

class AddProposalDialog(QDialog):
    """Dialog for adding/editing proposal"""
    
    def __init__(self, parent=None, proposal=None):
        super().__init__(parent)
        self.proposal = proposal
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        title = "Sửa ứng viên" if self.proposal else "Thêm ứng viên"
        self.setWindowTitle(title)
        self.setFixedSize(500, 300)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tên ứng viên")
        if self.proposal:
            self.name_input.setText(self.proposal.candidate_name)
        
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Mô tả về ứng viên...")
        self.desc_input.setMaximumHeight(150)
        if self.proposal:
            self.desc_input.setPlainText(self.proposal.description)
        
        layout.addRow("Tên ứng viên:", self.name_input)
        layout.addRow("Mô tả:", self.desc_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Lưu")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        self.setLayout(layout)

class AddVoterDialog(QDialog):
    """Dialog for adding voter"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Thêm cử tri")
        self.setFixedSize(400, 200)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Họ và tên")
        
        self.weight_input = QSpinBox()
        self.weight_input.setMinimum(1)
        self.weight_input.setMaximum(10)
        self.weight_input.setValue(1)
        
        layout.addRow("Họ tên:", self.name_input)
        layout.addRow("Quyền biểu quyết:", self.weight_input)
        
        info = QLabel("🔐 Khóa công khai/riêng tư sẽ được tạo tự động")
        info.setObjectName("infoLabel")
        layout.addRow(info)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Thêm")
        add_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Hủy")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        self.setLayout(layout)
