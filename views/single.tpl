% include('header.tpl', title=data.get('TITLE', ''))
% include('item.tpl', identifier=identifier, name=data.get('TITLE', ''), description=data.get('TITLE', ''), content=content)
% include('footer.tpl', engine=False)
