# Controls Overview and Screen Navigation

## Screen: CompetitorEntryScreen

### Controls List
```python
class CompetitorEntryScreen(FlaskForm):
    """Maps PowerApps CompetitorEntryScreen controls"""
    
    # Button Controls
    btnAdd = SubmitField('Add')
    btnCompLoad = SubmitField('Load')
    btnFinished = SubmitField('Finished')
    
    # Dropdown Control
    ddCompetitorProduct = SelectField(
        'Competitor Product',
        validators=[DataRequired()]
    )
    
    # Progress Controls
    progress_indicator = IntegerField(
        default=0,
        render_kw={'type': 'range', 'max': 100}
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_competitor_products()
    
    def load_competitor_products(self):
        """Load dropdown options from CS_EXP_Sel_PLProducts"""
        products = PlatformLoadProduct.query.filter_by(
            is_active=True
        ).all()
        self.ddCompetitorProduct.choices = [
            (p.id, p.name) for p in products
        ]
```

## Screen: CSPLOBMappingScreen
```python
class CSPLOBMappingScreen(FlaskForm):
    """Maps PowerApps CSPLOBMappingScreen controls"""
    
    # Header Controls
    header_text = StringField(
        default='CSP LOB Mapping',
        render_kw={'readonly': True}
    )
    
    # Grid Controls
    mapping_grid = GridField(
        model=CSPLOBMapping,
        columns=['lob', 'csp_product', 'status']
    )
```

## Screen Navigation Implementation
```python
from flask import Blueprint, redirect, url_for

screens_bp = Blueprint('screens', __name__)

@screens_bp.route('/competitor-entry')
def competitor_entry():
    """Maps to CompetitorEntryScreen"""
    form = CompetitorEntryScreen()
    return render_template(
        'competitor_entry.html',
        form=form
    )

@screens_bp.route('/success-competitor')
def success_competitor():
    """Maps to SuccessScreenCompetitorData"""
    return render_template('success_competitor.html')

# Navigation Service
class NavigationService:
    """Maps PowerApps Navigation functions"""
    
    @staticmethod
    def navigate(screen_name: str, params: dict = None):
        """Maps to Navigate() function"""
        if params:
            session['nav_params'] = params
        return redirect(url_for(f'screens.{screen_name}'))
```

## Detailed Controls Implementation

### Screen Properties
```python
class ScreenProperties:
    """Maps PowerApps screen properties"""
    
    def __init__(self):
        self.height = 1136
        self.width = 800
        self.fill = "#FFFFFF"
        self.image_position = "stretch"
        self.loading_spinner_color = "#000000"
        
    @property
    def template_vars(self):
        return {
            'height': f"{self.height}px",
            'width': f"{self.width}px",
            'background_color': self.fill,
            'background_size': 'cover'
        }
```

### Control Types
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ControlProperties:
    """Maps PowerApps control properties"""
    
    # Design Properties
    height: int
    width: int
    x: int
    y: int
    border_style: str = "None"
    border_thickness: int = 0
    font_weight: str = "Normal"
    
    # Color Properties
    fill: str = "#FFFFFF"
    border_color: str = "#000000"
    hover_fill: str = "#E6E6E6"
    
    # Behavior Properties
    visible: bool = True
    disabled: bool = False
    
    def get_style(self) -> dict:
        """Convert to CSS style"""
        return {
            'height': f"{self.height}px",
            'width': f"{self.width}px",
            'position': 'absolute',
            'left': f"{self.x}px",
            'top': f"{self.y}px",
            'background-color': self.fill,
            'border': f"{self.border_thickness}px {self.border_style} {self.border_color}",
            'font-weight': self.font_weight,
            'display': 'block' if self.visible else 'none',
            'opacity': '0.5' if self.disabled else '1'
        }
```

### Form Implementation
```python
class BaseScreenForm(FlaskForm):
    """Base form with common PowerApps screen properties"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen_props = ScreenProperties()
        self.controls = {}
        self.setup_controls()
    
    def setup_controls(self):
        """Setup screen-specific controls"""
        pass
    
    def get_control_style(self, control_name: str) -> dict:
        """Get control-specific styles"""
        if control_name in self.controls:
            return self.controls[control_name].get_style()
        return {}
```

### Timer Implementation
```python
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

class TimerControl:
    """Maps PowerApps Timer control"""
    
    def __init__(self, duration: int, repeat: bool = False):
        self.scheduler = BackgroundScheduler()
        self.duration = duration
        self.repeat = repeat
        self.active = False
        
    def start(self, callback: callable):
        """Start timer"""
        if self.repeat:
            self.scheduler.add_job(
                callback,
                'interval',
                seconds=self.duration/1000,
                id='timer_job'
            )
        else:
            self.scheduler.add_job(
                callback,
                'date',
                run_date=datetime.now() + timedelta(
                    milliseconds=self.duration
                ),
                id='timer_job'
            )
        self.active = True
        
    def stop(self):
        """Stop timer"""
        self.scheduler.remove_job('timer_job')
        self.active = False
``` 