"""Enhanced Admin view with modern dashboard and better UX"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QMessageBox, QGroupBox, QLineEdit, QTextEdit,
                               QDialog, QFormLayout, QComboBox, QTabWidget,
                               QHeaderView, QSpinBox, QFrame, QGridLayout,
                               QScrollArea)
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

class AdminViewEnhanced(QWidget):
    """Enhanced view for administrators with modern dashboard"""
    
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
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header with welcome message
        header_layout = QHBoxLayout()
        header = QLabel("🔧 Bảng điều khiển quản trị")
        header.setObjectName("titleLabel")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        # Logout button in header
        logout_btn = QPushButton("🚪 Đăng xuất")
        logout_btn.setObjectName("dangerButton")
        logout_btn.clicked.connect(self.logout_signal.emit)
        logout_btn.setMaximumWidth(180)
        header_layout.addWidget(logout_btn)
        layout.addLayout(header_layout)
        
        # Dashboard with statistics
        dashboard = self.create_dashboard()
        layout.addWidget(dashboard)
        
        # Tabs for different sections
        tabs = QTabWidget()
        tabs.addTab(self.create_election_tab(), "📋 Cuộc bầu cử")
        tabs.addTab(self.create_proposals_tab(), "🎯 Ứng viên")
        tabs.addTab(self.create_voters_tab(), "👥 Cử tri")
        tabs.addTab(self.create_blockchain_tab(), "⛓️ Blockchain")
        tabs.addTab(self.create_results_tab(), "📊 Kết quả")
        layout.addWidget(tabs)
        
        self.setLayout(layout)
    
    def create_dashboard(self):
        """Create dashboard with statistics cards"""
        dashboard = QFrame()
        dashboard_layout = QGridLayout()
        dashboard_layout.setSpacing(20)
        
        # Get statistics
        all_voters = self.voting_service.db_manager.get_all_voters()
        all_elections = self.voting_service.db_manager.get_all_elections()
        current_election = self.election_service.get_current_election()
        
        total_voters = len(all_voters)
        verified_voters = len([v for v in all_voters if v.verified])
        total_elections = len(all_elections)
        blockchain_blocks = len(self.blockchain.chain)
        
        # Card 1: Total Voters
        card1 = self.create_stat_card(
            "👥", "Tổng số cử tri", str(total_voters),
            f"{verified_voters} đã xác thực", "dashboardCard"
        )
        dashboard_layout.addWidget(card1, 0, 0)
        
        # Card 2: Elections
        card2 = self.create_stat_card(
            "🗳️", "Cuộc bầu cử", str(total_elections),
            "Tổng số cuộc bầu cử", "successCard"
        )
        dashboard_layout.addWidget(card2, 0, 1)
        
        # Card 3: Blockchain
        is_valid = self.blockchain.is_chain_valid()
        card3 = self.create_stat_card(
            "⛓️", "Blockchain", str(blockchain_blocks),
            "✅ Hợp lệ" if is_valid else "❌ Không hợp lệ",
            "successCard" if is_valid else "dangerCard"
        )
        dashboard_layout.addWidget(card3, 0, 2)
        
        # Card 4: Current Election Status
        if current_election:
            proposals = self.voting_service.db_manager.get_all_proposals(current_election.id)
            total_votes = sum(p.vote_count for p in proposals)
            card4 = self.create_stat_card(
                "📊", "Phiếu bầu hiện tại", str(total_votes),
                f"{len(proposals)} ứng viên", "warningCard"
            )
        else:
            card4 = self.create_stat_card(
                "📊", "Phiếu bầu hiện tại", "0",
                "Chưa có cuộc bầu cử", "warningCard"
            )
        dashboard_layout.addWidget(card4, 0, 3)
        
        dashboard.setLayout(dashboard_layout)
        return dashboard
    
    def create_stat_card(self, icon, title, value, subtitle, card_type):
        """Create a statistics card"""
        card = QFrame()
        card.setObjectName(card_type)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(10)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 32pt;")
        header_layout.addWidget(icon_label)
        header_layout.addStretch()
        
        title_label = QLabel(title)
        title_label.setObjectName("statLabel")
        
        card_layout.addLayout(header_layout)
        card_layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setObjectName("statNumber")
        card_layout.addWidget(value_label)
        
        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("infoLabel")
        card_layout.addWidget(subtitle_label)
        
        card.setLayout(card_layout)
        card.setMinimumHeight(140)
        return card

    
    def create_election_tab(self):
        """Create election management tab with modern design"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(25)
        
        # Current election info card
        info_group = QGroupBox("📊 Thông tin cuộc bầu cử hiện tại")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        
        self.election_info_label = QLabel("Chưa có cuộc bầu cử")
        self.election_info_label.setWordWrap(True)
        self.election_info_label.setObjectName("valueLabel")
        info_layout.addWidget(self.election_info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # State machine visual
        state_group = QGroupBox("🔄 Quy trình bầu cử (State Machine)")
        state_layout = QVBoxLayout()
        state_layout.setSpacing(20)
        
        # Current state indicator
        self.current_state_label = QLabel("Trạng thái hiện tại: Chưa có cuộc bầu cử")
        self.current_state_label.setObjectName("subtitleLabel")
        self.current_state_label.setAlignment(Qt.AlignCenter)
        self.current_state_label.setStyleSheet("""
            padding: 18px;
            border-radius: 12px;
            background-color: rgba(30, 41, 59, 0.8);
            border: 2px solid rgba(59, 130, 246, 0.3);
        """)
        state_layout.addWidget(self.current_state_label)
        
        # State transition buttons in grid
        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(15)
        
        self.validate_btn = QPushButton("1️⃣ Xác thực\ncử tri")
        self.validate_btn.setMinimumHeight(70)
        self.validate_btn.clicked.connect(lambda: self.transition_state(ElectionState.VALIDATE_VOTER))
        
        self.vote_btn = QPushButton("2️⃣ Mở\nbỏ phiếu")
        self.vote_btn.setMinimumHeight(70)
        self.vote_btn.clicked.connect(lambda: self.transition_state(ElectionState.VOTE))
        
        self.count_btn = QPushButton("3️⃣ Kiểm\nphiếu")
        self.count_btn.setMinimumHeight(70)
        self.count_btn.clicked.connect(lambda: self.transition_state(ElectionState.COUNT))
        
        self.declare_btn = QPushButton("4️⃣ Công bố\nkết quả")
        self.declare_btn.setMinimumHeight(70)
        self.declare_btn.clicked.connect(lambda: self.transition_state(ElectionState.DECLARE_WINNER))
        
        self.done_btn = QPushButton("5️⃣ Kết thúc")
        self.done_btn.setMinimumHeight(70)
        self.done_btn.clicked.connect(lambda: self.transition_state(ElectionState.DONE))
        
        self.state_buttons = {
            ElectionState.START: None,
            ElectionState.VALIDATE_VOTER: self.validate_btn,
            ElectionState.VOTE: self.vote_btn,
            ElectionState.COUNT: self.count_btn,
            ElectionState.DECLARE_WINNER: self.declare_btn,
            ElectionState.DONE: self.done_btn
        }
        
        buttons_grid.addWidget(self.validate_btn, 0, 0)
        buttons_grid.addWidget(self.vote_btn, 0, 1)
        buttons_grid.addWidget(self.count_btn, 0, 2)
        buttons_grid.addWidget(self.declare_btn, 1, 0)
        buttons_grid.addWidget(self.done_btn, 1, 1)
        
        state_layout.addLayout(buttons_grid)
        state_group.setLayout(state_layout)
        layout.addWidget(state_group)
        
        # Create new election button
        create_btn = QPushButton("➕ Tạo cuộc bầu cử mới")
        create_btn.setObjectName("successButton")
        create_btn.setMinimumHeight(55)
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("🎯 Quản lý ứng viên")
        header.setObjectName("subtitleLabel")
        layout.addWidget(header)
        
        # Proposals table
        self.proposals_table = QTableWidget()
        self.proposals_table.setColumnCount(4)
        self.proposals_table.setHorizontalHeaderLabels(["ID", "Ứng viên", "Mô tả", "Số phiếu"])
        self.proposals_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.proposals_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.proposals_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.proposals_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.proposals_table.setColumnWidth(1, 220)
        self.proposals_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.proposals_table.setAlternatingRowColors(True)
        self.proposals_table.verticalHeader().setVisible(False)
        self.proposals_table.setMinimumHeight(350)
        layout.addWidget(self.proposals_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        add_btn = QPushButton("➕ Thêm ứng viên")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_proposal)
        add_btn.setMinimumHeight(45)
        
        edit_btn = QPushButton("✏️ Sửa")
        edit_btn.clicked.connect(self.edit_proposal)
        edit_btn.setMinimumHeight(45)
        
        delete_btn = QPushButton("🗑️ Xóa")
        delete_btn.setObjectName("dangerButton")
        delete_btn.clicked.connect(self.delete_proposal)
        delete_btn.setMinimumHeight(45)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_proposals)
        refresh_btn.setMinimumHeight(45)
        
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("👥 Quản lý cử tri")
        header.setObjectName("subtitleLabel")
        layout.addWidget(header)
        
        # Voters table
        self.voters_table = QTableWidget()
        self.voters_table.setColumnCount(7)
        self.voters_table.setHorizontalHeaderLabels([
            "ID", "Họ tên", "CCCD", "Khuôn mặt", "Đã bỏ phiếu", "Đã xác thực", "Public Key"
        ])
        self.voters_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.voters_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.voters_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.voters_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.voters_table.setColumnWidth(1, 200)
        self.voters_table.setColumnWidth(2, 130)
        self.voters_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.voters_table.setAlternatingRowColors(True)
        self.voters_table.verticalHeader().setVisible(False)
        self.voters_table.setMinimumHeight(350)
        layout.addWidget(self.voters_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        add_btn = QPushButton("➕ Thêm cử tri")
        add_btn.setObjectName("successButton")
        add_btn.clicked.connect(self.add_voter)
        add_btn.setMinimumHeight(45)
        
        verify_btn = QPushButton("✅ Xác thực")
        verify_btn.setObjectName("successButton")
        verify_btn.clicked.connect(self.verify_voter)
        verify_btn.setMinimumHeight(45)
        
        face_register_btn = QPushButton("📸 Đăng ký khuôn mặt")
        face_register_btn.setObjectName("warningButton")
        face_register_btn.clicked.connect(self.register_voter_face)
        face_register_btn.setMinimumHeight(45)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_voters)
        refresh_btn.setMinimumHeight(45)
        
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("⛓️ Blockchain Explorer")
        header.setObjectName("subtitleLabel")
        layout.addWidget(header)
        
        # Blockchain info
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)
        
        self.chain_valid_label = QLabel()
        self.chain_valid_label.setObjectName("valueLabel")
        self.chain_length_label = QLabel()
        self.chain_length_label.setObjectName("valueLabel")
        
        info_layout.addWidget(self.chain_valid_label)
        info_layout.addWidget(self.chain_length_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Blocks table
        self.blocks_table = QTableWidget()
        self.blocks_table.setColumnCount(6)
        self.blocks_table.setHorizontalHeaderLabels([
            "Index", "Timestamp", "Voter ID", "Proposal ID", "Hash", "Previous Hash"
        ])
        self.blocks_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.blocks_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.blocks_table.setMinimumHeight(350)
        layout.addWidget(self.blocks_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        verify_btn = QPushButton("🔍 Kiểm tra tính toàn vẹn")
        verify_btn.setObjectName("warningButton")
        verify_btn.clicked.connect(self.verify_blockchain)
        verify_btn.setMinimumHeight(45)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_blockchain)
        refresh_btn.setMinimumHeight(45)
        
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
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("📊 Kết quả bầu cử")
        header.setObjectName("subtitleLabel")
        layout.addWidget(header)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Ứng viên", "Số phiếu", "Tỷ lệ %"])
        self.results_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.results_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Interactive)
        self.results_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.results_table.setColumnWidth(1, 150)
        self.results_table.setColumnWidth(2, 150)
        self.results_table.setMinimumHeight(350)
        layout.addWidget(self.results_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        refresh_btn = QPushButton("🔄 Làm mới")
        refresh_btn.clicked.connect(self.load_results)
        refresh_btn.setMinimumHeight(45)
        
        chart_btn = QPushButton("📊 Xem biểu đồ")
        chart_btn.setObjectName("successButton")
        chart_btn.clicked.connect(self.show_chart)
        chart_btn.setMinimumHeight(45)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(chart_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        self.load_results()
        return widget

    
    # Implementation methods (same logic as original but with UI updates)
    def update_election_info(self):
        """Update election information display"""
        election = self.election_service.get_current_election()
        if election:
            info_text = f"""
📋 <b>Tiêu đề:</b> {election.title}<br>
📝 <b>Mô tả:</b> {election.description}<br>
🔄 <b>Trạng thái:</b> {election.state}<br>
⛓️ <b>Chế độ:</b> {election.blockchain_mode}<br>
⏰ <b>Bắt đầu:</b> {election.start_time.strftime('%Y-%m-%d %H:%M:%S') if election.start_time else 'N/A'}
            """
            self.election_info_label.setText(info_text)
            
            # Update state display
            state_colors = {
                ElectionState.START: ("#3b82f6", "🟦 Start - Khởi tạo"),
                ElectionState.VALIDATE_VOTER: ("#f59e0b", "🟨 ValidateVoter - Xác thực cử tri"),
                ElectionState.VOTE: ("#10b981", "🟩 Vote - Đang bỏ phiếu"),
                ElectionState.COUNT: ("#f97316", "🟧 Count - Kiểm phiếu"),
                ElectionState.DECLARE_WINNER: ("#8b5cf6", "🟪 DeclareWinner - Công bố kết quả"),
                ElectionState.DONE: ("#6b7280", "⬜ Done - Đã kết thúc")
            }
            
            color, text = state_colors.get(election.state, ("#3b82f6", election.state))
            self.current_state_label.setText(f"<b>Trạng thái hiện tại:</b> {text}")
            self.current_state_label.setStyleSheet(f"""
                padding: 18px;
                border-radius: 12px;
                background-color: {color};
                color: #ffffff;
                font-weight: bold;
                border: 3px solid rgba(255, 255, 255, 0.3);
            """)
            
            # Reset button styles
            for btn in self.state_buttons.values():
                if btn:
                    btn.setStyleSheet("")
            
            # Highlight current button
            current_btn = self.state_buttons.get(election.state)
            if current_btn:
                current_btn.setStyleSheet(f"""
                    background-color: {color};
                    color: #ffffff;
                    font-weight: bold;
                    border: 3px solid rgba(255, 255, 255, 0.5);
                """)
        else:
            self.election_info_label.setText("Chưa có cuộc bầu cử")
            self.current_state_label.setText("Trạng thái hiện tại: Chưa có cuộc bầu cử")
            self.current_state_label.setStyleSheet("""
                padding: 18px;
                border-radius: 12px;
                background-color: rgba(30, 41, 59, 0.8);
                border: 2px solid rgba(59, 130, 246, 0.3);
            """)
    
    def transition_state(self, new_state: str):
        """Transition election state"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Chưa có cuộc bầu cử")
            return
        
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
                QMessageBox.
    def update_election_info(self):
        """Update election information display"""
        election = self.election_service.get_current_election()
        if election:
            info_text = f"""
📋 <b>Tiêu đề:</b> {election.title}<br>
📝 <b>Mô tả:</b> {election.description}<br>
🔄 <b>Trạng thái:</b> {election.state}<br>
⛓️ <b>Chế độ:</b> {election.blockchain_mode}<br>
⏰ <b>Bắt đầu:</b> {election.start_time.strftime('%Y-%m-%d %H:%M:%S') if election.start_time else 'N/A'}
            """
            self.election_info_label.setText(info_text)
            
            # Update state display
            state_colors = {
                ElectionState.START: ("#3b82f6", "🟦 Start - Khởi tạo"),
                ElectionState.VALIDATE_VOTER: ("#f59e0b", "🟨 ValidateVoter - Xác thực cử tri"),
                ElectionState.VOTE: ("#10b981", "🟩 Vote - Đang bỏ phiếu"),
                ElectionState.COUNT: ("#f97316", "🟧 Count - Kiểm phiếu"),
                ElectionState.DECLARE_WINNER: ("#8b5cf6", "🟪 DeclareWinner - Công bố kết quả"),
                ElectionState.DONE: ("#6b7280", "⬜ Done - Đã kết thúc")
            }
            
            color, text = state_colors.get(election.state, ("#3b82f6", election.state))
            self.current_state_label.setText(f"<b>Trạng thái hiện tại:</b> {text}")
            self.current_state_label.setStyleSheet(f"""
                padding: 18px;
                border-radius: 12px;
                background-color: {color};
                color: #ffffff;
                font-weight: bold;
                border: 3px solid rgba(255, 255, 255, 0.3);
            """)
            
            # Reset button styles
            for btn in self.state_buttons.values():
                if btn:
                    btn.setStyleSheet("")
            
            # Highlight current button
            current_btn = self.state_buttons.get(election.state)
            if current_btn:
                current_btn.setStyleSheet(f"""
                    background-color: {color};
                    color: #ffffff;
                    font-weight: bold;
                    border: 3px solid rgba(255, 255, 255, 0.5);
                """)
        else:
            self.election_info_label.setText("Chưa có cuộc bầu cử")
            self.current_state_label.setText("Trạng thái hiện tại: Chưa có cuộc bầu cử")
            self.current_state_label.setStyleSheet("""
                padding: 18px;
                border-radius: 12px;
                background-color: rgba(30, 41, 59, 0.8);
                border: 2px solid rgba(59, 130, 246, 0.3);
            """)
    
    def transition_state(self, new_state: str):
        """Transition election state"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Chưa có cuộc bầu cử")
            return
        
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
        self.load_proposals()
    
    def create_new_election(self):
        """Create new election dialog"""
        from PySide6.QtWidgets import QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Tạo cuộc bầu cử mới")
        dialog.setMinimumWidth(500)
        
        layout = QFormLayout()
        
        title_input = QLineEdit()
        title_input.setPlaceholderText("Nhập tiêu đề...")
        
        desc_input = QTextEdit()
        desc_input.setPlaceholderText("Nhập mô tả...")
        desc_input.setMaximumHeight(100)
        
        mode_combo = QComboBox()
        mode_combo.addItems([BlockchainMode.POW, BlockchainMode.POS])
        
        layout.addRow("Tiêu đề:", title_input)
        layout.addRow("Mô tả:", desc_input)
        layout.addRow("Chế độ blockchain:", mode_combo)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        dialog.setLayout(main_layout)
        
        if dialog.exec() == QDialog.Accepted:
            title = title_input.text().strip()
            description = desc_input.toPlainText().strip()
            mode = mode_combo.currentText()
            
            if not title:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tiêu đề")
                return
            
            success, message = self.election_service.create_election(title, description, mode)
            if success:
                QMessageBox.information(self, "Thành công", message)
                self.update_election_info()
            else:
                QMessageBox.warning(self, "Lỗi", message)
    
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
        """Add new proposal"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Chưa có cuộc bầu cử")
            return
        
        from PySide6.QtWidgets import QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm ứng viên")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nhập tên ứng viên...")
        
        desc_input = QTextEdit()
        desc_input.setPlaceholderText("Nhập mô tả...")
        desc_input.setMaximumHeight(100)
        
        layout.addRow("Tên ứng viên:", name_input)
        layout.addRow("Mô tả:", desc_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        dialog.setLayout(main_layout)
        
        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            description = desc_input.toPlainText().strip()
            
            if not name:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên ứng viên")
                return
            
            proposal = Proposal(0, election.id, name, description, 0)
            self.voting_service.db_manager.add_proposal(proposal)
            QMessageBox.information(self, "Thành công", "Đã thêm ứng viên")
            self.load_proposals()
    
    def edit_proposal(self):
        """Edit selected proposal"""
        selected_row = self.proposals_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        proposal_id = int(self.proposals_table.item(selected_row, 0).text())
        election = self.election_service.get_current_election()
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        proposal = next((p for p in proposals if p.id == proposal_id), None)
        
        if not proposal:
            return
        
        from PySide6.QtWidgets import QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Sửa ứng viên")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        name_input = QLineEdit(proposal.candidate_name)
        desc_input = QTextEdit()
        desc_input.setPlainText(proposal.description)
        desc_input.setMaximumHeight(100)
        
        layout.addRow("Tên ứng viên:", name_input)
        layout.addRow("Mô tả:", desc_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        dialog.setLayout(main_layout)
        
        if dialog.exec() == QDialog.Accepted:
            proposal.candidate_name = name_input.text().strip()
            proposal.description = desc_input.toPlainText().strip()
            
            self.voting_service.db_manager.update_proposal(proposal)
            QMessageBox.information(self, "Thành công", "Đã cập nhật ứng viên")
            self.load_proposals()
    
    def delete_proposal(self):
        """Delete selected proposal"""
        selected_row = self.proposals_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ứng viên")
            return
        
        proposal_id = int(self.proposals_table.item(selected_row, 0).text())
        
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
            self.voters_table.setItem(row, 2, QTableWidgetItem(voter.cccd))
            self.voters_table.setItem(row, 3, QTableWidgetItem("✅" if voter.face_registered else "❌"))
            self.voters_table.setItem(row, 4, QTableWidgetItem("✅" if voter.has_voted else "❌"))
            self.voters_table.setItem(row, 5, QTableWidgetItem("✅" if voter.verified else "❌"))
            self.voters_table.setItem(row, 6, QTableWidgetItem(voter.public_key[:50] + "..."))
    
    def add_voter(self):
        """Add new voter"""
        from PySide6.QtWidgets import QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm cử tri")
        dialog.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nhập họ tên...")
        
        cccd_input = QLineEdit()
        cccd_input.setPlaceholderText("Nhập số CCCD (12 số)...")
        cccd_input.setMaxLength(12)
        
        layout.addRow("Họ tên:", name_input)
        layout.addRow("CCCD:", cccd_input)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        dialog.setLayout(main_layout)
        
        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            cccd = cccd_input.text().strip()
            
            if not name or not cccd:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return
            
            if len(cccd) != 12 or not cccd.isdigit():
                QMessageBox.warning(self, "Lỗi", "CCCD phải là 12 chữ số")
                return
            
            private_key, public_key = self.crypto_service.generate_key_pair()
            voter = Voter(0, name, public_key, private_key, cccd, False, 1, False)
            self.voting_service.db_manager.add_voter(voter)
            QMessageBox.information(self, "Thành công", "Đã thêm cử tri")
            self.load_voters()
    
    def verify_voter(self):
        """Verify selected voter"""
        selected_row = self.voters_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cử tri")
            return
        
        voter_id = int(self.voters_table.item(selected_row, 0).text())
        voter = self.voting_service.db_manager.get_voter_by_id(voter_id)
        
        if voter.verified:
            QMessageBox.information(self, "Thông báo", "Cử tri đã được xác thực")
            return
        
        voter.verified = True
        self.voting_service.db_manager.update_voter(voter)
        QMessageBox.information(self, "Thành công", "Đã xác thực cử tri")
        self.load_voters()
    
    def register_voter_face(self):
        """Register face for selected voter"""
        selected_row = self.voters_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cử tri")
            return
        
        voter_id = int(self.voters_table.item(selected_row, 0).text())
        QMessageBox.information(self, "Thông báo", 
            f"Chức năng đăng ký khuôn mặt cho cử tri ID {voter_id}\n"
            "Vui lòng sử dụng chức năng đăng ký từ màn hình chính")
    
    def load_blockchain(self):
        """Load blockchain into table"""
        is_valid = self.blockchain.is_chain_valid()
        self.chain_valid_label.setText(f"Trạng thái: {'✅ Hợp lệ' if is_valid else '❌ Không hợp lệ'}")
        self.chain_length_label.setText(f"Số blocks: {len(self.blockchain.chain)}")
        
        self.blocks_table.setRowCount(len(self.blockchain.chain))
        
        for row, block in enumerate(self.blockchain.chain):
            self.blocks_table.setItem(row, 0, QTableWidgetItem(str(block.index)))
            self.blocks_table.setItem(row, 1, QTableWidgetItem(block.timestamp))
            self.blocks_table.setItem(row, 2, QTableWidgetItem(str(block.voter_id)))
            self.blocks_table.setItem(row, 3, QTableWidgetItem(str(block.proposal_id)))
            self.blocks_table.setItem(row, 4, QTableWidgetItem(block.hash[:50] + "..."))
            self.blocks_table.setItem(row, 5, QTableWidgetItem(block.previous_hash[:50] + "..."))
    
    def verify_blockchain(self):
        """Verify blockchain integrity"""
        is_valid = self.blockchain.is_chain_valid()
        
        if is_valid:
            QMessageBox.information(self, "Kết quả kiểm tra", 
                "✅ Blockchain hợp lệ\n\n"
                f"Tổng số blocks: {len(self.blockchain.chain)}\n"
                "Tất cả các blocks đều có hash hợp lệ và liên kết đúng")
        else:
            QMessageBox.warning(self, "Kết quả kiểm tra", 
                "❌ Blockchain không hợp lệ\n\n"
                "Phát hiện sự bất thường trong chuỗi blocks")
    
    def load_results(self):
        """Load election results"""
        election = self.election_service.get_current_election()
        if not election:
            self.results_table.setRowCount(0)
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        total_votes = sum(p.vote_count for p in proposals)
        
        self.results_table.setRowCount(len(proposals))
        
        for row, proposal in enumerate(proposals):
            percentage = (proposal.vote_count / total_votes * 100) if total_votes > 0 else 0
            
            self.results_table.setItem(row, 0, QTableWidgetItem(proposal.candidate_name))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(proposal.vote_count)))
            self.results_table.setItem(row, 2, QTableWidgetItem(f"{percentage:.2f}%"))
    
    def show_chart(self):
        """Show results chart"""
        election = self.election_service.get_current_election()
        if not election:
            QMessageBox.warning(self, "Lỗi", "Chưa có cuộc bầu cử")
            return
        
        proposals = self.voting_service.db_manager.get_all_proposals(election.id)
        
        if not proposals:
            QMessageBox.warning(self, "Lỗi", "Chưa có ứng viên")
            return
        
        # Simple text-based chart
        chart_text = "📊 KẾT QUẢ BẦU CỬ\n\n"
        max_votes = max(p.vote_count for p in proposals) if proposals else 1
        
        for proposal in sorted(proposals, key=lambda p: p.vote_count, reverse=True):
            bar_length = int((proposal.vote_count / max_votes * 30)) if max_votes > 0 else 0
            bar = "█" * bar_length
            chart_text += f"{proposal.candidate_name:20} {bar} {proposal.vote_count}\n"
        
        QMessageBox.information(self, "Biểu đồ kết quả", chart_text)
