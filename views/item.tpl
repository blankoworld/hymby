<article>
  <header>
    <ol class="actions">
      <li><a class="delete" href="/delete/{{ identifier }}" title="Delete permanently: {{ name }}"><i class="fa fa-times fa-fw"></i></a></li>
      <li><a class="edition-title" href="/edit/{{ identifier }}" title="Edit: {{ name }}"><i class="fa fa-pencil-square-o fa-fw"></i></a></li>
    </ol>
    <h1 class="entry-title"><a href="/item/{{ identifier }}" title="{{ description }}">{{ name }}</a></h1>
  </header>
  <section class="excerpt">
    {{ !content }}
  </section>
  <footer>
    <p>&nbsp;</p>
  </footer>
  <a class="edition" href="/edit/{{ identifier }}" title="Edit: {{ name }}"><i class="fa fa-pencil-square-o fa-fw"></i></a>
</article>
