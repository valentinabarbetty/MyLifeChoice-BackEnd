from django.db import models
from users.models import User

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    recommendation = models.TextField()

    def __str__(self):
        return f"Feedback de {self.user.nickname}"
