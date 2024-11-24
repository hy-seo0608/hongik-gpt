from django.apps import AppConfig
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os


class DialogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialog"

    def ready(self):
        if os.environ.get("RUN_MAIN", None) is not None:  # RUN_MAIN 이 'true' 인 경우에 스케쥴러 실행
            print(" RUN_MAIN :", os.environ.get("RUN_MAIN", None))
            from .corn import main

            main()
