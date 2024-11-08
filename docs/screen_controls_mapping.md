# Detailed Screen Controls Mapping

## EditProjectScreen
```python
class EditProjectScreen(BaseScreenForm):
    """Maps PowerApps EditProjectScreen"""
    
    def setup_controls(self):
        self.controls = {
            'txtProjectId': ControlProperties(
                height=40,
                width=200,
                x=20,
                y=100,
                border_style="Solid"
            ),
            'ddRegion': ControlProperties(
                height=40,
                width=300,
                x=20,
                y=160
            ),
            'btnSave': ControlProperties(
                height=40,
                width=100,
                x=20,
                y=220,
                fill="#0078D4",
                hover_fill="#005A9E"
            )
        }
        
    class Meta:
        model = ProjectTranslation
        fields = ['project_id', 'region', 'status']
```

## YLineScreen
```python
class YLineScreen(BaseScreenForm):
    """Maps PowerApps YLineScreen"""
    
    def setup_controls(self):
        self.controls = {
            'grdYLines': GridControl(
                height=400,
                width=700,
                x=20,
                y=100,
                columns=[
                    {'field': 'y_line_id', 'header': 'Y-Line ID'},
                    {'field': 'description', 'header': 'Description'},
                    {'field': 'status', 'header': 'Status'}
                ]
            ),
            'btnAdd': ControlProperties(
                height=40,
                width=100,
                x=20,
                y=520,
                fill="#107C10",
                hover_fill="#0B5C0B"
            )
        }
```

## Navigation Implementation
```python
class NavigationManager:
    """Maps PowerApps navigation system"""
    
    SCREEN_FLOW = {
        'EntryScreen': {
            'next': ['NewProjectScreen', 'EditProjectScreen'],
            'back': None
        },
        'NewProjectScreen': {
            'next': ['YLineScreen'],
            'back': 'EntryScreen'
        },
        'EditProjectScreen': {
            'next': ['YLineScreen'],
            'back': 'EntryScreen'
        },
        'YLineScreen': {
            'next': ['CompetitorEntryScreen'],
            'back': ['NewProjectScreen', 'EditProjectScreen']
        },
        'CompetitorEntryScreen': {
            'next': ['SuccessScreenCompetitorData'],
            'back': 'YLineScreen'
        }
    }
    
    @classmethod
    def can_navigate(cls, from_screen: str, to_screen: str) -> bool:
        """Validate navigation path"""
        if from_screen not in cls.SCREEN_FLOW:
            return False
        
        valid_next = cls.SCREEN_FLOW[from_screen]['next']
        valid_back = cls.SCREEN_FLOW[from_screen]['back']
        
        return to_screen in (valid_next or []) or to_screen in (valid_back or [])
``` 