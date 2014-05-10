  </div>

  <footer id="footer">
    <hr />
    <p>Powered by <a href="#" title="Hymby">Hymby</a> 
  </footer>

<script type="text/javascript" src="/static/js/jquery.js"></script>
<script src="/static/js/Markdown.Converter.js"></script>
<script src="/static/js/Markdown.Sanitizer.js"></script>
<script language="javascript">
$(function() {
    // When using more than one `textarea` on your page, change the following line to match the one you’re after
    var $textarea = $('textarea'),
    $preview = $('<div id="preview" />').insertAfter($textarea),
    convert = new Markdown.getSanitizingConverter().makeHtml;

    // instead of `keyup`, consider using `input` using this plugin: http://mathiasbynens.be/notes/oninput#comment-1
    $textarea.keyup(function() {
      $preview.html(convert($textarea.val()));
      }).trigger('keyup');
    });
$('.delete').on('click', function () {
      return confirm('Are you sure?');
    });
</script>
</body>
</html>
