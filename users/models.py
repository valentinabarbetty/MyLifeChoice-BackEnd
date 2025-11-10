from django.db import models

class PlayerType(models.Model):
    player_type_id = models.AutoField(primary_key=True)
    player_type = models.CharField(max_length=100)

    def __str__(self):
        return self.player_type

class Guide(models.Model):
    guide_id = models.AutoField(primary_key=True)
    guide = models.CharField(max_length=100)

    def __str__(self):
        return self.guide
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    player_type = models.ForeignKey(PlayerType, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    def __str__(self):
        return self.nickname

