# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
import os
import subprocess
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

SCRAPERS_ROOT = env('SCRAPERS_ROOT')
#sys.path.append(SCRAPERS_ROOT)



@task()
def scrape_haestirettur():
    return subprocess.call(['{}/bin/scrapy'.format(os.environ['VIRTUAL_ENV']), 'crawl', '--loglevel', 'INFO', 'haestirettur'], cwd=SCRAPERS_ROOT)


@task()
def scrape_heradsdomstolar():
    return subprocess.call(['{}/bin/scrapy'.format(os.environ['VIRTUAL_ENV']), 'crawl', '--loglevel', 'INFO', 'heradsdomstolar'], cwd=SCRAPERS_ROOT)
