from django.db import models
from django.contrib.auth.models import User


class UserActivate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rpassword = models.CharField(max_length=30, blank=True)
    activate_status = models.BooleanField(default=False)
    email_sended = models.BooleanField(default=False)
