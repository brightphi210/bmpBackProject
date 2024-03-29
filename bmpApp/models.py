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
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    profile_pic = models.ImageField(default='default.png', blank=True, null=True, upload_to='profile_pics/')

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
        return f" This is {self.name}"


class UserProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', default='default.png', blank=True, null=True)

    def __str__(self):
        return f"This is {self.user.email}"
    


class Product(models.Model):
    productName = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"This is the {self.productName} product name"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()

    def __str__(self):
        return f"This is {self.user.name} Made this payment {self.amount}"


    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"This {(self.product.productName)} is added to Cart"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=20)

    def __str__(self):
        return f"This {self.user.name} has made an Order"
    

class OrderItem(models.Model):
    quantity = models.IntegerField()
    order_price = models.IntegerField()
    price = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f"This is {self.product.productName} is an Order Item"
    

