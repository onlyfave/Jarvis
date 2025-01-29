# src/services/brain.py
from typing import List, Dict, Optional
import json
from ..config.settings import Settings
from ..utils.helpers import logger, format_response

class JarvisBrain:
    """
    Core intelligence of Jarvis, powered by Claude API.
    Handles natural language processing and decision making.
    """
    
    def __init__(self, client=None):
        """Initialize the brain with necessary components."""
        if client is None:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=Settings.ANTHROPIC_API_KEY)
        else:
            self.client = client
        
        # Maintain conversation history
        self.conversation_history: List[Dict] = []
        
        # Initialize system prompts
        self.system_prompts = self._initialize_system_prompts()
        
        logger.info("JarvisBrain initialized successfully")

    def _initialize_system_prompts(self) -> List[Dict]:
        """Set up the initial system prompts that define Jarvis's behavior."""
        return [
            {
                "role": "system",
                "content": """You are Jarvis, an advanced personal assistant. Your capabilities include:
                - Managing schedules and tasks
                - Analyzing content and social media performance
                - Providing intelligent recommendations
                - Learning from user preferences and patterns
                
                Always be helpful, concise, and adapt your responses based on context."""
            }
        ]

    def _prepare_messages(self, command: str, context: Optional[Dict]) -> List[Dict]:
        """Prepare the message list for Claude API."""
        messages = self.system_prompts.copy()
        
        # Add conversation history for context
        messages.extend(self.conversation_history[-5:])  # Last 5 messages for context
        
        # Add current command with context if provided
        command_with_context = command
        if context:
            command_with_context = f"Context: {json.dumps(context)}\nCommand: {command}"
        
        messages.append({"role": "user", "content": command_with_context})
        
        return messages

    def _process_response(self, response) -> str:
        """Process Claude's response and extract relevant information."""
        return response.content[0].text

    def _update_conversation_history(self, command: str, response: str) -> None:
        """Update the conversation history with the latest interaction."""
        self.conversation_history.append({"role": "user", "content": command})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Keep conversation history manageable
        if len(self.conversation_history) > 20:  # Keep last 10 interactions
            self.conversation_history = self.conversation_history[-20:]

    def add_to_system_prompt(self, new_prompt: str) -> None:
        """Add new information to system prompts."""
        self.system_prompts.append({
            "role": "system",
            "content": new_prompt
        })
        logger.info("Added new system prompt")

    def clear_conversation_history(self) -> None:
        """Clear the conversation history while maintaining system prompts."""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    async def process_command(self, command: str, context: Optional[Dict] = None) -> Dict:
        """Process user commands using Claude's intelligence."""
        try:
            # Prepare messages for Claude
            messages = self._prepare_messages(command, context)
            
            # Get response from Claude
            response = await self.client.messages.create(
                model=Settings.AI_MODEL,
                messages=messages,
                max_tokens=Settings.AI_MAX_TOKENS
            )
            
            # Process and store the response
            processed_response = self._process_response(response)
            self._update_conversation_history(command, processed_response)
            
            return format_response(
                success=True,
                data={"response": processed_response}
            )
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return format_response(
                success=False,
                error=f"Failed to process command: {str(e)}"
            )
