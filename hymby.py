#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hymby stands for Host You MiniBlog Yourself. It aims to be a fast and
 lightweight web application that permits to install and manage your
 static weblog engine.

Copyright (c) 2014, Olivier DOSSMANN
License: MIT (see LICENSE for details)
"""

import bottle
from bottle import Bottle
from bottle import route
from bottle import run
from bottle import template
from bottle import redirect
from bottle import request
from bottle import static_file
from bottle import ConfigDict
from bottle import default_app
from os import listdir
from os import path
from threading import Thread

hymby = application = Bottle()
hymby.params = {}
# General configuration
general_config = {
    'filename': 'hymbyrc',
    'checked': False,
    'refresh_errors': 'refresh_errors.log',
}
hymby.params.update(general_config)
# Useful info
hymby.DBFILES = [] # contains list of files that contains the metadata of each post

# Miscellaneous
module_pyfile = 'main'
module_configfile = 'configrc'

def check_config():
    '''
    Check that configuration file exist regarding hymby.params['filename'] variable.
    If not: go to the installation page to create the file.
    '''
    # if configuration file exists and hymby.params filled in, nothing to do
    if path.exists(hymby.params['filename']) and hymby.params.get('checked', False) and path.exists(hymby.params.get('general.path', False)):
        return True
    # Check if configuration file exists.
    #+ If not, launch /install procedure
    #+ If exist, read configuration file
    if not path.exists(hymby.params['filename']):
        # TODO: Add a param to inform why we launch installation
        redirect('/install')

    # Read configuration file
    conf = ConfigDict().load_config(hymby.params['filename'])
    hymby.params.update(conf)

    # TODO: Check if engine module exists regarding the configuration file ('engine' variable)
    # If not, launch /install procedure
    engine = hymby.params.get('general.engine', False)
    if not engine:
        redirect('/install')

    # Check if blog exists regarding the configuration file ('path' variable)
    #+ If not, launch /install procedure
    if not path.exists(hymby.params.get('general.path', False)):
        # TODO: Add a param to inform why we launch installation
        redirect('/install')
    # Load given engine special features (main.py file in given engine)
    module = __import__('engines.' + engine)
    loaded_engine = getattr(module, engine)
    hymby.engine = getattr(loaded_engine, module_pyfile)
    # Load given engine specific configuration (configrc file in given engine)
    engine_config_filepath = '/'.join(['engines', engine, module_configfile])
    engine_config = ConfigDict().load_config(engine_config_filepath)
    hymby.params.update(engine_config)
    hymby.params.update({'checked': True}) # Configuration checked
    # Add new specific views from given engine to Hymby
    bottle.TEMPLATE_PATH.append('/'.join(['engines', engine, 'views']))
    return True

def install(message='', message_type='normal'):
    '''
    Launch the installation procedure:
      - fetch some info
      - create the configuration file
      - fetch the given static weblog engine
    '''
    installed = False
    if request.forms.get('save', '').strip():
        # TODO: check that engine + path have been filled in
        #+ If not, redirect to '/install' with message "missing info"
        # TODO: perform installation regarding given info
        pathname = request.forms.getunicode('path', '').encode('utf-8').strip()
        if not pathname:
            return template('install.tpl', message='Path missing', message_type='warning', installed=False)
        return "<p>Installation succeeded.</p>"
    else:
        config_exists = path.exists(hymby.params.get('filename', '')) or False
        config_checked = hymby.params.get('checked', False)
        if config_exists and config_checked:
            installed = True
        return template('install.tpl', installed=installed, message=message, message_type=message_type)

def get_items():
    return error404('No engine found', 'error')

@hymby.route('/')
def homepage():
    '''
    Check configuration file then redirect to the items list
    '''
    check_config()
    # If all is OK, redirect user to the list of items
    redirect('/items')

@hymby.route('/items')
def items():
    '''
    List of items
    '''
    check_config()
    item_list = hymby.engine.get_items(hymby) or []
    return template('items', items=item_list, blog_title=hymby.engine.get_title(hymby), blog_desc=hymby.engine.get_description(hymby))

def new_item():
    '''
    New item creation page.
    If no data, get form view.
    If data given, add the new item.
    '''
    check_config()
    data = {}
    if request.POST.get('save', '').strip():
        # Fetch info
        r = request.POST
        pname = r.getunicode('name', '').encode('utf-8').strip()
        pdesc = r.getunicode('description', '').encode('utf-8').strip()
        pdate = r.getunicode('date', '').encode('utf-8').strip()
        ptype = r.getunicode('type', '').encode('utf-8').strip()
        ptags = r.getunicode('tags', '').encode('utf-8').strip()
        pkeyword = r.getunicode('keyword', '').encode('utf-8').strip()
        pauthor = r.getunicode('author', '').encode('utf-8').strip()
        pcontent = r.getunicode('content', '').encode('utf-8').strip()
        # Create the new item
        data.update({
          'NAME': pname,
          'DESCRIPTION': pdesc,
          'DATE': pdate,
          'TYPE': ptype,
          'TAGS': ptags,
          'KEYWORDS': pkeyword,
          'AUTHOR': pauthor,
        })
        pid, msg = hymby.engine.new_item(hymby, data, pcontent)
        if not pid:
            return template('errors.tpl', title='Warning', message_type='warning', message=msg)
        # If all is OK, refresh blog
        t = Thread(group=None, target=hymby.engine.refresh, name=None, args=(hymby, hymby.params.get('refresh_errors')))
        t.start()
        redirect('/item/%s' % pid)
    else:
      return template('new_post.tpl', name='New post', title='Add a new post')

def edit_item(name=False):
    '''
    Edit an item content.
    If not item, return to the item list.
    '''
    check_config()
    if not name:
        redirect('/items')
    data = {}
    if request.POST.get('save', '').strip():
        # Fetch info
        r = request.POST
        pname = r.getunicode('name', '').encode('utf-8').strip()
        pdesc = r.getunicode('description', '').encode('utf-8').strip()
        pdate = r.getunicode('date', '').encode('utf-8').strip()
        ptype = r.getunicode('type', '').encode('utf-8').strip()
        ptags = r.getunicode('tags', '').encode('utf-8').strip()
        pkeyword = r.getunicode('keyword', '').encode('utf-8').strip()
        pauthor = r.getunicode('author', '').encode('utf-8').strip()
        pcontent = r.getunicode('content', '').encode('utf-8').strip()
        # Create the new item
        data.update({
          'NAME': pname,
          'DESCRIPTION': pdesc,
          'DATE': pdate,
          'TYPE': ptype,
          'TAGS': ptags,
          'KEYWORDS': pkeyword,
          'AUTHOR': pauthor,
          'CONTENT': pcontent,
        })
        res, msg = hymby.engine.edit_item(hymby, name, data)
        if not res:
            return template('errors.tpl', title='Warning', message_type='warning', message=msg)
        # If all is OK, refresh blog
        t = Thread(group=None, target=hymby.engine.refresh, name=None, args=(hymby, hymby.params.get('refresh_errors')))
        t.start()
        redirect('/item/%s' % name)
    else:
      # Read post content
      details = hymby.engine.get_item_metadata(hymby, name)
      content = hymby.engine.get_item_content(hymby, name, transformed=False)
      return template('edit.tpl', name=name, title='Edition', forms=details, content=content)

@hymby.route('/item/<name>')
def item(name):
    '''
    Display content of given post (name)
    '''
    check_config()
    # search the post
    details = hymby.engine.get_item_metadata(hymby, name)
    # if no details, return to /items
    if not details:
        redirect('/items')
    return template('single.tpl', identifier=name, content=hymby.engine.get_item_content(hymby, name, replacements=True), data=details, title=details.get('TITLE', ''))
@hymby.route('/delete/<name>')
def delete_item(name):
    """
    Delete given item (name).
    """
    check_config()
    # search the post
    item_exists = hymby.engine.item_exists(hymby, name)
    # if not details, post doesn't exist, return an error
    if not item_exists:
        msg = 'Post not found: %s' % (name or '')
        return template('errors.tpl', title='Error', message_type='error', message=msg)
    # otherwise delete items and return to item list
    result, msg = hymby.engine.delete_item(hymby, name)
    if result:
        # If all is OK, refresh blog
        t = Thread(group=None, target=hymby.engine.refresh, name=None, args=(hymby, hymby.params.get('refresh_errors')))
        t.start()
        redirect('/items')
    else:
        return template('errors.tpl', title='Error', message_type='error', message=msg)

@hymby.route('/help')
def go_to_help():
    redirect('/help/en')

@hymby.route('/help/<language>')
def help(language='en'):
    """
    Display given help page.
    If language not found, return 404 page.
    """
    content = ''
    helppath = './doc/README.%s.md' % (language)
    if path.exists(helppath):
        with open(helppath, 'r') as f:
            content = f.read()
            f.close()
    else:
        content = "No help found! You're alone..."
    if content:
        try:
            mdwn = __import__('markdown')
            content = mdwn.markdown(content.decode('utf-8'), extensions=['toc'])
        except ImportError as e:
            content = 'python-markdown module missing!'
    return template('help.tpl', title='Help', content=content)

@hymby.route('/config')
def config_page():
    """
    Display current configuration and permit to change values.
    """
    check_config()
    # TODO: Make an if/else to permit to write changes
    return template('config.tpl', title='Configuration', config=hymby.params, engine_config=hymby.engine.get_config(hymby))

# STATIC routes
@hymby.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static/')

@hymby.route('/fonts/<filename:path>')
def send_static_markitup(filename):
    return static_file(filename, root='./static/fonts/')

@hymby.route('/engine/<filename:path>')
def send_static_engine(filename):
    check_config()
    engine = hymby.params.get('general.engine')
    static_path = '/'.join([hymby.params.get('general.path', ''), hymby.params.get(engine + 'static_directory', '')])
    return static_file(filename, root=static_path)

# ERRORS
@hymby.error(404)
def error404(error='', error_type='none'):
    '''
    Default 404 page.
    '''
    return template('404.tpl', message=error, message_type=error_type)

# SPECIAL routes
hymby.route('/install', ['GET', 'POST'], install)
hymby.route('/items/new', ['GET', 'POST'], new_item)
hymby.route('/edit/<name>', ['GET', 'POST'], edit_item)

# Run application
#+ DEBUG   : should be set to False in production
#+ RELOADER: idem
if __name__ == '__main__':
    hymby.run(host='0.0.0.0', port=8080, debug=True, reloader=True)
