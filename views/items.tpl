% include('header.tpl', title='Items')
<h3>Posts</h3>
<ul>
% for item in items:
%   title = item[1].get('TITLE', '')
  <li><a href="/item/{{item[0]}}" alt="Read {{title}}">{{title}}</a></li>
% end
</ul>
% include('footer.tpl')
