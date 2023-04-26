# Django system settings

---

Django app to manage project related settings from forms.

Settings attributes are stored into JSONField in database so there is no need to migrate if you need to add new attributes.

---

## Installation

pip install git+ssh://git@github.com/COEXCZ/django_system_settings.git

Add to settings.py

## Usage

Add to settings.py

```python
INSTALLED_APPS = [
    ...
    'django_system_settings',
    ...
]
```

### Settings conf

Add attributes and settings anywhere in your project

```python
from django import forms

from system_settings import SettingsAttributes, SettingsAttribute, InMemorySystemSettings

class MySettingsAttributes(SettingsAttributes):
    my_settings_attribute = SettingsAttribute(
        form_field=forms.CharField,
        form_field_kwargs=dict(
            label='My settings attribute',
            widget=forms.Textarea
        )
    )
    
    
my_settings_attributes = MySettingsAttributes()


class MySettings(InMemorySystemSettings):
    name = 'my_settings'
    attributes = my_settings_attributes

    
my_settings = MySettings()
```

### Forms

```python
from system_settings.forms import SystemSettingsForm


class MySettingsForm(SystemSettingsForm):
    settings_attributes = my_settings_attributes
```

### Views

```python
from system_settings.views import SystemSettingsView

class MySettingsView(SystemSettingsView):
    settings = my_settings
    form_class = MySettingsForm
    template_name = "user/preferences/my_settings.html"
```


## Caching

To not ask database for every access of settings attrs there is caching layer.

### In memory cache

`InMemorySystemSettings` settings are stored in app memory during runtime. Suitable for apps deployed as single process.

### Django cache

`CachedSystemSettings` settings using django cache. By default `default` cache is used.

