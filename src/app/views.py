from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import logout_then_login
from django.http import Http404

# from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from django.forms import modelformset_factory, formset_factory, inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import UpdateView 
from django.views.generic import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


from .forms import *
from .models import User, Applicant, Employer, Experience, Vacancy
from .filters import VacancyFilterSettings
from . import services


class HomeView(View):
    """Home page View"""

    def get(self, *args, **kwargs):
        return render(self.request, 'home.html')


# @method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):#( View):
    """Profile View"""

    model = User
    template_name = 'profile.html'
    slug_field = 'pk'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        context['user_view'] = self.object
        context['MEDIA_URL'] = settings.MEDIA_URL
        context['BADGES_URL'] = settings.BADGES_URL
        if self.object.company:
            context['vacancies'] = self.object.employer.vacancies.filter(active=True)
        return context

    # @method_decorator(login_required)
    @method_decorator(permission_required('app.view_user'))
    def dispatch(self, *args, **kwargs):
        try:
            super().get_object()
        except Http404:
            return render(self.request, 'errors/unexist_profile.html')

        return super().dispatch(self.request, *args, **kwargs)

    # permission_required = 'app.profile_view'

    #@method_decorator(login_required)
    # def get(self, request, *args, **kwargs):
    #     try:
    #         user_view = User.objects.get(pk=kwargs['user_id'])
    #     except User.DoesNotExist:
    #         return render(request, 'errors/unexist_profile.html')

        # context = {
        #     'user': request.user,
        #     'user_view': user_view,
        #     'MEDIA_URL': settings.MEDIA_URL,
        #     'BADGES_URL': settings.BADGES_URL,
        # }
        
        # if user_view.company:
        #     vacancies = user_view.employer.vacancies.all()
        #     context['vacancies'] = vacancies
        #     context['active_vacancies'] = vacancies.filter(active=True)
        #     context['inactive_vacancies'] = vacancies.filter(active=False)
        #     context['active_vacancies_count'] = vacancies.filter(active=True).count()

        # ANONYMOUS
        # if not request.user.is_authenticated:
        #     if not user_view.company:
        #         return redirect(reverse('login') + f'?next={request.get_full_path()}')
        # APPLICANT
        # elif request.user.is_authenticated and not request.user.company and (
        # not request.user.is_admin and request.user != user_view):
        #     if not user_view.company:
        #         return render(request, 'errors/403.html', status=403)

        #return render(request, 'profile.html', context)


class EditPersonalView(View):
    """View for editing user's personal data"""

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
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
                profile_form = ApplicantProfileForm(
                    instance=user.applicant, 
                    data=request.POST, 
                    files=request.FILES
                )
            else:
                user_form = EmployerEditForm(instance=user, data=request.POST)
                profile_form = EmployerProfileForm(
                    instance=user.employer, 
                    data=request.POST, 
                    files=request.FILES
                )

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


