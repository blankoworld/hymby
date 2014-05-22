<article id="makefly">
  <header>
    <h1>Makefly</h1>
  </header>
  <section>
    <form action="/config" method="POST">
      % for field, value in [(x, config[x]) for x in config]:
      <label for='{{ field }}'>{{ field }}:</label><input type='text' maxlength='256' name='{{ field }}' id='{{ field }}' value='{{ value }}'><br />
      % end
      <input type='submit' name='save_engine' value='Save' id='save_engine'>
    </form>
  </section>
</article>
