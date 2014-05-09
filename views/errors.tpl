% include('header.tpl')
  <article id="error">
    <header>
      <h1>{{ title }}</h1>
    </header>
    <section id="{{ message_type }}">
      <p class="{{ message_type }}">{{ message }}</p>
    </section>
    <footer>
      <p>&nbsp;</p>
    </footer>
  </article>
% include('footer.tpl')