class EditPhotoView(View):
    """View for editing users' photo"""

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            if not user.company:
                form = PhotoForm(instance=user.applicant)
            else:
                form = PhotoForm(instance=user.employer)
            
            context = {'form': form}

            return render(request, 'edit_photo.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if not user.company:
                form = PhotoForm(
                    instance=user.applicant, 
                    data=request.POST, 
                    files=request.FILES)
            else:
                form = PhotoForm(
                    instance=user.employer, 
                    data=request.POST, 
                    files=request.FILES)
            if form.is_valid():
                form.save()

            return redirect('profile', request.user.id)
        return redirect('login')


class EditEducationView(View):
    """View for editing applicant's EDU"""
    
    def get(self, request):
        if request.user.is_authenticated:
            form = EducationForm(instance=request.user.applicant)
            context = {
                'form': form
            }

            return render(request, 'edit_education.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            form = EducationForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()

        return redirect('profile', user.id)


class EditSkillsView(View):
    """View for editing applicant's skills"""

    def get(self, request):
        if request.user.is_authenticated:
            form = SkillsForm(instance=request.user.applicant)
            context = {
                'form': form
            }

            return render(request, 'edit_skills.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            form = SkillsForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()

        return redirect('profile', request.user.id)


class EditLanguagesView(View):
    """View for editing applicant's languages"""

    def get(self, request):
        if request.user.is_authenticated:
            form = LanguagesForm(instance=request.user.applicant)
            context = {
                'form': form
            }

            return render(request, 'edit_languages.html', context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = LanguagesForm(instance=request.user.applicant, data=request.POST)
            if form.is_valid():
                form.save()

            return redirect('profile', user.id)
        return redirect('login')


class AddExperienceView(View):
    """View for adding applicant's Work Experience"""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')
        
        user = request.user

        if not user.applicant:
            return redirect('profile', user.id)

        context = { 
            'form': ExperienceForm(),
            'user': user,
        }

        return render(request, 'add_experience.html', context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')
            
        user = request.user
        
        if not user.applicant:
            return redirect('profile', user.id)
            
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            data = form.cleaned_data
            if not services.is_true_period(data):
                context = { 
                    'form': ExperienceForm(data),
                    'user': user
                }
                return render(request, 'add_experience.html', context)
            form.instance.applicant = user.applicant
            form.save()
        return redirect('profile', user.id)


class EditExperienceView(View):
    """View for editing applicant's Work Experience"""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')

        user = request.user
        if user.company:
            return redirect('profile', user.id)
        
        form_set = modelformset_factory(Experience, form=ExperienceForm, extra=0)
        forms = form_set(queryset=Experience.objects.filter(applicant=user.applicant))
        context = {
            'forms': forms, 
            'MEDIA_URL': settings.MEDIA_URL,
            'BADGES_URL': settings.BADGES_URL,
        }
        return render(request, 'edit_experience.html', context)
            

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')

        user = request.user
        if user.company:
            return redirect('profile', user.id)

        form_set = modelformset_factory(Experience, form=ExperienceForm)
        forms = form_set(request.POST)

        if forms.is_valid():
            forms.save(commit=False)
            for form in forms:
                data = form.cleaned_data
                if not services.is_true_period(data):
                    context = {
                        'forms': forms,
                        'MEDIA_URL': settings.MEDIA_URL,
                        'BADGES_URL': settings.BADGES_URL,
                    }
                    return render(request, 'edit_experience.html', context)
                form.instance.applicant = user.applicant
                form.save()
        return redirect('profile', user.id)
        

class DeleteExperienceView(View):
    """View for deliting applicant's Work Experience"""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')
        
        if request.user.company:
            return redirect('profile', request.user.id)

        applicant = request.user.applicant

        try:
            experience = Experience.objects.filter(pk=kwargs['experience_id']).filter(applicant=applicant).get()
        except Experience.DoesNotExist:
            return redirect('profile', request.user.id)

        return render(request, 'delete_work_exp.html', {'experience_id': experience.id})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')
        
        if request.user.company:
            return redirect('profile', request.user.id)

        applicant = request.user.applicant

        try:
            experience = Experience.objects.filter(pk=kwargs['experience_id']).filter(applicant=applicant).get()
        except Experience.DoesNotExist:
            return redirect('profile', request.user.id)

        experience.delete()
        return redirect('profile', request.user.id)


class RegistrationView(View):
    """View for register users"""

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'registration/registration.html')
        

class ApplicantRegistrationView(View):
    """View for register applicants"""

    def get(self, request):
        return render(request, 'registration/applicant.html', {'form': ApplicantCreationForm()})

    def post(self, request):
        user = ApplicantCreationForm(request.POST)
        if user.is_valid():
            user = user.save()
            #user = user.save(commit=False)
            #user.user_type = 'applicant'
            #user.save()
            Applicant.objects.create(user=user)
            #user = user.save()
            services.send_mail_registration(user)
            return render(request, 'registration/success.html', {'user': user})
        for error in user.errors:
            messages.error(request, user.errors[error])
        return redirect('registration_applicant')


class EmployerRegistrationView(View):
    """View for register employeers"""

    def get(self, request):
        return render(request, 'registration/employer.html', {'form': EmployerCreationForm()})

    def post(self, request):
        user = EmployerCreationForm(request.POST)
        if user.is_valid():
            user = user.save()
            Employer.objects.create(user=user)
            services.send_mail_registration(user)
            return render(request, 'registration/success.html', {'user': user})
        for error in user.errors:
            messages.error(request, user.errors[error])
        return redirect('registration_employer')


class EmployerVacancyView(View):
    """View only for employers for view all vacancies which it created"""

    def get(self, *args, **kargs):   
        add = self.request.GET.get('add')
        edit = self.request.GET.get('edit')
        delete = self.request.GET.get('delete')
        user = self.request.user

        if not user.is_authenticated:
            return redirect(reverse('login') + f'?next={self.request.get_full_path()}')

        if not user.company:
            return redirect('profile', user.id)

        context = {
            'user': user,
            'MEDIA_URL': settings.MEDIA_URL,
            'BADGES_URL': settings.BADGES_URL
        }
        
        if add == 'new' and (not edit and not delete):
            context['form'] = VacancyForm()
            return render(self.request, 'add_vacancy.html', context)
        elif edit and not add and not delete:
            try:
                vacancy_id = int(edit)
                vacancy = user.employer.vacancies.get(pk=vacancy_id)
            except ValueError:
                return render(self.request, 'errors/400.html', status=400)
            except Vacancy.DoesNotExist:
                return render(self.request, 'errors/unexist_vacancy.html')

            context['form'] = VacancyForm(instance=vacancy)# user.employer.vacancies.get(pk=vacancy_id))
            context['vacancy'] = vacancy
            return render(self.request, 'edit_vacancy.html', context)
        elif delete and (not add and not edit):
            try:
                vacancy_id = int(delete)
                vacancy = user.employer.vacancies.get(pk=vacancy_id)
            except ValueError:
                return render(self.request, 'errors/400.html', status=400)
            except Vacancy.DoesNotExist:
                return render(self.request, 'errors/unexist_vacancy.html')
            context['vacancy_id'] = vacancy.id
            return render(self.request, 'delete_vacancy.html', context)

        context['active_vacancies'] = Vacancy.objects.filter(employer=user.employer).filter(active=True)
        context['inactive_vacancies'] = Vacancy.objects.filter(employer=user.employer).filter(active=False)
        return render(self.request, 'vacancy_list.html', context)
        
    def post(self, request, *args, **kwargs):
        add = request.POST.get('add')
        edit = request.POST.get('edit')
        delete = request.POST.get('delete')
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse('login') + f'?next={request.get_full_path()}')

        if not user.employer:
            return render(request, 'errors/403.html', status=403)

        if add == 'new' and (not edit and not delete):
            form = VacancyForm(request.POST)

            if form.is_valid():
                form.save(commit=False)
                form.instance.employer = user.employer
                form.save()

            return redirect('vacancy_list')
            
        if edit and not add and not delete:
            try:
                vacancy_id = int(edit)
                vacancy = user.employer.vacancies.get(pk=vacancy_id)
            except ValueError:
                return render(request, 'errors/400.html', status=400)
            except Vacancy.DoesNotExist:
                return render(request, 'errors/unexist_vacancy.html')

            form = VacancyForm(request.POST, instance=vacancy)# user.employer.vacancies.get(pk=vacancy_id))
            
            if form.is_valid():
                form.save()

            return redirect('vacancy_detail', vacancy.id)
        
        if delete and not edit and not add:
            try:
                vacancy_id = int(delete)
                vacancy = user.employer.vacancies.get(pk=vacancy_id)
            except ValueError:
                return render(request, 'errors/400.html', status=400)
            except Vacancy.DoesNotExist:
                return render(request, 'errors/unexist_vacancy.html')

            Vacancy.objects.get(pk=vacancy_id).delete()
            return redirect('vacancy_detail')

        return render(request, 'errors/400.html', status=400)


class VacancyView(View):
    """View for view vacancies for all users with oppotunity edit/delete them if viewer is an employer who created it"""

    def get(self, *args, **kwargs):
        add = self.request.GET.get('add')
        edit = self.request.GET.get('edit')
        delete = self.request.GET.get('delete')
        user = self.request.user

        try:
            vacancy = Vacancy.objects.get(pk=kwargs.get('vacancy_id'))
        except Vacancy.DoesNotExist:
            return render(self.request, 'errors/unexist_vacancy.html')
                
        context = {
            'user': user,
            'MEDIA_URL': settings.MEDIA_URL,
            'BADGES_URL': settings.BADGES_URL,
            'vacancy': vacancy, 
            'body': vacancy.body,
            'employer': vacancy.employer
        }

        if not vacancy.is_active:
            if not user == vacancy.employer.user:
                return render(self.request, 'errors/unexist_vacancy.html')
            context['form'] = VacancyForm(instance=vacancy)
            return render(self.request, 'edit_vacancy.html', context)
           
        return render(self.request, 'vacancy.html', context)


# SEARCH


class VacancySearchView(ListView):
    """View for vacancy searching"""

    # queryset = Vacancy.objects.filter(active=True)
    template_name = 'vacancy_search.html'
    paginate_by = 5
    context_object_name = 'vacancies'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['experience0'] = {
            'Без опыта': 'noExperience', 
            'От 1 года до 3 лет': 'from1To3', 
            'От 3 до 6 лет': 'from3To6', 
            'Более 6 лет': 'over6'
        }
        context['employment0'] = {
            'Полная занятость': 'full',
            'Частичная занятость': 'part',
            'Стажировка': 'traineeship'
        }
        context['schedule0'] = {
            'Полный день': 'full',
            'Сменный график': 'shift',
            'Гибкий график': 'flexible',
            'Удаленная работа': 'remote'
        }

        context["experience"] = ''.join([f"experience={x}&" for x in self.request.GET.getlist("experience")])
        context["employment"] = ''.join([f"employment={x}&" for x in self.request.GET.getlist("employment")])
        context["schedule"] = ''.join([f"schedule={x}&" for x in self.request.GET.getlist("experience")])
        context["employer"] = ''.join([f"employer={x}&" for x in self.request.GET.getlist("employer")]) if self.request.GET.get("employer") else 'NONE'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = Vacancy.objects.filter(active=True)
        if self.request.GET.get('employer'):
            queryset = queryset.filter(Q(employer__user__company__icontains=self.request.GET.get('employer')))
        if self.request.GET.get('experience') or (
            self.request.GET.get('employment')) or (
            self.request.GET.get('schedule')):
            queryset = queryset.filter(
                Q(experience__in=self.request.GET.getlist('experience')),
                # Q(employment__in=self.request.GET.getlist('employment')),
                # Q(schedule__in=self.request.GET.getlist('schedule'))
            ).distinct()
        return queryset


class EmployerSearchView(ListView):
    """View for vacancy searching"""

    template_name = 'employer_search.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        
        if self.request.GET.get('employer'):
            context["employer"] = ''.join(
                [f"employer={x}&" for x in self.request.GET.get("employer")]
            )
        return context
        
    def get_queryset(self, **kwargs):
        queryset = Employer.objects.select_related('user').prefetch_related('vacancies').order_by('user__company')
        if self.request.GET.get('employer'):
            queryset = Employer.objects.filter(
                user__company__icontains=self.request.GET.get('employer')
            ).select_related(
                'user'
            ).prefetch_related(
                'vacancies'
            ).order_by(
                'user__company'
            )
        return queryset

    


# CRUD PERMISSIONS *(PRIME)
# content_type = ContentType.objects.get_for_model(Vacancy)
# permission, created = Permission.objects.get_or_create(
#     codename='CRUD_vacancies',
#     name='Can CRUD vacancies',
#     content_type=content_type
# )
# user.user_permissions.add(permission)


class LoginView(View):
    """View for logging in"""

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        if next:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'next': next})
        return render(request, 'login.html', {'form': AuthenticationForm()})

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
                    return redirect(next)
                return redirect('profile', user.id)
        if username_exist:
            messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Invalid email')
        return redirect('login')


class LogoutView(View):
    """View for logging out"""

    def get(self, request):
        return logout_then_login(request, login_url='/login')
        #logout(request)


class PasswordChangeView(View):
    """View for changing user's password"""

    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            return render(request, 'password/change/change.html', {'form': PasswordChangeForm(user)})
        return redirect('login')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
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
    """"View for reseting user's password by it email"""

    def get(self, request):
        return render(request, 'password/reset/reset.html', {'form': PasswordResetForm()})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email')
                return redirect('password_reset')
            
            domain = request.get_host()
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            url = reverse(
                'password_reset_complete', 
                kwargs={
                    'uidb64': uid,
                    'token': token
                }
            )

            link = f'https://{domain}{url}'
            subject = "Password Reset Instruction"
            message = f"To reset your password click at this link:\n{link}"
            send_mail(
                subject, 
                message,
                settings.EMAIL_HOST_USER, 
                [user.email], 
                fail_silently=False
            )

            return redirect('password_reset_link')
        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('password_reset')


class PasswordResetLinkView(View):
    """View for informate user about an email on it mail"""

    def get(self, request):
        return render(request, 'password/reset/link.html')


class PasswordResetCompleteView(View):
    """View for setting new user's password"""

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            user_id = int(force_str(urlsafe_base64_decode(uidb64)))
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, token):
                messages.error(request, 'Invalid link, get a new one')
                return redirect('password_reset')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return redirect('password_reset')
        
        context = {
            'form': PasswordSetForm(user),
            'uidb64': kwargs['uidb64'], 
            'token': kwargs['token']
        }
        return render(request, 'password/reset/set.html', context)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email')
            return redirect('password_reset')
        
        form = PasswordSetForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'password/reset/complete.html')

        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('password_reset')


def error_400(request, exception):
    """"""
    return render(request, 'errors/400.html')


def error_403(request, exception):
    """"""
    return render(request, 'errors/403.html')


def error_404(request, exception):
    """"""
    return render(request, 'errors/404.html')


def error_500(request):
    """"""
    return render(request, 'errors/500.html')
