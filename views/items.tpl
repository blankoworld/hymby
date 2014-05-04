% include('header.tpl', title='Items')
<h3>Posts</h3>
<ul>
% for item in items:
  <li><a href="/delete/{{item[0]}}" title=""><img src="/static/edit-delete.png" alt="delete"/></a> <a href="/item/{{item[0]}}" title="{{item[2]}}">{{item[1]}}</a></li>
% end
</ul>
% include('footer.tpl')
