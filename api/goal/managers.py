from django.db import models


class MoonshotManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self

    def action_retrieve(self):
        return self


class HandshakeManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self

    def action_retrieve(self):
        return self


class GoalManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self.select_related("target_employee", "created_by").prefetch_related("moonshots", "handshakes")

    def action_retrieve(self):
        return self.select_related("target_employee", "created_by").prefetch_related("moonshots", "handshakes")
