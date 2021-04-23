from datetime import date
from django.utils.translation import gettext_lazy as _


YEAR_MIN = date.today().year - 10
YEAR_MAX = YEAR_MIN - 100
YEAR_NOW = date.today().year
YEAR_MIN_WORK = YEAR_NOW - 60

YEARS = [year for year in range(YEAR_MIN, YEAR_MAX, -1)]
WORK_YEARS = [year for year in range(YEAR_NOW, YEAR_MIN_WORK, -1)]

LOCATION = [
    (None, '------------'),
    (('Belarus'), (
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
    ('Russian', _('Russian')),
    ('Belarussian', _('Belarussian')),
    ('English', _('English')),
    ('Ukrainian', _('Ukrainian')),
    ('Lithuanian', _('Lithuanian')),
    ('Latvian', _('Latvian')),
    ('Polish', _('Polish')),
    ('Estonian', _('Estonian')),
    ('German', _('German')),
    ('French', _('French')),
    ('Spanish', _('Spanish')),
    ('Chinese', _('Chinese')),
    ('Japanese', _('Japanese'))
]

COUNTRIES = [
    (None, '------------'),
    ('Republic of Belarus', 'Republic of Belarus'),
    ('Russian Federation', 'Russian Federation'),
    ('Ukraine', 'Ukraine'),
    ('Republic of Lithuania', 'Republic of Lithuania'),
    ('Republic of Latvia', 'Republic of Latvia'),
    ('Republic of Poland', 'Republic of Poland'),
    ('Republic of Estonia', 'Republic of Estonia')
]

SKILLS = [
    ('driving licence B', _('Driving licence B')),
    ('strees_tolerance', _('Stress tolerance')),
    ('ms_office', _('MS Office')),
    ('grammatically_correct_speech', _('Grammatically correct speech')),
    ('teamwork', _('Teamwork')),
    ('literacy', _('Literacy')),
    ('corporate_ethics', _('Corporate ethics')),
    ('negotiation', _('Negotiation'))
]

SPHERES = [
    ('Energetics', _('Energetics')),
    ('Financial_sector', _('Financial sector')),
    ('Chemical_industry', _('The chemical industry')),
    ('Art and culture', _('Art and culture')),
    ('Education', _('Education')),
    ('Medecine', _('Medicine')),
    ('Retail', _('Retail')),
    ('Car_business', _('Car business')),
    ('IT', _('IT'))
]

EDUCATION = [
    (None, '------------'),
    ('High school', _('Hight school diploma')),
    ("Associate's", _("Associate’s")),
    ("Bachelor's", _("Bachelor’s")),
    ("Master's", _("Master’s")),
    ('Doctoral', _('Doctoral'))
]

SPECIALIZATION = [
    (None, '------------'),
    ('Economist', _('Economist')),
    ('Lawyer', _('Lawyer')),
    ('Engineer', _('Engineer')),
    ('Architect', _('Architect')),
    ('Teacher', _('Teacher')),
    ('Driver', _('Driver')),
    ('Cook', _('Cook')),
    ('Seller', _('Seller')),
    ('Manager', _('Manager'))
]

NEED_EXP = [
    (None, '------------'),
    ('', _('Нет опыта')),
    ('from 1 to 3 years', _('From 1 to 3 years')),
    ('1-6 years', _('From 3 to 6 years')),
    ('Over 6 years', _('Over 6 years'))
]

EMPLOYMENT = [
    ('Full-time', _('Full-time')),
    ('Part-time', _('Part-time')),
    ('Traineeship', _('Traineeship'))
]

SCHEDULE = [
    ('Full day', _('Full day')),
    ('Shift work', _('Shift work')),
    ('Flexible schedule', _('Flexible schedule')),
    ('Remote work', _('Remote work'))
]

CURRENCY = [
    (None, '------------'),
    ('BYN', 'BYN'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
    ('RUB', 'RUB')
]
