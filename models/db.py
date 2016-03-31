# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db= DAL('mysql://ztree_server:balaagan@localhost/ZTree', pool_size=0,migrate=True, fake_migrate=True, migrate_enabled = True, fake_migrate_all = True)

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service, plugins = Service(), PluginManager()


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False, migrate=True)
auth.wiki(resolve=False, render='html')
## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('stages',Field('experiment_id','integer'),Field('stage_number','integer'),Field('type_stage',requires=IS_IN_SET(['Request','Response','Wait','End'])),Field("message",'string'))

db.define_table('experiment_participant',Field('experiment_id','integer'),Field('participant_id','integer'))

db.define_table('experiment',Field('title','string',unique=True),Field('typeExperiment',requires=IS_IN_SET(['stag and hare','coin effort'])),Field ('rounds','integer'))

db.define_table('participant',Field('IP','string'),Field('model_name','string'))

db.define_table('results',Field('experiment_id','integer'),Field('participant_id','integer'),Field('stage_id','integer'),Field('round_id','integer'),Field('name','string'),Field('valueInt','double'),Field('returnvar','double'),Field('total','double'))

db.define_table('setupExperiment',Field ('experiment_id','integer'),Field('name','string'),Field('valueString','string'))
## after defining tables, uncomment below to enable auditing

experiments=db(db.experiment.id>0).select()

# auth.enable_record_versioning(db)
import logging
logger = logging.getLogger("web2py.app.myapp")
logger.setLevel(logging.DEBUG)
