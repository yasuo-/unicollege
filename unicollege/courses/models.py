from django.db import models
from django.contrib.auth import get_user_model

from ..core.models import TimeStampedModel


class Subject(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        db_table = 'subject'
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(TimeStampedModel):
    instructor = models.ForeignKey(get_user_model(),
                                   related_name='courses_created',
                                   on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()

    class Meta:
        db_table = 'course'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Module(TimeStampedModel):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'course_module'

    def __str__(self):
        return self.title
