#!/usr/bin/env lua

init = require('lib.init')
utils = require('lib.utils')

DEBUG = true

-- main info about queries
QUERY_STRING = os.getenv("QUERY_STRING") or ''
REQUEST_METHOD = os.getenv("REQUEST_METHOD") or ''
HTTP_HOST = os.getenv("HTTP_HOST") or ''

-- VARIABLES
routes = {
  home = 'Homepage',
  list = 'List',
}
content = ''

-- HYMBY CONFIGURATION
config = getConfig('hymby.config')
blog_path = config['path']

-- MAKEFLY specific
function render_makefly_post(path)
  local conf = getConfig(path)
  local post_filename = string.match(path, "%d+,(.+)")
  return '<li><a href="?post=' .. post_filename .. '">' .. conf['TITLE'] .. '</a></li>'
end

function render_makefly_posts(directory, extension)
  local result = '<h2>Posts</h2>'
  if not lfs.attributes(directory) then
    return result .. "<p>No " .. directory .. " directory.</p>"
  end
  dbfiles = listing(directory, extension)
  local res = {}
  for k, path in ipairs(dbfiles) do
    res[k] = render_makefly_post(path)
  end
  if res then
    result = result .. '<ul>'
    for i, j in ipairs(res) do
      result = result .. j
    end
  end
  return result
end

function render_makefly_single_post(directory, name)
  if not lfs.attributes(directory) then
    return "<h2>Error</h2>\n<p>No " .. directory .. " directory.</p>"
  end
  local dbfilepath = directory .. '/' .. name
  local filepath = string.gsub(dbfilepath, '.mk', '.md')
  if not lfs.attributes(filepath) then
    return "<h2>Error</h2>\n<p>Post " .. name .. " not found!</p>"
  else
    return readFile(filepath, 'r') or ''
  end
end

-- HYMBY displays
function post_list()
  local check_engine, ce_msg = check_blog_engine()
  if check_engine == false then
    content = ce_msg
    return
  end
  if config['engine'] == 'makefly' then
    content = render_makefly_posts(blog_path .. '/db', 'mk')
  end
  return
end

function post(name)
  local check_engine, ce_msg = check_blog_engine()
  if check_engine == false then
    content = ce_msg
    return
  end
  local post_content = ''
  if config['engine'] == 'makefly' then
    markdown = require('markdown')
    if markdown == nil or markdown == '' then
      content = "<h2>Error</h2>\n<p>Markdown not found.</p>"
      return
    end
    local single_post = render_makefly_single_post(blog_path .. '/src', name) or ''
    post_content = markdown(single_post)
  end
  content = post_content
  return
end

function render(content)
  -- templates
  header = readFile('tmpl/header.tmpl', 'r')
  footer = readFile('tmpl/footer.tmpl', 'r')
  -- header
  print("Content-type: text/html\n\n")
  -- page
  print(header)
  if DEBUG == true then
    print("<div id='dev'>")
    print("<h2>Dev Info</h2>")
    print("<p>query_string: " .. QUERY_STRING .. "<br/>")
    print("Req: " .. REQUEST_METHOD .. "<br/>")
    a = os.getenv('HTTP_REFERER') or ''
    b = os.getenv('REQUEST_URI') or ''
    print("HTTP_REFERER | REQUEST_URI: " .. a .. '|' .. b .. "<br/>")
    print("Config: Engine, " .. config['engine'] .. '. Path, ' .. config['path'] .. "</p>")
    print("</div>")
  end
  -- content
  print(content)
  -- footer
  print(footer)
end

-- MISCELLANEOUS FUNCTION
function check_blog_engine()
  msg = ''
  res = true
  if config and config['engine'] ~= 'makefly' then
    msg = '<p>Selected engine unknown: ' .. config['engine'] .. '</p>'
    res = false
  end
  return res, msg
end

-- BEGIN
-- routing
if REQUEST_METHOD and REQUEST_METHOD == 'GET' and QUERY_STRING then
  if QUERY_STRING == 'home' then
    content = 'Accueil'
  elseif QUERY_STRING == 'list' then
    post_list()
  elseif QUERY_STRING == 'config' then
    config_form = [[<h2>Configuration</h2>
    <form METHOD="post" ACTION=.%s>
    <p>Enter data here: <input type="text" name="var1" size="20" maxlength="20">
    <input type="submit" name="submit" value="Validate">
    </p>
    </form>
    ]]
    REQUEST_URI = os.getenv('REQUEST_URI') or ''
    -- delete useless slash '/' at the begining of REQUEST_URI
    REQUEST_URI = string.gsub(REQUEST_URI, "^/*", '')
    content = string.format(config_form, REQUEST_URI)
  else
    qs_vars = QUERY_STRING:split('&')
    for i, values in pairs(qs_vars) do
      if values then
        action, value = string.match(values, "(.+)=(.+)")
	if action == 'post' and value ~= nil then
	  post(value)
	end
      end
    end
  end
elseif REQUEST_METHOD and REQUEST_METHOD == 'POST' and QUERY_STRING and QUERY_STRING == 'config' then
  content = "<h2>Configuration</h2>\n" .. io.read("*a")
end


-- END
render(content)
