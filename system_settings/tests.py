from django import forms
from django.test import TestCase

from system_settings.base import SettingsAttributes, SettingsAttribute, InMemorySystemSettings
from system_settings.models import SystemSettings


class TestSettingsAttributes(SettingsAttributes):
    test_attr = SettingsAttribute(
        form_field=forms.CharField,
        default='test_init'
    )


test_settings_attributes = TestSettingsAttributes()


class TestSettings(InMemorySystemSettings):
    name = 'test'
    attributes = test_settings_attributes


test_settings = TestSettings()


class InMemorySystemSettingsTestCase(TestCase):

    def test_get(self):
        self.assertFalse(SystemSettings.objects.exists())

        self.assertEqual(test_settings.test_attr, 'test_init')
        self.assertTrue(SystemSettings.objects.exists())

        settings_instance = SystemSettings.objects.first()
        settings_instance.options['test_attr'] = 'test_set'
        settings_instance.save()

        self.assertEqual(test_settings.test_attr, 'test_init')

        test_settings.invalidate()

        self.assertEqual(test_settings.test_attr, 'test_set')
