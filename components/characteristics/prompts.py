class CharacteristicsManager:
    """Manages AI characteristics, prompts, and behaviors"""
    
    def __init__(self, config):
        self.config = config
        self.base_prompts = {}
        self.personalities = {}
        self.behaviors = {}
        
    async def initialize(self):
        """Load characteristics configurations"""
        # Load from files or database
        self._load_base_prompts()
        self._load_personalities()
        self._load_behaviors()
    
    async def get_profile(self, session_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get complete characteristics profile for interaction"""
        return {
            "system_prompt": self._build_system_prompt(context),
            "personality": self._select_personality(context),
            "behaviors": self._get_active_behaviors(context),
            "fine_tuning_params": self._get_fine_tuning_params()
        }
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build dynamic system prompt based on context"""
        base_prompt = self.base_prompts.get("default", "You are a helpful AI assistant.")
        
        # Add context-specific instructions
        if context.get("user_preferences"):
            base_prompt += f"\n\nUser preferences: {context['user_preferences']}"
        
        return base_prompt
