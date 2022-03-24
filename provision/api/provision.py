import logging
from typing import Dict, List

from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from provision.models.provision import Provision
from provision.serializers.provision import CreateProvisionSerializer
from provision.service.provision import ProvisionService

log = logging.getLogger("django")


class ProvisionAPIView(GenericViewSet):
    """
    Django 프로젝트 생성 APIView
    """

    parser_classes = (JSONParser,)

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CreateProvisionSerializer

        return super().get_serializer_class()

    def create(self, request: Request, *args: List, **kwargs: Dict) -> HttpResponse:
        log.info("Generate django project API")

        serializer_class = self.get_serializer_class()

        serializer: CreateProvisionSerializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provision_obj: Provision = serializer.save()

        log.info("Provision data : " + str(serializer.data))

        log.info("Created provision ID : " + str(provision_obj.id))

        provision_service = ProvisionService(**serializer.data)

        response: HttpResponse = provision_service.make_zip_file_response()

        return response
