# PHP 面试
- PHP 基础知识
- JavaScript/jQuery/Ajax 基础知识
- Linux 基础知识
- MySQL 数据库的基础和优化
- 程序设计题
- PHP 框架基础知识
- 算法、逻辑思维
- 高并发解决方案

## 面试基本流程
- 帅选**个人简历**（HR和技术leader）
- 进行**技术面试**(电话面试/face-to-face面试)
- 商议**薪资待遇**，双方达成共识（HR）
- 办理**入职**流程、上岗

## 求职者的起个等级阶段（君子不器，先要为器，器中成道）
- 架构师（解决方案层次）
- 服务端技术专家（脱离语言，全栈工程师）
- PHP 高级程序猿(大量的项目开发经验，优化和设计)
- PHP 中级程序猿(较多的项目开发经验，优化)
- PHP 初学程序猿(有一定的项目开发经验，功能)
- PHP 初学者(菜鸟，少量代码)
- PHP 爱好者(小白，学习者)

## 常见经典面试题
- 什么是**引用变量**？在 PHP 当中，用什么符号定义引用变量
- 编写 jQuery中，使用处理 **Ajax** 的几种方法
- 写出尽可能多的 **Linux** 命令
- 写出 3 种以上 MySQL **数据库存储引擎**的名称
- 编写在线留言本，实现用户的**在线留言**功能
- 谈谈对 **MVC** 的认识，介绍几种目前比较流行的 MVC 框架
- 编写常见的排序**算法**
- PHP 如何解决网站**大流量和高并发**的问题

## 解题思路和技巧
- **回忆**知识点
- **揣测**面试官的考察思路
- **量**的前提是**精**


## PHP 基础知识
### 引用变量
- 面试：什么是**引用变量**？在 PHP 当中，用什么符号定义引用变量
- 考官考点：
	+ PHP 引用变量的**概念**及**定义方式**
	+ 延伸：PHP **引用变量的原理**

- PHP 引用变量的概念
	+ 不同的名字访问同一个变量内容数据
	+ 程序运行为进程时在内存的物理空间上所有变量名映射为物理内存地址，引用变量存储的是存储数据的地址
- 定义方式
	+ 使用 & 符号定义

- 引用变量的原理
`$a = range(0, 1000); // 30`
内存空间：0x00000001($a) => 30
`var_dump(memory_get_usage());` // int(387800)

`$b = $a;`
PHP Cow(copy on write) 机制：$a和$b都指向同一个30，当其中一个变量改变时才会分配新的内存空间赋值其他数据
- 内存空间：
0x00000001($a) => 30
0x00000002($b) => 0x00000001
简单理解就是: $a,$b => 30
`var_dump(memory_get_usage());` // int(387832)

`$a = 40`
- 内存空间：
0x00000001($a) => 40
0x00000002($b) => 30
简单理解就是: $a等于40, $b等于30
`var_dump(memory_get_usage());` // int(424752)

`$b = &$a;`
- 两个变量都指向同一内存空间地址存储的数据

`<?php
// zaval 变量容器
$a = range(0, 3);
$b = $a;
$d = $a;
$c = & $a;
$f = & $a;
// 需要 xdebug 扩展
xdebug_debug_zval('a');
echo "\n";
xdebug_debug_zval('b');
echo "\n";
xdebug_debug_zval('c');
echo "\n";
echo "-----------------\n";
echo "-----------------\n";
$a = 10;
xdebug_debug_zval('a');
echo "\n";
xdebug_debug_zval('b');
echo "\n";
?>`


- unset 只会取消引用，不会销毁空间
`$a = 1;
$b = &$a;
unset($b);
echo $a; // 1`

- 对象本身也是引用传递
`class Person
{
	public $name = "lingyima";
}
$p1 = new Person;
xdebug_debug_zval('p1');
$p2 = $p1;
xdebug_debug_zval('p1');
$p2->name = "zhangshan";
xdebug_debug_zval('p1');`


- 真题
<?php
$data=['a','b','c'];
foreach($data as $k=>$v)
{
	$v = &$data[$k];
}
// 程序运行时，每一次循环结束后变量$data的值是什么
// 程序执行完成后，变量$data的值是什么？请解释


$data=['a','b','c'];
分配内存地址
0x01 => a
0x02 => b
0x03 => c
data[0] => 0x01
data[1] => 0x02
data[3] => 0x03

