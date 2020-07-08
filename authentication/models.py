from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.template.defaultfilters import slugify



class AuthorManager(BaseUserManager):
    def create_user(self, email, name, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not username:
            raise ValueError('Users must have a username')
        author = self.model(
            email=self.normalize_email(email),
            name = name,
            username = username
        )
        author.set_password(password)
        author.save(using=self._db)
        return author
    
    def create_staffuser(self, email, name, username, password):
        author = self.create_user(
            email,
            name,
            username,
            password=password
        )
        author.staff = True
        author.save(using=self._db)
        return author

    def create_superuser(self, email, name, username, password):
        author = self.create_user(
            email,
            name,
            username,
            password=password
        )
        author.staff = True
        author.admin = True
        author.save(using=self._db)
        return author


class Author(AbstractBaseUser):
    bio = models.TextField(max_length=280)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(null=False, unique=True)
    website = models.URLField()
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=20)
    profile_picture = models.ImageField(null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    age = models.FloatField(null=True, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    following = models.ManyToManyField(
        'self',
        related_name="following"
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        self.following.add(self)
        return super().save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    objects = AuthorManager()
