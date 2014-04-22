<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<style type="text/css">
			body {color:#222; font-size:13px;font-family: sans-serif; background:#fff url(/static/404bg.png) left top repeat-x;}
			h1 {font-size:300%;font-family:'Trebuchet MS', Verdana, sans-serif; color:#000}
			#page {font-size:122%;width:720px; margin:144px auto 0 auto;text-align:left;line-height:1.2;}
			#message {padding-right:400px;min-height:360px;background:transparent url(/static/404.png) right top no-repeat;}
		</style>
		<meta http-equiv="Content-Type" content="application/xhtml; charset=utf-8" />
		<meta name="description" content="Page not found" />
		<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
		<title>Error 404 – Page non trouvée</title>

    <style>
  p.warning {
    background-color: #FCFCE9;
    width: 98%;
    margin: 5px auto;
    padding: 1%;
    border: thin solid gray;
    color: #494949;
  }
  p.error {
    background-color: #FFDFDF;
    width: 98%;
    margin: 5px auto;
    padding: 1%;
    border: thin solid gray;
    color: #494949;
  }

    </style>
	</head>
	<body>
		<div id="page">
		<div id="message">
			<h1>Page not found</h1>
      <p class='{{ message_type }}'>{{ message }}</p>
			<p>For an unexplicable reason the page you request is unreachable.</p>
			<p><a href="/" title="Homepage">Return to the homepage</a></p>
		</div>
		</div>
</body>
</html>