- 第一次
$k=0 			0x04 => 0 
$v=a 			0x05 => 0x01
$v=&$data[0] 	0x05 => 0x01
`$data = a,b,c`

- 第二次
$k=1			0x04 => 1
$v=b, 			0x05 => 0x01 
**$v上次是第一次引用变量$v=&$data[0]，所以修改$data[0]=b**			
$v=&$data[1] 	0x05 => 0x02
`$data = b,b,c`

- 第三次
$k=2			0x04 => 2
$v=c, 			0x05 => 0x02 
**$v上次是第二次引用变量$v=&$data[1]，所以修改$data[1]=c**			
$v=&$data[2] 	0x05 => 0x03
`$data = b,c,c`

- 执行结果
`$data = b,c,c`

- 总结：foreach 循环遍历中 **$v是变量元素**第1次循环体开始，首先**引用计数变量**，然后变为**引用变量**并把**当前遍历的变量元素地址**赋给$v，而第二次遍历中由于第一次遍历结果的**$v为引用变量**，所以首先**修改引用变量的值**，然后又把**当前遍历的变量地址**赋给$v，依此类推。除了第一次循环之外，其他循环都会版当前遍历元素值赋给上一次遍历元素。


### 常量及数据类型
- 面试：**PHP中字符串**可以使用哪三种**定义方式**以及各自的**区别**是什么？

- 字符串定义：
	+ 双引号：解析变量，使用特殊字符${}包含变量,解析所有转义字符，可以用.连接符
		* 内容中包含的双引号必须转义
	+ 单引号：不能解析变量，不能解析转义字符，只能解析单引号和反斜线，效率高于双引号
		* 变量和变量、变量和字符串、字符串之间可以.连接符
	+ heredc和newdoc：处理大文本
		* heredoc 类似于双引号: `<<<EoT
		Eot`
		* newdoc 类似于单引号: `'<<<EoT'
		Eot`

#### 数据类型
- 三大数据类型
	+ 标量: boolean, integer, float, string
	+ 复合: array, object
	+ 特殊: null, resource

- 浮点类型：不能用于相等运算符
$a=0.1;
$b=0.7;
// $a+$b=>0.7999
if($a+$b == 0.8)
{
	// 不会执行
}

- 布尔类型
	+ false：0, 0.0, '', '0', false, array(), NULL

- 数组类型
	+ 超全局数据:`$GLOBALS, $_GET, $_POST, $_REQUEST, $_SESSION, $_COOKIE, $_SERVER, $_FILES, $_ENV`

`$_SERVER['SERVER_ADDR'] 服务器IP地址
$_SERVER['SERVER_NAME'] 服务器名称
$_SERVER['SERVER_TIME'] 请求时间
$_SERVER['SERVER_STRING']
$_SERVER['HTTP_REFERER']
$_SERVER['HTTP_USER_AGENT']
$_SERVER['REMOTE_ADDR']
$_SERVER['REQUEST_URI']
$_SERVER['PATH_INFO']`

- NULL
赋值
未定义的变量
unser销毁的变量

- 常量
const(语言结构，更快)，定义类常量 （定义之后不能删除和修改）
define(函数)
defined

- 预定义常量
`__FILE__, __LINE__, __DIR__, __FUNCTION__, __CLASS__, __TRAIT__, __METHOD__, __NAMESPACE__`

- TRAIT: 5.4
<?php
trait Log{
    public function startLog() {
        // echo ..
    }
    public function endLog() {
        // echo ..
    }
}
// Publish.php
<?php
class Publish {
    use Log;
}
$publish = new Publish();
$publish->startLog();
$publish->endLog();
// Answer.php
<?php
class Answer {
    use Log;
}
$answer = new Answer();
$answer->startLog();
$answer->endLog();

- 继承的方式虽然也能解决问题,但其思路违背了面向对象的原则,显得很粗暴;多态方式也可行,但不符合软件开发中的DRY原则,增加了维护成本。而Trait方式则避免了上述的不足之处,相对优雅的实现了代码的复用。

- 类成员优先级为:当前类>Trait>父类

### 运算符
- 面试：foo()和@foo()之间的区别？
- 考点：
1. PHP的运算符的错误控制符@
放置在表达式之前，该表达式可能产生的任何错误信息都被忽略掉

