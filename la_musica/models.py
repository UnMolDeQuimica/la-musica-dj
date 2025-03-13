from typing import ClassVar, TYPE_CHECKING
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


if TYPE_CHECKING:
    from .models import User  # noqa: F401

class UserManager(DjangoUserManager["User"]):
    """Custom manager for the User model."""

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            msg = "The given email must be set"
            raise ValueError(msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):  # type: ignore[override]
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Default custom user model for La Mamadura.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"), unique=True)
    slug = models.CharField(max_length=100, verbose_name=_("Slug"), blank=True, unique=True, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)


class FlatSheetMusic(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", primary_key=True, unique=True, default=uuid.uuid4)
    title = models.CharField(max_length=100, verbose_name=_("Title"), unique=True)
    subtitle = models.CharField(max_length=250, verbose_name=_("Subtitle"), blank=True, null=True)
    url = models.URLField(verbose_name=_("URL"))
    embed_url = models.URLField(verbose_name=_("Embed url"))
    author = models.CharField(max_length=100, verbose_name=_("Author"), default="Anónimo")
    arranger = models.CharField(max_length=100, verbose_name=_("Arranger"), blank=True, null=True)
    slug = models.CharField(max_length=100, verbose_name=_("Slug"), blank=True, null=True, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="flat_sheet_music", verbose_name=_("Group"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        super().save(*args, **kwargs)

