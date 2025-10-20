"""zKillboard API Client for fetching kill data and threat assessment."""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ZKillboardClient:
    """Client for zKillboard API."""
    
    BASE_URL = "https://zkillboard.com/api"
    
    def __init__(self):
        """Initialize zKillboard client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EVE-Neocom-2.0/2.0.0',
            'Accept': 'application/json'
        })
    
    def get_system_kills(self, system_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent kills in a solar system.
        
        Args:
            system_id: Solar system ID
            limit: Maximum number of kills to retrieve
            
        Returns:
            List of kill dictionaries
        """
        try:
            url = f"{self.BASE_URL}/kills/solarSystemID/{system_id}/"
            params = {'limit': limit}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get system kills: {e}")
            return []
    
    def get_character_kills(self, character_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent kills for a character.
        
        Args:
            character_id: Character ID
            limit: Maximum number of kills to retrieve
            
        Returns:
            List of kill dictionaries
        """
        try:
            url = f"{self.BASE_URL}/kills/characterID/{character_id}/"
            params = {'limit': limit}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get character kills: {e}")
            return []
    
    def get_system_stats(self, system_id: int) -> Dict[str, Any]:
        """Get kill statistics for a solar system.
        
        Args:
            system_id: Solar system ID
            
        Returns:
            Statistics dictionary including kill counts and danger level
        """
        try:
            url = f"{self.BASE_URL}/stats/solarSystemID/{system_id}/"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get system stats: {e}")
            return {}
    
    def analyze_system_threat(self, system_id: int, hours: int = 24) -> Dict[str, Any]:
        """Analyze threat level in a system based on recent activity.
        
        Args:
            system_id: Solar system ID
            hours: Time window in hours to analyze
            
        Returns:
            Threat analysis dictionary with danger level and active gankers
        """
        kills = self.get_system_kills(system_id, limit=100)
        
        if not kills:
            return {
                'system_id': system_id,
                'danger_level': 'safe',
                'recent_kills': 0,
                'active_gankers': [],
                'pod_kills': 0,
                'total_value_lost': 0
            }
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_kills = []
        gankers = {}
        pod_kills = 0
        total_value = 0
        
        for kill in kills:
            kill_time = datetime.strptime(kill['killmail_time'], '%Y-%m-%dT%H:%M:%SZ')
            if kill_time >= cutoff_time:
                recent_kills.append(kill)
                
                # Count pod kills
                if kill.get('victim', {}).get('ship_type_id') == 670:  # Capsule
                    pod_kills += 1
                
                # Track total ISK lost
                total_value += kill.get('zkb', {}).get('totalValue', 0)
                
                # Track attackers (potential gankers)
                for attacker in kill.get('attackers', []):
                    char_id = attacker.get('character_id')
                    if char_id:
                        gankers[char_id] = gankers.get(char_id, 0) + 1
        
        # Sort gankers by activity
        top_gankers = sorted(gankers.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Determine danger level
        if len(recent_kills) > 20 or pod_kills > 5:
            danger_level = 'very dangerous'
        elif len(recent_kills) > 10 or pod_kills > 2:
            danger_level = 'dangerous'
        elif len(recent_kills) > 5:
            danger_level = 'moderate'
        else:
            danger_level = 'safe'
        
        return {
            'system_id': system_id,
            'danger_level': danger_level,
            'recent_kills': len(recent_kills),
            'active_gankers': [{'character_id': gid, 'kills': count} 
                             for gid, count in top_gankers],
            'pod_kills': pod_kills,
            'total_value_lost': total_value,
            'analysis_period_hours': hours
        }
