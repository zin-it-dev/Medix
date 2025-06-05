import uuid

from django.db import models
from django.contrib import admin
from django.utils.safestring import mark_safe
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.utils.translation import gettext_lazy as _

from .sec_models import User
from .mixins import AuditMixin, SlugMixin


class Common(AuditMixin):
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)


class EmployeeProxy(Employee):
    class Meta:
        proxy = True
        


class Category(Common, SlugMixin):
    name = models.CharField(unique=True, max_length=80)
    
    class Meta:
        verbose_name_plural =  _("Categories")
    
    def __str__(self):
        return self.name


class Course(Common, SlugMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="courses/%Y/%m/%d/", null=True, blank=True, storage=MediaCloudinaryStorage)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    @admin.display(description="Photo")
    def photo_image(self):
        return mark_safe('<img src="{url}" class="img-thumbnail rounded" width="{width}" height={height} />'.format(
            url=self.image.url,
            width=80,
            height=80)
        )
    
    def __str__(self):
        return self.title