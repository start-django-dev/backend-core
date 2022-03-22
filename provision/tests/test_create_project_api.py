from django.test import TestCase

from provision.models.provision import Provision


class CreateProjectAPITest(TestCase):
    """
    프로젝트 생성 API 에 대한 테스트
    """

    def test_장고_프로젝트_생성을_요청합니다(self):
        # given
        payload = {
            "python_version": "3.8",
            "django_version": "3.2.12",
            "project_name": "django_project",
        }

        # when
        res = self.client.post(
            path="/api/provision/",
            data=payload,
            content_type="application/json",
        )

        # then
        self.assertEqual(res.status_code, 201)
        # self.assertIsInstance(res.content)
        provision_obj: Provision = Provision.objects.get()
        self.assertEqual(provision_obj.python_version, payload["python_version"])
        self.assertEqual(provision_obj.django_version, payload["django_version"])
        self.assertEqual(provision_obj.project_name, payload["project_name"])
