#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir
from os import path
from re import sub
from re import compile as recompile
from datetime import datetime

def text2url(text):
    if not text:
        return ''
    text = text.strip()
    htmlcodes = ['A;', 'a', 'A', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'A', 'a', 'C', 'c', 'E', 'e', 'E', 'e', 'E', 'e', 'E', 'e', 'E', 'e', 'I', 'i', 'I', 'i', 'I', 'i', 'I', 'i', 'N', 'n', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 'O', 'o', 's', 'P', 'p', 'U', 'u', 'U', 'u', 'U', 'u', 'U', 'u', 'Y', 'y', 'y', 'C', 'R', 'TM', 'E', 'C', 'L', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
    funnychars = ['\xc1','\xe1','\xc0','\xc2','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3','\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9','\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc','\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2','\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf','\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc','\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018','\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc','\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
    newtext = ''
    for char in text:
        if char not in funnychars:
            # delete special char
            if not char.isalnum():
                newtext = newtext + '_'
            else:
                newtext = newtext + char
        else:
            newtext  = newtext + htmlcodes[funnychars.index(char)]
    # TODO: delete duplicates of _
    return newtext

def makefly_metafiles(self, pathname, extension):
    '''
    Return list of meta files from the 'db' directory (by default Makefly configure it to be 'db')
    '''
    files = []
    for listed_file in listdir(pathname):
        if listed_file.endswith(extension):
            files.append(listed_file)
    if not self.DBFILES and files:
        self.DBFILES = files
    return files

def makefly_metadata(self, filepath):
    '''
    Read meta data from given filepath.
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

def get_items(self):
    '''
    Return the list of items from Makefly as a tuple list.
    Each tuple contains:
      - unique id used by get_item method to display the content of a given post
      - title of the post
      - description of the post
    '''
    # Prepare some values
    result = []
    files = self.DBFILES
    metafiles_path = '/'.join([self.config.get('general.path', ''), self.config.get('makefly.db_directory', '')]) + '/'
    # Check files ' list presence
    if not files:
        metafiles_extension = self.config.get('makefly.db_extension', '')
        files = makefly_metafiles(self, metafiles_path, metafiles_extension)
    # Search post's info
    for f in files:
        metafile_path = '' + metafiles_path + f
        metadata = makefly_metadata(self, metafile_path)
        if metadata:
            title = metadata.get('TITLE', 'Untitled')
            description = metadata.get('DESCRIPTION', 'No description available')
            result.append((f, title, description))
    return result

def get_item_metadata(self, identifier):
    """
    Return meta
    """
    # Some checks
    if not identifier:
        return {}
    # Prepare some value
    metafiles_path = '/'.join([self.config.get('general.path', ''), self.config.get('makefly.db_directory', '')]) + '/'
    metafile_path = '' + metafiles_path + identifier
    # Fetch info and return result
    metadata = makefly_metadata(self, metafile_path)
    return metadata

def get_item_content(self, identifier):
    """
    Get the content of the given identifier
    """
    # Some checks
    if not identifier:
        return ''
    # Prepare some value
    content = ''
    # Fetch post content
    regex = recompile('(?P<timestamp>\d+),(?P<basename>.*)(?P<extension>\.mk)')
    matching = regex.match(identifier)
    source_file = ''
    if matching:
        source_file = '/'.join([self.config.get('general.path', ''), self.config.get('makefly.src_directory', ''), matching.groups()[1] + self.config.get('makefly.src_extension', '')])
    if source_file:
        sf = open(source_file, 'r')
        content = sf.read()
        sf.close()
    try:
        mdwn = __import__('markdown')
        content = mdwn.markdown(content)
    except ImportError as e:
        content = 'python-markdown is missing!'
    return content

def new_item(self, data):
    """
    Create a new item with info in data
    """
    # Some checks
    if not data:
        return False, 'No data specified'
    # Prepare some values
    res = False
    message = ''
    metafiles_path = '/'.join([self.config.get('general.path', ''), self.config.get('makefly.db_directory', '')]) + '/'
    srcfiles_path = '/'.join([self.config.get('general.path', ''), self.config.get('makefly.src_directory', '')]) + '/'
    title = data.get('NAME', False)
    description = data.get('DESCRIPTION', False)
    ptype = data.get('TYPE', False)
    author = data.get('AUTHOR', False)
    date = data.get('DATE', False)
    tags = data.get('TAGS', False)
    keyword = data.get('KEYWORDS', False)
    # Mandatories field
    if not title:
        return False, 'No title specified!'
    # Create the new post
    today = datetime.today()
    timestamp = today.strftime('%s')
    new_title = text2url(title)
    print new_title
    return res, message
