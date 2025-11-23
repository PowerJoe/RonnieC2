"""
Database models for BrowserC2
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models
from .agent import Agent
from .command import Command
from .campaign import Campaign
from .click import Click
from .fingerprint import EnhancedFingerprint
from .cookie import StolenCookie, StolenStorage

__all__ = ['db', 'Agent', 'Command', 'Campaign', 'Click', 'EnhancedFingerprint', 'StolenCookie', 'StolenStorage']
