from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_reviewer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_to_home2 = models.BooleanField(null=True, blank=True, default=None)  # Allow null and blank
    reviewer_feedback = models.CharField(max_length=20, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending')
    reviewer = models.ForeignKey(User, related_name='reviewed_files', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = UploadedFile.objects.get(pk=self.pk)
            if not original.uploaded_to_home2 and self.uploaded_to_home2:
                self.send_email_notification('Your paper has been published')
            if original.reviewer_feedback != self.reviewer_feedback:
                if self.reviewer_feedback == 'accepted':
                    self.send_email_notification('Your paper has been accepted by the reviewer')
                elif self.reviewer_feedback == 'rejected':
                    self.send_email_notification('Your paper has been rejected by the reviewer')
        super().save(*args, **kwargs)

    def send_email_notification(self, message):
        subject = message
        recipient_list = [self.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

# Signals to create or save UserProfile when a User is created or saved
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
