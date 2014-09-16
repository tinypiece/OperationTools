import sys
import os

sys.stdout = sys.stderr

os.environ['TRAC_ENV_PARENT_DIR'] = '/home/user/trac/projects/'
os.environ['PYTHON_EGG_CACHE'] = '/home/user/trac/.eggs/'

from trac.web.standalone import AuthenticationMiddleware
from trac.web.main import dispatch_request
from trac.web.auth import BasicAuthentication
#def application(environ, start_application):
#    auth = {"*" : BasicAuthentication("/home/user/trac/htpasswd.trac", "realm")}
#    wsgi_app = AuthenticationMiddleware(dispatch_request, auth)
#    return wsgi_app(environ, start_application)
#application = trac.web.main.dispatch_request
application = dispatch_request