2. 延伸：PHP 所有运算符考点
- 运算符的优先级
	+ clone, new
	+ []，左
	+ `**` 右
	+ ++,--,~ (int|float|string|array|aobject|bool),@ 右
	+ instanceof
	+ ! 右
	+  * / % 左
	+ + - . 左
	+ << >> 左
	+ <, <=, >, >=
	+ ==, !=, !==, <>, <=>
	+ & 左
	+ ^ 左
	+ | 左
	+ && 左
	+ || 左
	+ ?? 左
	+ ?: 左
	+ `=, +=, -=, *=, **=, /=,.=,%=,^=,<<=,>>=`
	+ and 左
	+ xor 左
	+ or 左

`递增/递减>!>算术运算符>大小比较>不相等比较>引用>位运算符(^)>位运算符(|)>逻辑与>逻辑或>三目>赋值>and>xor>or`

**括号：可读性**

- 比较运算符
== 和 === 的区别
等值判断(false的其中情况)
if('==false'){
echo '';
}elseif('0'==0){
	echo '';
} elseif(0.0==0){
	echo '';
}

- 递增/递减运算符
	+ 不影响布尔值
	+ 递减 NULL 值没有效果
	+ 递增 NULL 值为1
	+ ++i，先运算
	+ i--，后运算

- 逻辑运算符
短路作用
||和&& 与 or 和 and的优先级不同

$a = true || $b == 3; // true
$b = false && $a == 1; // false

|| && and or
$a = false || true; // true
$b = false or true; // b=false, 整体true

- 重点递增/递减/运算符的运算规则，逻辑运算符的短路效果，看到逻辑运算符多考虑优先级问题

- 真题
下列程序中请写出打印输出的结果
`<?php
$a = 0;
$b = 0;
if($a = 3>0 || $b=3>0) // $a = true, $b=0
{
	$a++;
	$b++;
	echo $a."\n"; // 1
	echo $b."\n"; // 1
}
$a = 0;
$b = 0;`

### 流程控制
- 面试：列出3种PHP数组操作的语法，并注明各种循环的区别

- 考官考点
	+ 三种遍历数组的方式
	+ 区别
- 延伸：分支结构

- 遍历数组的方式
	+ for: 索引数组
	+ foreach：索引/关联数组
		* 遍历时会对数组进行 reset() 操作
	+ while list(),each()： 索引/关联数组
		* 不会 reset()


- PHP 分支考点

`if...elseif`
**优先范围小的放在前面**

`switch...case...`
- 表达式数据类型只能是**整型，浮点型，字符串型**
`continue` 作用等价于break
`continue 2` 跳出两层循环
**生成跳转表**，直接俄跳转到对应 case
- 效率：体检比一个简单的比较要复杂得多的或者在一个很多次的循环中，switch语句可能快一些

**面试**：如何优化if...else 语句？
- 可能性判断成立大的放在前置
- 判断复杂的判断使用switch case


### 自定义函数及内部函数
- 面试题
写出如下程序的输出结果
`<?php
$count = 5;
function get_count()
{
	static $count; // NULL
	return $count++;
}
echo $count; // 5;
++$count;
echo get_count(); // NULL
echo get_count(); / 1`

- 考官考点：
	+ 变量作用域
	+ 静态变量
	+ 延伸：函数的参数及参数的引用传递
	+ 延伸：函数的返回值及引用返回
	+ 延伸：外部不文件的导入
	+ 延伸：系统内置函数

#### 变量作用域
> 变量的范围，即定义的上下文背景

- 函数内声明全局变量方式：
	+ `global 变量名;`
	+ `$_GLOBALS['变量名'];`
	+ 其他超全局变量
- 静态变量
	+ 尽在局部函数域名存在
	+ 当程序执行离开此作用域时，其值并不会消失

- 静态变量特性
	+ 仅初始化一次
	+ 初始化需要赋值
	+ 每次执行函数该值会保留
	+ static 修饰的变量是局部的，尽在函数内部有效
	+ 记录函数的调用次数，从而可以在某些条件下终止递归

#### 函数的参数
- 默认，函数参数通过值传递
- 可以引用传递参数
`$a = 1;
function fun(& $a)
{
	$a = 2;
}
fun($a);
echo　$a; // 2`


#### 函数的返回值
- 使用 return 语句返回值
- 返回包括数组和对象
- 可以提前返回函数调用处
- 省略 return，返回值为NULL
- 不能有多个返回值

