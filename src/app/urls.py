from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # PROFILE
    path('id<slug:pk>/', views.ProfileView.as_view(), name='profile'),
    # REGISTRATION
    path('registration/applicant/', views.ApplicantRegistrationView.as_view(), name='registration_applicant'),
    path('registration/employer/', views.EmployerRegistrationView.as_view(), name='registration_employer'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    # LOG IN/OUT
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # APPLICANT
    path('edit/', views.EditPersonalView.as_view(), name='edit_personal'),
    path('edit/photo/', views.EditPhotoView.as_view(), name='edit_photo'),


    path('edit/education/new/', views.AddEducationView.as_view(), name='add_education'),
    path('edit/education/<int:edu_id>', views.EditEducationView.as_view(), name='edit_education'),
    path('edit/experience/new/', views.AddExperienceView.as_view(), name='add_experience'),
    path('edit/experience/<int:exp_id>', views.EditExperienceView.as_view(), name='edit_experience'),
    path('edit/language/new/', views.AddLanguageView.as_view(), name='add_language'),
    path('edit/language/<int:lang_id>', views.EditLanguageView.as_view(), name='edit_language'),
   

    # VACANCY
    path('vacancy/<int:vacancy_id>/', views.VacancyView.as_view(), name='vacancy_detail'),
    path('vacancy/', views.EmployerVacancyView.as_view(), name='vacancy_list'),
    # SEARCH
    path('search/', views.SearchView.as_view(), name='search'),
    path('search/vacancy/', views.VacancySearchView.as_view(), name='vacancy_search'),
    path('search/employer/', views.EmployerSearchView.as_view(), name='employer_search'),
    # PASSWORD CHANGE/RESET
    # path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/<uidb64>/<token>/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('password-reset/done/', views.PasswordResetLinkView.as_view(), name='password_reset_link'),
]
