# PowerApps to Python Component Mapping Guide

## 1. Screen Components

### PowerApps Screen → Python/Flask Route
```python
# PowerApps
Screen1:
    OnVisible: Set(varData, "value")

# Python/Flask Equivalent
@app.route('/screen1')
def screen1():
    session['var_data'] = 'value'
    return render_template('screen1.html')
```

### Navigation
```python
# PowerApps
Navigate(Screen2, ScreenTransition.None)

# Python/Flask Equivalent
return redirect(url_for('screen2'))
```

## 2. Controls

### Button
```python
# PowerApps
Button1:
    OnSelect: UpdateContext({x: 1})

# Python/Flask Equivalent
@app.route('/button1_action', methods=['POST'])
def button1_action():
    session['x'] = 1
    return jsonify({'status': 'success'})
```

### Data Table
```python
# PowerApps
Gallery1:
    Items: Filter(DataSource, field = "value")

# Python/Flask Equivalent
@app.route('/data')
def get_data():
    data = db.session.query(Model).filter(
        Model.field == 'value'
    ).all()
    return render_template('gallery.html', items=data)
```

## 3. Data Operations

### Collection Management
```python
# PowerApps
ClearCollect(
    MyCollection,
    Filter(DataSource, field = "value")
)

# Python/Flask Equivalent
class DataManager:
    def refresh_collection(self):
        self.my_collection = db.session.query(Model)\
            .filter(Model.field == 'value')\
            .all()
```

### Context Variables
```python
# PowerApps
UpdateContext({varName: "value"})

# Python/Flask Equivalent
session['var_name'] = 'value'
```

## 4. Forms

### Form Control
```python
# PowerApps
Form1:
    DataSource: DataSource1
    OnSuccess: Navigate(Screen1)

# Python/Flask Equivalent
@app.route('/form1', methods=['POST'])
def handle_form():
    form = Form1(request.form)
    if form.validate():
        db.session.add(form.data)
        db.session.commit()
        return redirect(url_for('screen1'))
    return render_template('form1.html', form=form)
```

## 5. Authentication

### User Context
```python
# PowerApps
User().Email

# Python/Flask Equivalent
from flask_login import current_user
current_user.email
```

## 6. Integration

### Office 365 Connection
```python
# PowerApps
Office365Users.MyProfile()

# Python/Flask Equivalent
from O365 import Account
account = Account(credentials)
user = account.get_current_user()
```

## 7. State Management

### Global Variables
```python
# PowerApps
Set(globalVar, "value")

# Python/Flask Equivalent
from flask import g
g.global_var = 'value'
```

## 8. Error Handling

### Error Patterns
```python
# PowerApps
If(
    IsError(operation),
    Notify("Error occurred")
)

# Python/Flask Equivalent
try:
    operation()
except Exception as e:
    flash('Error occurred')
    return render_template('error.html', error=str(e))
``` 