from django.contrib import admin
from src.settings import AUTH_USER_MODEL, MEDIA_URL
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.auth.models import Permission, Group

from .models import Applicant, Education, Employer, Experience, Vacancy, User, Language, ApplicantLanguage


class ApplicantInline(admin.TabularInline): # or admin.StackedInline
    model = Applicant
    readonly_fields = ('photo', 'get_image', 'birthday', 'location', 'citizenship')#, 
                        # 'education', 'specialization', 'skills', 'languages')

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={ obj.photo.url } width="60" height="80">')
        except ValueError:
            return mark_safe(f'<img src={ MEDIA_URL }blank.png width="60" height="80">')

    get_image.short_description = 'Фото'


class EmployerInline(admin.TabularInline): # or admin.StackedInline
    model = Employer
    readonly_fields = ('photo', 'get_image', 'company_email', 'company_site', 'company_info', 
                        'company_spheres', )

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={ obj.photo.url } width="60" height="80">')
        except ValueError:
            return mark_safe(f'<img src={ MEDIA_URL }blank.png width="60" height="80">')

    get_image.short_description = 'Лого'


class VacancyInline(admin.TabularInline):  # or admin.StackedInline
    model = Vacancy
    readonly_fields = ('employer', 'published', 'position', 'body', 'active', 'experience',
                        'employment', 'schedule', 'salary', 'currency')
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_fullname', 'email', 'company', 'is_admin', 'is_superuser')
    list_display_links = ('id', 'get_fullname', 'email')
    list_filter = ('company', 'is_active', 'is_admin',  'applicant__location', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('id', 'last_login', 'company')
    # list_editable = ('is_admin',)
    inlines = [ApplicantInline, EmployerInline]
    save_on_top = True
    save_as = True
    fieldsets = (
        (None, {
            'fields': (('id', 'last_login', 'is_active', 'is_admin', 'is_superuser'),)
        }),
        (None, {
            'fields': (('first_name', 'last_name', 'email'),)
        }),
        (None, {
            'fields': (('password', 'company'),)
        }),
        ("Groups & Permissions", {
            'classes': ('collapse',),
            'fields': (('groups', 'user_permissions'),)
        }),
    )
    
    def get_fullname(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
    get_fullname.short_description = 'ФИО'

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.photo.url} width="60" height="80">')
        except (ValueError, AttributeError):
            return mark_safe(f'<img src={MEDIA_URL}blank.png width="60" height="80">')

    get_image.short_description = 'Фото/Лого'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        if not is_superuser:
            disabled_fields = {
                'is_superuser',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_image')
    list_display_links = ('user', 'get_image')
    list_filter = ('photo','birthday', 'location', 'citizenship')#, 'education', 
                    # 'specialization'), 'skills', 'languages')
    search_fields = ('photo', 'birthday', 'location', 'citizenship', 'user__first_name')#, 'education',
                    #  'specialization', 'skills', 'languages', )
    readonly_fields = ('user', 'photo', 'get_image', 'birthday', 'location', 'citizenship')#, 
                        # 'education', 'specialization', 'skills', 'languages')
    #inlines = [ExperienceInline]

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={ obj.photo.url } width="60" height="80">')
        except ValueError:
            return mark_safe(f'<img src={ MEDIA_URL }blank.png width="60" height="80">')

    get_image.short_description = 'Фото'


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_image')
    list_display_links = ('user', 'get_image')
    list_filter = ('company_spheres',)
    search_fields = ('company_email', 'company_site', 'company_info')
    readonly_fields = ('user', 'photo', 'get_image', 'company_email', 'company_site', 'company_info', 'company_spheres')
    inlines = [VacancyInline]

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={ obj.photo.url } width="60" height="60">')
        except ValueError:
            return mark_safe(f'<img src={ MEDIA_URL }blank.png width="60" height="60">')

    get_image.short_description = 'Лого'


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('employer', 'position', 'published', 'active')
    list_display_links = ('employer', 'published', 'position')
    search_fields = ('employer__user__company', 'position')
    list_filter = ('employer', 'position', 'published', 'active', 'experience', 'employment',
                    'schedule', 'salary', 'currency')
    readonly_fields = ('position', 'employer', 'published', 'active', 'body', 'experience', 'employment',
                        'schedule', 'salary', 'currency')
    save_on_top = True
    save_as = True
    list_editable = ('active',)
    actions = ['set_inactive', 'set_active']

    def set_inactive(self, request, queryset):
        row_update = queryset.update(active=False)

        self.message_user(request, f'{row_update} вакансия(и,й) скрыта(ы)')

    set_inactive.short_description = 'Скрыть'
    set_inactive.allowed_permissions = ('change',)

    def set_active(self, request, queryset):
        row_update = queryset.update(active=True)

        self.message_user(request, f'{row_update} вакансия(и,й) опубликована(ы)')

    set_active.short_description = 'Опубликовать'
    set_active.allowed_permissions = ('change',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    # list_display = ('name', 'permissions')

    def get_perm(self):
        return Group.objects.filter()


admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users')
    readonly_fields = ('name', 'get_users')

    def get_users(self, obj):
        users = User.objects.filter(groups=obj)
        return ', '.join([str(u) for u in users[:10]])

    get_users.short_description = 'Пользователи'


admin.site.register(Language)
admin.site.register(ApplicantLanguage)
admin.site.register(Education)
admin.site.register(Experience)





admin.site.site_title = 'GimmeJob'
admin.site.site_header = 'GimmeJob'
