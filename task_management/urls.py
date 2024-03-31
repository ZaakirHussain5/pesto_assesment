from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Define the namespace for the task management application
app_name = "task_management"

# Initialize a DefaultRouter object for API endpoints
router = DefaultRouter()

# Register the TaskViewSet with the router
router.register("tasks", views.TaskViewSet, "tasks")

# Define urlpatterns for routing
urlpatterns = [
    # Route for the index page, authenticated users only
    path('', views.index, name="index"),
    
    # Route for the authentication page
    path('authentication', views.authentication, name="authentication"),
    
    # Route for user logout
    path('logout', views.logout, name="logout"),
    
    # Route for user registration API
    path('api/signup', views.RegisterAPI.as_view(), name="RegisterAPI"),
    
    # Route for user login API
    path('api/login', views.LoginAPI.as_view(), name="LoginAPI"),
    
    # Route for including API endpoints from the router
    path('api/', include(router.urls)),
]
