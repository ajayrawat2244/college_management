from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, tenant=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "superadmin")
        return self.create_user(email, password=password, tenant=None, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    email = models.EmailField()
    tenant = models.ForeignKey("tenants.College", null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant", "email"], name="uniq_user_email_per_tenant"),
        ]

    def clean(self):
        super().clean()
        if self.role != "superadmin" and not self.tenant:
            raise ValidationError({"tenant": "Tenant is required for non-superadmin users."})

    def __str__(self):
        return self.email