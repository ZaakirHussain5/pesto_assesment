from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import Task

# Get the user model defined in Django authentication system
User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Includes additional fields for displaying usernames and status display.

    Methods:
        get_status_display: Retrieve the human-readable display value for the status.
        get_created_by_username: Retrieve the username of the creator of the task.
        get_assignee_username: Retrieve the username of the assignee of the task.
    """
    created_by_username = serializers.SerializerMethodField()
    assignee_username = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        """
        Retrieve the human-readable display value for the status.

        Args:
            obj: Task object

        Returns:
            Human-readable status display value
        """
        return obj.get_status_display()

    def get_created_by_username(self, obj):
        """
        Retrieve the username of the creator of the task.

        Args:
            obj: Task object

        Returns:
            Username of the creator
        """
        return obj.created_by.username
   
    def get_assignee_username(self, obj):
        """
        Retrieve the username of the assignee of the task.

        Args:
            obj: Task object

        Returns:
            Username of the assignee, or an empty string if assignee is not set
        """
        return obj.assignee.username if obj.assignee else ""

    class Meta:
        model=Task
        fields=(
            'id', 
            'title', 
            'description', 
            'assignee', 
            'created_by', 
            'status', 
            'created_at', 
            'created_by_username', 
            'assignee_username',
            'status_display'
        )
        extra_kwargs={"created_by": {"required": False}}

class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def create(self, validated_data):
        """
        Create a new user based on the provided data.

        Args:
            validated_data: Validated data for user registration

        Returns:
            Newly created user instance

        Raises:
            serializers.ValidationError: If user with the same username already exists
        """
        try:
            user = User.objects.create_user(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'], 
                email=validated_data['email'], 
                password=validated_data['password']
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError("User Already Exists")

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validate user credentials.

        Args:
            data: Data containing username and password for login

        Returns:
            Validated user instance

        Raises:
            serializers.ValidationError: If provided username does not exist or password is incorrect
        """
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username":"User with the username does not exists."})
        
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid Credentials")
        
        return user
