% include('header.tpl', title='Notes', blog_title=blog_title, blog_desc=blog_desc)
<a id="new" href="/items/new" title="Publish a new note">
  <article>
    <header>
      <p>What's new today?</p>
    </header>
  </article>
</a>
% for item in items:
% include('item.tpl', identifier=item[0], name=item[1], description=item[2], content=item[3])
% end
% include('footer.tpl', engine=False)
