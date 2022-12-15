"""
WSGI config for autoBatWeb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


# =====================
# wsgi.py file begin 

import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('/home/abusr/autoBatWeb/auto-BAT-Web')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/abusr/anaconda3/envs/AutoBat/lib/python3.8/site-packages')

# poiting to the project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoBatWeb.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# wsgi.py file end
# ===================

