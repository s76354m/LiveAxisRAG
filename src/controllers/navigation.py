from flask import Blueprint, redirect, url_for, session
from .navigation_manager import NavigationManager

nav_bp = Blueprint('navigation', __name__)

@nav_bp.route('/navigate/<to_screen>')
def navigate(to_screen: str):
    """Handle screen navigation"""
    current_screen = session.get('current_screen', 'EntryScreen')
    
    if NavigationManager.can_navigate(current_screen, to_screen):
        session['current_screen'] = to_screen
        return redirect(url_for(f'screens.{to_screen.lower()}'))
    
    return redirect(url_for('screens.error', 
                          message="Invalid navigation path")) 