from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "students"

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/',
         cache_page(60 * 15)(views.StudentCourseListView.as_view()),
         name='student_course_list'),
    path('course/<pk>/',
         views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/', (views.StudentCourseDetailContentView.as_view()),
         name='student_course_detail_module'),
    path('module/completed/', views.student_module_view,
         name='student_course_detail_module_completed'),
    path('connect/beautyvenue/', views.connect_beauty_venue,
         name='student_connect_beautyvenue'),
]
