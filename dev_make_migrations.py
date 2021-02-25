# https://stackoverflow.com/questions/37528286/how-to-make-migrations-for-a-reusable-django-app

'''
this script is for making migrations without a dedicated project/settings.py file
instead, it uses dev_settings.py and configures the migrations automatically
this is useful for running tests outside of a project
'''

import os
import sys
import dev_settings
from django.conf import settings
import django

if __name__ == "__main__":
    settings_params = dev_settings.settings()
    settings.configure(**settings_params)
    django.setup()    
    from django.core.management import execute_from_command_line
    args = sys.argv + ["makemigrations", "protecc"]
    execute_from_command_line(args)