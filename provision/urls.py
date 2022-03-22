from django.urls import path

from provision.api.provision import ProvisionAPIView

urlpatterns = [
    path(
        "",
        ProvisionAPIView.as_view(
            {
                "post": "create",
            }
        ),
    ),
]
