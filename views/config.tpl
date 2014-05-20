% include('header.tpl', title=title)
<article>
  <header>
    <h1>General</h1>
  </header>
  <section>
    <form action="/config" method="POST">
      <label for='path'>Path:</label><input type='text' maxlength='256' name='path' id='path' value='{{ config.get('general.path', '') }}'><br />
      <input type='submit' name='save' value='Save' id='save'>
    </form>
  </section>
</article>
% include('config.%s.tpl' % (config.get('general.engine', '')), config=engine_config)
% include('footer.tpl', engine=False)
