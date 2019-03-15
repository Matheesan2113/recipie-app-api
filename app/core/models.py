from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        creates and saves a new user
        """
        if not email:
            raise ValueError("User must have email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model that supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    """Tag to be used for recipie"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
        
class Ingredient(models.Model):
    """ Ingredient to be used in recipie"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Recipie(models.Model):
    """ Recipie object to be used"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    ##   Blnak = true means a new link might be set to a blank string... optional
    link = models.CharField(max_length=255, blank=True)
    #  Diff types of foreign keys, 1 recipie to 1 field or tag, but we 
    #  can have multipe to multiple
    #  Many recipies can be assigned to many ingredients
    # Make sure to put a string around Ingredient to keep order 
    # in making the classes
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')


    def __str__(self):
        return self.title
