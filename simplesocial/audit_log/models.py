from django.db import models

class AuditLog(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
    params = models.CharField(max_length=255, null=True)
    time = models.DateTimeField()


class DBResponseAudit(models.Model):
    log = models.ForeignKey(AuditLog, related_name='db_responses', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    object_id = models.IntegerField()
    content = models.JSONField(null=True)


    class Meta:
        verbose_name_plural = "DB Responses"
