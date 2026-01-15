from django.db import models
from django.contrib.auth.models import User
import uuid




class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    licence_id=models.UUIDField(default=uuid.uuid4,editable=False)
    created_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.user.username




class Role(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    choice=models.TextField()

    def __str__(self):
        return self.user.username
