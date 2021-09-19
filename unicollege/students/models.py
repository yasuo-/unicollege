from django.db import models
from django.contrib.auth import get_user_model
from ..core.models import TimeStampedModel

from unicollege.courses.models import Course, Module


class StudentCompletedModule(TimeStampedModel):
    """StudentCompletedModule
    完了したモジュール
    """
    student = models.ForeignKey(get_user_model(),
                                related_name='students_created',
                                on_delete=models.CASCADE)
    course = models.ForeignKey(Course,
                               related_name='students_course',
                               on_delete=models.CASCADE)
    module = models.ForeignKey(Module,
                               related_name='students_module',
                               on_delete=models.CASCADE)

    class Meta:
        db_table = 'student_completed_course_module'
