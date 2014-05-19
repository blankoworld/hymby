<article id="makefly">
  <header>
    <h1>Makefly</h1>
  </header>
  <section>
    <form action="/config" method="POST">
      <label for='installdir'>Installdir:</label><input type='text' maxlength='256' name='installdir' id='installdir' value='{{ config.get('installdir', '') }}'><br />
      <input type='submit' name='save' value='Save' id='save'>
    </form>
  </section>
</article>
