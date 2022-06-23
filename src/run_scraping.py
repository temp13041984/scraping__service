import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *

from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://rabota.by/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1002'),
    (hh, 'https://hh.ru/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1&customDomain=1'),

)

city = City.objects.filter(slug='minsk')
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()




