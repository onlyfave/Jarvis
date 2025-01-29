# src/utils/helpers.py
import logging
from datetime import datetime
from typing import Any, Dict

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_response(success: bool, data: Any = None, error: str = None) -> Dict:
    """Format a standardized API response."""
    return {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data if data is not None else {},
        "error": error if error is not None else ""
    }

def log_command(command: str, user_id: str = "default") -> None:
    """Log user commands for analysis."""
    logger.info(f"User {user_id} executed command: {command}")

def validate_command(command: str) -> bool:
    """Validate if a command is properly formatted."""
    if not command or not isinstance(command, str):
        return False
    if len(command.strip()) == 0:
        return False
    return True

def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    # Remove any potentially harmful characters
    # This is a basic implementation - expand based on needs
    return text.strip()
