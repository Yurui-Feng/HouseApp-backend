from django.urls import path

from .views import HouseViewSet, CheckerAPIView

urlpatterns = [
    path('houses', HouseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('houses/<str:pk>', HouseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('checkers', CheckerAPIView.as_view())
]