% include('header.tpl', title='Items')
<h3>Posts</h3>
<ul>
% for item in items:
  <li><a href="/item/{{item[0]}}" alt="{{item[2]}}">{{item[1]}}</a></li>
% end
</ul>
% include('footer.tpl')
