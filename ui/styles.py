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
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #e2e8f0;
}

/* Buttons - Blockchain style with glow effect */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:1 #2563eb);
    color: white;
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 10pt;
    min-width: 120px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:1 #3b82f6);
    border: 1px solid rgba(96, 165, 250, 0.5);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2563eb, stop:1 #1e40af);
    padding: 13px 23px 11px 25px;
}

QPushButton:disabled {
    background: #1e293b;
    color: #475569;
    border: 1px solid #334155;
}

/* Success Button - Green blockchain style */
QPushButton#successButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #10b981, stop:1 #059669);
    border: 1px solid rgba(16, 185, 129, 0.3);
}

QPushButton#successButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #34d399, stop:1 #10b981);
    border: 1px solid rgba(52, 211, 153, 0.5);
}

QPushButton#successButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #059669, stop:1 #047857);
}

/* Danger Button - Red blockchain style */
QPushButton#dangerButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #ef4444, stop:1 #dc2626);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

QPushButton#dangerButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f87171, stop:1 #ef4444);
    border: 1px solid rgba(248, 113, 113, 0.5);
}

QPushButton#dangerButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #dc2626, stop:1 #b91c1c);
}

/* Warning Button - Orange blockchain style */
QPushButton#warningButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #f59e0b, stop:1 #d97706);
    border: 1px solid rgba(245, 158, 11, 0.3);
}

QPushButton#warningButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #fbbf24, stop:1 #f59e0b);
    border: 1px solid rgba(251, 191, 36, 0.5);
}

/* Secondary Button - Outlined style */
QPushButton#secondaryButton {
    background: transparent;
    border: 2px solid #3b82f6;
    color: #60a5fa;
}

QPushButton#secondaryButton:hover {
    background: rgba(59, 130, 246, 0.1);
    border: 2px solid #60a5fa;
}

/* Input Fields - Blockchain style with glow */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    padding: 12px 16px;
    border: 2px solid #1e293b;
    border-radius: 10px;
    background-color: rgba(15, 23, 42, 0.8);
    color: #e2e8f0;
    selection-background-color: #3b82f6;
    font-size: 10pt;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #3b82f6;
    background-color: rgba(15, 23, 42, 0.95);
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #60a5fa;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 2px solid #3b82f6;
    border-radius: 8px;
    color: #e2e8f0;
    selection-background-color: #3b82f6;
    padding: 5px;
}

/* Labels - Enhanced typography */
QLabel {
    color: #e2e8f0;
}

QLabel#titleLabel {
    font-size: 32pt;
    font-weight: 800;
    color: transparent;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #60a5fa, stop:0.5 #a78bfa, stop:1 #ec4899);
    -webkit-background-clip: text;
    padding: 20px 0;
}

QLabel#subtitleLabel {
    font-size: 18pt;
    font-weight: 700;
    color: #60a5fa;
    padding: 15px 0;
    letter-spacing: 0.5px;
}

QLabel#infoLabel {
    color: #94a3b8;
    font-size: 10pt;
    line-height: 1.6;
}

QLabel#valueLabel {
    color: #f1f5f9;
    font-size: 11pt;
    font-weight: 600;
    padding: 8px 0;
}

QLabel#blockchainLabel {
    color: #60a5fa;
    font-size: 12pt;
    font-weight: 700;
    font-family: 'Courier New', monospace;
    background: rgba(59, 130, 246, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #3b82f6;
}

/* Tables - Blockchain grid style */
QTableWidget {
    background-color: rgba(15, 23, 42, 0.6);
    border: 2px solid #1e293b;
    border-radius: 12px;
    gridline-color: #1e293b;
    color: #e2e8f0;
    selection-background-color: rgba(59, 130, 246, 0.3);
    alternate-background-color: rgba(30, 41, 59, 0.3);
}

QTableWidget::item {
    padding: 14px 10px;
    border-bottom: 1px solid rgba(51, 65, 85, 0.5);
}

QTableWidget::item:selected {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(59, 130, 246, 0.4), stop:1 rgba(96, 165, 250, 0.4));
    color: #ffffff;
    font-weight: 600;
    border-left: 3px solid #3b82f6;
}

