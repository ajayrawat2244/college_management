from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class College(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.SlugField(max_length=63, unique=True)
    domain = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to="college_logos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    RESERVED_SUBDOMAINS = {"www", "admin", "api", "static", "media", "localhost"}

    class Meta:
        ordering = ["name"]

    def clean(self):
        if self.subdomain:
            self.subdomain = self.subdomain.strip().lower()
            if self.subdomain in self.RESERVED_SUBDOMAINS:
                raise ValidationError({"subdomain": "This subdomain is reserved."})

    def save(self, *args, **kwargs):
        if self.subdomain:
            self.subdomain = slugify(self.subdomain)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


"""from django.db import models

class College(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
"""