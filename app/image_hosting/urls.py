from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# Wiring up the API using automatic URL routing.
# Additionally, including login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('images/', views.image_list_create_view, name="image_list_create_view"),
    path('images/<int:pk>/', views.image_retrieve_update_delete_view, name="image_retrieve_update_delete_view"),
    path('users/', views.user_list_view, name="user_list_view"),
    path('users/<int:pk>/', views.user_retrieve_view, name="user_retrieve_view"),
]