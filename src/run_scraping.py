import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *

from scraping.models import Vacancy, City, Language, Error

User = get_user_model()


parsers = (
    (work, 'https://rabota.by/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1002'),
    (hh, 'https://hh.ru/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1&customDomain=1'),

)

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

q = get_settings()
city = City.objects.filter(slug='minsk').first()
language = Language.objects.filter(slug='python').first()

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

#h = codecs.open('work.txt', 'w', 'utf-8')
#h.write(str(jobs))
#h.close()




