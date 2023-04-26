from django import forms
from pydantic import BaseModel

from system_settings.models import SystemSettings


class SystemSettingsForm(forms.ModelForm):
    settings_attributes: BaseModel = NotImplemented

    class Meta:
        model = SystemSettings
        exclude = ['name', 'options']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, value in self.settings_attributes:
            field = value.form_field(
                initial=self.instance.options.get(key, value.default),
                **value.form_field_kwargs,
            )
            self.fields[key] = field

    def save(self, commit=True):
        self.instance.options = self.cleaned_data

        if commit:
            self.instance.save()

        return self.instance
