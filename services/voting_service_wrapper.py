"""
Wrapper for backward compatibility
Allows using VotingServiceEnhanced with existing code
"""
from services.voting_service import VotingService
from services.voting_service_enhanced import VotingServiceEnhanced
from database.db_manager import DatabaseManager
from blockchain.blockchain import Blockchain

class VotingServiceWrapper(VotingService):
    """
    Wrapper that extends VotingService with enhanced features
    Maintains backward compatibility while adding new privacy features
    """
    
    def __init__(self, db_manager: DatabaseManager, blockchain: Blockchain, 
                 use_enhanced: bool = False):
        """
        Initialize wrapper
        
        Args:
            db_manager: Database manager
            blockchain: Blockchain instance
            use_enhanced: If True, use enhanced features (default: False for compatibility)
        """
        # Initialize parent (original VotingService)
        super().__init__(db_manager, blockchain)
        
        # Store enhanced service
        self.use_enhanced = use_enhanced
        if use_enhanced:
            self.enhanced_service = VotingServiceEnhanced(db_manager, blockchain)
            self.enhanced_service.set_privacy_mode('token')  # Default to token mode
            print("🔒 Enhanced voting service enabled (Privacy mode: TOKEN)")
        else:
            self.enhanced_service = None
            print("ℹ️ Using standard voting service (Enhanced features disabled)")
    
    def cast_vote(self, voter, proposal_id: int, election):
        """
        Cast vote - delegates to enhanced service if enabled
        """
        if self.use_enhanced and self.enhanced_service:
            return self.enhanced_service.cast_vote(voter, proposal_id, election)
        else:
            return super().cast_vote(voter, proposal_id, election)
    
    def enable_enhanced_features(self, privacy_mode: str = 'token'):
        """
        Enable enhanced features at runtime
        
        Args:
            privacy_mode: 'token' or 'zkp'
        """
        if not self.enhanced_service:
            self.enhanced_service = VotingServiceEnhanced(self.db_manager, self.blockchain)
        
        self.enhanced_service.set_privacy_mode(privacy_mode)
        self.use_enhanced = True
        print(f"🔒 Enhanced features enabled (Privacy mode: {privacy_mode.upper()})")
    
    def disable_enhanced_features(self):
        """Disable enhanced features (use standard voting)"""
        self.use_enhanced = False
        print("ℹ️ Enhanced features disabled (using standard voting)")
    
    def finalize_election(self, election):
        """Finalize election (only works with enhanced mode)"""
        if self.use_enhanced and self.enhanced_service:
            self.enhanced_service.finalize_election(election)
        else:
            print("⚠️ Finalize election requires enhanced mode")