#### 函数的引用返回
- 从函数返回一个引用，必须在函数声明和指派返回值给一个变量时都使用引用运算符 &
function & refFun()
{
	static $b = 10;
	return $b;
}
$a = refFun(); // 10
$b = &refFun(); // 10，与静态变量$b互为引用
$b = 100;
echo refFun(); // 100


<?php
$out = 10;

`function &referenceFunc(&$param)
{
        static $inner = 100;
        $param++;
        return $inner++;
}
echo "out=".$out ."\n"; // 10
$a = referenceFunc($out);
$a = referenceFunc($out);
echo "a=".$a."\n";      // 100
echo "out=".$out ."\n"; // 11
$b = &referenceFunc($out);
echo "a=".$b."\n";      // 101
echo "out=".$out ."\n"; // 11
$a = referenceFunc($out);
echo "a=".$a."\n";      // 100
echo "out=".$out ."\n"; // 11`

#### 外部文件的导入
- include/require 语句包函并运行指定文件
- 如果没有给出路径，否则从include_path 环境变量查找
- include_path 路径没有，则从调用脚本文件所在的目录和当前工作目录下寻找

- 加载过程中没有找到文件
	+ include 结构会发出警告
		* E_WARNING 脚本继续执行
	+ require 会发出致命错误
		* E_COMPILE_ERROR 脚本终止

#### 系统函数
- 时间日期函数：
	 + date()
	 + strototime()
	 + mktime()
	 + time()
	 + microtime()
	 + date_default_timezone_set()

- IP 处理函数
	+ ip2long()
	+ long2ip()

- 打印处理
	+ print() 仅可打印一个变量
	+ printf() 
	+ print_r() 格式化输出
	+ echo() 可打印多个变量
	+ sprintf() 
	+ var_dump() 数据类型
	+ var_export() 

- 序列化
	+ serialize()
	+ unserialize()

- 字符串处理
	+ implode()
	+ explode()
	+ join()
	+ strrev()
	+ trim/ltrim/rtrim
	+ strstr()
	+ number_format()

- 数组处理函数
	+ array_keys
	+ array_values
	+ array_diff
	+ array_intersect
	+ array_merge
	+ array_shift
	+ array_unshift
	+ array_pop
	+ array_push
	+ sort

### 正则表达式
- 至少写出一种验证139开关的11位手机号码的正则表达式



### 文件及目录处理


### 会话控制


### 面向对象


### 网络协议


### 开发环境相关


## JavaScript/jQuery/Ajax 基础知识

### javaScript
- 面试：下列不属于 JavaScript 语法关键/保留字的是（var,$,function,while）

- 考官考点
	+ JavaScript语法
	+ 延伸：JavaScript 内置对象
	+ 延伸：HTML DOM 对象
	+ jQuery 基础知识

- 变量的定义
	+ 必须以字母、$和_符号开头
	+ 变量名大小写敏感
	+ var 关键字声明变量
	+ 可以声明很多变量
	+ 未使用值来声明的变量，值是 undefined
	+ 重新声明 JavaScript 变量，该变量的值不会丢失
		* var a = 1;
		* var a; // 1

- 数据类型
	+ String
	+ Number
	+ Boolean
	+ Array
	+ Object
	+ Null
	+ Undefined

- JavaScript 变量都是对象。
- 声明一个变量，就创建一个新的对象	
- 创建对象
	+ new Object()
	+ 使用构造器
	+ 使用 JSON 对象
- 函数
	+ 定义方法
	+ 无默认值
	+ 函数内部声明的变量（使用var）是局部变量
	+ 函数外声明的变量是全局变量，所以脚本和函数都能访问它
- 运算符
	+ 加号可以字符串拼接

- else if 必须分开写
- 内置对象
	+ Number:
		* var pi = 3.14;
		* var n = New Numer(value);
		* var n = Number(vaue);
	+ String
		* var str = 'string';
		* var str = new String(s);
		* var str = String(s)
	+ Boolean
		* var b = true;
		* var b = new Boolean(value);
		* var b = Boolean(value);
	+ Array
		* var a = new Array();
		* var a = new Array(size);
		* var a = new Array(e1,e2,e3,...en);
	+ Date
		* var d = new Date();
	+ Math
		* var pi = Math.PI;
		* var s = Math.sqrt(15);
	+ RegExp
		* /pattern/attributes
		* new RegExp(pattern, attributes);
- Windows 对象
	+ windows
	+ Navigator
	+ Screen
	+ History
	+ Location
