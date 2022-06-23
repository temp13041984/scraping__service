import codecs

from scraping.parsers import *

parsers = (
    (work, 'https://rabota.by/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1002'),
    (hh, 'https://hh.ru/search/vacancy?text=Python&from=suggest_post&fromSearchLine=true&area=1&customDomain=1'),

)

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()




