from django.db import models


class ValueManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self.select_related("created_by").prefetch_related("value_items")

    def action_retrieve(self):
        return self.select_related("created_by").prefetch_related("value_items")


class ValueItemManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self

    def action_retrieve(self):
        return self


class ValueAssessmentItemManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self.select_related("value_item")

    def action_retrieve(self):
        return self.select_related("value_item")


class ValueAssessmentManager(models.QuerySet):
    def action_list(self):
        return self

    def action_detailed(self):
        return self.select_related("target_employee", "assigned_employee")

    def action_retrieve(self):
        return self.select_related("target_employee", "assigned_employee")