- DOM 对象
	+ Document
	+ Element
	+ Attribute
	+ Event

- jQuery 基础知识
	+ jQuery 选择器
		* 基本
		* 层次
		* 过滤
		* 可见性过滤
		* 属性过滤
		* 子元素过滤
		* 表单对象过滤
	+ jQuery 事件
	+ jQuery 效果
	+ jQuery DOM 操作
		* 属性
		* 值
		* 节点
		* CSS
		* 尺寸
		






### Ajax 基础内容考点
- 面试：Ajax 技术利用了什么协议？简述 Ajax 的工作机制
- 考官考点
	+ Ajax 的基本工作原理
	+ 延伸：jQuery 的 Ajax 操作

#### Ajax 的基本工作原理
> Asynchronous JavaScript and XML
- 通过在后台与服务器进行少量数据交换，Ajax 可以使网页实现异步更新

- **Ajax 工作原理**
	+ XMLHttpRequest 是Ajax 的基础
	+ XMLHttpRequest 用于在后台与服务器交换数据

- XMLHttpRequest 对象请求
open(method,url,is_async)
send(string)

- XMLHttpRequest 对象响应
responseText
responseXML
onreadstatechange
readState
	0: not init
	1: 服务器连接已建立
	2: 请求已接受
	3: 请求处理中
	4: 请求已完成，且响应已就绪

status: 200, 400

- 常用方法
$(ele).load()
$.ajax()
$.get()
$.post()
$.getJSON()
$.getScript()

- 编写 jQuery中，使用处理 **Ajax** 的几种方法

## Linux 基础知识
- 写出尽可能多的 **Linux** 命令

### 常用命令
+ 系统安全：
	* sudo, su, chmod, setfacl
+ 进程管理：
	* w,top,ps,kill,pkill,pstree,killall
+ 用户管理：
	* id,usermod,useradd,groupadd,userdel
+ 文件系统：
	* mount,umount,fsck,df,du
+ 系统关机和重启
	* shutdown,reboog
+ 网络应用
	* curl,wget, telnet, mail, elinks
+ 网络测试：
	 * ping, netstat, host
+ 网络配置
	* hostname, ifconfig
+ 常用工具
	* ssh,screen,clear,who,date
+ 软件包管理
	* yum,rpm,apt-get
+ 文件查找和比较
	* locate,find
+ 文件内容查看
	* tail,head,less,more
+ 文件处理
	* touch, unlink, rename, ln, cat
+ 目录操作
	* cd,mv,rm,pwd,tree,cp,ls
+ 文件权限属性
	* setfact, chmod, chown, chgrp
+ 压缩/解压
	* bzip2/bunzip2, gzip/gunzip,zip/unzip,tar
+ 文件传输
	* ftp,scp

### 延伸：
- 系统定时任务
	+ crontab 命令
	+ crontab -e
	+ `分 时 日 月 周 命令`格式
	+ at 命令: at 2:00 tomorrow
		* at> /path/to/do_job
		* at>Ctrl+D
- vim 编辑器
	+ 一般模式：删除/赋值/粘贴
	+ 编辑模式：i/I/o/O/a/A/r/R
	+ 命令行模式:
		* :,/,?
		* :$,.d
	+ 移动光标
	+ 查找替换：
		* /work, ?work, :n1,n2s/workd1/work2/g
		* :1,$s/workd1/workd2/g,
		* :1,$s/workd1/workd/gc
	+ 删除/粘贴/粘贴
		* x/X,dd,ndd,yy,nyy,p,P,Ctrl+r, ., u
	+ 保存退出
		* w/wq
	+ 视图模式
		* v,V
		* Ctrl+v
		* y,d
	+ 配置：
		* :setnu,
		* :setnonu
- shell 编程
	+ 脚本执行权限：
		* chmod +x test.sh; ./test.sh
		* 调用解释器执行脚本：bash/csh/sh/bash/ksh
		* source 命令
	+ 编写
		`#!/bin/bash`
		
- 面试：0 晨重启服务
`0 0 * * * reboot`



## MySQL 数据库的基础和优化

### MySQL基础知识

### 创建高性能索引

### SQL语句编写和优化

### MySQL 高可扩展和高可用及安全性考察点

## 程序设计题

- 面试：编写一个在线留言本，实现用户的在线留言功能，留言信息存储到数据库，要求设计数据表内容以及使用PHP编写完成
- 考官考点：
	+ 数据库表设计
	+ 数据表创建语句
	+ PHP 连接数据库的方式
	+ 编码能力

