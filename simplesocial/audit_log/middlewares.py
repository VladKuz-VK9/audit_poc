import json
from datetime import datetime
from typing import Any
from django.forms import model_to_dict
from dataclasses import dataclass, field
from .models import AuditLog, DBResponseAudit


@dataclass
class DBResponse:
    model_name: str
    object_id: int
    content: Any


@dataclass
class LogRecord:
    user_id: int
    username: str
    url: str
    method: str
    params: str
    time: datetime = field(default_factory=datetime.now)


class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith('/admin'):
            log_record = LogRecord(
                url=request.path,
                user_id=request.user.id,
                username=request.user.username,
                method=request.method,
                params=request.GET.dict() or None,
            )
            db_responses = []
            if hasattr(response, 'context_data'):
                if object_list := response.context_data.get('object_list', ''):
                    for single_object in object_list:
                        db_responses.append(self._log_db_response(single_object))
                elif single_object := response.context_data.get('object', ''):
                    db_responses.append(self._log_db_response(single_object))

            log = AuditLog.objects.create(
                user_id=log_record.user_id,
                username=log_record.username,
                url=log_record.url,
                method=log_record.method,
                params=log_record.params,
                time=log_record.time,
            )
            for db_response in db_responses:
                DBResponseAudit.objects.create(
                    log=log,
                    model_name=db_response.model_name,
                    object_id=db_response.object_id,
                    content=json.loads(json.dumps(db_response.content, default=str)),
                )
        return response

    @staticmethod
    def _log_db_response(model_object):
        model_name = f"{model_object._meta.app_label.title()} | {model_object._meta.verbose_name.title()}"
        model_dict = model_to_dict(model_object)
        if model_name == "Groups | Group":
            model_dict['posts'] = list(model_object.posts.values('id', 'user', 'created_at', 'message'))
        return DBResponse(
            model_name=model_name,
            object_id=model_object.id,
            content=model_dict,
        )
