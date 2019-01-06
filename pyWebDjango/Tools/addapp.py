# set /p app_name=
# cd apps
# python ../manage.py startapp %app_name%

# pause

import os

app_name  = input('app_name:')
# print(r'cd ..\apps && ..\manage.py startapp ' + app_name)
os.popen(r'cd ..\apps && python ..\manage.py startapp ' + app_name)