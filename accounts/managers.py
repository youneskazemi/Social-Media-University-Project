from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None, email=None):
        """
        Creates and saves a User with the given username,email ,date_of_birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username=None, password=None, email=None):
        """
        Creates and saves superuser with the given username,email and password.
        """
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_admin = True
        user.save(using=self.db)
        return user
