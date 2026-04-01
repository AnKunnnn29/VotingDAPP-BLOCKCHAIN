"""Constants for the voting DApp"""

# Election states following smart contract state machine
class ElectionState:
    START = "Start"
    VALIDATE_VOTER = "ValidateVoter"
    VOTE = "Vote"
    COUNT = "Count"
    DECLARE_WINNER = "DeclareWinner"
    DONE = "Done"

# Blockchain modes
class BlockchainMode:
    PERMISSIONLESS = "Permissionless"
    PERMISSIONED = "Permissioned"

# User roles
class UserRole:
    VOTER = "Voter"
    ADMIN = "Admin"

# Colors for modern UI
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#BBDEFB',
    'accent': '#FF4081',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'divider': '#BDBDBD'
}
