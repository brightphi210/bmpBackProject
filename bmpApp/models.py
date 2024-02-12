from django.db import models

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin

from django.conf import settings

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
# ======================== Creatives =============================
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def save(self, *args, **kwargs):
        count_id = User.objects.all().count()
        self.auto_id = count_id+1
        super(User, self).save(*args, **kwargs)

    def _str_(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', default='default.png', blank=True, null=True)

    def __str__(self):
        return self.user.email