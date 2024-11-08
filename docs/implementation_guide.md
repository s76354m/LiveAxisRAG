# PowerApps to Python Migration Guide

## 1. Component Mappings

### Screen Controls
```python
# PowerApps Screen
# Screen1:
#   OnVisible: Set(varData, "value")
#   Fill: RGBA(255,255,255,1)

# Python/Flask Implementation
@app.route('/screen1')
def screen1():
    session['var_data'] = 'value'
    return render_template(
        'screen1.html',
        background_color='rgb(255,255,255)'
    )
```

### Form Controls
```python
# PowerApps Form
# Form1:
#   DataSource: Competitors
#   DefaultMode: Edit

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

class CompetitorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    product = SelectField('Product', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product.choices = self.get_product_choices()
        
    def get_product_choices(self):
        return [(p.id, p.name) for p in Product.query.all()]
```

## 2. State Management

### Context Variables
```python
# PowerApps
# UpdateContext({varName: "value"})

from flask import session
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class StateManager:
    def __init__(self):
        self.redis_client = Redis()
        
    def update_context(self, updates: Dict[str, Any]):
        for key, value in updates.items():
            session[key] = value
            # Backup in Redis for persistence
            self.redis_client.hset(
                f"user:{current_user.id}:context",
                key,
                json.dumps(value)
            )
```

## 3. Timer Implementation
```python
# PowerApps
# Timer1:
#   Duration: 5000
#   OnTimerEnd: Set(varComplete, true)

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

class TimerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.active_timers = {}
        
    def start_timer(self, timer_id: str, duration: int, 
                   callback: Callable):
        """
        Start a timer with specified duration
        Args:
            timer_id: Unique timer identifier
            duration: Duration in milliseconds
            callback: Function to call when timer ends
        """
        run_date = datetime.now() + timedelta(milliseconds=duration)
        job = self.scheduler.add_job(
            callback,
            'date',
            run_date=run_date,
            id=timer_id
        )
        self.active_timers[timer_id] = job
        
    def stop_timer(self, timer_id: str):
        """Stop a running timer"""
        if timer_id in self.active_timers:
            self.active_timers[timer_id].remove()
            del self.active_timers[timer_id]
```

## 4. Office 365 Integration
```python
# PowerApps
# Office365Users.MyProfile()
# Office365.SendEmail()

from O365 import Account, Message
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EmailTemplate:
    subject: str
    body: str
    
    def render(self, context: dict) -> tuple[str, str]:
        return (
            self.subject.format(**context),
            self.body.format(**context)
        )

class Office365Service:
    def __init__(self, credentials: dict):
        self.account = Account(credentials)
        self.mailbox = self.account.mailbox()
        self.templates: Dict[str, EmailTemplate] = {}
        
    def send_email(self, 
                   template_name: str,
                   context: dict,
                   to_addresses: List[str],
                   attachments: Optional[List[str]] = None):
        """
        Send email using template
        Args:
            template_name: Name of email template
            context: Template variables
            to_addresses: List of recipient emails
            attachments: Optional list of attachment paths
        """
        template = self.templates[template_name]
        subject, body = template.render(context)
        
        message = self.mailbox.new_message()
        message.subject = subject
        message.body = body
        message.to.add(to_addresses)
        
        if attachments:
            for attachment in attachments:
                message.attachments.add(attachment)
                
        return message.send()
```

## 5. Testing Framework
```python
# Component Validation Tests
def test_competitor_form():
    form = CompetitorForm(
        data={'name': 'Test', 'product': 1}
    )
    assert form.validate()
    
# Integration Tests
def test_office365_integration():
    service = Office365Service(test_credentials)
    result = service.send_email(
        'test_template',
        {'name': 'Test'},
        ['test@example.com']
    )
    assert result.success
    
# Timer Tests
def test_timer_accuracy():
    timer = TimerService()
    start_time = datetime.now()
    completed = False
    
    def on_complete():
        nonlocal completed
        completed = True
        
    timer.start_timer('test', 1000, on_complete)
    time.sleep(1.1)  # Wait slightly longer than timer
    assert completed
    duration = datetime.now() - start_time
    assert 1.0 <= duration.total_seconds() <= 1.2
```

## 6. Migration Steps

1. **Database Migration**
```python
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create new tables
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.String(50), nullable=False),
        sa.Column('status', sa.String(20)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )
    
    # Migrate data
    op.execute("""
        INSERT INTO projects (project_id, status)
        SELECT ProjectID, ProjectStatus 
        FROM powerapp_projects
    """)
```

2. **State Transfer**
```python
def migrate_state():
    """Migrate PowerApps state to Python application"""
    powerapp_state = get_powerapp_state()
    
    # Convert to session variables
    for key, value in powerapp_state.items():
        session[key] = convert_value(value)
        
    # Store in Redis for persistence
    redis_client.hmset(
        f"user:{current_user.id}:state",
        powerapp_state
    )
``` 