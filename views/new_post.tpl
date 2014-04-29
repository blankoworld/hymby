% include('header.tpl')
<h3>{{name}}</h3>
<form action="/items/new" method="POST">
<label for='name'>Title:</label><input type="text" maxlength="128" name="name" id="name"><br />
<label for='description'>Description:</label><input type="text" maxlength="256" name="description" id="description"><br />
<label for='date'>Posting date:</label><input type='date' name='date' id='date'><br />
<label for='tags'>Tags:</label><input type="text" maxlength="128" name="tags" id="tags"><br />
<label for='type'>Type:</label><input type="text" maxlength="64" name="type" id="type"><br />
<label for='keyword'>Keywords:</label><input type="text" maxlength="128" name="keyword" id="keyword"><br />
<label for='author'>Author:</label><input type="text" maxlength="64" name='author' id='author'><br />
<input type="submit" name="save" value="Save">
</form>
% include('footer.tpl')
