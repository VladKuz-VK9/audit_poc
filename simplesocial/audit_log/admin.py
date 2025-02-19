import csv
import json

from . import models
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe


class DBResponseInline(admin.TabularInline):
    model = models.DBResponseAudit
    fields = ('model_name', 'object_id', 'formatted_content',)
    readonly_fields = ('formatted_content',)

    def formatted_content(self, obj):
        return mark_safe(f"<pre>{json.dumps(obj.content, indent=4)}</pre>")

    formatted_content.short_description = 'Content'


@admin.register(models.AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user_id', 'url', 'method', 'params', 'all_db_responses', 'time')
    inlines = (DBResponseInline,)
    actions = ('export_to_csv',)
    list_filter = ('username',)

    def all_db_responses(self, obj):
        model_names = set(obj.db_responses.values_list('model_name', flat=True))
        return ", ".join(model_names) if model_names else "-"

    all_db_responses.short_description = 'Requested Models'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="audit_log.csv"'
        writer = csv.writer(response)
        writer.writerow(['Log ID', 'Username', 'User ID', 'URL', 'Method', 'Params', 'Requested Model', 'Object ID', 'Object Content', 'Time'])

        for log in queryset:
            db_responses = log.db_responses.all()
            if db_responses.exists():
                for db_response in db_responses:
                    writer.writerow([log.id, log.username, log.user_id, log.url, log.method, log.params, db_response.model_name, db_response.object_id, db_response.content, log.time])
            else:
                writer.writerow(
                    [log.id, log.username, log.user_id, log.url, log.method, log.params, None, None, None, log.time])

        return response

    export_to_csv.short_description = 'Export selected to CSV'
