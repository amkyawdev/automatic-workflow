"""
Vercel API Handler
Entry point for Vercel serverless functions
"""

from src.presentation.app import app

handler = app
