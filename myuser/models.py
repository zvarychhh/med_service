import enum
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class GroupEnum(enum.Enum):
    first = 1
    second = 2
    third = 3
    forth = 4


class RezusEnum(enum.Enum):
    positive = "+"
    negative = "-"


class GenderEnum(enum.Enum):
    male = "Чоловік"
    female = "Жінка"
    unknown = "Не вказувати"


class BloodTypeRezus(models.Model):
    name = models.CharField(
        max_length=1,
        choices=[
            (RezusEnum.positive, RezusEnum.positive),
            (RezusEnum.negative, RezusEnum.negative),
        ],
        unique=True,
    )

    def __str__(self):
        return self.name


class BloodTypeGroup(models.Model):
    name = models.IntegerField(
        choices=[
            (GroupEnum.first, GroupEnum.first),
            (GroupEnum.second, GroupEnum.second),
            (GroupEnum.third, GroupEnum.third),
            (GroupEnum.forth, GroupEnum.forth),
        ],
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class BloodType(models.Model):
    rezus = models.ForeignKey(BloodTypeRezus, on_delete=models.PROTECT)
    group = models.ForeignKey(BloodTypeGroup, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.rezus} {self.group}"


class Gender(models.Model):
    name = models.CharField(
        max_length=100,
        choices=[
            (GenderEnum.male, GenderEnum.male),
            (GenderEnum.female, GenderEnum.female),
            (GenderEnum.unknown, GenderEnum.unknown),
        ],
        unique=True,
    )

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64, null=False)
    blood_type = models.ForeignKey(BloodType, blank=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)

    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_superuser = models.BooleanField(default=False, null=False)

    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)
