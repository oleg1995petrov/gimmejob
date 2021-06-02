from datetime import date

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import logout_then_login
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.db.models.query import RawQuerySet
from django.forms import formset_factory, inlineformset_factory, modelformset_factory, Select
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic import DetailView, ListView, UpdateView, View

from app import widgets

from . import services
from .forms import *
from .mixins import VacancyFilterMixin
from .models import Applicant, Employer, Education, Experience, User, Vacancy, Language, ApplicantLanguage


class HomeView(View):
    """Home page View"""

    def get(self, request, *args, **kwargs):
        # Vacancy.objects.bulk_create(
        #     [Vacancy(
        #         active=True,
        #         position=f'Python Developer {i}',
        #         experience='noExp',
        #         employment='ftime',
        #         schedule='fday',
        #         body='Test',
        #         employer_id=1
        #     ) for i in range(21)]
        # )  
        if request.user.is_anonymous:
            return redirect('login')
        return render(request, 'home.html')


  # @method_decorator(permission_required('app.view_user'))
# @method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):#( View):
    """Profile View"""

    model = User
    template_name = None
    slug_field = 'pk'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.is_employer:
            context['vacancies'] = Vacancy.objects.filter(
                employer=self.object.employer, active=True).only('id', 'position')
           
        return context
  
    def dispatch(self, request, *args, **kwargs):
        try:
            obj = super().get_object()
            if obj.is_employer:
                self.template_name = 'profile-employer.html'
            else:
                self.template_name = 'profile-applicant.html'
        except Http404:
            return render(request, 'errors/unexist_profile.html')
        return super().dispatch(request)


class EditPersonalView(View):
    """View for editing user's personal data"""

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_applicant:
                applicant = request.user.applicant
                CATEGORIES = ['education', 'career', 'languages']
                category = request.GET.get('cat')

                user_form = ApplicantEditForm(instance=request.user)
                profile_form = ApplicantProfileForm(instance=applicant)
                education_form = EducationForm(instance=applicant)
                
                template = 'edit_applicant.html'
                context = {
                    'applicant': applicant,
                    'category': category,
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'education_form': education_form,
                    'categories': CATEGORIES,
                }

                if category == 'career':
                    if applicant.experience.exists():
                        experience_formset = modelformset_factory(Experience, form=ExperienceForm, extra=1)
                        experience_forms = experience_formset(queryset=Experience.objects.filter(applicant=applicant))
                        context['experience_forms'] = experience_forms
                    else:
                        context['experience_form'] = ExperienceForm()
                elif category == 'languages':
                    if applicant.languages.exists():
                        language_formset = modelformset_factory(Language, form=LanguageForm, extra=1)
                        language_forms = language_formset(queryset=Language.objects.filter(applicant=applicant))
                        context['language_forms'] = language_forms
                    else:
                        context['language_form'] = LanguageForm()
                

            # else:
            #     employer = request.user.employer
            #     user_form = EmployerEditForm(instance=employer.user)
            #     profile_form = EmployerProfileForm(instance=employer)
            #     template = 'edit_employer.html'
            #     context = {
            #         'user_form': user_form,
            #         'profile_form': profile_form, 
            #     }

            return render(request, template, context)
        return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            has_errors = False
            if request.user.is_applicant:
                applicant = request.user.applicant
            # else:
            #     employer = request.user
            #     user_form = EmployerEditForm(
            #         instance=employer, 
            #         data=request.POST
            #     )
            #     profile_form = EmployerProfileForm(
            #         instance=employer, 
            #         data=request.POST, 
            #     )
                # USER_FORM & PROFILE_FORM

                # delete_exp = request.POST.get('delete_exp')
                # if delete_exp:
                #     delete_exp = int(delete_exp)
                #     Experience.objects.get(id=delete_exp).delete()

                if 'first_name' in request.POST:
                    user_form = ApplicantEditForm(
                        instance=request.user,
                        data=request.POST,
                    )
                    if user_form.is_valid():
                        user_form.save()
                    for error in user_form.errors:
                        messages.error(request, user_form.errors[error])
                        has_errors = True

                    profile_form = ApplicantProfileForm(
                        instance=applicant,
                        data=request.POST,
                    )
                    if profile_form.is_valid():
                        profile_form.save()
                    for error in profile_form.errors:
                        messages.error(request, profile_form.errors[error])
                        has_errors = True
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal'))

                # EDUCATION_FORM
                if 'education' in request.POST:
                    education_form = EducationForm(
                        instance=applicant,
                        data=request.POST,
                    )
                    if education_form.is_valid():
                        education_form.save()
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal') + f'?cat=education')

                # EXPERIENCE_FORM                    
                if 'form-0-position' in request.POST:
                    experience_formset = modelformset_factory(Experience, form=ExperienceForm)
                    experience_forms = experience_formset(request.POST)
                    if experience_forms.is_valid():
                        experience_forms.save(commit=False)
                        for form in experience_forms:
                            cd = form.cleaned_data
                            begin = cd.get('begin')
                            position = cd.get('position')
                            if not begin or not position:
                                continue
                            form.instance.applicant = applicant
                            form.save()
                    for form in experience_forms:
                        for error in form.errors:
                            messages.error(request, form.errors[error])
                            has_errors = True
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal') + f'?cat=career')
                
                if 'position' in request.POST:
                    experience_form = ExperienceForm(request.POST)
                    if experience_form.is_valid():
                        experience_form.save(commit=False)
                        experience_form.instance.applicant = applicant
                        experience_form.save()
                    for error in experience_form.errors:
                        messages.error(request, experience_form.errors[error])
                        has_errors = True
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal') + f'?cat=career')
                
                # LANGUAGE_FORM
                if 'language' in request.POST:
                    language_form = LanguageForm(request.POST)
                    if language_form.is_valid():
                        cd = language_form.cleaned_data
                        lang = cd['language']
                        lvl = cd['level']
                        if lang: 
                            new_lang, created = Language.objects.get_or_create(
                                language=lang, level=lvl
                            )
                            new_lang.applicant.add(applicant)
                    for error in language_form.errors:
                        messages.error(request, language_form.errors[error])
                        has_errors = True
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal') + f'?cat=languages')
                if 'form-0-language' in request.POST:
                    language_formset = modelformset_factory(Language, form=LanguageForm)
                    language_forms = language_formset(request.POST)
                    if language_forms.is_valid():
                        for form in language_forms:
                            cd = form.cleaned_data
                            lang = cd.get('language')
                            lvl = cd.get('level')
                            if not lang:
                                continue
                            new_lang, created = Language.objects.get_or_create(
                                language=lang, level=lvl
                            )
                            entries = ApplicantLanguage.objects.filter(applicant_id=applicant.id)
                            if entries.exists():
                                language = Language.objects.filter(language=lang, applicant=applicant).first()
                                if language:
                                    if language.level != lvl:
                                        language.applicant.remove(applicant)
                                        new_lang.applicant.add(applicant)
                                else:
                                    new_lang.applicant.add(applicant)
                            else:
                                new_lang.applicant.add(applicant)
                                        
                    for form in language_forms:
                        for error in form.errors:
                            messages.error(request, form.errors[error])
                            has_errors = True
                    services.message_succes(request, has_errors=has_errors)
                    return redirect(reverse('edit_personal') + f'?cat=languages')

            # if not has_errors:
            #     messages.success(
            #         request,
            #         mark_safe('<b>Изменения сохранены.</b><br>Ваш профиль был успешно обновлен.')
            #     )
            # print(request.POST)
        return redirect('login')


