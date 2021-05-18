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
    (('Беларусь'), (
        ('Brest', _('Brest')),
        ('Гродно', _('Гродно')),
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

COUNTRIES = [
    (None, '------------'),
    ('Беларусь', 'Беларусь'),
    ('Russia', 'Russia'),
    ('Ukraine', 'Ukraine'),
    ('Lithuania', 'Lithuania'),
    ('Latvia', 'Latvia'),
    ('Poland', 'Poland'),
    ('Estonia', 'Estonia')
]

SKILLS = [
    ('driving licence B', _('Водительское удостоверение категории В')),
    ('strees_tolerance', _('Стрессоустойчивость')),
    ('ms_office', _('МС Офис')),
    ('grammatically_correct_speech', _('Грамотная речь')),
    ('teamwork', _('Командная работа')),
    ('literacy', _('Грамотность')),
    ('corporate_ethics', _('Корпоративная этика')),
    ('negotiation', _('Ведение переговоров')),
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
    ('ИТ', _('ИТ'))
]

EDUCATION = [
    (None, '------------'),
    ('Школа', _('Hight school diploma')),
    ("Колледж", _("Associate’s")),
    ("Бакалавр", _("Бакалавр")),
    ("Мастер", _("Master’s")),
    ('Доктор', _('Doctoral'))
]

SPECIALIZATION = [
    (None, '------------'),
    ('Экономист', _('Экономист')),
    ('Lawyer', _('Lawyer')),
    ('Инженер', _('Инженер')),
    ('Разработчик ПО', _('Разработчик ПО')),
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
    ('ftime', _('Полная занятость')),
    ('ptime', _('Частичная занятость')),
    ('trainee', _('Стажировка'))
)

SCHEDULE = (
    ('fday', _('Полный день')),
    ('shift', _('Сменный график')),
    ('flex', _('Гибкий график')),
    ('remote', _('Удаленная работа'))
)

CURRENCY = (
    (None, '------------'),
    ('BYN', 'BYN'),
    ('RUB', 'RUB'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
)
