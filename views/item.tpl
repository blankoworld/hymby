% include('header.tpl')
<article>
  <header>
    <a class="delete" href="/delete/{{identifier}}" title="Delete permanently: {{data.get('TITLE', '')}}"><span class="fa-stack fa-lg"><i class="fa fa-times fa-stack-1x"></i></span></a><a class="edition-title" href="/edit/{{identifier}}" title="Edit: {{data.get('TITLE', '')}}"><span class="fa-stack fa-lg"><i class="fa fa-pencil-square-o fa-stack-1x"></i></span></a>
    <h1 class="entry-title">{{data.get('TITLE', '')}}</a></h1>
  </header>
  <section class="excerpt">
    {{!content}}
  </section>
  <footer>
    <p>&nbsp;</p>
  </footer>
  <a class="edition" href="/edit/{{identifier}}" title="Edit: {{data.get('TITLE', '')}}"><span class="fa-stack fa-lg"><i class="fa fa-pencil-square-o fa-stack-1x"></i></span></a>
</article>
% include('footer.tpl')
