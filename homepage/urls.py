from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # 首页
    path("", views.homepage, name='homepage'),

    # 新生报名
    path('apply/', views.application_form, name='application_form'),

    # 面试官登录相关
    path('interviewer/login/', views.interviewer_login, name='interviewer_login'),
    path('interviewer/logout/', views.interviewer_logout, name='interviewer_logout'),

    # 面试官系统首页
    path('interviewer/dashboard/', views.interviewer_dashboard, name='interviewer_dashboard'),

    # 申请管理
    path('interviewer/applications/', views.application_list, name='application_list'),
    path('interviewer/applications/<uuid:applicant_id>/', views.application_detail, name='application_detail'),

    # 面试安排
    path('interviewer/schedule/', views.interview_schedule, name='interview_schedule'),

    # 时间设置
    path('interviewer/time-slots/', views.time_slots, name='time_slots'),

    # 管理员相关
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/departments/', views.admin_departments, name='admin_departments'),
    path('admin/applications/', views.admin_applications, name='admin_applications'),
    path('admin/decisions/', views.admin_decisions, name='admin_decisions'),
    path('admin/admissions/', views.admin_admissions, name='admin_admissions'),
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin/export/admissions/', views.export_admissions, name='export_admissions'),
    path('admin/export/feedback/', views.export_feedback, name='export_feedback'),
]

# 开发环境下提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
