import json
import typing

from django import forms
from django.utils.cache import caches


from pydantic import BaseModel, Extra


class SettingsAttribute(BaseModel):
    default: typing.Any
    form_field: typing.Any = forms.IntegerField
    form_field_kwargs: dict = {}

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


class SettingsAttributes(BaseModel):
    def get_default_values(self) -> dict:
        return {
            key: value.default
            for key, value in self
        }


class BasePersistentSystemSettings:
    name: str = NotImplemented
    attributes: SettingsAttributes = NotImplemented

    def _load_db_data(self):
        raise NotImplementedError()

    def invalidate(self):
        raise NotImplementedError()

    def get_db_object(self):
        from system_settings.models import SystemSettings

        settings_obj, _ = SystemSettings.objects.get_or_create(
            name=self.name,
            defaults={
                'options': self.attributes.get_default_values()
            }
        )
        return settings_obj

    def get(self, key):
        raise NotImplementedError()

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, item):
        return self.get(item)


class InMemorySystemSettings(BasePersistentSystemSettings):

    def __init__(self):
        self._data = {}

    def _load_db_data(self):
        settings_obj = self.get_db_object()
        self._data = settings_obj.options

    def get(self, key):
        if not self._data:
            self._load_db_data()

        if key in self._data:
            return self._data[key]

        attribute = getattr(self.attributes, key)

        return attribute.default

    def invalidate(self):
        self._data = {}


class CachedSystemSettings(BasePersistentSystemSettings):
    cache_name: str = 'default'

    def __init__(self):
        self._cache = caches[self.cache_name]
        self._cache_key = self.get_cache_key(self.name)

    def get_cache_key(self, key: str):
        return self._cache.make_key(key)

    def _load_db_data(self):
        settings_obj = self.get_db_object()
        self._cache.set(self._cache_key, json.dumps(settings_obj.options))

    def get(self, key):
        data_dict = json.loads(self._cache.get(self._cache_key, '{}'))
        if not data_dict:
            self._load_db_data()
            data_dict = json.loads(self._cache.get(self._cache_key))

        if key in data_dict:
            return data_dict[key]
        attribute = getattr(self.attributes, key)
        return attribute.default

    def invalidate(self):
        self._cache.delete(self._cache_key)
