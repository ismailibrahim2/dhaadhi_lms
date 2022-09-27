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


def save_course_intros(instance, filename):
    upload_to = 'Course Intros/'
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
    overview_vid = models.FileField(upload_to=save_course_intros)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

    def __str__(self):
        return self.title


def save_lesson_videos(instance, filename):
    upload_to = 'Course Lessons/'
    ext = filename.split('.')[-1]
    if instance.name:
        filename = f'{instance.module.course.instructor.user.user}/{instance.module.course.title}/{instance.module.title}/{instance.name}/{instance.name}.{ext}'
    return os.path.join(upload_to, filename)


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    video = models.FileField(upload_to=save_lesson_videos)

    def __str__(self):
        return self.name
