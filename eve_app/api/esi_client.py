"""EVE ESI API Client for fetching character and game data."""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ESIClient:
    """Client for EVE Online ESI API."""
    
    BASE_URL = "https://esi.evetech.net/latest"
    OAUTH_URL = "https://login.eveonline.com/v2/oauth"
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        """Initialize ESI client with optional OAuth credentials.
        
        Args:
            client_id: EVE application client ID
            client_secret: EVE application client secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EVE-Neocom-2.0/2.0.0',
            'Accept': 'application/json'
        })
    
    def get_character_info(self, character_id: int) -> Dict[str, Any]:
        """Get character public information.
        
        Args:
            character_id: Character ID
            
        Returns:
            Character information dictionary
        """
        try:
            url = f"{self.BASE_URL}/characters/{character_id}/"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character info: {e}")
            return {}
    
    def get_character_skills(self, character_id: int, access_token: str) -> Dict[str, Any]:
        """Get character skills (requires authentication).
        
        Args:
            character_id: Character ID
            access_token: OAuth access token
            
        Returns:
            Character skills dictionary
        """
        try:
            url = f"{self.BASE_URL}/characters/{character_id}/skills/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character skills: {e}")
            return {}
    
    def get_character_assets(self, character_id: int, access_token: str) -> List[Dict[str, Any]]:
        """Get character assets (requires authentication).
        
        Args:
            character_id: Character ID
            access_token: OAuth access token
            
        Returns:
            List of asset dictionaries
        """
        try:
            url = f"{self.BASE_URL}/characters/{character_id}/assets/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character assets: {e}")
            return []
    
    def get_character_orders(self, character_id: int, access_token: str) -> List[Dict[str, Any]]:
        """Get character market orders (requires authentication).
        
        Args:
            character_id: Character ID
            access_token: OAuth access token
            
        Returns:
            List of market order dictionaries
        """
        try:
            url = f"{self.BASE_URL}/characters/{character_id}/orders/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character orders: {e}")
            return []
    
    def get_character_location(self, character_id: int, access_token: str) -> Dict[str, Any]:
        """Get character current location (requires authentication).
        
        Args:
            character_id: Character ID
            access_token: OAuth access token
            
        Returns:
            Location information dictionary
        """
        try:
            url = f"{self.BASE_URL}/characters/{character_id}/location/"
            headers = {'Authorization': f'Bearer {access_token}'}
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character location: {e}")
            return {}
    
    def get_system_info(self, system_id: int) -> Dict[str, Any]:
        """Get solar system information.
        
        Args:
            system_id: Solar system ID
            
        Returns:
            System information dictionary
        """
        try:
            url = f"{self.BASE_URL}/universe/systems/{system_id}/"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get system info: {e}")
            return {}
    
    def get_route(self, origin: int, destination: int, 
                  flag: str = "shortest") -> List[int]:
        """Get route between two systems.
        
        Args:
            origin: Origin system ID
            destination: Destination system ID
            flag: Route type (shortest, secure, insecure)
            
        Returns:
            List of system IDs forming the route
        """
        try:
            url = f"{self.BASE_URL}/route/{origin}/{destination}/"
            params = {'flag': flag}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get route: {e}")
            return []
    
    def search(self, search_term: str, categories: List[str]) -> Dict[str, Any]:
        """Search for items, systems, etc.
        
        Args:
            search_term: Search query
            categories: Categories to search (e.g., ['solar_system', 'station'])
            
        Returns:
            Search results dictionary
        """
        try:
            url = f"{self.BASE_URL}/search/"
            params = {
                'search': search_term,
                'categories': ','.join(categories),
                'strict': 'false'
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to search: {e}")
            return {}
