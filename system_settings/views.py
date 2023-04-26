from django.db import transaction
from django.views.generic import UpdateView

from system_settings.base import BasePersistentSystemSettings
from system_settings.forms import SystemSettingsForm
from system_settings.models import SystemSettings


class SystemSettingsView(UpdateView):
    model = SystemSettings
    settings: BasePersistentSystemSettings = NotImplemented
    form_class = SystemSettingsForm

    def get_settings(self):
        return self.settings

    def get_object(self, queryset=None):
        return self.get_settings().get_db_object()

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction.on_commit(self.settings.invalidate)
        return response

    def get_success_url(self):
        return self.request.path

