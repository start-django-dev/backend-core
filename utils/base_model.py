from django.db import models


class AbstractDateTime(models.Model):
    """
    생성 시간, 수정 시간에 대해 저장하는 추상 모델
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
