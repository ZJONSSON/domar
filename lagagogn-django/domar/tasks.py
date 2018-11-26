# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
import os
import subprocess
import environ
import sys

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

SCRAPERS_ROOT = env('SCRAPERS_ROOT')
#sys.path.append(SCRAPERS_ROOT)



@task()
def scrape_haestirettur():
    #os.environ['SCRAPY_SETTINGS_MODULE'] = 'scrapers.settings'
    return subprocess.call(['scrapy', 'crawl', '--loglevel', 'INFO', 'haestirettur'], cwd=SCRAPERS_ROOT)
    #return subprocess.call('pwd')
