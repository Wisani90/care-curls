from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from geoposition.fields import GeopositionField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    birthday = models.DateField(blank=True, default='1990-12-01')
    town = models.CharField(max_length=128, blank=True)
    # relationship = models.CharField(blank=True, max_length=128,
    #     choices=[('1', 'married'), ('2', 'in relationship'), ('3', 'single')])
    # relation_user = models.ManyToManyField('self', blank=True, related_name='relationship')
    visible_name = models.CharField(blank=True, max_length=128)
    url = models.CharField(blank=True, max_length=256)
    # friends = models.ManyToManyField('self', blank=True, related_name='friends')
    # friend_requests = models.ManyToManyField('self', blank=True, related_name='friend_requests')    
    
    contact_number = models.CharField(max_length=32, blank=True)
    position = GeopositionField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.visible_name = self.get_visible_name()
        # self.url = reverse('profile', args=[self.user.username])
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_visible_name(self):
        return ' '.join([str(self.first_name), str(self.last_name)]).strip()

    def send_friend_request(self, user_profile):
        self.friend_requests.add(user_profile)
        noti = Notification.objects.create(owner=self, type=Notification.FRIEND_REQUEST, sender=user_profile.user.username)
        self.notification_set.add(noti)
        return self.friend_requests.count()

    def cancel_friend_request(self, user_profile):
        self.friend_requests.remove(user_profile)
        self.notification_set.get(type=Notification.FRIEND_REQUEST, sender=user_profile.user.username).delete()
        noti = Notification.objects.create(owner=user_profile, type=Notification.DECLINED_FRIEND_REQUEST, sender=self.user.username)
        user_profile.notification_set.add(noti)
        return self.friend_requests.count()

    def add_friend(self, user_profile):
        self.friend_requests.remove(user_profile)
        self.notification_set.get(type=Notification.FRIEND_REQUEST, sender=user_profile.user.username).delete()
        self.friends.add(user_profile)
        user_profile.friends.add(self)
        noti = Notification.objects.create(owner=user_profile, type=Notification.ACCEPTED_FRIEND_REQUEST, sender=self.user.username)
        user_profile.notification_set.add(noti)
        return self.friends.count()

    def remove_friend(self, user_profile):
        self.friends.remove(user_profile)
        user_profile.friends.remove(self)
        noti = Notification.objects.create(owner=user_profile, type=Notification.REMOVED_FRIEND, sender=self.user.username)
        user_profile.notification_set.add(noti)
        return self.friends.count()

    def __str__(self):
        return self.get_visible_name()

    @staticmethod
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

    instance.userprofile.save()