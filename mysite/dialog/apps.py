from django.apps import AppConfig
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import os


class DialogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialog"

    # def ready(self):
    #     if not os.environ.get("APP"):
    #         os.environ["APP"] = "True"
    #     from .utils import intent
