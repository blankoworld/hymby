from bottle import Bottle, route, run, template, redirect
from os import listdir, path
from re import sub, compile as recompile

hymby = Bottle()
hymby.DBFILES = []
hymby.dbfiles_extension = '.mk'
hymby.CONFIG = {}

@hymby.route('/install')
def install():
    '''
    Launch the installation procedure
    '''
    # TODO: if not hymby.CONFIG, check config file to initialize variable or do /install
    content = '<p>TODO: Perform installation</p>'
    if hymby.CONFIG and hymby.CONFIG.get('engine', False):
        content = '<p>Already installed. <a href="/items">List items</a></p>'
    return '<h3>Installation</h3>' + content

def dblist(path, extension):
    '''
    Return list of item from the DB
    TODO: read a specific configuration file to know from which engine 
    we come and were to find the DB (or specific method for each one).
    '''
    files = []
    for listed_file in listdir(path):
        if listed_file.endswith(extension):
            files.append(listed_file)
    # Complete DBFILES global variable
    if not hymby.DBFILES:
        hymby.DBFILES = list(files)
    return files

def item_data(filepath):
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

@hymby.route('/')
def check_config_file():
    # TODO: Check if configuration file exists (make a global variable with the name of the configuration file).
    #+ If not, launch /install procedure
    #+ If exist, read configuration file
    # TODO: read configuration file and fill in "hymby.CONFIG" variable with result
    hymby.CONFIG.update({
        'engine': 'makefly',
        'path': './hosted_engine',
    })
    # TODO: Check if engine module exists regarding the configuration file ('engine' variable)
    # If not, launch /install procedure
    # TODO: Check if blog exists regarding the configuration file ('path' variable)
    #+ If not, launch /install procedure

    # If all is OK, read configuratigo to the webadmin panel (list of items)
    redirect('/items')

@hymby.route('/items')
def homepage():
    # TODO: if not hymby.CONFIG, check config file to initialize variable or do /install
    res = '<h3>List</h3>'
    db_path = hymby.CONFIG.get('path', '') + '/' + 'db' + '/'
    files = dblist(db_path, hymby.dbfiles_extension)
    return template('items', items=[(x, item_data(db_path + x)) for x in files])

@hymby.error(404)
def error404(error):
    return 'Nothing here! Try this: <a href="/">Homepage</a>'

@hymby.route('/item/<name>')
def item(name='Untitled'):
    '''
    Display content of given post (name)
    '''
    # TODO: if not hymby.CONFIG, check config file to initialize variable or do /install
    # TODO: return to homepage or give a redirection to /items if name == Untitled
    if name == 'Untitled':
        return HTTPError(404)
    regex = recompile('(?P<timestamp>\d+),(?P<basename>.*)(?P<extension>\.mk)')
    matching = regex.match(name)
    source_file = ''
    if matching:
        print matching
        source_file = hymby.CONFIG.get('path', '') + '/src/' + matching.groups()[1] + '.md'
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

hymby.run(host='localhost', port=8080, debug=True)