QTableWidget::item:hover {
    background-color: rgba(59, 130, 246, 0.15);
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e293b, stop:1 #0f172a);
    color: #60a5fa;
    padding: 14px 12px;
    border: none;
    border-bottom: 2px solid #3b82f6;
    font-weight: 700;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 1px;
}

QHeaderView::section:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #334155, stop:1 #1e293b);
}

/* Tabs - Blockchain style */
QTabWidget::pane {
    border: 2px solid #1e293b;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(15, 23, 42, 0.8), stop:1 rgba(30, 41, 59, 0.6));
    border-radius: 12px;
    padding: 10px;
}

QTabBar::tab {
    background: rgba(15, 23, 42, 0.6);
    color: #94a3b8;
    padding: 14px 28px;
    margin-right: 6px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: 600;
    font-size: 10pt;
    border: 2px solid transparent;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1e293b, stop:1 rgba(30, 41, 59, 0.8));
    color: #60a5fa;
    border: 2px solid #3b82f6;
    border-bottom: none;
}

QTabBar::tab:hover:!selected {
    background: rgba(30, 41, 59, 0.8);
    color: #e2e8f0;
    border: 2px solid #334155;
}

/* GroupBox - Card style */
QGroupBox {
    border: 2px solid #1e293b;
    border-radius: 12px;
    margin-top: 20px;
    padding-top: 20px;
    font-weight: 700;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(30, 41, 59, 0.4), stop:1 rgba(15, 23, 42, 0.6));
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 8px 16px;
    color: #60a5fa;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 rgba(59, 130, 246, 0.2), stop:1 rgba(96, 165, 250, 0.2));
    border-radius: 8px;
    border: 1px solid rgba(59, 130, 246, 0.3);
    left: 15px;
    font-size: 11pt;
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

/* Scrollbars - Sleek design */
QScrollBar:vertical {
    border: none;
    background: rgba(15, 23, 42, 0.5);
    width: 10px;
    margin: 0px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #334155, stop:1 #475569);
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #475569, stop:1 #64748b);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: rgba(15, 23, 42, 0.5);
    height: 10px;
    margin: 0px;
    border-radius: 5px;
}

QScrollBar::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #334155, stop:1 #475569);
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #475569, stop:1 #64748b);
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0px;
}

/* Progress Bar - Blockchain loading style */
QProgressBar {
    border: 2px solid #1e293b;
    border-radius: 10px;
    text-align: center;
    background-color: rgba(15, 23, 42, 0.8);
    color: #e2e8f0;
    height: 24px;
    font-weight: 600;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3b82f6, stop:0.5 #60a5fa, stop:1 #3b82f6);
    border-radius: 8px;
}

/* Status indicators */
QLabel#statusSuccess {
    color: #10b981;
    font-weight: 700;
    background: rgba(16, 185, 129, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #10b981;
}

QLabel#statusError {
    color: #ef4444;
    font-weight: 700;
    background: rgba(239, 68, 68, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #ef4444;
}

QLabel#statusWarning {
    color: #f59e0b;
    font-weight: 700;
    background: rgba(245, 158, 11, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #f59e0b;
}

QLabel#statusInfo {
    color: #3b82f6;
    font-weight: 700;
    background: rgba(59, 130, 246, 0.1);
    padding: 8px 12px;
    border-radius: 6px;
    border-left: 3px solid #3b82f6;
}

/* Blockchain-specific styles */
QLabel#blockHash {
    font-family: 'Courier New', 'Consolas', monospace;
    color: #a78bfa;
    background: rgba(167, 139, 250, 0.1);
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 9pt;
}

QLabel#chainLink {
    color: #60a5fa;
    font-size: 20pt;
    font-weight: 900;
}

/* Card style container */
QFrame#card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(30, 41, 59, 0.6), stop:1 rgba(15, 23, 42, 0.8));
    border: 2px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
}

QFrame#card:hover {
    border: 2px solid rgba(59, 130, 246, 0.5);
}
"""
