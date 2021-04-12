from core_nav import views
from django.urls import path

app_name = 'core_nav'
urlpatterns = [
        path('settings/', views.SettingsView.as_view(), name='settings'),
        path('about/', views.AboutView.as_view(), name='about'),
        path('choose-signup-option/', views.ChooseSignUpOption.as_view(), name='choose-signup-option'),
        path('school-details/', views.SchoolDetailsView.as_view(), name='school-details'),
        path('school-code/', views.SchoolCode.as_view(), name='school-code'),
        path('check-school-code/', views.check_school_code, name='check-school-code'),


        path('get-started/', views.GetStarted.as_view(), name='get-started'),
        path('get-started-invite/', views.GetStarted.as_view(), name='get-started-invite'),
        path('overview-help/', views.OverviewHelp.as_view(), name='overview-help'),
]
