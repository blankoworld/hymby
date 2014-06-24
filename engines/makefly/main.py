#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of Hymby static weblog engine management tool.

Copyright (c) 2014, Olivier DOSSMANN
License: MIT (see LICENSE for details)
"""

from os import listdir
from os import path
from os import remove
from os import environ
from re import sub
from re import compile as recompile
from subprocess import Popen, PIPE
from itertools import islice
import logging
from time import sleep

MAKEFLY_CONFIGRC = 'makefly.rc'
MAKEFLY_DBFILE_REGEX = recompile('(?P<timestamp>\d+),(?P<basename>.*)(?P<extension>\.mk)')
MAKEFLY_POST_LIMIT = 15

def makefly_metafiles(self, pathname, extension):
    """
    Return a list of files that contains the metadata of posts.
    In Makefly: 'db' directory is the default directory that contains them
    """
    files = []
    for listed_file in listdir(pathname):
        if listed_file.endswith(extension):
            files.append(listed_file)
    if not self.DBFILES and files:
        self.DBFILES = files
    return files

def makefly_metadata(self, filepath):
    """
    Get data from given filepaths
    Default Makefly's format is:

        variable = content

    This method delete whitespace at beginning and end of variable and content.
    """
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

def makefly_content(self, identifier, limit=False):
    """
    Get content of given <identifier>
    Return a string
    """
    # Fetch post content
    matching = MAKEFLY_DBFILE_REGEX.match(identifier)
    source_file = ''
    content = ''
    if matching:
        source_file = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.src_directory', ''), matching.groups()[1] + self.params.get('makefly.src_extension', '')])
    if source_file:
        with open(source_file, 'r') as sf:
            if not limit:
                content = sf.read()
            else:
                content = ''.join(list(islice(sf,limit)))
            sf.close()
    return content

def do_replacements(self, string):
    """
    Do replacements in <string>:
      * Change "${BLOG_URL}" to /engine: this is to display pictures
    """
    # Change value of BLOG_URL by another value
    return string.replace("${BLOG_URL}", '/engine')

def refresh(self, errorfile):
    """
    Recompile all the entire blog.
    Put the result into a log file.
    """
    # BUG FROM MAKEFLY WITH HYMBY: The refresh method is called at the same time than the post creation.
    #+ This way, the new post have the same date as the compilation.
    #+ In Makefly, we don't compile posts that are in the future and in the present (a kind of crazy time machine :p)
    # So Makefly doesn't add the new created post because of Python/Bottle/Lua are too fast.
    #+ We have to wait 1 second before refreshing.
    sleep(1)
    # Prepare some values
    blogdir = self.params.get('general.path')
    logging.basicConfig(filename=errorfile, format=logging.BASIC_FORMAT)
    generation = Popen(['lua', 'makefly', 'refresh'], stdout=PIPE, stderr=PIPE, cwd=blogdir)
    # Launch clean up then generation
    stdout = ()
    try:
        stdout = generation.communicate()
    except Exception as e:
        logging.exception("Popen refresh error")
        return False, e
    if stdout and len(stdout) > 1 and stdout[1]:
        logging.error(stdout[1])
        return False, 'Blog refresh failed!'
    return True

def get_config(self):
    """
    Get Makefly's configuration.
    """
    res = {}
    config = ''
    configpath = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.configfile', '')])
    with open(configpath, 'r') as f:
        config = f.read()
        f.close()
    for line in config.split('\n'):
        if line:
            field, content = line.split('=')
            res[field.strip()] = content.strip()
    return res

def set_config(self, data={}):
    """
    Write configuration.
    """
    # do nothing if no data or no configuration file found
    configpath = '/'.join([self.params.get('general.path'), MAKEFLY_CONFIGRC])
    if not data or not path.exists(configpath):
        return False
    # Open old values
    conf = get_config(self)
    for field in data:
        if field != 'save_engine':
            conf.update({field: data[field]})
    # Write values
    with open(configpath, 'w') as configfile:
        for element in conf:
            configfile.write('%s = %s\n' % (element, conf[element]))
        configfile.close()
    return True

def get_title(self):
    """
    Fetch blog title.
    """
    return get_config(self).get('BLOG_TITLE', 'No blog title')

def get_description(self):
    """
    Fetch blog description.
    """
    return get_config(self).get('BLOG_SHORT_DESC', '')

def get_items(self):
    """
    Return the list of items from Makefly as a tuple list.
    Each tuple contains:
      - unique id used by get_item method to display the content of a given post
      - title of the post
      - description of the post
    """
    # Prepare some values
    result = []
    files = self.DBFILES
    metafiles_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.db_directory', '')]) + '/'
    # Check files ' list presence
    if not files:
        metafiles_extension = self.params.get('makefly.db_extension', '')
        files = makefly_metafiles(self, metafiles_path, metafiles_extension)
    # Search post's info
    # Sort list by timestamp. As files contains name with timestamp, just use files list to do the sort.
    for f in sorted(files, reverse=True):
        metafile_path = '' + metafiles_path + f
        metadata = makefly_metadata(self, metafile_path)
        if metadata:
            title = metadata.get('TITLE', 'Untitled')
            description = metadata.get('DESCRIPTION', 'No description available')
            content = makefly_content(self, f, limit=MAKEFLY_POST_LIMIT)
            content = do_replacements(self, content)
            try:
                mdwn = __import__('markdown')
                content = mdwn.markdown(content.decode('utf-8'))
            except ImportError as e:
                content = 'python-markdown is missing!'
            result.append((f, title, description, content))
    return result

def item_exists(self, identifier):
    """
    Check if the item exists. For Makefly: check that <identifier> exists in 'db' directory.
    Return a boolean.
    """
    # Some checks
    if not identifier:
        return False
    # Prepare some values
    metafiles_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.db_directory', '')]) + '/'
    metafile_path = '' + metafiles_path + identifier
    return path.exists(metafile_path)

def get_item_metadata(self, identifier):
    """
    Return metadata of the given post (<identifier>).
    """
    # Some checks
    if not identifier:
        return {}
    # Prepare some value
    metafiles_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.db_directory', '')]) + '/'
    metafile_path = '' + metafiles_path + identifier
    # Fetch info and return result
    metadata = makefly_metadata(self, metafile_path)
    return metadata

def get_item_content(self, identifier, transformed=True, replacements=False):
    """
    Get the content of the given post (<identifier>).
    If transformed is False, then just give the content of the article.
    If transformed is True, transform the content into HTML by using Markdown.
    replacements means that we apply some replacements in the content.
    """
    # Some checks
    if not identifier:
        return ''
    # Prepare some value
    content = makefly_content(self, identifier)
    if transformed:
        try:
            mdwn = __import__('markdown')
            content = mdwn.markdown(content.decode('utf-8'))
        except ImportError as e:
            content = 'python-markdown is missing!'
    if replacements:
        return do_replacements(self, content)
    return content

def new_item(self, data, content):
    """
    Create a new item using given info.
    """
    # Some checks
    if not data:
        return False, 'No data specified'
    # Prepare some values
    message = ''
    blog_path = self.params.get('general.path', '')
    db_path = '/'.join([blog_path, self.params.get('makefly.db_directory', '')])
    metafiles_path = db_path + '/'
    src_path = '/'.join([blog_path, self.params.get('makefly.src_directory', '')])
    title = data.get('NAME', False)
    description = data.get('DESCRIPTION', False)
    ptype = data.get('TYPE', False)
    author = data.get('AUTHOR', False)
    # TODO: examine date in order to not have a wrong value
    date = data.get('DATE', False)
    tags = data.get('TAGS', False)
    keyword = data.get('KEYWORDS', False)
    # Mandatories field
    if not title:
        return False, 'No title specified!'
    # Create the new post
    p = Popen(["%s/tools/create_post.sh" % (blog_path), "-q"], stdin=PIPE, stdout=PIPE, env={"DBDIR": db_path, "SRCDIR": src_path})
    try:
        stdout = p.communicate(input="%s\n%s\n%s\n%s\n%s\n%s\n" % (author or 'Unknown', title, description or ' ', tags or 'news', ptype or 'normal', keyword or 'unknown'))
    except Exception as e:
        return False, e
    # Check result
    # first that an output exist
    if not len(stdout) or not len(stdout) > 1:
        return False, 'Post creation failed!'
    # then that given output begins with "Metafile" word
    if not stdout[0].startswith('Metafile: '):
        return False, "Makefly's error: %s" % stdout[0]
    result = stdout[0].split('\n')
    db_filename = path.basename(result[0])
    if content:
        src_filename = path.basename(result[1])
        srcfile_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.src_directory', ''), src_filename])
        with open(srcfile_path, 'w') as srcfile:
            srcfile.write(content)
            srcfile.close()
    # Add new item to list of posts
    self.DBFILES.append(db_filename)
    return db_filename, message

def edit_item(self, identifier, data={}):
    """
    Modify given post (<identifier>).
    """
    res = False
    msg = ''
    # Some checks
    if not data:
        return res, "No info given."
    # Mandatories fields
    for field in ['NAME', 'CONTENT']:
        if not data.get(field, False):
            return res, "'%s' field is mandatory!" % field
    # Prepare some values
    metafiles_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.db_directory', '')]) + '/'
    metafile = '' + metafiles_path + identifier
    source_file = ''
    # Get source file path
    matching = MAKEFLY_DBFILE_REGEX.match(identifier)
    if matching:
        source_file = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.src_directory', ''), matching.groups()[1] + self.params.get('makefly.src_extension', '')])
    else:
        return res, 'Regex problem on this item ID: %s' % identifier
    if not source_file:
        msg = 'No source file found!'
    # Write changes in metadata file
    with open(metafile, 'w') as mfile:
        for param in data:
            new_key = param
            new_value = data[param]
            # Specific behaviours
            if param in ['CONTENT', 'DATE']:
                continue
            if param == 'NAME':
                new_key = 'TITLE'
            mfile.write('%s = %s\n' % (new_key, new_value))
        mfile.close()
    # Write content in src filepath
    if 'CONTENT' in data and data.get('CONTENT', False):
        with open(source_file, 'w') as sfile:
            sfile.write(data['CONTENT'])
            sfile.close()
    res = True
    return res, msg

def delete_item(self, identifier):
    """
    Delete given post (regarding its <identifier>).
    """
    # Prepare some values
    res = False
    msg = ''
    metafiles_path = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.db_directory', '')]) + '/'
    metafile_path = '' + metafiles_path + identifier
    # Get source file path
    matching = MAKEFLY_DBFILE_REGEX.match(identifier)
    source_file = ''
    if matching:
        source_file = '/'.join([self.params.get('general.path', ''), self.params.get('makefly.src_directory', ''), matching.groups()[1] + self.params.get('makefly.src_extension', '')])
    # Delete files (but only if source_file found)
    if source_file and path.exists(source_file):
        remove(metafile_path)
        remove(source_file)
        res = True
    elif source_file:
        remove(metafile_path)
        msg = 'Source file (%s) not found! Metafile deleted.' % (source_file)
        res=  True
    else:
        msg = 'No source file. Metafile deleted'
    return res, msg
