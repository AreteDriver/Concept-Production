"""Route planning module with support for jump-capable ships and skill considerations."""

from typing import Dict, List, Optional, Any, Tuple
import logging
import math

logger = logging.getLogger(__name__)


class RoutePlanner:
    """Plans routes for EVE Online considering ship capabilities and pilot skills."""
    
    # Jump drive capable ship types (simplified)
    JUMP_CAPABLE_SHIPS = {
        'titan': {'max_range': 6.0, 'skill': 'Jump Drive Calibration'},
        'supercarrier': {'max_range': 6.0, 'skill': 'Jump Drive Calibration'},
        'carrier': {'max_range': 7.0, 'skill': 'Jump Drive Calibration'},
        'dreadnought': {'max_range': 7.0, 'skill': 'Jump Drive Calibration'},
        'force_auxiliary': {'max_range': 7.0, 'skill': 'Jump Drive Calibration'},
        'jump_freighter': {'max_range': 10.0, 'skill': 'Jump Freighters'},
        'black_ops': {'max_range': 8.0, 'skill': 'Black Ops'}
    }
    
    def __init__(self, esi_client, zkill_client):
        """Initialize route planner.
        
        Args:
            esi_client: ESI API client
            zkill_client: zKillboard API client
        """
        self.esi_client = esi_client
        self.zkill_client = zkill_client
        self.system_cache = {}
        self.threat_cache = {}
    
    def calculate_route(self, origin: int, destination: int, 
                       ship_type: str = 'regular',
                       avoid_dangerous: bool = True,
                       skill_level: int = 5) -> Dict[str, Any]:
        """Calculate route between two systems.
        
        Args:
            origin: Origin system ID
            destination: Destination system ID
            ship_type: Type of ship (regular, carrier, jump_freighter, etc.)
            avoid_dangerous: Whether to avoid dangerous systems
            skill_level: Jump drive skill level (0-5)
            
        Returns:
            Route information dictionary
        """
        # Get basic route from ESI
        flag = 'secure' if avoid_dangerous else 'shortest'
        route = self.esi_client.get_route(origin, destination, flag=flag)
        
        if not route:
            return {
                'success': False,
                'error': 'Could not calculate route',
                'route': []
            }
        
        # Analyze route
        route_analysis = self._analyze_route(route)
        
        # Check if ship has jump capability
        jump_info = None
        if ship_type.lower() in self.JUMP_CAPABLE_SHIPS:
            jump_info = self._calculate_jump_route(origin, destination, 
                                                   ship_type, skill_level)
        
        return {
            'success': True,
            'origin': origin,
            'destination': destination,
            'ship_type': ship_type,
            'gate_route': route,
            'jump_route': jump_info,
            'analysis': route_analysis,
            'alternatives': self._find_alternative_routes(origin, destination, route)
        }
    
    def _analyze_route(self, route: List[int]) -> Dict[str, Any]:
        """Analyze a route for threats and statistics.
        
        Args:
            route: List of system IDs
            
        Returns:
            Route analysis dictionary
        """
        total_jumps = len(route) - 1
        dangerous_systems = []
        security_stats = {'highsec': 0, 'lowsec': 0, 'nullsec': 0, 'wormhole': 0}
        
        for system_id in route:
            # Get system info
            system_info = self._get_system_info(system_id)
            security = system_info.get('security_status', 0)
            
            # Categorize security
            if security >= 0.5:
                security_stats['highsec'] += 1
            elif security > 0.0:
                security_stats['lowsec'] += 1
            elif security <= 0.0:
                security_stats['nullsec'] += 1
            
            # Check threats in low/null sec
            if security < 0.5:
                threat = self._get_system_threat(system_id)
                if threat['danger_level'] in ['dangerous', 'very dangerous']:
                    dangerous_systems.append({
                        'system_id': system_id,
                        'name': system_info.get('name', 'Unknown'),
                        'threat': threat
                    })
        
        return {
            'total_jumps': total_jumps,
            'security_stats': security_stats,
            'dangerous_systems': dangerous_systems,
            'overall_danger': self._calculate_overall_danger(dangerous_systems)
        }
    
    def _calculate_jump_route(self, origin: int, destination: int,
                             ship_type: str, skill_level: int) -> Dict[str, Any]:
        """Calculate jump drive route for capital ships.
        
        Args:
            origin: Origin system ID
            destination: Destination system ID
            ship_type: Ship type with jump capability
            skill_level: Jump drive skill level
            
        Returns:
            Jump route information
        """
        ship_config = self.JUMP_CAPABLE_SHIPS.get(ship_type.lower(), {})
        base_range = ship_config.get('max_range', 5.0)
        
        # Calculate actual range based on skill
        actual_range = base_range * (1 + (skill_level * 0.2))
        
        # Get system positions (would need actual system coordinate data)
        # This is simplified - real implementation would calculate based on coordinates
        
        return {
            'available': True,
            'ship_type': ship_type,
            'max_range_ly': actual_range,
            'skill_level': skill_level,
            'estimated_jumps': 'Variable based on cyno chain',
            'note': 'Requires cyno beacons or player cynos at midpoints'
        }
    
    def _find_alternative_routes(self, origin: int, destination: int,
                                current_route: List[int]) -> List[Dict[str, Any]]:
        """Find alternative routes.
        
        Args:
            origin: Origin system ID
            destination: Destination system ID
            current_route: Current route to compare against
            
        Returns:
            List of alternative routes
        """
        alternatives = []
        
        # Try different route flags
        for flag in ['shortest', 'secure', 'insecure']:
            alt_route = self.esi_client.get_route(origin, destination, flag=flag)
            if alt_route and alt_route != current_route:
                analysis = self._analyze_route(alt_route)
                alternatives.append({
                    'route': alt_route,
                    'type': flag,
                    'analysis': analysis
                })
        
        return alternatives
    
    def _get_system_info(self, system_id: int) -> Dict[str, Any]:
        """Get cached or fetch system information.
        
        Args:
            system_id: System ID
            
        Returns:
            System information dictionary
        """
        if system_id not in self.system_cache:
            self.system_cache[system_id] = self.esi_client.get_system_info(system_id)
        return self.system_cache[system_id]
    
    def _get_system_threat(self, system_id: int) -> Dict[str, Any]:
        """Get cached or fetch system threat analysis.
        
        Args:
            system_id: System ID
            
        Returns:
            Threat analysis dictionary
        """
        if system_id not in self.threat_cache:
            self.threat_cache[system_id] = self.zkill_client.analyze_system_threat(system_id)
        return self.threat_cache[system_id]
    
    def _calculate_overall_danger(self, dangerous_systems: List[Dict]) -> str:
        """Calculate overall danger level for route.
        
        Args:
            dangerous_systems: List of dangerous systems in route
            
        Returns:
            Overall danger level string
        """
        if not dangerous_systems:
            return 'safe'
        
        very_dangerous = sum(1 for s in dangerous_systems 
                           if s['threat']['danger_level'] == 'very dangerous')
        
        if very_dangerous > 0:
            return 'very dangerous'
        elif len(dangerous_systems) > 3:
            return 'dangerous'
        else:
            return 'moderate'
    
    def get_2d_map_data(self, route: List[int]) -> Dict[str, Any]:
        """Get 2D map visualization data for a route.
        
        Args:
            route: List of system IDs
            
        Returns:
            Map data dictionary with system positions and connections
        """
        systems = []
        connections = []
        
        for i, system_id in enumerate(route):
            system_info = self._get_system_info(system_id)
            threat = self._get_system_threat(system_id)
            
            systems.append({
                'id': system_id,
                'name': system_info.get('name', f'System {system_id}'),
                'security': system_info.get('security_status', 0),
                'danger_level': threat['danger_level'],
                'position': i,  # Simplified positioning
                # Real implementation would use actual coordinates
                'x': i * 100,  # Placeholder
                'y': system_info.get('security_status', 0) * 100  # Placeholder
            })
            
            if i > 0:
                connections.append({
                    'from': route[i-1],
                    'to': system_id,
                    'type': 'gate'
                })
        
        return {
            'systems': systems,
            'connections': connections,
            'total_systems': len(systems)
        }
