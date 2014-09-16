install
# yum groupinstall Development Tools
# yum update
# reboot
# yum install python-devel python-setuptools
# easy_install pip
# pip install virtualenv virtualenvwrapper

一般ユーザで実施
$ vi ~/.bashrc
※以下を追記
=============================================================
export PIP_DOWNLOAD_CACHE=$HOME/.pip_download_cache

if [ -f /usr/bin/virtualenvwrapper.sh ]
then
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
        export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
        export WORKON_HOME=$HOME/.virtualenvs
        source /usr/bin/virtualenvwrapper.sh
fi
=============================================================

$ source ~/.bashrc
$ mkvirtualenv trac
$ pip install docutils babel pygments
$ pip install trac
$ pip install gunicorn
$ mkdir -p ~/trac/sites
$ mkdir -p ~/trac/plugins
$ mkdir -p ~/trac/security
$ cd ~/trac/sites
$ trac-admin adminproj initenv
プロジェクト名 [My Project]> 管理プロジェクト
データベース接続文字列 [sqlite:db/trac.db]>
$ trac-admin adminproj permission add adminuser TRAC_ADMIN
$ vi adminproj/conf/trac.ini
[header_logo] -> src を common/trac_banner.png に修正
$ cd ../security/
$ htpasswd -c trac.htpasswd adminuser
New password: 
Re-type new password: 
Adding password for user adminuser
$ cd ../plugins/
$ svn co http://trac-hacks.org/svn/accountmanagerplugin/tags/acct_mgr-0.4.3/
$ cd acct_mgr-0.4.3/
$ python setup.py compile_catalog -f
$ python setup.py bdist_egg
$ cp dist/TracAccountManager-0.4.3-py2.6.egg ../../sites/adminproj/plugins/
$ cd ../../
$ vi gunicorn_trac.py
===============================================================
import sys
import os

sys.stdout = sys.stderr
os.environ['TRAC_ENV_PARENT_DIR'] = '/home/ghiblar/trac/sites/'
os.environ['PYTHON_EGG_CACHE'] = '/home/ghiblar/trac/.eggs/'

from trac.web.standalone import AuthenticationMiddleware
from trac.web.main import dispatch_request
from trac.web.auth import BasicAuthentication
def application(environ, start_application):
    auth = {"*" : BasicAuthentication("/home/ghiblar/trac/security/trac.htpasswd", "Trac")}
    wsgi_app = AuthenticationMiddleware(dispatch_request, auth)
    return wsgi_app(environ, start_application)
===============================================================
$ mkdir /home/ghiblar/trac/.eggs/
$ chmod 755 /home/ghiblar/trac/.eggs/
$ gunicorn -w2 -b 0.0.0.0:8080 gunicorn_trac:application

■ プラグインの設定
- Account Manager
  + acct_mgr.register.*, acct_mgr.guard.* 以外を有効化

■ Account Manager の設定
- HtPasswdStore を 1 に
- filename に設定ファイルパスを記載
- メールアドレスを必ず確認するのチェックをはずす






