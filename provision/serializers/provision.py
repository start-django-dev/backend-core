from rest_framework import serializers

from provision.models.provision import Provision


class CreateProvisionSerializer(serializers.ModelSerializer):
    """
    Django 프로젝트 생성에 대한 serializer
    """

    class Meta:
        model = Provision
        fields = (
            "python_version",
            "django_version",
            "project_name",
        )
