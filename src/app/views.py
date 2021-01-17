from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View

from src.settings import EMAIL_HOST_USER
from .forms import *
from .models import User, Applicant, Employer, Experience, Vacancy


REGISTRATION_SUCCESS = "You're has been successfully registered"


class HomeView(View):
    def get(self, request):
        #User.objects.get(pk=40).delete()
        #User.objects.filter(id__gt=40).delete()
        #Applicant.objects.filter(id__gt=1).delete()
        return render(request, 'home.html')


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        today = date.today()
        domain = request.get_host()

        context = {
            'user': request.user,
            'domain': domain,
        }

        if not request.user.is_authenticated:
            try:
                user_view = User.objects.get(pk=kwargs['user_id'])
            except User.DoesNotExist:
                return render(request, 'errors/unexist_profile.html')

            if not user_view.company:
                return redirect(reverse('login') + f'?next={request.path}')
            
            vacancies = user_view.employer.vacancies.all()
            context['user_view'] = user_view
            context['vacancies'] = vacancies
            context['active_vacancies'] = vacancies.filter(active=True)
            context['inactive_vacancies'] = vacancies.filter(active=False)
            context['active_vacancies_count'] = vacancies.filter(active=True).count()
            return render(request, 'profile.html', context)

        if request.user.is_authenticated and not request.user.company:
            try:
                user_view = User.objects.get(pk=kwargs['user_id'])
            except User.DoesNotExist:
                return render(request, 'errors/unexist_profile.html')

            if user_view.company:
                vacancies = user_view.employer.vacancies.all()
                context['user_view'] = user_view
                context['vacancies'] = vacancies
                context['active_vacancies'] = vacancies.filter(active=True)
                context['inactive_vacancies'] = vacancies.filter(active=False)
                context['active_vacancies_count'] = vacancies.filter(active=True).count()
                return render(request, 'profile.html', context)

            if user_view == request.user or request.user.is_admin:
                experience = user_view.applicant.experience.all()
                context['user_view'] = user_view
                context['experience'] = experience
                context['first_exp'] = experience.first()
                context['last_exp'] = experience.last()
                if user_view.applicant.birthday:
                    if today.month >= user_view.applicant.birthday.month or (
                    today.month == user_view.applicant.birthday.month and
                    today.day >= user_view.applicant.birthday.day):
                        age = today.year - user_view.applicant.birthday.year
                        context['age'] = age
                    else:
                        age = today.year - user_view.applicant.birthday.year - 1
                        context['age'] = age
                return render(request, 'profile.html', context)
            return render(request, 'errors/403.html', status=403)

        if request.user.is_authenticated and request.user.company:
            try:
                user_view = User.objects.get(pk=kwargs['user_id'])
            except User.DoesNotExist:
                return render(request, 'errors/unexist_profile.html')
            
            if user_view.company:
                vacancies = user_view.employer.vacancies.all()
                context['user_view'] = user_view
                context['vacancies'] = vacancies
                context['active_vacancies'] = vacancies.filter(active=True)
                context['inactive_vacancies'] = vacancies.filter(active=False)
                context['active_vacancies_count'] = vacancies.filter(active=True).count()
                return render(request, 'profile.html', context)

            experience = user_view.applicant.experience.all()
            context['user_view'] = user_view
            context['experience'] = experience
            context['first_exp'] = experience.first()
            context['last_exp'] = experience.last()
            if user_view.applicant.birthday:
                if today.month >= user_view.applicant.birthday.month or (
                today.month == user_view.applicant.birthday.month and
                today.day >= user_view.applicant.birthday.day):
                    age = today.year - user_view.applicant.birthday.year
                    context['age'] = age
                else:
                    age = today.year - user_view.applicant.birthday.year - 1
                    context['age'] = age
            return render(request, 'profile.html', context)


