from datetime import timezone

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

from .forms import CourseEnrollForm

from ..users.models import ConnectBeautyVenue
from ..courses.models import Course
from .models import StudentCompletedModule
from .forms import PostCompletedForm, ConnectBeautyVenueForm


class StudentRegistrationView(CreateView):
    """StudentRegistrationView"""
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('students:student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)

        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """StudentEnrollCourseView"""
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """StudentCourseListView"""
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    """StudentCourseDetailView"""
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
            completed = StudentCompletedModule.objects.filter(course=self.kwargs['pk'], student=self.request.user)
            context['completed_list'] = completed
        else:
            # get first module
            context['module'] = course.modules.all()
            completed = StudentCompletedModule.objects.filter(course=self.kwargs['pk'], student=self.request.user)
            context['completed_list'] = completed

        print(context)
        return context


class StudentCourseDetailContentView(DetailView):
    """StudentCourseDetailView"""
    model = Course
    template_name = 'students/course/detail_content.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
            completed = StudentCompletedModule.objects.filter(course=self.kwargs['pk'], student=self.request.user)
            context['completed_list'] = completed
            completed_module = StudentCompletedModule.objects.filter(module=self.kwargs['module_id'], student=self.request.user)
            context['completed_module'] = completed_module
            context['connect_beauty_venue'] = ConnectBeautyVenue.objects.filter(user=self.request.user)
            print(context['completed_list'])
        else:
            # get first module
            context['module'] = course.modules.all()
            completed_list = StudentCompletedModule.objects.filter(course=self.kwargs['pk'], student=self.request.user)
            context['completed_list'] = completed_list

        print(context)
        return context


def student_module_view(request):
    """student_module_view
    postでモデュール完了
    """
    template = 'students/course/detail_content.html'

    if request.method == "POST":
        form = PostCompletedForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user
            post.save()

            messages.success(request, 'このモジュールを完了しました。')
            return redirect('students:student_course_detail_module', pk=post.course.id, module_id=post.module.id)
    else:
        form = PostCompletedForm()

    return render(request, template, {'form': form})


def connect_beauty_venue(request):

    template = 'students/course/detail_content.html'

    if request.method == "POST":
        form = ConnectBeautyVenueForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, '登録しました。BeautyVenueには明日連携されています')

            return redirect('students:student_course_detail_module', pk=request.course, module_id=request.module)
        else:
            form = PostCompletedForm()

    return render(request, template, {'form': form})
