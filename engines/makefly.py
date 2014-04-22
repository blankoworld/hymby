#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir, path
from re import sub

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
