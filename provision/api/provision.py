import logging
from typing import Dict, List

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from provision.serializers.provision import CreateProvisionSerializer

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

    def create(self, request: Request, *args: List, **kwargs: Dict) -> Response:
        log.info("Generate django project API")

        serializer_class = self.get_serializer_class()

        serializer: CreateProvisionSerializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        log.info("Provision data : " + str(serializer.data))

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data,
        )
