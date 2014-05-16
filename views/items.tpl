% include('header.tpl', title='Items')
<a id="new" href="/items/new" title="Create a new post">
  <article>
    <header>
      <p>What's new today?</p>
    </header>
  </article>
</a>
% for item in items:
<article>
  <header>
    <a class="delete" href="/delete/{{item[0]}}" title="Delete permanently: {{item[1]}}"><span class="fa-stack fa-lg"><i class="fa fa-times fa-stack-1x"></i></span></a><a class="edition-title" href="/edit/{{item[0]}}" title="Edit: {{item[1]}}"><span class="fa-stack fa-lg"><i class="fa fa-pencil-square-o fa-stack-1x"></i></span></a>
    <h1 class="entry-title"><a href="/item/{{item[0]}}" title="{{item[2]}}">{{item[1]}}</a></h1>
  </header>
  <section class="excerpt">
    {{!item[3]}}
  </section>
  <footer>
    <p>&nbsp;</p>
  </footer>
  <a class="edition" href="/edit/{{item[0]}}" title="Edit: {{item[1]}}"><span class="fa-stack fa-lg"><i class="fa fa-pencil-square-o fa-stack-1x"></i></span></a>
</article>
% end
% include('footer.tpl')
