from django.db import models
from users.models import User

class Insignia(models.Model):
    insignia_id = models.AutoField(primary_key=True)
    insignia_name = models.CharField(max_length=100)

    def __str__(self):
        return self.insignia_name


class Career(models.Model):
    career_id = models.AutoField(primary_key=True)
    career_name = models.CharField(max_length=100)
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE, related_name='careers')

    def __str__(self):
        return self.career_name


class Progress(models.Model):
    STATE_CHOICES = [
        ('to do', 'To Do'),
        ('in progress', 'In Progress'),
        ('done', 'Done'),
    ]

    progress_id = models.AutoField(primary_key=True)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='progresses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresses')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='to do')
    feedback = models.TextField(blank=True, null=True)
    progress = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.nickname} - {self.career.career_name} ({self.state})"
