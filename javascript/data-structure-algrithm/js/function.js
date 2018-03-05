function echo(text) {
	var tag = arguments.length === 2 ? arguments[1] : 'div';
	var tagNode = document.createElement(tag);
	var textNode = document.createTextNode(text);
	tagNode.appendChild(textNode);
	document.body.appendChild(tagNode);
	var hr = document.createElement('hr');
	document.body.appendChild(hr);
}