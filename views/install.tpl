% include('header.tpl', title='Installation')
%if message:
<p class="{{message_type}}">{{message}}</p>
%end
<h3>Installation</h3>
%if installed:
<p>Already installed. <a href="/items">List posts</a></p>
%else:
<form action="/install" method="POST">
<input type="text" size="100" maxlength="100" name="path">
<input type="submit" name="save" value="save">
</form>
%end
% include('footer.tpl', engine=False)
