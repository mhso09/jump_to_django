from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
# Create your models here.


# class User(AbstractUser):
#     nic_name = models.CharField(_("name of User"), blank=True, max_length=255) # 닉네임
#     user_name = models.CharField(blank=True, max_length=255) # 이름
#     profile_photo = models.ImageField(blank=True) # 프로필 사진
#     bio = models.TextField(blank=True) # 나이
#     email = models.CharField(blank=True, max_length=255)
#     phon_number = models.CharField(blank=True, max_length=255)

#     class Meta:
#         managed = False

#     def __str__(self):
#         return "id : " + self.nic_name + ", email : " + self.email
