from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.db.models import Count
from ..models import Subject, Course


class CourseListView(TemplateResponseMixin, View):
    """
    CourseListView
    """
    model = Course
    template_name = "courses/course/list.html"

    def get(self, request, subject=None):
        subject = Subject.objects.annotate(total_courses=Count("courses"))
        courses = Course.objects.annotate(total_modules=Count("modules"))

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response({"subjects": subject,
                                        "subject": subject,
                                        "courses": courses})


class CourseDetailView(DetailView):
    """
    CourseDetailView
    """
    model = Course
    template_name = "courses/course/detail.html"
