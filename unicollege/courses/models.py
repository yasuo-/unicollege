from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from ..core.models import TimeStampedModel, BaseContentModel


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


class Content(TimeStampedModel):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'content'


class ItemBaseModel(TimeStampedModel):
    instructor = models.ForeignKey(get_user_model(),
                                   related_name='%(class)s_related',
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(BaseContentModel):
    body = models.TextField()

    class Meta:
        db_table = 'content_text'


class Text(ItemBaseModel):
    content = models.TextField()

    class Meta:
        db_table = 'item_text'


class File(ItemBaseModel):
    file = models.FileField(upload_to='files')

    class Meta:
        db_table = 'item_file'


class Image(ItemBaseModel):
    file = models.FileField(upload_to='images')

    class Meta:
        db_table = 'item_image'


class Video(ItemBaseModel):
    url = models.URLField()

    class Meta:
        db_table = 'item_video'
