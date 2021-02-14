from django.urls import path
from app import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # REGISTRATION
    path('registration/applicant/', views.ApplicantRegistrationView.as_view(), name='registration_applicant'),
    path('registration/employer/', views.EmployerRegistrationView.as_view(), name='registration_employer'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    # LOGIN/LOGOUT
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # APPLICANT ACTIONS
    path('id<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('edit/personal/', views.EditPersonalView.as_view(), name='edit_personal'),
    path('edit/photo/', views.EditPhotolView.as_view(), name='edit_photo'),
    path('edit/education/', views.EditEducationlView.as_view(), name='edit_education'),
    path('edit/skills/', views.EditSkillslView.as_view(), name='edit_skills'),
    path('edit/languages/', views.EditLanguageslView.as_view(), name='edit_languages'),
    path('add/experience/', views.AddExperienceView.as_view(), name='add_experience'),
    path('edit/experience/', views.EditExperienceView.as_view(), name='edit_experience'),
    path('delete/experience/id<int:exp_id>/', views.DeleteExperienceView.as_view(), name='delete_experience'),
    # EMPLOYER ACTIONS
    path('id<int:user_id>/vacancies/', views.EmployerVacancyView.as_view(), name='vacancies'),

    # VACANCIES
    path('vacancy/<int:vac_id>/', views.VacancyView.as_view(), name='vacancy'),
    path('vacancy/', views.VacancySearchView.as_view(), name='vacancy_search'),
   # path('/', views.JobSearchView.as_view(), name='job_search'),

    # PASSWORD CHANGE/RESET
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/<uidb64>/<token>/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/done/', views.PasswordResetLinkView.as_view(), name='password_reset_link'),
]


