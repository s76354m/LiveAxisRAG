# PowerApps to Python Complete Mapping Report

## 1. Data Sources Implementation

### Database Models
```python
from datetime import datetime
from sqlalchemy import Enum, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, onupdate=datetime.utcnow)
    created_by = db.Column(String(100))

# CS_EXP_Project_Translation
class ProjectTranslation(BaseModel):
    __tablename__ = 'cs_exp_project_translation'
    
    id = db.Column(Integer, primary_key=True)
    project_id = db.Column(String(12), unique=True, nullable=False)
    name = db.Column(String(200))
    status = db.Column(String(50))
    region = db.Column(String(100))
    is_active = db.Column(Boolean, default=True)

# CS_EXP_Competitor_Translation
class CompetitorTranslation(BaseModel):
    __tablename__ = 'cs_exp_competitor_translation'
    
    id = db.Column(Integer, primary_key=True)
    project_id = db.Column(String(12), ForeignKey('cs_exp_project_translation.project_id'))
    product_id = db.Column(Integer, ForeignKey('cs_exp_platform_load_products.id'))
    status = db.Column(String(50))
    project = relationship('ProjectTranslation', backref='competitors')

# CS_EXP_PlatformLoadProducts
class PlatformLoadProduct(BaseModel):
    __tablename__ = 'cs_exp_platform_load_products'
    
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200))
    category = db.Column(String(100))
    is_active = db.Column(Boolean, default=True)
```

### Service Layer Implementation
```python
from typing import Optional, List
from datetime import datetime

class ProjectService:
    def __init__(self):
        self.workflow_id = '473be22f-b755-ef11-a317-000d3a114ae5'
    
    def check_project_id(self, project_id: str) -> bool:
        """Maps to CheckProjectID PowerApp datasource"""
        project = ProjectTranslation.query.filter_by(
            project_id=project_id,
            is_active=True
        ).first()
        return project is not None
    
    def get_project_notes(self, project_id: str) -> List[dict]:
        """Maps to CS_EXP_ProjectNotes datasource"""
        notes = ProjectNote.query.filter_by(project_id=project_id).all()
        return [note.to_dict() for note in notes]
    
    def get_service_areas(self, project_id: str) -> List[dict]:
        """Maps to uspCsExpProjectServiceAreaV2 datasource"""
        return db.session.execute(
            "EXEC uspCsExpProjectServiceAreaV2 :project_id",
            {"project_id": project_id}
        ).fetchall()

class CompetitorService:
    def get_competitor_products(self) -> List[dict]:
        """Maps to CS_EXP_Sel_PLProducts datasource"""
        products = PlatformLoadProduct.query.filter_by(
            is_active=True
        ).order_by(PlatformLoadProduct.name).all()
        return [product.to_dict() for product in products]
```

### Office 365 Integration
```python
from O365 import Account, FileSystemTokenBackend

class Office365Service:
    def __init__(self, client_id: str, client_secret: str):
        self.account = Account((client_id, client_secret))
        self.mailbox = self.account.mailbox()
    
    def get_user_profile(self) -> dict:
        """Maps to Office365Users.MyProfileV2()"""
        user = self.account.get_current_user()
        return {
            'mail': user.mail,
            'display_name': user.display_name,
            'id': user.object_id
        }
    
    def send_email(self, subject: str, body: str, 
                  to_recipients: List[str]) -> bool:
        """Maps to Office365Outlook.SendEmail"""
        message = self.mailbox.new_message()
        message.subject = subject
        message.body = body
        message.to.add(to_recipients)
        return message.send()
```

### Data Access Layer
```python
from typing import Optional, List
from sqlalchemy import text

class DataAccess:
    def __init__(self, db_session):
        self.session = db_session
    
    def execute_stored_procedure(self, proc_name: str, 
                               params: dict) -> List[dict]:
        """Execute stored procedures like uspCsExpCheckProjectId"""
        result = self.session.execute(
            text(f"EXEC {proc_name} :params"),
            params
        )
        return [dict(row) for row in result]
    
    def get_service_areas(self, project_id: str) -> List[dict]:
        """Maps to uspCsExpZtrxServiceAreaV4"""
        return self.execute_stored_procedure(
            'uspCsExpZtrxServiceAreaV4',
            {'project_id': project_id}
        )
```

### Configuration
```python
class DataSourceConfig:
    """Maps PowerApps datasource configurations"""
    DATASOURCES = {
        'CS_EXP_Project_Translation': {
            'table_name': 'cs_exp_project_translation',
            'is_writable': True,
            'cdp_revision': 1,
            'dataset_name': 'CS_EXP_Project_Translation'
        },
        'Office365Users': {
            'api_id': '/providers/microsoft.powerapps/apis/shared_office365users',
            'service_kind': 'ConnectedWadl',
            'workflow_entity_id': '473be22f-b755-ef11-a317-000d3a114ae5'
        }
    }
``` 