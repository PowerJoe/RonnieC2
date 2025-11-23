"""
Route blueprints for BrowserC2
"""
from .main import main_bp
from .agents import agents_bp
from .commands import commands_bp
from .campaigns import campaigns_bp
from .stats import stats_bp

__all__ = [
    'main_bp',
    'agents_bp', 
    'commands_bp',
    'campaigns_bp',
    'stats_bp'
]
