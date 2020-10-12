from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    """
    User Model of the project.
    Created following the best Django practises.
    """
    pass


class Reviewer(models.Model):
    """
    Reviewer Model.
    All Reviewer's extra metadata that aren't in User Model can be added in
    this Model.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    self_description = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Returns the representation of the instance.
        """
        return str(self.user)


class Company(models.Model):
    """
    Company Model.
    """
    name = models.CharField(max_length=40)

    def __str__(self):
        """
        Returns the representation of the instance.
        """
        return self.name


class Review(models.Model):
    """
    Representation of a Review.
    """
    reviewer = models.ForeignKey(
    	Reviewer,
    	on_delete=models.CASCADE
    )
    company = models.ForeignKey(
    	Company,
    	on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
    	choices=[
    		(1, 1),
    		(2, 2),
    		(3, 3),
    		(4, 4),
    		(5, 5),
    	]
    )
    title = models.CharField(max_length=60)
    summary = models.TextField(max_length=10000)
    submission_date = models.DateField(auto_now_add=True)
    ip_address = models.CharField(max_length=45)

    def __str__(self):
        """
        Returns the representation of the instance.
        """
        return '%s - %s' % (self.reviewer, self.company)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Creates AUTH TOKEN for the created User.
    """
    if created:
        Token.objects.create(user=instance)
