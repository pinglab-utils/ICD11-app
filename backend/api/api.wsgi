activate_this = '/var/www/app/backend/api/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

  
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/ubuntu/app/backend/api')
from api import app as application
application.secret_key = 'anything you wish'                                        
