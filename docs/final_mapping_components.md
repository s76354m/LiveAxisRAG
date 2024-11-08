# Complete PowerApps to Python Mapping

## 1. Remaining Data Sources

### uspCsExpProjectServiceAreaV2
```python
class ServiceAreaRepository:
    """Maps uspCsExpProjectServiceAreaV2 stored procedure"""
    
    def __init__(self, db_session):
        self.session = db_session
    
    def get_service_areas(self, project_id: str) -> List[dict]:
        result = self.session.execute(
            text("EXEC uspCsExpProjectServiceAreaV2 :project_id"),
            {'project_id': project_id}
        )
        return [dict(row) for row in result]
```

### Office365Users Integration
```python
class Office365Integration:
    """Maps Office365Users data source"""
    
    def __init__(self, credentials):
        self.account = Account(credentials)
    
    def get_current_user(self) -> dict:
        """Maps to Office365Users.MyProfileV2()"""
        profile = self.account.get_current_user()
        return {
            'mail': profile.mail,
            'display_name': profile.display_name,
            'id': profile.object_id
        }
```

## 2. Remaining Screen Controls

### NotesEntryScreen
```python
class NotesEntryScreen(BaseScreenForm):
    """Maps PowerApps NotesEntryScreen"""
    
    class NotesForm(FlaskForm):
        category = SelectField(
            'Category',
            choices=[],
            validators=[DataRequired()]
        )
        note_text = TextAreaField(
            'Note',
            validators=[DataRequired(), Length(max=1000)]
        )
        
    def setup_controls(self):
        self.controls = {
            'ddCategory': ControlProperties(
                height=40,
                width=300,
                x=20,
                y=100
            ),
            'txtNote': ControlProperties(
                height=200,
                width=600,
                x=20,
                y=160,
                border_style="Solid"
            ),
            'btnSave': ControlProperties(
                height=40,
                width=100,
                x=20,
                y=380,
                fill="#0078D4"
            )
        }
```

## 3. Complete Navigation Flow

```python
class NavigationConfig:
    """Complete navigation configuration"""
    
    SCREEN_FLOW = {
        'EntryScreen': {
            'next': ['NewProjectScreen', 'EditProjectScreen'],
            'back': None,
            'controls': ['btnNew', 'btnEdit']
        },
        'NewProjectScreen': {
            'next': ['SuccessScreenNewProject'],
            'back': 'EntryScreen',
            'controls': ['btnSave', 'btnCancel']
        },
        'EditProjectScreen': {
            'next': ['SuccessScreenEditProject'],
            'back': 'EntryScreen',
            'controls': ['btnSave', 'btnCancel']
        },
        'CompetitorEntryScreen': {
            'next': ['SuccessScreenCompetitorData'],
            'back': 'YLineScreen',
            'controls': ['btnAdd', 'btnFinished']
        },
        'NotesEntryScreen': {
            'next': ['EntryScreen'],
            'back': 'EntryScreen',
            'controls': ['btnSave', 'btnCancel']
        }
    }
```

## 4. Complete Variable Mapping

```python
class StateManager:
    """Maps all PowerApps variables"""
    
    def __init__(self):
        self.session = session
        
    def initialize_state(self):
        """Initialize all required state variables"""
        self.session['varGridEdit'] = False
        self.session['varProjectTranslation'] = None
        self.session['varExistingProjectsScreenFormData'] = None
        self.session['varEditProject'] = False
        self.session['varmsid'] = None
        self.session['CurrentStep'] = 0
        self.session['TotalSteps'] = 10
        self.session['TimerRunning'] = True
        
    def update_context(self, updates: dict):
        """Update multiple context variables"""
        for key, value in updates.items():
            self.session[key] = value
```

## 5. Timer Implementation

```python
class TimerManager:
    """Maps PowerApps timer functionality"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.active_timers = {}
    
    def start_progress_timer(self):
        """Maps to Timer1 in PowerApps"""
        def update_progress():
            current = session.get('CurrentStep', 0)
            total = session.get('TotalSteps', 10)
            
            if current < total:
                session['CurrentStep'] = current + 1
            else:
                self.stop_timer('progress')
        
        self.scheduler.add_job(
            update_progress,
            'interval',
            seconds=0.5,
            id='progress'
        )
        
    def stop_timer(self, timer_id: str):
        """Stop specific timer"""
        if timer_id in self.scheduler.get_jobs():
            self.scheduler.remove_job(timer_id)
```

## 6. Complete Form Validation

```python
class ValidationManager:
    """Maps PowerApps validation rules"""
    
    @staticmethod
    def validate_project_id(project_id: str) -> bool:
        if not project_id or len(project_id) != 12:
            raise ValidationError("Project ID must be 12 characters")
        
        if not project_id.isalnum():
            raise ValidationError("Project ID must be alphanumeric")
        
        return True
    
    @staticmethod
    def validate_competitor_entry(form_data: dict) -> bool:
        required_fields = ['product', 'status']
        
        for field in required_fields:
            if not form_data.get(field):
                raise ValidationError(f"{field} is required")
        
        return True
``` 