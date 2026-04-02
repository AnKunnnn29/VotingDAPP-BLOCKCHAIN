"""Modern blockchain-themed stylesheet for the application"""

MAIN_STYLE = """
/* Main Window - Dark blockchain theme with gradient */
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a0e27, stop:0.5 #0f172a, stop:1 #1a1f3a);
}

QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0a0e27, stop:0.5 #0f172a, stop:1 #1a1f3a);
}

QWidget {
    font-family: 'Segoe UI', 'Inter', 'Roboto', Arial, sans-serif;
    font-size: 10pt;
    color: #e2e8f0;
}

/* Dashboard Cards */
QFrame#dashboardCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(59, 130, 246, 0.15), stop:1 rgba(30, 41, 59, 0.8));
    border: 2px solid rgba(59, 130, 246, 0.3);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

QFrame#dashboardCard:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(59, 130, 246, 0.25), stop:1 rgba(30, 41, 59, 0.9));
    border: 2px solid rgba(59, 130, 246, 0.5);
}

QFrame#successCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(16, 185, 129, 0.15), stop:1 rgba(30, 41, 59, 0.8));
    border: 2px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

QFrame#successCard:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(16, 185, 129, 0.25), stop:1 rgba(30, 41, 59, 0.9));
    border: 2px solid rgba(16, 185, 129, 0.5);
}

QFrame#warningCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(245, 158, 11, 0.15), stop:1 rgba(30, 41, 59, 0.8));
    border: 2px solid rgba(245, 158, 11, 0.3);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

QFrame#warningCard:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(245, 158, 11, 0.25), stop:1 rgba(30, 41, 59, 0.9));
    border: 2px solid rgba(245, 158, 11, 0.5);
}

QFrame#dangerCard {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(239, 68, 68, 0.15), stop:1 rgba(30, 41, 59, 0.8));
    border: 2px solid rgba(239, 68, 68, 0.3);
    border-radius: 16px;
    padding: 20px;
    min-height: 120px;
}

QFrame#dangerCard:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(239, 68, 68, 0.25), stop:1 rgba(30, 41, 59, 0.9));
    border: 2px solid rgba(239, 68, 68, 0.5);
}

/* Stat Labels */
QLabel#statNumber {
    font-size: 36pt;
    font-weight: 900;
    color: #60a5fa;
    padding: 10px 0;
}

QLabel#statLabel {
    font-size: 11pt;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Buttons - Modern style with smooth transitions */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:1 #2563eb);
    color: white;
    border: 2px solid rgba(59, 130, 246, 0.4);
    padding: 14px 28px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 10pt;
    min-width: 130px;
    min-height: 45px;
    letter-spacing: 0.5px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:1 #3b82f6);
    border: 2px solid rgba(96, 165, 250, 0.6);
    padding: 14px 28px;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563eb, stop:1 #1e40af);
    padding: 15px 27px 13px 29px;
}

QPushButton:disabled {
    background: rgba(30, 41, 59, 0.6);
    color: #475569;
    border: 2px solid #334155;
}

/* Success Button - Modern green style */
QPushButton#successButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #10b981, stop:1 #059669);
    border: 2px solid rgba(16, 185, 129, 0.4);
}

QPushButton#successButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #34d399, stop:1 #10b981);
    border: 2px solid rgba(52, 211, 153, 0.6);
}

QPushButton#successButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #047857);
}

/* Danger Button - Modern red style */
QPushButton#dangerButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ef4444, stop:1 #dc2626);
    border: 2px solid rgba(239, 68, 68, 0.4);
}

QPushButton#dangerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f87171, stop:1 #ef4444);
    border: 2px solid rgba(248, 113, 113, 0.6);
}

QPushButton#dangerButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #b91c1c);
}

/* Warning Button - Modern orange style */
QPushButton#warningButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f59e0b, stop:1 #d97706);
    border: 2px solid rgba(245, 158, 11, 0.4);
}

QPushButton#warningButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #fbbf24, stop:1 #f59e0b);
    border: 2px solid rgba(251, 191, 36, 0.6);
}

/* Secondary Button - Modern outlined style */
QPushButton#secondaryButton {
    background: rgba(59, 130, 246, 0.1);
    border: 2px solid #3b82f6;
    color: #60a5fa;
}

QPushButton#secondaryButton:hover {
    background: rgba(59, 130, 246, 0.2);
    border: 2px solid #60a5fa;
    color: #93c5fd;
}

/* Input Fields - Modern style with better focus */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    padding: 14px 18px;
    border: 2px solid rgba(30, 41, 59, 0.8);
    border-radius: 12px;
    background-color: rgba(15, 23, 42, 0.9);
    color: #e2e8f0;
    selection-background-color: #3b82f6;
    font-size: 10pt;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #3b82f6;
    background-color: rgba(15, 23, 42, 1);
}

QComboBox::drop-down {
    border: none;
    width: 35px;
    padding-right: 5px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid #60a5fa;
    margin-right: 12px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 2px solid #3b82f6;
    border-radius: 10px;
    color: #e2e8f0;
    selection-background-color: #3b82f6;
    padding: 8px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 10px;
    border-radius: 6px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: rgba(59, 130, 246, 0.2);
}

/* Labels - Modern typography */
QLabel {
    color: #e2e8f0;
}

QLabel#titleLabel {
    font-size: 38pt;
    font-weight: 900;
    color: #60a5fa;
    padding: 25px 0;
    letter-spacing: 1px;
}

QLabel#subtitleLabel {
    font-size: 20pt;
    font-weight: 800;
    color: #60a5fa;
    padding: 18px 0;
    letter-spacing: 0.8px;
}

QLabel#infoLabel {
    color: #94a3b8;
    font-size: 10pt;
    line-height: 1.8;
}

QLabel#valueLabel {
    color: #f1f5f9;
    font-size: 12pt;
    font-weight: 700;
    padding: 10px 0;
}

QLabel#blockchainLabel {
    color: #60a5fa;
    font-size: 13pt;
    font-weight: 800;
    font-family: 'Courier New', 'Consolas', monospace;
    background: rgba(59, 130, 246, 0.15);
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
}

/* Tables - Modern grid style */
QTableWidget {
    background-color: rgba(15, 23, 42, 0.7);
    border: 2px solid rgba(30, 41, 59, 0.8);
    border-radius: 14px;
    gridline-color: rgba(51, 65, 85, 0.4);
    color: #e2e8f0;
    selection-background-color: rgba(59, 130, 246, 0.4);
    alternate-background-color: rgba(30, 41, 59, 0.4);
    outline: none;
}

QTableWidget::item {
    padding: 16px 12px;
    border-bottom: 1px solid rgba(51, 65, 85, 0.3);
    outline: none;
}

QTableWidget::item:focus {
    outline: none;
    border: none;
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(59, 130, 246, 0.5), stop:1 rgba(96, 165, 250, 0.5));
    color: #ffffff;
    font-weight: 700;
    border-left: 4px solid #3b82f6;
    outline: none;
}

QTableWidget::item:selected:focus {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(59, 130, 246, 0.5), stop:1 rgba(96, 165, 250, 0.5));
    color: #ffffff;
    outline: none;
    border: none;
    border-left: 4px solid #3b82f6;
}

QTableWidget::item:hover {
    background-color: rgba(59, 130, 246, 0.2);
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e293b, stop:1 #0f172a);
    color: #60a5fa;
    padding: 16px 14px;
    border: none;
    border-bottom: 3px solid #3b82f6;
    font-weight: 800;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    outline: none;
}

QHeaderView::section:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #334155, stop:1 #1e293b);
    color: #93c5fd;
}

/* Fix text eliding - remove dashes */
QTableView {
    text-elide-mode: none;
    outline: none;
    show-decoration-selected: 1;
}

QTableWidget QTableCornerButton::section {
    background: #0f172a;
    border: none;
}

/* Tabs - Modern style */
QTabWidget::pane {
    border: 2px solid rgba(30, 41, 59, 0.8);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(15, 23, 42, 0.9), stop:1 rgba(30, 41, 59, 0.7));
    border-radius: 14px;
    padding: 15px;
}

QTabBar::tab {
    background: rgba(15, 23, 42, 0.7);
    color: #94a3b8;
    padding: 16px 32px;
    margin-right: 8px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-weight: 700;
    font-size: 10pt;
    border: 2px solid transparent;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(59, 130, 246, 0.3), stop:1 rgba(30, 41, 59, 0.9));
    color: #60a5fa;
    border: 2px solid #3b82f6;
    border-bottom: none;
}

QTabBar::tab:hover:!selected {
    background: rgba(30, 41, 59, 0.9);
    color: #e2e8f0;
    border: 2px solid rgba(59, 130, 246, 0.3);
}

/* GroupBox - Modern card style */
QGroupBox {
    border: 2px solid rgba(30, 41, 59, 0.8);
    border-radius: 14px;
    margin-top: 24px;
    padding-top: 24px;
    font-weight: 800;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(30, 41, 59, 0.5), stop:1 rgba(15, 23, 42, 0.7));
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 10px 20px;
    color: #60a5fa;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(59, 130, 246, 0.25), stop:1 rgba(96, 165, 250, 0.25));
    border-radius: 10px;
    border: 2px solid rgba(59, 130, 246, 0.4);
    left: 18px;
    font-size: 12pt;
    font-weight: 800;
    letter-spacing: 0.5px;
}

/* Message Box */
QMessageBox {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0f172a, stop:1 #1e293b);
}

QMessageBox QLabel {
    color: #e2e8f0;
    font-size: 10pt;
}

QMessageBox QPushButton {
    min-width: 100px;
    padding: 10px 20px;
}

/* Scrollbars - Sleek modern design */
QScrollBar:vertical {
    border: none;
    background: rgba(15, 23, 42, 0.6);
    width: 12px;
    margin: 0px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #475569, stop:1 #64748b);
    border-radius: 6px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #64748b, stop:1 #94a3b8);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: rgba(15, 23, 42, 0.6);
    height: 12px;
    margin: 0px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #475569, stop:1 #64748b);
    border-radius: 6px;
    min-width: 40px;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #64748b, stop:1 #94a3b8);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Progress Bar - Modern loading style */
QProgressBar {
    border: 2px solid rgba(30, 41, 59, 0.8);
    border-radius: 12px;
    text-align: center;
    background-color: rgba(15, 23, 42, 0.9);
    color: #e2e8f0;
    height: 28px;
    font-weight: 700;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:0.5 #60a5fa, stop:1 #3b82f6);
    border-radius: 10px;
}

/* Status indicators - Modern badges */
QLabel#statusSuccess {
    color: #10b981;
    font-weight: 800;
    background: rgba(16, 185, 129, 0.15);
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid #10b981;
}

QLabel#statusError {
    color: #ef4444;
    font-weight: 800;
    background: rgba(239, 68, 68, 0.15);
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid #ef4444;
}

QLabel#statusWarning {
    color: #f59e0b;
    font-weight: 800;
    background: rgba(245, 158, 11, 0.15);
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid #f59e0b;
}

QLabel#statusInfo {
    color: #3b82f6;
    font-weight: 800;
    background: rgba(59, 130, 246, 0.15);
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid #3b82f6;
}

/* Blockchain-specific styles */
QLabel#blockHash {
    font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
    color: #a78bfa;
    background: rgba(167, 139, 250, 0.15);
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 9pt;
    font-weight: 600;
}

QLabel#chainLink {
    color: #60a5fa;
    font-size: 24pt;
    font-weight: 900;
}

/* Card style container */
QFrame#card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(30, 41, 59, 0.7), stop:1 rgba(15, 23, 42, 0.9));
    border: 2px solid rgba(30, 41, 59, 0.8);
    border-radius: 14px;
    padding: 24px;
}

QFrame#card:hover {
    border: 2px solid rgba(59, 130, 246, 0.6);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(30, 41, 59, 0.8), stop:1 rgba(15, 23, 42, 1));
}
"""
