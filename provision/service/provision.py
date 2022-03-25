import os
import shutil
import time
import uuid
from typing import Tuple
from wsgiref.util import FileWrapper

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Engine, Template


class ProvisionService:
    """
    Django 프로젝트 파일을 제공하는 로직을 구현한 서비스 클래스
    """

    def __init__(self, **project_setting_data):
        """
        장고 프로젝트 생성에 필요한 데이터 초기화
        :param python_version: 개발 환경에서 사용할 파이썬 버전
        :param django_version: 개발 환경에서 사용할 장고 버전
        :param project_name: 장고 프로젝트 이름
        """
        self.python_version: str = project_setting_data["python_version"]
        self.django_version: str = project_setting_data["django_version"]
        self.project_name: str = project_setting_data["project_name"]

        self.rewrite_template_suffixes = (
            (".py-tpl", ".py"),
            (".txt-tpl", ".txt"),
        )

        # 프로젝트 생성에 사용되는 project_template 경로
        self.template_dir: str = os.path.join(os.getcwd(), "conf/project_template/")

        # Context 객체 생성을 위한 kwargs 선언
        self.base_name: str = "project_name"
        self.camel_case_name = f"camel_case_{self.project_name}_name"
        self.camel_case_value = "".join(
            x for x in self.project_name.title() if x != "_"
        )

        # Template 객체의 변수들을 변환해줄 context 객체
        self.context = Context(
            {
                "project_name": "django_project",
                "base_directory": self.template_dir,
                "camel_case_name": self.camel_case_value,
            },
            autoescape=False,
        )

    def generate_django_project(self) -> Tuple[str, str]:
        # 장고 프로젝트 생성을 진행한 개별 디렉토리를 생성
        dir_name: str = self.generate_random_dir_name()

        # 장고 프로젝트 세팅할 디렉토리를 지정
        working_dir: str = settings.DJANGO_PROJECT_SAVE_PATH / dir_name

        # 실제 작업 디렉토리 생성 (이미 존재하는 디렉토리라면 OSError 발생)
        os.makedirs(working_dir, exist_ok=False)

        # project_template 이 있는 위치에서 모든 디렉토리에 대한 루프
        for root, dirs, files in os.walk(self.template_dir):
            # 해당 디렉토리의 위치에서 템플릿 디렉토리에 대한 path 를 제외한 나머지 경로르 가져옴
            path_rest: str = root[len(self.template_dir) :]
            # 나머지 경로에서 project_template 에 있는 project_name 디렉토리 이름을 사용자가 지정한 프로젝트 이름으로 치환
            relative_dir: str = path_rest.replace("project_name", self.project_name)

            # relative_dir 이 root 가 아닌 하위 디렉토리일 경우
            if relative_dir:
                # 실제 프로젝트가 생성되는 위치의 dir
                target_dir: str = os.path.join(working_dir, relative_dir)
                os.makedirs(target_dir, exist_ok=True)

            for filename in files:
                if filename.endswith((".pyo", ".pyc", ".py.class")):
                    # Ignore some files as they cause various breakages.
                    continue

                # project_template 안에 있는 파일 경로
                old_path: str = os.path.join(root, filename)
                # 실제 프로젝트가 생성되는 위치의 파일 경로
                new_path: str = os.path.join(working_dir, relative_dir, filename)

                # 변경해야할 파일 확장자들을 변환
                for old_suffix, new_suffix in self.rewrite_template_suffixes:
                    if new_path.endswith(old_suffix):
                        new_path: str = new_path[: -len(old_suffix)] + new_suffix
                        break

                if new_path.endswith(".py"):  # 생성하려고 하는 파일의 확장자 .py 일 경우
                    with open(old_path, encoding="utf-8") as template_file:
                        content: str = template_file.read()
                    template: Template = Engine().from_string(content)
                    content: str = template.render(self.context)
                    with open(new_path, "w", encoding="utf-8") as new_file:
                        new_file.write(content)
                else:  # 아닐 경우
                    shutil.copyfile(old_path, new_path)

        return working_dir, dir_name

    def make_project_archive(self) -> Tuple[str, str, str]:
        working_dir, dir_name = self.generate_django_project()

        # 생성된 프로젝트를 zip 파일로 압축
        shutil.make_archive(
            self.project_name, "zip", settings.DJANGO_PROJECT_SAVE_PATH / dir_name
        )

        zip_path: str = settings.BASE_DIR / f"{self.project_name}.zip"
        filename: str = self.project_name.replace(" ", "_")

        return working_dir, zip_path, filename

    def make_zip_file_response(self) -> HttpResponse:
        working_dir, zip_path, filename = self.make_project_archive()

        # 압축한 파일을 리턴하는 httpResponse 객체를 생성
        response: HttpResponse = HttpResponse(
            FileWrapper(open(zip_path, "rb")), content_type="application/zip"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}.zip"'

        self.remove_all_created_files(working_dir, zip_path)

        return response

    @staticmethod
    def remove_all_created_files(working_dir: str, zip_path: str):
        # 프로젝트 생성을 위해 만들었던 디렉토리 삭제
        shutil.rmtree(working_dir)
        # 프로젝트 zip 파일 삭제
        os.remove(zip_path)

    @staticmethod
    def generate_random_dir_name() -> str:
        return str(time.time()) + "." + str(uuid.uuid4())
