#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import Bottle, route, run, template, redirect, request, static_file
from os import listdir, path
from re import sub, compile as recompile
from ConfigParser import SafeConfigParser as ConfigParser

hymby = Bottle()
hymby.config = {}
# General configuration
general_config = {
    'filename': 'hymbyrc',
    'checked': False
}
hymby.config.update(general_config)

# Makefly default configuration
makefly_config = {
    'makefly.db_extension': '.mk',
    'makefly.src_extension': '.md',
    'makefly.db_directory': 'db',
    'makefly.src_directory': 'src',
}
hymby.config.update(makefly_config)

# Useful info
hymby.DBFILES = [] # contains list of files that contains the metadata of each post

def check_config():
    '''
    Check that configuration file exist regarding hymby.config['filename'] variable.
    If not: go to the installation page to create the file.
    '''
    # if configuration file exists and hymby.config filled in, nothing to do
    if path.exists(hymby.config['filename']) and hymby.config.get('checked', False) and path.exists(hymby.config.get('general.path', False)):
        return True
    # Check if configuration file exists.
    #+ If not, launch /install procedure
    #+ If exist, read configuration file
    if not path.exists(hymby.config['filename']):
        # TODO: Add a param to inform why we launch installation
        redirect('/install')

    # Read configuration file
    conf = ConfigParser()
    conf.read(hymby.config['filename'])
    for section in conf.sections():
        for key, value in conf.items(section):
            key = section + '.' + key
            hymby.config.update({key: value})
    hymby.config.update({'checked': True}) # Configuration checked

    # TODO: Check if engine module exists regarding the configuration file ('engine' variable)
    # If not, launch /install procedure
    conf_engine = hymby.config.get('general.engine', False)
    if not conf_engine:
        redirect('/install')

    # Check if blog exists regarding the configuration file ('path' variable)
    #+ If not, launch /install procedure
    if not path.exists(hymby.config.get('general.path', False)):
        # TODO: Add a param to inform why we launch installation
        redirect('/install')
    # Load given engine special features
    loaded_engine = __import__('engines.' + conf_engine)
    hymby.get_items = getattr(loaded_engine, conf_engine).get_items(hymby)
    return True

def item_data(filepath):
    '''
    Read meta data from files in the given path.
    The format is:
        variable = content
    Also delete whitespace at beginning and end of variable and content.
    '''
    variables = {}
    if path.exists(filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                data = line.split('=')
                if data and len(data) > 1:
                    # delete first and last spaces
                    variable = sub(' *$', '', data[0])
                    variable = sub('^ *', '', variable)
                    content = sub(' *$', '', data[1])
                    content = sub('^ *', '', content)
                    variables.update({variable: content.replace('\n', '')})
            f.close()
    return variables

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
        pathname = request.forms.get('path', '').strip()
        if not pathname:
            return template('install.tpl', message='Path missing', message_type='warning', installed=False)
        return "<p>Installation succeeded.</p>"
    else:
        config_exists = path.exists(hymby.config.get('filename', '')) or False
        config_checked = hymby.config.get('checked', False)
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
    item_list = hymby.get_items or []
    return template('items', items=item_list)

@hymby.route('/items/new')
def new_item(method='GET'):
    '''
    New item creation page.
    If no data, get form view.
    If data given, add the new item.
    '''
    check_config()
    if request.GET.get('save', '').strip():
        name = request.GET.get('name', '').strip()
        # TODO: fetch info
        return '<p>New post added successfully: %s.</p>' % (name)
    else:
      return template('new_post.tpl', name='New post', title='Add a new post')

@hymby.route('/item/<name>')
def item(name='Untitled'):
    '''
    Display content of given post (name)
    '''
    check_config()
    # TODO: if not hymby.config, check config file to initialize variable or do /install
    # TODO: return to homepage or give a redirection to /items if name == Untitled
    if name == 'Untitled':
        return HTTPError(404)
    regex = recompile('(?P<timestamp>\d+),(?P<basename>.*)(?P<extension>\.mk)')
    matching = regex.match(name)
    source_file = ''
    if matching:
        source_file = '/'.join([hymby.config.get('general.path', ''), hymby.config.get('makefly.src_directory', ''), matching.groups()[1] + hymby.config.get('makefly.src_extension', '')])
    content = ''
    if source_file:
        sf = open(source_file, 'r')
        content = sf.read()
        sf.close()
    details = item_data(name)
    try:
        mdwn = __import__('markdown')
        content = mdwn.markdown(content)
    except ImportError as e:
        content = 'python-markdown is missing!'
    return template('item.tpl', content=content, name=details.get('TITLE', ''), title=details.get('TITLE', ''))

# Serve static files
@hymby.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static/')

@hymby.error(404)
def error404(error='', error_type='none'):
    '''
    Default 404 page.
    '''
    return template('404.tpl', message=error, message_type=error_type)

# Setup route
hymby.route('/install', ['GET', 'POST'], install)

# Run application
#+ DEBUG   : should be set to False in production
#+ RELOADER: idem
hymby.run(host='localhost', port=8080, debug=True, reloader=True)
