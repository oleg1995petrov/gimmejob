from datetime import date
from django.utils.translation import gettext_lazy as _


YEAR_MIN = date.today().year - 10
YEAR_MAX = YEAR_MIN - 100
YEARS = [year for year in range(YEAR_MIN, YEAR_MAX, -1)]
YEAR_NOW = date.today().year
YEAR_MIN_WORK = YEAR_NOW - 60
WORK_YEARS = [year for year in range(YEAR_NOW, YEAR_MIN_WORK, -1)]

LOCATION = [
    (_('Belarus'), (
        ('Brest', _('Brest')),
        ('Grodno', _('Grodno')),
        ('Gomel', _('Gomel')),
        ('Minsk', _('Minsk')),
        ('Mogilev', _('Mogilev')),
        ('Vitebsk', _('Vitebsk')),
    )
    ),
    (_('Russia'), (
        ('Moscow', _('Moscow')),
    )
    ),
    (_('Poland'), (
        ('Warsaw', _('Warsaw')),
    )
    ),
    (_('Ukraine'), (
        ('Kiev', _('Kiev')),
    )
    ),
    (_('Lithuania'), (
        ('Vilnius', _('Vilnius')),
    )
    ),
    (_('Latvia'), (
        ('Riga', _('Riga')),
    )
    ),
    (_('Estonia'), (
        ('Tallinn', _('Tallinn')),
    )
    )
]

LANGUAGES = [
    ('russian', _('Russian')),
    ('belarussian', _('Belorussian')),
    ('english', _('English')),
    ('ukrainian', _('Ukrainian')),
    ('lithuanian', _('Lithuanian')),
    ('latvian', _('Latvian')),
    ('polish', _('Polish')),
    ('estonian', _('Estonian')),
    ('german', _('German')),
    ('french', _('French')),
    ('spanish', _('Spanish')),
    ('chinese', _('Chinese')),
    ('japanese', _('Japanese'))
]

COUNTRIES = [
    ('Republic of Belarus', 'Republic of Belarus'),
    ('Russian Federation', 'Russian Federation'),
    ('Ukraine', 'Ukraine'),
    ('Republic of Lithuania', 'Republic of Lithuania'),
    ('Republic of Latvia', 'Republic of Latvia'),
    ('Republic of Poland', 'Republic of Poland'),
    ('Republic of Estonia', 'Republic of Estonia')
]

SKILLS = [
    ('driving_licence_b', _('Driving licence B')),
    ('strees_tolerance', _('Stress tolerance')),
    ('ms_office', _('MS Office')),
    ('grammatically_correct_speech', _('Grammatically correct speech')),
    ('teamwork', _('Teamwork')),
    ('literacy', _('Literacy')),
    ('corporate_ethics', _('Corporate ethics')),
    ('negotiation', _('Negotiation'))
]

SPHERES = [
    ('energetics', _('Energetics')),
    ('financial_sector', _('Financial sector')),
    ('chemical_industry', _('The chemical industry')),
    ('art', _('Art and culture')),
    ('education', _('Education')),
    ('medecine', _('Medicine')),
    ('retail', _('Retail')),
    ('car_business', _('Car business')),
    ('it', _('Information Technology'))
]

EDUCATION = [
    ('high school', _('Hight school diploma')),
    ('associate', _("Associate’s degree")),
    ('bachelor', _("Bachelor’s degree")),
    ('master', _("Master’s degree")),
    ('doctoral', _('Doctoral degree'))
]

SPECIALIZATION = [
    ('economist', _('Economist')),
    ('lawyer', _('Lawyer')),
    ('engineer', _('Engineer')),
    ('architect', _('Architect')),
    ('teacher', _('Teacher')),
    ('driver', _('Driver')),
    ('cook', _('Cook')),
    ('seller', _('Seller')),
    ('manager', _('Manager'))
]

NEED_EXP = [
    ('not_required', _('No experience')),
    ('1-3_years', _('From 1 to 3 years')),
    ('1-6_years', _('From 3 to 6 years')),
    ('over_6_years', _('Over 6 years'))
]

EMPLOYMENT = [
    ('full_time', _('Full-time')),
    ('part_time', _('Part-time')),
    ('traineeship', _('Traineeship'))
]

SCHEDULE = [
    ('full', _('Full day')),
    ('shift', _('Shift work')),
    ('flexible ', _('Flexible schedule')),
    ('remote', _('Remote work'))
]
