from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("",  csrf_exempt(views.upload_file), name='upload_file'),
]