from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-points',]
    
class Info(models.Model):
    information = models.TextField()
    is_true = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acertos = models.IntegerField(default=0)
    erros = models.IntegerField(default=0)
    
    def __str__(self):
        return self.information

class Voto(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    is_true = models.BooleanField(default=False)
    
    @classmethod
    def create(cls, user,info,is_true):
        vote = cls(user=user,info=info,is_true=is_true)
        # do something with the book
        return vote
    
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    

    



