% include('header.tpl')
<form action="/edit/{{name}}" method="POST">
  <article id="edit post">
    <header>
      <h1><input type="text" name="name" id="name" value="{{forms.get('TITLE', '')}}"></h1>
    </header>
    <section id="metadata">
        <label for='description'>Description:</label><input type="text" maxlength="256" name="description" id="description" value="{{forms.get('DESCRIPTION', '')}}"><br />
        <label for='date'>Posting date:</label><input type='date' name='date' id='date' value="{{forms.get('DATE', '')}}"><br />
        <label for='tags'>Tags:</label><input type="text" maxlength="128" name="tags" id="tags" value="{{forms.get('TAGS', '')}}"><br />
        <label for='type'>Type:</label><input type="text" maxlength="64" name="type" id="type" value="{{forms.get('TYPE', '')}}"><br />
        <label for='keyword'>Keywords:</label><input type="text" maxlength="128" name="keyword" id="keyword" value="{{forms.get('KEYWORDS', '')}}"><br />
        <label for='author'>Author:</label><input type="text" maxlength="64" name='author' id='author' value="{{forms.get('AUTHOR', '')}}"><br />
    </section>
    <section id="content">
        <textarea name="content" rows="20">{{content}}</textarea>
    </section>
    <input type="submit" name="save" value="Save" id="save">
  </article>
</form>
% include('footer.tpl', engine=False)
