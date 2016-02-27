# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = 'ZTreeServer'
response.subtitle = 'VR emulation'

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Cat Kutay <cat.kutay@unsw.edu.au>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (T('Setup '), False, URL('experiments', 'setup_interface')),
	 (T('Results '), False, URL('experiments', 'display_results')),
         (T('Reset '), False, URL('experiments', 'reset')),
        (T('Edit App'), False, URL('admin', 'default', 'design/%s' % app)), 
        (T('Edit Controller'), False,
         URL(
         'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr)))
         ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
