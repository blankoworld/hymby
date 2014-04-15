% include('header.tpl')
<h3>{{name}}</h3>
<form action="/items/new" method="GET">
<input type="text" size="100" maxlength="100" name="name">
<input type="submit" name="save" value="save">
</form>
% include('footer.tpl')