class EditPersonalView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                user_form = ApplicantEditForm(instance=user)
                profile_form = ApplicantProfileForm(instance=user.applicant)
                template = 'edit_applicant.html'
                context = {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'user': user
                }
            else:
                user_form = EmployerEditForm(instance=user)
                profile_form = EmployerProfileForm(instance=user.employer)
                template = 'edit_employer.html'
                context = {
                    'user_form': user_form,
                    'profile_form': profile_form, 
                    'user': user
                }
            return render(request, template, context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                user_form = ApplicantEditForm(instance=user, data=request.POST)
                profile_form = ApplicantProfileForm(instance=user.applicant, data=request.POST, files=request.FILES)
            else:
                user_form = EmployerEditForm(instance=user, data=request.POST)
                profile_form = EmployerProfileForm(instance=user.employer, data=request.POST, files=request.FILES)

            if user_form.is_valid():
                user_form.save()
            if profile_form.is_valid():
                profile_form.save()
            
            for error in user_form.errors:
                messages.error(request, user_form.errors[error])
            
            for error in profile_form.errors:
                messages.error(request, profile_form.errors[error])
        
            return redirect('profile', user.id)
        return redirect('login')


class EditPhotolView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                form = PhotoForm(instance=user.applicant)
            else:
                form = PhotoForm(instance=user.employer)
            
            context = {'form': form}
            return render(request, 'edit_photo.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                form = PhotoForm(instance=user.applicant, data=request.POST, files=request.FILES)
            else:
                form = PhotoForm(instance=user.employer, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
            return redirect('profile', user.id)
        return redirect('login')


class EditEducationlView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = EducationForm(instance=request.user.applicant)
            template = 'edit_education.html'
            context = {
                'form': form
            }
            return render(request, template, context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            form = EducationForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()
        return redirect('profile', user.id)


class EditSkillslView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = SkillsForm(instance=request.user.applicant)
            template = 'edit_skills.html'
            context = {
                'form': form
            }
            return render(request, template, context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            form = SkillsForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()
        return redirect('profile', user.id)


class EditLanguageslView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = LanguagesForm(instance=request.user.applicant)
            template = 'edit_languages.html'
            context = {
                'form': form
            }
            return render(request, template, context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            form = LanguagesForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()
            return redirect('profile', user.id)
        return redirect('login')


class AddExperienceView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                form_set = modelformset_factory(Experience, form=ExperienceForm, extra=1)
                forms = form_set(queryset=request.user.applicant.experience.none())
                template = 'add_experience.html'
                context = {
                    'forms': forms,
                    'user': user
                }
                return render(request, template, context)
            return render(request, 'errors/403.html', status=403)
        return redirect('login')
    
    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                FormSet = modelformset_factory(Experience, form=ExperienceForm)
                forms = FormSet(request.POST)
                if forms.is_valid():
                    forms.save(commit=False)
                    for form in forms:
                        form.instance.applicant = user.applicant
                        form.save()
                return redirect('profile', user.id)
            return render(request, 'errors/403.html', status=403)
        return redirect('login')


class EditExperienceView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                if not Experience.objects.filter(applicant=user.applicant).count():
                    FormSet = modelformset_factory(Experience, form=ExperienceForm, extra=1)
                else:
                    FormSet = modelformset_factory(Experience, form=ExperienceForm, extra=0)
                forms = FormSet(queryset=Experience.objects.filter(applicant=user.applicant))
                template = 'edit_experience.html'
                context = {
                    'forms': forms,
                    'user': user
                }
                return render(request, template, context)
            return render(request, 'errors/403.html', status=403)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if not user.company:
                FormSet = modelformset_factory(Experience, form=ExperienceForm)
                forms = FormSet(request.POST, queryset=Experience.objects.filter(applicant=user.applicant))
                if forms.is_valid():
                    forms.save(commit=False)
                    for form in forms:
                        data = form.cleaned_data
                        if data['end'] and data['begin'] > data['end'] or (
                        not data['end'] and not data['now'] or (
                        data['end'] and data['now'])):
                            break
                        form.instance.applicant = user.applicant
                        form.save()
                return redirect('profile', user.id)
            return render(request, 'errors/403.html', status=403)
        return redirect('login')


class DeleteExperienceView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                exp = Experience.objects.get(pk=kwargs['exp_id'])
            except Experience.DoesNotExist:
                return redirect('profile', request.user.id)
                
            if exp.applicant.user == request.user:
                exp.delete()
 
            return redirect('profile', request.user.id)
        return redirect('login')


class RegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'registration/registration.html')
        

class ApplicantRegistrationView(View):
    def get(self, request):
        return render(request, 'registration/applicant.html', {'form': ApplicantCreationForm()})

    def post(self, request):
        user = ApplicantCreationForm(request.POST)
        if user.is_valid():
            user = user.save()
            Applicant.objects.create(user=user)
            send_mail(
                REGISTRATION_SUCCESS,
                f'Dear {user.first_name} {user.last_name},\nWelcome to GimmeJob!',
                EMAIL_HOST_USER, 
                [user.email],
                fail_silently=False,
            )
            return render(request, 'registration/success.html', {'user': user})
            #return redirect('home')
        for error in user.errors:
            messages.error(request, user.errors[error])
        return redirect('registration_applicant')


class EmployerRegistrationView(View):
    def get(self, request):
        return render(request, 'registration/employer.html', {'form': EmployerCreationForm()})

    def post(self, request):
        user = EmployerCreationForm(request.POST)
        if user.is_valid():
            user = user.save()
            Employer.objects.create(user=user)
            #Vacancy.objects.create(applicant=employer)
            send_mail(
                REGISTRATION_SUCCESS,
                f'Dear {user.first_name} {user.last_name},\nWelcome to GimmeJob!',
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'registration/success.html', {'user': user})
            #return redirect('home')
        for error in user.errors:
            messages.error(request, user.errors[error])
        return redirect('registration_employer')


class EmployerVacancyView(View):
    def get(self, request, *args, **kwargs):   
        add: int = request.GET.get('add')
        edit: int = request.GET.get('edit')
        delete: int = request.GET.get('delete')
        vac_id: int = request.GET.get('vac_id')

        try:
            user_view = User.objects.get(pk=kwargs['user_id'])
        except User.DoesNotExist:
            return render(request, 'errors/unexist_profile.html')
        
        if not user_view.employer:
            return render(request, 'errors/400.html')

        user = request.user
        if vac_id:
            vacansy = user_view.employer.vacancies.filter(pk=vac_id)

        context = {
            'user': user,
            'user_view': user_view
        }
        
        if not user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.path}')
        if user.company:
            if not add and not edit and not delete:                
                context['vacancies'] = Vacancy.objects.filter(employer=user.employer)
                context['active_vacancies'] = Vacancy.objects.filter(employer=user.employer).filter(active=True)
                context['inactive_vacancies'] = Vacancy.objects.filter(employer=user.employer).filter(active=False)
                return render(request, 'all_vacancies.html', context)
            if add and not edit and not delete and user == user_view:
                context['form'] = VacancyForm()
                return render(request, 'add_vacancy.html', context)
            if edit and not add and not delete and vacansy:
                vacansy = user.employer.vacancies.get(pk=vac_id)
                context['form'] = VacancyForm(instance=vacansy)
                context['vac_id'] = vacansy.id
                return render(request, 'edit_vacancy.html', context)
            if delete and not add and not edit and vacansy and user == user_view:
                Vacancy.objects.get(pk=vac_id).delete()
                return redirect('vacancies', user.id)
        return render(request, 'errors/400.html', status=400)
        
    def post(self, request, *args, **kwargs):
        add: int = request.POST.get('add')
        edit: int = request.POST.get('edit')
        vac_id: int = request.POST.get('vac_id')
        
        if not request.user.is_authenticated or request.user.is_authenticated and not request.user.employer:
            return render(request, 'errors/403.html', status=403)

        user = request.user
        if not user.company:
            return render(request, 'errors/400.html')

        if add:
            form = VacancyForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.instance.employer = user.employer
                form.save()
            return redirect('vacancies', user.id)
            
        if edit and vac_id:
            form = VacancyForm(request.POST, instance=user.employer.vacancies.get(pk=vac_id))
            if form.is_valid():
                form.save()
            return redirect('vacancies', user.id)

        return render(request, 'errors/400.html')


class VacancyView(View):
    def get(self, request, *args, **kwargs):
        try:
            vacancy = Vacancy.objects.get(pk=kwargs['vac_id'])
        except Vacancy.DoesNotExist:
            return render(request, 'errors/unexist_vacancy')

        if not vacancy.active:
            vacancy = None
            return render(request, 'vacancy.html', {'vacancy': vacancy})

        #body = vacancy.body.replace('\n', ' < br >', 100)
        context = {
            'user': request.user,
            'employer': Employer.objects.get(vacancies=vacancy),
            'vacancy': vacancy, 
            'body': vacancy.body,
            'vac_id': vacancy.id,
            'company': vacancy.employer.user.company,
            'company_id': vacancy.employer.user.id
        }
        
        return render(request, 'vacancy.html', context)
            
    def post(self, request, *args, **kwargs):
        pass


# CRUD PERMISSIONS *(PRIME)
# content_type = ContentType.objects.get_for_model(Vacancy)
# permission, created = Permission.objects.get_or_create(
#     codename='CRUD_vacancies',
#     name='Can CRUD vacancies',
#     content_type=content_type
# )
# user.user_permissions.add(permission)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        if next:
            return render(request, 'login.html', {'form': MyAuthenticationForm(), 'next': next})
        return render(request, 'login.html', {'form': MyAuthenticationForm()})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        username_exist = User.objects.filter(email=username)
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next')
                if next:
                    current_site = get_current_site(request)
                    print(current_site)
                    domain = request.get_host()
                    return redirect(f"{domain}{next}")
                return redirect('profile', user.id)
        if username_exist:
            messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Invalid email')
        return redirect('login')


class LogoutView(View):
    def get(self, request):
        return logout_then_login(request, login_url='/login')
        #logout(request)


class PasswordChangeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            return render(request, 'password/change/change.html', {'form': MyPasswordChangeForm(user)})
        return redirect('login')

    def post(self, request):
        form = MyPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('profile', user.id)
        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('password_change')


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'password/reset/reset.html', {'form': MyPasswordResetForm()})

    def post(self, request):
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email')
                return redirect('password_reset')
            
            context = {
                "user": user, 
                'domain': request.get_host(),
                "uid": urlsafe_base64_encode(force_bytes(user.id)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https://'
            }

            url = reverse(
                'password_reset_completed', 
                kwargs={
                    'uidb64': context['uid'],
                    'token': context['token']
                }
            )

            link = f"{context['protocol']}{context['domain']}{url}"
            subject = "Password Reset Instruction"
            message = f"To reset your password click at this link:\n{link}"
            send_mail(
                subject, 
                message,
                EMAIL_HOST_USER, 
                [user.email], 
                fail_silently=False
            )

            return redirect('password_reset_link')
        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('password_reset')


class PasswordResetLinkView(View):
    def get(self, request):
        return render(request, 'password/reset/link.html')


class PasswordResetCompletedView(View):
    def get(self, request, *args, **kwargs):
        try:
            user_id = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, kwargs['token']):
                messages.error(request, 'Invalid link, get a new one')
                return redirect('password_reset')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return redirect('password_reset')
        
        context = {
            'form': MyPasswordSetForm(user),
            'uidb64': kwargs['uidb64'], 
            'token': kwargs['token']
        }
        return render(request, 'password/reset/set.html', context)

    def post(self, request, *args, **kwargs):
        try:
            user_id = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return redirect('password_reset')
        
        form = MyPasswordSetForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'password/reset/completed.html')

        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('password_reset')


def error_400(request, exception):
    return render(request, 'errors/400.html')


def error_403(request, exception):
    return render(request, 'errors/403.html')


def error_404(request, exception):
    return render(request, 'errors/404.html')


def error_500(request):
    return render(request, 'errors/500.html')