### 数据表设计
- 分析数据表结构
- 留言板有哪些信息要存储
- 留言信息：id,title,content,add_time,name

- MySQLi: 支持MySQL操作、支持预处理、面向对象和过程，效率较高
- mysql: 支持MySQL操作，没有预处理、面向过程


`form(action=store.php, method=post)
	input(type=text,name=title)
	textarea(name=content)
	input(type=text,name=name)
	submit`

`$title = $_POST['title']
$content = $_POST['content']
$name = $_POST['name']
if (empty($title) || empty($content) || empty($name))
{
	exit('title or content is empty')
}
try 
{
	$dsn = 'mysql:dbname:test;host=localhost';
	$user = 'test';
	$passwd = 'test';
	$attr = [
		PDO::ATTR_ERRMODE => pdo::ERRMODE_EXCEPTION
	];
	$pdo = new DPO($dsn, $user, $passwd, $attr);
	$sql = 'insert into message(title,content,add_time,name) values(:title, :content, :add_time, :name)';
	$stmt = $dpo->prepare($sql);
	$data = [
		':title' => $title,
		':content' => $content,
		':add_time' => time(),
		':name' => $name
	];
	$stmt->execute($data);
} 
catch(PDOException $e)
{
	echo $e->getMessage();
}
`

- 面试：设计一个无限分类表
id/title/pid/path
1/服装/0/0-1
2/上衣/1/0-1-2
3/长轴/2/0-1-2-3

- order by: id/title/pid


## PHP 框架基础知识
- 面试：谈谈对 **MVC** 的认识，介绍几种目前比较流行的 MVC 框架
- 考点：
	+ MVC 工作原理
	+ 常见 MVC 框架
- 延伸：单一入口的工作原理
- 延伸：模板引擎的理解

#### MVC 工作原理
- Model 数据模型操作层
	+ 对数据进行加工及其他处理
- View 视图交互层
	+ 跟用户交互的页面
- Controller 业务逻辑层
	
#### MVC 框架
- ThinkPHP, Yii2, CI, Yaf, Phalcon

#### 单一入口的工作原理
- 用一个处理程序文件处理所有的 HTTP 请求，根据请求参数的不同区分不同模块和操作的请求

- 优势：
	+ 统一的安全性检查
	+ 集中处理程序
- 劣	势
	+ URL 不美观（URL重写）
	+ 处理效率会稍低

#### 模板引擎的理解
- PHP 是 HTML 内嵌式的在服务端执行的脚本语言
- 模板引擎可以将PHP代码与HTML代码进行分开管理

- 常见模板引擎：**Smarty**, Twig, Haml, Liquid
- 工作原理：庞大完善的正则表达式替换库

#### 常见框架的特性特点： 
- 面试：PHP框架都有什么，用过哪些？各自的优缺点是什么？

- 考试考点：
	+ 开发经验
	+ PHP 的框架的差异和优缺点
	+ 遇到那些困难？怎么解决？

##### Yaf 框架
> 以 C 语言编写的PHP 扩展的形式写的，比PHP代码写的框架要快一个数量级。
- 优点：执行效率高、轻量级框架、可扩展性强
- 缺点：高版本兼容性差、底层代码可读性差、需要安装扩展、功能单一、开发需要编写大量的插件

##### Yii2 框架
> 结构简单优雅、使用功能丰富、扩展性强、性能高是它最突出的优点
- 缺点：学习成本高，量级比Yaf重

- 面试：Yii2 框架如何实现数据的自动验证



## 算法、逻辑思维
- 常见数据结构特征
- 算法的工作原理
- 时间复杂度
- 空间复杂度
- 其他逻辑算法
- PHP 内置函数实现

## 高并发解决方案
- 如何理解高并发（PV/UV/QPS）
- 优化时机（QPS 阶段性优化）


### 优化案例
- 防盗链
- 减少 HTTP 请求
- 浏览器缓存
- CDN
- 数据库缓存(Memcache/NoSQL)
- MySSQL 读写分离
- 分区以及分库分表
- LVS 负载均衡


## 面试技巧
- 谦虚谨慎
- 机智应变
- 扬长避短
- 显示潜能

- 忌讳
	+ 不自信
	+ 小动作多
	+ 说话不清晰
	+ 对面试官不屑一顾
	+ 骄傲自大




