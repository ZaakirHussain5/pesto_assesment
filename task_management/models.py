from django.db import models
from django.contrib.auth import get_user_model

# Get the user model defined in Django authentication system
User = get_user_model()

class Task(models.Model):
    """
    Model representing a task.

    Attributes:
        TO_DO (int): Constant representing 'To Do' status.
        IN_PROGRESS (int): Constant representing 'In Progress' status.
        DONE (int): Constant representing 'Done' status.
        STATUS (tuple): Choices for the status field.
        title (CharField): Title of the task.
        description (TextField): Description of the task.
        status (PositiveSmallIntegerField): Status of the task.
        created_by (ForeignKey): User who created the task.
        assignee (ForeignKey): User assigned to the task.
        created_at (DateTimeField): Date and time when the task was created.
    """
    TO_DO = 1
    IN_PROGRESS = 2
    DONE = 3

    STATUS = (
        (TO_DO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (DONE, "Done"),
    )

    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.PositiveSmallIntegerField(choices=STATUS)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the task.

        Returns:
            String representation of the task title.
        """
        return self.title
