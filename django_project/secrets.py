import json
import os

from django.core.exceptions import ImproperlyConfigured

# settings file 과 다른 위치에서의 BASE_DIR 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# secret_file 불러오기
secret_file = os.path.join(BASE_DIR, "secrets.json")

# secret file 내용 deserialize
with open(secret_file) as f:
    secrets = json.loads(f.read())


# 환경 변수 값 가져오는 함수
def get_secrets(key, secrets=secrets):
    try:
        return secrets[key]
    except KeyError:
        error_msg = f"Set the {key} environment variable"

        raise ImproperlyConfigured(error_msg)
