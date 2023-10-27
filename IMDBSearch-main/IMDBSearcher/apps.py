# import sys
#
# from django.apps import AppConfig
#
# # from IMDBSearcher.consumers import starter
#
#
# class ImdbSearcherConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'IMDBSearcher'
#
#     def ready(self):
#         if 'runserver' not in sys.argv:
#             return True
#         from .models import Basic,Names,Principal,Ratings,TitleToName
#         # starter.start()
