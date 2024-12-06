from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import EventAPIView

app_name = "calendarapp"


router = SimpleRouter()

router.register('event', EventAPIView)


urlpatterns = [
    path(r'', include(router.urls))
]
