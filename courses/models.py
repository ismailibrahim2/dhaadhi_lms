import os
from django.db import models
from django.template.defaultfilters import slugify
from instructors.models import Instructor


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True, max_length=50, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def save_course_image(instance, filename):
    upload_to = 'Course thumbnails/'
    ext = filename.split('.')[-1]
    if instance.title:
        filename = f'{instance.instructor.user.user}/{instance.category.name}/{instance.title}/{instance.title}.{ext}'
    return os.path.join(upload_to, filename)


class Course(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=save_course_image)
    description = models.TextField()
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
