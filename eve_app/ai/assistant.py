"""AI assistant for route planning, fitting suggestions, and logistics decisions."""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AIAssistant:
    """AI-powered assistant for EVE Online decision support."""
    
    def __init__(self, openai_api_key: str = None):
        """Initialize AI assistant.
        
        Args:
            openai_api_key: OpenAI API key for advanced features
        """
        self.api_key = openai_api_key
        self.use_openai = openai_api_key is not None
        
        # Ship fitting database (simplified)
        self.fitting_templates = {
            'hauler': {
                'tank': ['Shield Extender', 'Damage Control'],
                'navigation': ['Inertial Stabilizer', 'Nanofiber'],
                'utility': ['Cloak', 'Survey Scanner']
            },
            'combat': {
                'tank': ['Shield Booster', 'Armor Repairer', 'Damage Control'],
                'weapons': ['Guns', 'Missiles', 'Drones'],
                'utility': ['Tackle', 'EWAR', 'Cap Booster']
            },
            'exploration': {
                'scanning': ['Core Scanner Probe', 'Sisters Probe'],
                'tank': ['Shield Extender', 'Damage Control'],
                'utility': ['Cloak', 'Analyzer', 'Salvager']
            }
        }
    
    def suggest_route(self, route_data: Dict[str, Any], 
                     cargo_value: float = 0,
                     urgency: str = 'normal') -> Dict[str, Any]:
        """Provide AI-powered route suggestions.
        
        Args:
            route_data: Route information from route planner
            cargo_value: Estimated cargo value in ISK
            urgency: Urgency level (low, normal, high)
            
        Returns:
            Route suggestion dictionary
        """
        analysis = route_data.get('analysis', {})
        alternatives = route_data.get('alternatives', [])
        
        # Analyze risk vs reward
        danger_level = analysis.get('overall_danger', 'safe')
        dangerous_systems = analysis.get('dangerous_systems', [])
        
        recommendations = []
        
        # High value cargo + dangerous route = suggest alternatives
        if cargo_value > 1_000_000_000 and danger_level in ['dangerous', 'very dangerous']:
            recommendations.append({
                'priority': 'high',
                'type': 'route_change',
                'message': 'High-value cargo detected on dangerous route. Consider safer alternative.',
                'action': 'Use secure route or wait for safer conditions'
            })
            
            # Find safest alternative
            safest = self._find_safest_route(alternatives)
            if safest:
                recommendations.append({
                    'priority': 'medium',
                    'type': 'alternative_route',
                    'message': f'Alternative route available with {safest["analysis"]["total_jumps"]} jumps',
                    'route': safest
                })
        
        # Suggest escort for valuable cargo
        if cargo_value > 5_000_000_000:
            recommendations.append({
                'priority': 'high',
                'type': 'escort',
                'message': 'Extremely valuable cargo. Strongly recommend escort or scout.',
                'action': 'Arrange fleet support or use alt account for scouting'
            })
        
        # Time-based suggestions
        if urgency == 'low' and dangerous_systems:
            recommendations.append({
                'priority': 'low',
                'type': 'timing',
                'message': 'Consider traveling during off-peak hours for reduced risk.',
                'action': 'Schedule trip during low-activity periods (EU/US night)'
            })
        
        # Provide specific system warnings
        for sys in dangerous_systems[:3]:  # Top 3 most dangerous
            recommendations.append({
                'priority': 'medium',
                'type': 'system_warning',
                'message': f"Warning: {sys['name']} has {sys['threat']['recent_kills']} recent kills",
                'system': sys,
                'action': 'Have align-out ready, use cloak if available'
            })
        
        return {
            'overall_assessment': self._assess_route_safety(danger_level, cargo_value),
            'recommendations': recommendations,
            'confidence': 0.85  # Simplified confidence score
        }
    
    def suggest_fitting(self, ship_type: str, purpose: str,
                       budget: float = None) -> Dict[str, Any]:
        """Suggest ship fitting based on purpose.
        
        Args:
            ship_type: Type of ship
            purpose: Ship purpose (hauling, combat, exploration, etc.)
            budget: Budget in ISK
            
        Returns:
            Fitting suggestion dictionary
        """
        purpose_key = purpose.lower()
        if purpose_key not in self.fitting_templates:
            purpose_key = 'combat'  # Default
        
        template = self.fitting_templates[purpose_key]
        
        fitting = {
            'ship': ship_type,
            'purpose': purpose,
            'modules': [],
            'notes': []
        }
        
        # Add modules based on purpose
        for category, modules in template.items():
            fitting['modules'].extend([
                {'category': category, 'module': mod} for mod in modules
            ])
        
        # Add budget-specific notes
        if budget and budget < 100_000_000:
            fitting['notes'].append('Budget fit - prioritize essential modules')
        elif budget and budget > 1_000_000_000:
            fitting['notes'].append('High-budget fit - consider faction/officer modules')
        
        # Add purpose-specific advice
        if purpose_key == 'hauler':
            fitting['notes'].append('Fit for maximum tank and align time')
            fitting['notes'].append('Always use cloak + MWD trick in dangerous space')
        elif purpose_key == 'combat':
            fitting['notes'].append('Balance DPS, tank, and capacitor stability')
        elif purpose_key == 'exploration':
            fitting['notes'].append('Fit cloak for safety in null/wormhole space')
        
        return fitting
    
    def analyze_market_opportunity(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze market orders for trading opportunities.
        
        Args:
            orders: List of market orders
            
        Returns:
            Market analysis dictionary
        """
        if not orders:
            return {'message': 'No active orders to analyze'}
        
        analysis = {
            'total_orders': len(orders),
            'buy_orders': sum(1 for o in orders if o.get('is_buy_order')),
            'sell_orders': sum(1 for o in orders if not o.get('is_buy_order')),
            'total_value': sum(o.get('price', 0) * o.get('volume_remain', 0) for o in orders),
            'recommendations': []
        }
        
        # Check for outdated orders
        analysis['recommendations'].append({
            'type': 'review',
            'message': 'Review and update prices regularly to stay competitive'
        })
        
        return analysis
    
    def provide_logistics_decision(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Provide decision support for logistics operations.
        
        Args:
            situation: Current situation dictionary
            
        Returns:
            Decision support dictionary
        """
        route = situation.get('route', {})
        cargo = situation.get('cargo_value', 0)
        threat = situation.get('threat_level', 'unknown')
        
        decision = {
            'recommendation': 'proceed',
            'confidence': 0.7,
            'reasoning': [],
            'alternative_actions': []
        }
        
        # High threat + high value = abort or wait
        if threat in ['dangerous', 'very dangerous'] and cargo > 1_000_000_000:
            decision['recommendation'] = 'wait_or_reroute'
            decision['confidence'] = 0.9
            decision['reasoning'].append('High risk to valuable cargo')
            decision['alternative_actions'].extend([
                'Wait for safer conditions',
                'Use alternative route',
                'Contract to courier service',
                'Use jump freighter if available'
            ])
        
        # Moderate threat = suggest precautions
        elif threat == 'moderate':
            decision['recommendation'] = 'proceed_with_caution'
            decision['reasoning'].append('Moderate risk detected')
            decision['alternative_actions'].extend([
                'Use scout alt if available',
                'Travel during off-peak hours',
                'Fit for maximum tank'
            ])
        
        return decision
    
    def _find_safest_route(self, alternatives: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find the safest alternative route.
        
        Args:
            alternatives: List of alternative routes
            
        Returns:
            Safest route or None
        """
        if not alternatives:
            return None
        
        # Score routes by safety
        danger_scores = {'safe': 0, 'moderate': 1, 'dangerous': 2, 'very dangerous': 3}
        
        safest = min(alternatives, 
                    key=lambda r: danger_scores.get(
                        r.get('analysis', {}).get('overall_danger', 'safe'), 0
                    ))
        return safest
    
    def _assess_route_safety(self, danger_level: str, cargo_value: float) -> str:
        """Assess overall route safety.
        
        Args:
            danger_level: Danger level of route
            cargo_value: Value of cargo
            
        Returns:
            Assessment string
        """
        if danger_level == 'safe':
            return 'Low risk - proceed normally'
        elif danger_level == 'moderate':
            if cargo_value > 1_000_000_000:
                return 'Moderate risk with valuable cargo - exercise caution'
            return 'Moderate risk - standard precautions advised'
        elif danger_level == 'dangerous':
            if cargo_value > 500_000_000:
                return 'High risk - strongly consider alternatives'
            return 'High risk - proceed with extreme caution'
        else:  # very dangerous
            if cargo_value > 100_000_000:
                return 'Extreme risk - DO NOT proceed without support'
            return 'Extreme risk - only for experienced pilots with proper fits'
