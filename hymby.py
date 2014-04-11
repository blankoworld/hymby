from bottle import Bottle, route, run, template
from os import listdir, path
from re import sub, compile as recompile

hymby = Bottle()
hymby.DBFILES = []
hymby.dbfiles_extension = '.mk'

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
def homepage():
    res = '<h3>List</h3>'
    files = dblist('./db', hymby.dbfiles_extension)
    if files:
        res += '<ul>\n'
    for f in files:
        f_data = item_data('./db/' + f)
        item_title = f_data.get('TITLE', 'Untitled')
        res += '  <li><a href="/item/%s" alt="Read %s">%s</a></li>' % (f, item_title, item_title)
    if files:
        res += '</ul>'
    return res

@hymby.error(404)
def error404(error):
    return 'Nothing here! Try this: <a href="/">Homepage</a>'

@hymby.route('/item/<name>')
def item(name='Untitled'):
    # TODO: return to homepage or give a redirection to /items if name == Untitled
    if name == 'Untitled':
        return HTTPError(404)
    regex = recompile('(?P<timestamp>\d+),(?P<basename>.*)(?P<extension>\.mk)')
    matching = regex.match(name)
    source_file = ''
    if matching:
        print matching
        source_file = './src/' + matching.groups()[1] + '.md'
    content = ''
    if source_file:
        sf = open(source_file, 'r')
        content = sf.read()
        sf.close()
    details = item_data(name)
    return template('<h3>%s</h3>\n<p>%s</p>' % (details.get('TITLE', ''), content), name=name)

hymby.run(host='localhost', port=8080, debug=True)
