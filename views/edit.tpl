% include('header.tpl')
<h3>{{name}}</h3>
<form action="/edit/{{name}}" method="POST">
<label for='name'>Title:</label><input type="text" maxlength="128" name="name" id="name" value="{{forms.get('TITLE', '')}}"><br />
<label for='description'>Description:</label><input type="text" maxlength="256" name="description" id="description" value="{{forms.get('DESCRIPTION', '')}}"><br />
<label for='date'>Posting date:</label><input type='date' name='date' id='date' value="{{forms.get('DATE', '')}}"><br />
<label for='tags'>Tags:</label><input type="text" maxlength="128" name="tags" id="tags" value="{{forms.get('TAGS', '')}}"><br />
<label for='type'>Type:</label><input type="text" maxlength="64" name="type" id="type" value="{{forms.get('TYPE', '')}}"><br />
<label for='keyword'>Keywords:</label><input type="text" maxlength="128" name="keyword" id="keyword" value="{{forms.get('KEYWORDS', '')}}"><br />
<label for='author'>Author:</label><input type="text" maxlength="64" name='author' id='author' value="{{forms.get('AUTHOR', '')}}"><br />
<label for='content'>Content:</label><textarea name="content" rows="10" cols="60">{{content}}</textarea><br />
<input type="submit" name="save" value="Save">
</form>
% include('footer.tpl')
