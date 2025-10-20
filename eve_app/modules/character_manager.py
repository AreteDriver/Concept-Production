"""Character management module for handling multiple EVE Online characters."""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Character:
    """Represents an EVE Online character."""
    
    def __init__(self, character_id: int, name: str, access_token: str = None,
                 refresh_token: str = None, token_expiry: datetime = None):
        """Initialize a character.
        
        Args:
            character_id: Character ID
            name: Character name
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            token_expiry: Token expiration datetime
        """
        self.character_id = character_id
        self.name = name
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = token_expiry
        self.skills = {}
        self.assets = []
        self.orders = []
        self.location = {}
        self.last_updated = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary."""
        return {
            'character_id': self.character_id,
            'name': self.name,
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary."""
        token_expiry = None
        if data.get('token_expiry'):
            token_expiry = datetime.fromisoformat(data['token_expiry'])
        
        char = cls(
            character_id=data['character_id'],
            name=data['name'],
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            token_expiry=token_expiry
        )
        
        if data.get('last_updated'):
            char.last_updated = datetime.fromisoformat(data['last_updated'])
        
        return char
    
    def is_token_valid(self) -> bool:
        """Check if access token is still valid."""
        if not self.access_token or not self.token_expiry:
            return False
        return datetime.utcnow() < self.token_expiry


class CharacterManager:
    """Manages multiple EVE Online characters (up to 100)."""
    
    MAX_CHARACTERS = 100
    
    def __init__(self, storage_path: str = None):
        """Initialize character manager.
        
        Args:
            storage_path: Path to store character data
        """
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 'data', 'characters.json'
            )
        self.storage_path = storage_path
        self.characters: Dict[int, Character] = {}
        self._load_characters()
    
    def _load_characters(self):
        """Load characters from storage."""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for char_data in data.get('characters', []):
                    char = Character.from_dict(char_data)
                    self.characters[char.character_id] = char
            logger.info(f"Loaded {len(self.characters)} characters")
        except Exception as e:
            logger.error(f"Failed to load characters: {e}")
    
    def _save_characters(self):
        """Save characters to storage."""
        try:
            data = {
                'characters': [char.to_dict() for char in self.characters.values()],
                'last_saved': datetime.utcnow().isoformat()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.characters)} characters")
        except Exception as e:
            logger.error(f"Failed to save characters: {e}")
    
    def add_character(self, character: Character) -> bool:
        """Add a character to the manager.
        
        Args:
            character: Character to add
            
        Returns:
            True if added successfully, False otherwise
        """
        if len(self.characters) >= self.MAX_CHARACTERS:
            logger.error(f"Cannot add character: maximum of {self.MAX_CHARACTERS} reached")
            return False
        
        if character.character_id in self.characters:
            logger.warning(f"Character {character.name} already exists, updating")
        
        self.characters[character.character_id] = character
        self._save_characters()
        logger.info(f"Added character: {character.name}")
        return True
    
    def remove_character(self, character_id: int) -> bool:
        """Remove a character from the manager.
        
        Args:
            character_id: Character ID to remove
            
        Returns:
            True if removed successfully, False otherwise
        """
        if character_id not in self.characters:
            logger.warning(f"Character {character_id} not found")
            return False
        
        char = self.characters.pop(character_id)
        self._save_characters()
        logger.info(f"Removed character: {char.name}")
        return True
    
    def get_character(self, character_id: int) -> Optional[Character]:
        """Get a character by ID.
        
        Args:
            character_id: Character ID
            
        Returns:
            Character if found, None otherwise
        """
        return self.characters.get(character_id)
    
    def get_all_characters(self) -> List[Character]:
        """Get all characters.
        
        Returns:
            List of all characters
        """
        return list(self.characters.values())
    
    def get_character_count(self) -> int:
        """Get the number of characters.
        
        Returns:
            Number of characters
        """
        return len(self.characters)
    
    def update_character_data(self, character_id: int, **kwargs):
        """Update character data.
        
        Args:
            character_id: Character ID
            **kwargs: Data to update
        """
        char = self.get_character(character_id)
        if not char:
            logger.warning(f"Character {character_id} not found")
            return
        
        for key, value in kwargs.items():
            if hasattr(char, key):
                setattr(char, key, value)
        
        char.last_updated = datetime.utcnow()
        self._save_characters()
