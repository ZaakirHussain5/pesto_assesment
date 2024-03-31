from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from knox.models import AuthToken
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Import models and serializers from the application
from .models import Task
from .serializers import TaskSerializer, RegistrationSerializer, LoginSerializer

# Get the user model defined in Django authentication system
User = get_user_model()

# Views for task management

@login_required(login_url="/authentication")
def index(request):
    """
    Render the tasks page with a list of assignees.

    Args:
        request: HTTP request object

    Returns:
        Rendered HTML page with tasks and assignees
    """
    return render(request, "pages/tasks.html", {
        "assignees": User.objects.all()
    })

def authentication(request):
    """
    Render the authentication page.

    Args:
        request: HTTP request object

    Returns:
        Rendered HTML page for authentication
    """
    return render(request, "pages/authentication.html")

@login_required(login_url="/authentication")
def logout(request):
    """
    Log out the user.

    Args:
        request: HTTP request object

    Returns:
        Redirect to login page after logout
    """
    AuthToken.objects.filter(user__id=request.user.id).delete()
    auth_logout(request)
    return redirect('task_management:login')

class RegisterAPI(GenericAPIView):
    """
    API endpoint for user registration.
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user registration.

        Args:
            request: HTTP request object
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            JSON response with authentication token upon successful registration
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(GenericAPIView):
    """
    API endpoint for user login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.

        Args:
            request: HTTP request object
            *args: Additional arguments
            **kwargs: Additional keyword arguments

        Returns:
            JSON response with authentication token upon successful login
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        AuthToken.objects.filter(user__id=user.id).delete()
        auth_login(request, user)
        _, token = AuthToken.objects.create(user)
        return Response({
            "token": token
        })

class TaskViewSet(ModelViewSet):
    """
    API endpoint for tasks management.
    """
    permission_classes = [
        IsAuthenticated
    ]
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Get queryset of tasks for the authenticated user.

        Returns:
            Queryset of tasks
        """
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assignee=self.request.user)
        )
    
    def perform_create(self, serializer):
        """
        Perform creation of a new task.

        Args:
            serializer: Task serializer object

        Returns:
            Newly created task instance
        """
        return serializer.save(created_by=self.request.user)
