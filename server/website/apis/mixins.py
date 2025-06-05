import csv

from django.contrib import admin, messages
from django.db import models
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext as _

from .forms import CsvImportForm
from .actions import ExportCsvMixin, ExportJsonMixin, ExportPdfMixin
from .paginators import TinyResultsSetPagination
from core.settings.base import MAX_OBJECTS


class SlugMixin(models.Model):
    slug = models.SlugField(default="", null=False)
    
    class Meta:
        abstract = True


class AuditMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    changed_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(class)s_created_by',
        null=True, blank=True
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='%(class)s_updated_by',
        null=True, blank=True
    )
    
    class Meta:
        abstract = True
    
    
class AdminMixin(admin.ModelAdmin, ExportCsvMixin, ExportJsonMixin, ExportPdfMixin):
    change_list_template = "entities/change_list.html"
    actions = ["export_as_csv", "export_as_json", "export_as_pdf"]
    exclude = ["created_on", "changed_on", "created_by", "changed_by"]
    readonly_fields = ["created_on", "changed_on", "created_by", "changed_by"]
    list_per_page = TinyResultsSetPagination.page_size
    date_hierarchy = 'created_on'
    empty_value_display = "- Unknown -"
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["file"].read().decode("utf-8").splitlines()
            reader = csv.DictReader(csv_file)
        
            for row in reader:
                try:
                    self.model.objects.create(**row, created_by=request.user)                 
                except Exception as e:
                    self.message_user(request, _("Error importing row: %(row)s – %(e)s") % {"row": row, "e": e}, messages.ERROR)
                    return redirect("..")
                
            self.message_user(request, _("Your csv file has been imported"), messages.SUCCESS)
            return redirect("..")
        
        form = CsvImportForm()
        model = self.model._meta.verbose_name.title() 
        return render(
            request, "admin/csv_form.html", {"form": form, "model_name": model}
        )
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        labels = dict(export_as_csv='CSV', export_as_json='JSON', export_as_pdf="PDF")
        
        for key, label_prefix in labels.items():
            if key in actions:
                func, name, _ = actions[key]
                actions[key] = (
                    func,
                    name,
                    f"Export {label_prefix} selected {self.model._meta.verbose_name_plural}"
                )
        return actions
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        if change:
            obj.changed_by = request.user
        super().save_model(request, obj, form, change)
    
    
class ReadOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    

class MaxObjectsMixin:    
    def has_add_permission(self, request):
        if self.model.objects.count() >= MAX_OBJECTS:
            return False
        return True