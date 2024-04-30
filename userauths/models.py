from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __stf__(self):
        return self.username
    
def default_image():
    return 'image/default_profile_image_MCVmlmz.webp'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='image', default=default_image)
    full_name=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)

    def __stf__(self):
        return f"{self.user.username} - {self.full_name} - {self.phone}"


def auto_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(auto_create_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
