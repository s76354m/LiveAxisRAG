# PowerApps to Python Mapping Report

## Variables & Collections

### Global Variables
| Variable Name | Control | Property | Python Implementation |
|--------------|---------|-----------|---------------------|
| varGridEdit | OnStart | Set(varGridEdit,false) | `session['grid_edit'] = False` |
| varProjectTranslation | OnStart | Set(varProjectTranslation,Defaults(CS_EXP_Project_Translation)) | `session['project_translation'] = ProjectTranslation.get_defaults()` |
| varmsid | OnStart | Set(varmsid,GetMSID.Run()) | `session['ms_id'] = office365_service.get_msid()` |

### Context Variables
| Variable Name | Control | Property | Python Implementation |
|--------------|---------|-----------|---------------------|
| CurrentStep | Timer1 | Set(CurrentStep,CurrentStep + 1) | `session['current_step'] += 1` |
| TotalSteps | OnStart | Set(TotalSteps,10) | `session['total_steps'] = 10` |

### Collections
| Collection Name | Control | Property | Python Implementation |
|----------------|---------|-----------|---------------------|
| colMiniMenu | OnStart | ClearCollect() | ```python
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tab_selected = db.Column(db.String(50))
``` |
| ProgressStatus | OnStart | ClearCollect() | ```python
class ProgressStatus(db.Model):
    step = db.Column(db.Integer)
``` |

## Data Sources

### CheckProjectID
| Name | Type | Python Implementation |
|------|------|---------------------|
| ApiId | /providers/microsoft.powerapps/apis/shared_logicflows | ```python
class ProjectValidator:
    def check_project_id(self, project_id: str) -> bool:
``` |
| ServiceKind | ConnectedWadl | `class ProjectService(BaseService):` |
| WorkflowEntityId | 473be22f-b755-ef11-a317-000d3a114ae5 | `WORKFLOW_ID = '473be22f-b755-ef11-a317-000d3a114ae5'` |

### CS_EXP_Project_Translation
| Name | Type | Python Implementation |
|------|------|---------------------|
| DatasetName | CS_EXP_Project_Translation | ```python
class ProjectTranslation(db.Model):
    __tablename__ = 'cs_exp_project_translation'
``` |
| IsWritable | True | `__table_args__ = {'info': {'writable': True}}` | 