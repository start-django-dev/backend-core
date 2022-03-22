from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.base_model import AbstractDateTime


class Provision(AbstractDateTime):
    """
    Django 프로젝트 생성에 대한 정보를 저장하는 모델
    """

    python_version = models.CharField(verbose_name=_("Python version"), max_length=10)
    django_version = models.CharField(verbose_name=_("Django version"), max_length=10)
    project_name = models.CharField(verbose_name=_("Project name"), max_length=20)

    class Meta:
        db_table = "provision"
        verbose_name = _("Provision")
        verbose_name_plural = f"{verbose_name} {_('List')}"

    def __str__(self):
        return f"Python: {self.python_version}, Django: {self.django_version}"