# class ExperienceDelete(View):
#     def post(self, request, id):
#         pk = int(id)
#         Experience.objects.get(pk=pk).delete()
#         return redirect(reverse('edit_personal') + f'?cat=career')


class EditPhotoView(View):
    """View for editing users' photo"""

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.is_applicant:
            # if not user.is_employer:
            #     form = PhotoForm(instance=user.employer)
            # else:
                form = PhotoForm(instance=user.applicant)
                context = {'form': form}
                return render(request, 'edit_photo.html', context)
            return redirect('profile', user.id)
        return redirect(reverse('login') + services.get_next_path(request))

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.is_applicant:
                form = PhotoForm(
                    instance=user.applicant, 
                    data=request.POST,
                    files=request.FILES
                )
            # else:
            #     form = PhotoForm(
            #         instance=user.employer,
            #         data=request.POST,
            #         files=request.FILES
            #     )
            if form.is_valid():
                form.save()

            for error in form.errors:
                messages.error(request, form.errors[error])

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
            print(request.POST)
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


# LANGUAGES
class AddLanguageView(View):
    """View for adding applicant's language"""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        context = {
            'form': LanguageForm()
        }
        return render(request, 'add_language.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        form = LanguageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            lang = cd.get('language')
            lvl = cd.get('level')
            new_lang, _ = Language.objects.get_or_create(
                language=lang, level=lvl
            )
            entries = ApplicantLanguage.objects.filter(applicant_id=request.user.applicant.id)
            if entries.exists():
                language = Language.objects.filter(
                    language=lang, applicant=request.user.applicant).first()
                if language:
                    if language.level != lvl:
                        language.applicant.remove(request.user.applicant)
            new_lang.applicant.add(request.user.applicant)

            has_errors = False
            for error in form.errors:
                messages.error(request, form.errors[error])
                has_errors = True
            services.message_succes(request, has_errors=has_errors)
            return redirect('profile', request.user.id)


class EditLanguageView(View):
    """View for editing applicant's language"""

    def dispatch(self, request, lang_id):
        method = request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(request, lang_id)
        return super().dispatch(request, lang_id)

    def get(self, request, lang_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            lang = request.user.applicant.languages.get(pk=lang_id)
        except Language.DoesNotExist:
            return render(request, 'errors/404.html')

        context = {
            'form': LanguageForm(instance=lang),
            'lang': lang,
        }
        return render(request, 'edit_language.html', context)

    def post(self, request, lang_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            lang = request.user.applicant.languages.get(pk=lang_id)
        except Language.DoesNotExist:
            return render(request, 'errors/404.html')

        form = LanguageForm(request.POST, instance=lang)
        if form.is_valid():
            form.save()
        has_errors = False
        for error in form.errors:
            messages.error(request, form.errors[error])
            has_errors = True
        services.message_succes(request, has_errors=has_errors)
        return redirect('profile', request.user.id)

    def delete(self, request, lang_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            lang = request.user.applicant.languages.get(pk=lang_id)
        except Language.DoesNotExist:
            return render(request, 'errors/404.html')

        lang.delete()
        return redirect('profile', request.user.id)
# LANGUAGE END


# EDUCATION
class AddEducationView(View):
    """View for adding applicant's work experience"""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        context = {
            'form': EducationForm(),
        }
        return render(request, 'add_education.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        form = EducationForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.applicant = request.user.applicant
            form.save()

        has_errors = False
        for error in form.errors:
            messages.error(request, form.errors[error])
            has_errors = True
        services.message_succes(request, has_errors=has_errors)
        return redirect('profile', request.user.id)


class EditEducationView(View):
    """View for editing applicant's work experience"""

    def dispatch(self, request, edu_id):
        method = request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(request, edu_id)
        return super().dispatch(request, edu_id)

    def get(self, request, edu_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            edu = request.user.applicant.education.get(pk=edu_id)
        except Education.DoesNotExist:
            return render(request, 'errors/404.html')

        context = {
            'form': EducationForm(instance=edu),
            'edu': edu,
        }
        return render(request, 'edit_education.html', context)

    def post(self, request, edu_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            edu = request.user.applicant.education.get(pk=edu_id)
        except Experience.DoesNotExist:
            return render(request, 'errors/404.html')

        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save()
        has_errors = False
        for error in form.errors:
            messages.error(request, form.errors[error])
            has_errors = True
        services.message_succes(request, has_errors=has_errors)
        return redirect('profile', request.user.id)

    def delete(self, request, edu_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            edu = request.user.applicant.education.get(pk=edu_id)
        except Experience.DoesNotExist:
            return render(request, 'errors/404.html')

        edu.delete()
        return redirect('profile', request.user.id)
# EDUCATION END


# WORK EXPERIENCE
class AddExperienceView(View):
    """View for adding applicant's work experience"""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)
     
        context = {
            'form': ExperienceForm(),
        }
        return render(request, 'add_experience.html', context)
    
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)
    
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.applicant = request.user.applicant
            form.save()

        has_errors = False
        for error in form.errors:
            messages.error(request, form.errors[error])
            has_errors = True
        services.message_succes(request, has_errors=has_errors)
        return redirect('profile', request.user.id)
    

class EditExperienceView(View):
    """View for editing applicant's work experience"""

    def dispatch(self, request, exp_id):
        method = request.POST.get('method', '').lower()
        if method == 'delete':
            return self.delete(request, exp_id)
        return super().dispatch(request, exp_id)

    def get(self, request, exp_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            exp = request.user.applicant.experience.get(pk=exp_id)
        except Experience.DoesNotExist:
            return render(request, 'errors/404.html')

        context = {
            'form': ExperienceForm(instance=exp),
            'exp': exp,
        }
        return render(request, 'edit_experience.html', context)

    def post(self, request, exp_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))
        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            exp = request.user.applicant.experience.get(pk=exp_id)
        except Experience.DoesNotExist:
            return render(request, 'errors/404.html')

        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
        has_errors = False
        for error in form.errors:
            messages.error(request, form.errors[error])
            has_errors = True
        services.message_succes(request, has_errors=has_errors)
        return redirect('profile', request.user.id)
    
    def delete(self, request, exp_id):
        if not request.user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not request.user.is_applicant:
            return redirect('profile', request.user.id)

        try:
            exp = request.user.applicant.experience.get(pk=exp_id)
        except Experience.DoesNotExist:
            return render(request, 'errors/404.html')

        exp.delete()
        return redirect('profile', request.user.id)
# WORK EXPERIENCE END

        
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

    def get(self, request):   
        add = request.GET.get('add')
        edit = request.GET.get('edit')
        delete = request.GET.get('delete')
        user = self.request.user

        if not user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

        if not user.company:
            return redirect('profile', user.id)

        context = {'user': user}
        
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
        
    def post(self, request):
        add = request.POST.get('add')
        edit = request.POST.get('edit')
        delete = request.POST.get('delete')
        user = request.user

        if not user.is_authenticated:
            return redirect(reverse('login') + services.get_next_path(request))

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

            form = VacancyForm(request.POST, instance=vacancy)
            
            if form.is_valid():
                form.save()

            return redirect('vacancy_list')
        
        if delete and not edit and not add:
            try:
                vacancy_id = int(delete)
                vacancy = user.employer.vacancies.get(pk=vacancy_id)
            except ValueError:
                return render(request, 'errors/400.html', status=400)
            except Vacancy.DoesNotExist:
                return render(request, 'errors/unexist_vacancy.html')

            Vacancy.objects.get(pk=vacancy_id).delete()
            return redirect('vacancy_list')

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
            'vacancy': vacancy, 
            'body': vacancy.body,
        }

        if not vacancy.is_active:
            if not user == vacancy.employer.user:
                return render(self.request, 'errors/unexist_vacancy.html')
            context['form'] = VacancyForm(instance=vacancy)
            return render(self.request, 'edit_vacancy.html', context)
           
        return render(self.request, 'vacancy_detail.html', context)


# SEARCH
class SearchView(View):
    def get(self, request):
        pass

class VacancySearchView(VacancyFilterMixin, ListView):
    """View for vacancy searching"""

    queryset = Vacancy.objects.filter(active=True)
    template_name = 'vacancy_search.html'
    paginate_by = 10
    paginate_orphans = 1
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
    
        page_object = context['page_obj']
        curr_page = page_object.number
        num_pages = page_object.paginator.num_pages
        
        context['count'] = page_object.paginator.count
        context['start'] = (curr_page - 1) * self.paginate_by + 1
        context['end'] = context['start'] + self.paginate_by - 1 if curr_page != num_pages else context['count']

        context['experience0'] = super().get_vacancy_experience()
        context['employment0'] = super().get_vacancy_employment()
        context['schedule0'] = super().get_vacancy_schedule()

        context["experience"] = ''.join([f"experience={x}&" for x in self.request.GET.getlist("experience")])
        context["employment"] = ''.join([f"employment={x}&" for x in self.request.GET.getlist("employment")])
        context["schedule"] = ''.join([f"schedule={x}&" for x in self.request.GET.getlist("experience")])
        context["employer_id"] = ''.join([f"employer_id={x}&" for x in self.request.GET.getlist("employer")])
        context['employer_query'] = self.request.GET.get('employer')
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset

        if self.request.GET.get('employer'):
            queryset = queryset.filter(
                Q(employer__user__company__icontains=self.request.GET.get('employer'))
            )
            return queryset

        if self.request.GET.get('employer_id'):
            try:
                emp_id = int(self.request.GET['employer_id'])
            except ValueError:
                emp_id = 0
            # queryset = queryset.filter(Q(employer__user__company__icontains=self.request.GET['employer']))
            queryset = queryset.filter(Q(employer_id=emp_id))

        if self.request.GET.get('experience') or (
            self.request.GET.get('employment')) or (
            self.request.GET.get('schedule')):
            queryset = queryset.filter(
                Q(experience__in=self.request.GET.getlist('experience'))#&
                # Q(employment__in=self.request.GET.getlist('employment'))
                # Q(schedule__in=self.request.GET.getlist('schedule'))
            ).distinct()
        
        # if self.request.GET.get('experience'):
        #     queryset = queryset.filter(Q(experience__in=self.request.GET.getlist('experience')))
     
        # if self.request.GET.get('employment'):
        #     queryset = queryset.filter(Q(employment__in=self.request.GET.getlist('employment')))

        # if self.request.GET.get('schedule'):
        #     queryset = queryset.filter(Q(schedule__in=self.request.GET.getlist('schedule')))
        print(self.request.GET.getlist('employment'))
        return queryset


class EmployerSearchView(ListView):
    """View for vacancy searching"""

    queryset = Employer.objects.select_related('user'
                                                    ).prefetch_related('vacancies'
                                                    ).only('user__company'
                                                    ).annotate(count=Count('vacancies')
                                                    ).order_by('user__company')
    template_name = 'employer_search.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        
        if self.request.GET.get('employer'):
            context["employer"] = self.request.GET.get("employer")
        return context
        
    def get_queryset(self, **kwargs):
        queryset = self.queryset
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
