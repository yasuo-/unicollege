from django.conf import settings
from uuid import uuid4
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin
)
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from ..core.models import TimeStampedModel
from . import GenderType
from .validators import validate_possible_number


class PossiblePhoneNumberField(PhoneNumberField):
    default_validators = [validate_possible_number]


class User(AbstractUser):
    """Default user for unicollege.
       reference to openid
       https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse
    """
    name = CharField(_("Name of User"), blank=True, max_length=255)
    family_name = models.CharField(_("family Name of User"), blank=True, max_length=256)
    given_name = models.CharField(max_length=256, blank=True)
    middle_name = models.CharField(max_length=256, blank=True)
    nickname = models.CharField(max_length=256, blank=True)
    preferred_username = None
    profile = None # URL of the End-User's profile page.
    picture = models.ImageField(upload_to="users/profiles/picture/", null=True, blank=True)
    website = None # URL of the End-User's Web page or blog.
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GenderType.CHOICES, default=GenderType.NOT_KNOWN)
    birthdate = models.DateField(blank=True, null=True) # YYYY-MM-DD
    zoneinfo = None # End-User's time zone.
    locale = None # For example, en_US;
    phone_number = PossiblePhoneNumberField(blank=True, default="")
    phone_number_verified = models.BooleanField(default=False)

    # USERNAME_FIELD = "email"

    class Meta:
        db_table = 'user'
        ordering = ("email",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def get_full_name(self) -> str:
        full_name = "%s %s" % (self.family_name, self.given_name)
        return full_name


class UserAddress(TimeStampedModel):
    """User Address"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(
        User,
        related_name="user_address",
        on_delete=models.CASCADE,
    )
    country = CountryField(blank=True) # Country name component.
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Zip code or postal code")
    region = models.CharField(max_length=256, blank=True, verbose_name="State, province, prefecture, or region")
    locality = models.CharField(max_length=256, blank=True, verbose_name="City or locality")
    street_address_1 = models.CharField(max_length=256, blank=True, verbose_name="Full street address 1")
    street_address_2 = models.CharField(max_length=256, blank=True, verbose_name="Full street address 2")

    class Meta:
        db_table = 'user_address'

    def __str__(self):
        return self.user.name
