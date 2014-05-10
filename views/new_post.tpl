% include('header.tpl')
<form action="/items/new" method="POST">
  <article id="new post">
    <header>
      <h1><input type="text" name="name" id="name"></h1>
    </header>
    <section id="metadata">
        <label for='description'>Description:</label><input type="text" maxlength="256" name="description" id="description"><br />
        <label for='date'>Posting date:</label><input type='date' name='date' id='date'><br />
        <label for='tags'>Tags:</label><input type="text" maxlength="128" name="tags" id="tags"><br />
        <label for='type'>Type:</label><input type="text" maxlength="64" name="type" id="type"><br />
        <label for='keyword'>Keywords:</label><input type="text" maxlength="128" name="keyword" id="keyword"><br />
        <label for='author'>Author:</label><input type="text" maxlength="64" name='author' id='author'><br />
    </section>
    <section id="content">
        <textarea name="content" rows="20" id="markdown"></textarea>
  <textarea id="html" class="full-height"></textarea>
  <div id="preview" class="full-height"></div>
</section>
    <input type="submit" name="save" value="Save" id="save">
  </article>
</form>
% include('footer.tpl')
