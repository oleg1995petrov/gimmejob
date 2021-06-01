from datetime import date
from django.utils.translation import gettext_lazy as _


YEAR_MIN = date.today().year - 10
YEAR_MAX = YEAR_MIN - 100
YEAR_NOW = date.today().year
YEAR_MIN_WORK = YEAR_NOW - 60

YEARS = [year for year in range(YEAR_MIN, YEAR_MAX, -1)]
WORK_YEARS = [year for year in range(YEAR_NOW, YEAR_MIN_WORK, -1)]

LOCATION2 = [
    (None, '---'),
    (('Belarus'), (
        ('Brest', _('Brest')),
        ('Hrodna', _('Hrodna')),
        ('Lida', _('Lida')),
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

LOCATION = [
    (None, '---'),
    (('Беларусь'), (
        ('Brest', _('Brest')),
        ('Hrodna', _('Hrodna')),
        ('Лида', _('Лида')),
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
    (None, '---'),
    ('Русский', _('Русский')),
    ('Беларусский', _('Беларусский')),
    ('Английский', _('Английский')),
    ('Украинский', _('Украинский')),
    ('Литовский', _('Литовский')),
    ('Латвийский', _('Латвийский')),
    ('Польский', _('Польский')),
    ('Эстонский', _('Эстонский')),
    ('Немецкий', _('Немецкий')),
    ('Французский', _('Французский')),
    ('Испанский', _('Испанский')),
    ('Китайский', _('Китайский')),
    ('Японский', _('Японский'))
]

LANGUAGES2 = [
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
    ('Japanese ', _('Japanese'))
]

LANGUAGE_LEVELS = [
    (None, '---'),
    ('A1', _('A1')),
    ('A2', _('A2')),
    ('B1', _('B1')),
    ('B2', _('B2')),
    ('C1', _('C1')),
    ('C2', _('C2'))
]

COUNTRIES2 = [
    (None, '---'),
    ('Belarus', 'Belarus'),
    ('Russia', 'Russia'),
    ('Ukraine', 'Ukraine'),
    ('Lithuania', 'Lithuania'),
    ('Latvia', 'Latvia'),
    ('Poland', 'Poland'),
    ('Estonia', 'Estonia')
]

COUNTRIES = [
    (None, '---'),
    ('Беларусь', 'Беларусь'),
    ('Russia', 'Russia'),
    ('Ukraine', 'Ukraine'),
    ('Lithuania', 'Lithuania'),
    ('Latvia', 'Latvia'),
    ('Poland', 'Poland'),
    ('Estonia', 'Estonia')
]

SKILLS2 = [
    ('Driving licence B', _('Driving licence B')),
    ('Strees tolerance', _('Strees tolerance')),
    ('MS Office', _('MS Office')),
    ('Grammatically correct speech', _('Grammatically correct speech')),
    ('Teamwork', _('Teamwork')),
    ('Literacy', _('Literacy')),
    ('Corporate ethics', _('Corporate_ethics')),
    ('Negotiation', _('Negotiation')),
]

SKILLS = [
    ('Водительское удостоверение категории В', _('Водительское удостоверение категории В')),
    ('Стрессоустойчивость', _('Стрессоустойчивость')),
    ('МС Офис', _('МС Офис')),
    ('Грамотная речь', _('Грамотная речь')),
    ('Командная работа', _('Командная работа')),
    ('Грамотность', _('Грамотность')),
    ('Корпоративная этика', _('Корпоративная этика')),
    ('Ведение переговоров', _('Ведение переговоров')),
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
    ('ИТ', _('IT'))
]

DEGREE = [
    (None, '---'),
    ('High School Diploma', _('High school diploma')),
    ("Associate degree", _("Associate’s degree")),
    ("Бакалавр", _("Бакалавр")),
    ("Мастер", _("Мастер")),
    ('Доктор', _('Доктор'))
]

DEGREE2 = [
    (None, '---'),
    ('High School Diploma', _('High school diploma')),
    ("Associate degree", _("Associate’s degree")),
    ("Bachelor's degree", _("Bachelor's degree")),
    ("Master's degree", _("Master's degree")),
    ('Doctoral degree', _('Doctoral degree'))
]

SPECIALIZATION = [
    (None, '---'),
    ('Экономист', _('Экономист')),
    ('Lawyer', _('Lawyer')),
    ('Инженер', _('Инженер')),
    ('Architect', _('Architect')),
    ('Teacher', _('Teacher')),
    ('Driver', _('Driver')),
    ('Cook', _('Cook')),
    ('Seller', _('Seller')),
    ('Manager', _('Manager'))
]

SPECIALIZATION2 = [
    (None, '---'),
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

EXPERIENCE = (
    ('noExp', _('Без опыта')),
    ('from1To3', _('От 1 года до 3 лет')),
    ('from3To6', _('От 3 до 6 лет')),
    ('over6', _('Более 6 лет'))
)

EMPLOYMENT = (
    (None, '---'),
    ('ftime', _('Полная занятость')),
    ('ptime', _('Частичная занятость')),
    ('trainee', _('Стажировка')),
    ('profedu', _('Профессиональное обучение')),
    ('business', _('Предприниматель')),
    ('free', _('Фриланс')),
)

SCHEDULE = (
    ('fday', _('Полный день')),
    ('shift', _('Сменный график')),
    ('flex', _('Гибкий график')),
    ('remote', _('Удаленная работа'))
)

CURRENCIES = (
    (None, '---'),
    ('BYN', 'BYN'),
    ('RUB', 'RUB'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
)



