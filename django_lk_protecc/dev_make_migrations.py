# https://stackoverflow.com/questions/37528286/how-to-make-migrations-for-a-reusable-django-app

'''
this script is for making migrations without a dedicated project/settings.py file
instead, it uses dev_settings.py and configures the migrations automatically
this is useful for running tests outside of a project
'''

import os
import sys
import dev_settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev_settings")
    from django.core.management import execute_from_command_line
    args = sys.argv + ["makemigrations", "protecc"]
    execute_from_command_line(args)