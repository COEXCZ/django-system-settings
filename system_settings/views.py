from django.db import transaction
from django.views.generic import UpdateView

from system_settings.base import BasePersistentSystemSettings
from system_settings.forms import SystemSettingsForm
from system_settings.models import SystemSettings


class GeneralSettingsView(UpdateView):
    model = SystemSettings
    settings: BasePersistentSystemSettings = NotImplemented
    form_class = SystemSettingsForm

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction.on_commit(self.settings.invalidate)
        return response
