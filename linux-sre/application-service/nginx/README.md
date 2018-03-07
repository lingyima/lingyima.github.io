# Nginx -[零壹码博客](https://lingyima.com)
> [Nginx官网](http://nginx.org/en/docs)

- C10K(Connections 10000并发)
- 解决C10K[Nginx官网](http://nginx.org/)
- engine X: nginx, Igor Sysoev, Rambler Media
- 二次开发：tengine(taobao), openresty

## 常见HTTP服务器
- httpd-Apache 基金会
- IIS-Microsoft
- GWS-Google

## HTTP请求
- Request
	+ 请求行
	+ 请求头
	+ 请求体
- Response
	+ 状态行
	+ 响应头
	+ 响应体

- curl -v https://lingyima.com
	+ -v: 显示 request/response



## Nginx的特性
- 模块化设计、较好扩展性(3rd modules)
- High reliability
	+ master/worker
- 支持热部署
	+ 不停机而更新配置文件、更换日志文件、更新服务器程序版本
- 低内存消耗
	+ 10000个keep-alive连接模式下的非活动连接仅消耗2.5MB内存
	+ 非活动连接：没有传输数据
- event-driven, aio, mmap(内存映射直接访问磁盘)

## 基本功能
- 纯静态资源的web服务器，能缓存打开的文件描述符
- http, smtp, pop3协议的反向代理服务器，缓存、负载均衡
	+ 正向代理：本地代理（地址转换）
	+ 反向代理：远程代理（地址转换）
- 支持FastCGI (fpm, lnmp), uWSCGI等协议
- 模块化（非DSO机制），著名模块有zip，SSI及图像大小调整
- 支持SSL
		
- web服务器相关的功能：
	+ 虚拟主机、keepalive、访问日志（用户行为分析）、url rewrite、路径别名、基于IP及用户的访问控制、支持速率限制及并发数限制，...

## 扩展功能
- 基于名称和IP的虚拟主机
- 支持keepalive
- 支持平滑升级
- 定制访问日志 ，支持使用日志缓冲区提高日志存储性能
- 支持url rewrite
- 支持路径别名
- 支持基于IP及用户的访问控制
- 支持速率限制，支持并发数限制
		
## Nginx arch
### master/worker
- 一个master进程，可生成一个或多个worker进程，每个worker响应n个请求
	+ master：加载配置文件、管理worker进程、平滑升级
	+ worker：http服务、http代理、fastcgi代理

- 事件驱动： epoll, kqueue, /dev/poll (event ports)
- 消息通知：select, poll, rt signals
- 磁盘IO	
	+ 支持sendfile, sendfile64
	+ 支持AIO
	+ 支持mmap（内存与磁盘映射关系）


## Nginx用来做什么？
- 静态资源的web服务器
- http协议反向代理


## Nginx 模块类型
- 核心模块：Core modules
- 标准模块：Standard HTTP modules
	+ Standard HTTP modules
	+ Optional HTTP modules
	+ Mail modules
- 第三方模块：3rd party modules

## 编译安装Nginx(epel源)：major.minor(偶数，稳定版).release
`/etc/yum.repos.d/nginx.repo
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/OS/OSRELEASE/$basearch/
gpgcheck=0
enabled=1`

`yum -y groupinstall "Development Tools" "Server Platform Development"`
`yum -y install pcre-devel openssl-devel zlib-devel`
./configure --prefix=/usr/local/nginx \
--user=nginx --group=nginx \
--sbin-path=/usr/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \ 		
--http-log-path=/var/log/nginx/access.log \
--pid-path=/var/run/nginx/nginx.pid \
--lock-path=/var/lock/nginx.lock \

编译模块：启用--with, 禁用--without
--with-http_ssl_module \
--with-http_stub_status_module \		状态页
--with-http_gzip_static_module \
--with-http_flv_module \				
--with-http_mp4_module \
--with-debug \

临时文件缓冲目录
--http-client-body-temp-path=/var/tmp/nginx/client \	上传文件临时缓冲目录
--http-proxy-temp-path=/var/tmp/nginx/proxy \			代理服务器缓冲目录
--http-fastcgi-temp-path=/var/tmp/nginx/fastcgi \		Fastcgi临时缓冲目录
--http-uwsgi-temp-path=/var/tmp/nginx/uwsgi \
--http-scgi-temp-path=/var/cahe/nginx/scgi \

make && make install





			
## Nginx 信号控制
- TERM,INT: Quick shutdown
- QUIT： gracefull shutdown，优雅关闭进程，等待请求结束后在关闭
- HUP: 平滑重读配置文件(旧进程使用就配置文件，新进程使用新配置文件)
- USR1: 重读日志，在日志按月/日分割时有用
- USR2: 平滑升级
- WINCH: 优雅关闭旧的进程（配合USR2来进行升级）

## nginx 服务
- /usr/local/nginx/
	+ conf 配置文件
	+ html 网页文件
	+ logs 日志文件
	+ sbin 二进制程序

- 启动服务
`# /usr/local/nginx/sbin/nginx`

- 重读配置文件
`# nginx -HUB PID`

- 关闭服务
`# kill -QUIT pid`

- PID：主进程

- kill -signal `cat /usr/local/nginx/log/nginx.pid`


## 配置文件的组成部分
- 主配置文件：`/etc/nginx/nginx.conf`
	+ `include conf.d/*.conf`
- fastcgi,scgi,uwscgi的相关配置
	+ fastcgi.conf
	+ fastcgi_params
	+ fastcgif.conf.default 默认配置
- mime.types

## 配置指令（必须以分号结尾）
`directive value1 [value2...];`
		
- 支持使用变量：
	+ 内置变量：由模块引入，可直接引用
	+　自定义变量：`set variable_name value;`
	+ 应用变量：`$variable_name`

## 配置文件结构
- main block：全局配置(对http及mail模块均有效)
- event{ ...}：事件驱动的相关配置
- http { ... }：http协议的相关配置
- mail { ... }：mail相关的配置

- http相关的配置
`http {
	...
	server {
		server_name
		root
		alias
		location /uri/ {
			...
		}
	}
	server {...}
	...
}`


## main block
- 配置指令的类别
	+ 正常运行必备的配置；
	+ 优化性能的配置；
	+ 用于调试、定位问题的配置；

### 正常运行必备的配置

#### user USERNAME [GROUPNAME]
- 指定用于运行 worker 进程的用户和组
- user nginx nginx;

#### pid /PATH/TO/PID_FILE
- 指定nginx进程pid文件路径
- pid /var/run/nginx.pid;

#### worker_rlimit_nofile number;
- 单个worker进程所能够打开的最大文件数
- worker_rlimit_nofile 1024;

### 性能优化相关的配置

#### worker_process number | auto
- worker的进程数；
- 通常应该为CPU的核心数减1（原因操作系统运行一个Core）；

- auto: nginx 1.8+支持

- 16 core：
- 15 core: 每个worker进程绑定每个核心（不用进程调度）
- 1 core：运行操作系统

- worker_process auto;

- `# ps aux`
- `# lscpu`
	+ CPU(s) : 4
	+ On-line CPU(s) list: 0-3
	+ 座：2
	+ Core(s) per socket: 2

#### worker_cpu_affinity cpumask ...;
- worker_cpu_affinity auto [cpumask];
- cpumask: 0000 0000 - 1111 1111
- 0000 0001：第0颗
- 0000 0010: 第1颗
- 0000 0100：第2颗
- 0000 1000：第3颗

#### worker_processes 2;
- worker_cpu_affinity 0010 0100; 第1个和第2个颗
- `# ps axo command,pid,psr`

#### worker_priority number;
- 进程优先级
- [-20,19] 100-139
- worker_priority -5;
- `# ps axo command,pid,psr,ni`

### 调式、定位问题
#### daemon on | off;
- 是否守护进程方式启动nginx进程；
- 默认on
- 调试是off，前台查看信息

#### master_process on | off;
- 正常：是否以master/worker模型启动nginx进程
- 调试：off

#### error_log file | stderr | syslog:server=address[,parameters=value]
| memory:size [debug | info | notice |warn | error | crit | alert | emerg]; 

- 错误日志文件的记录方式及其日志级别

- `file /PATH/TO/SOME_LOG_FILE;`
- `stderr`：发送到错误输出; 当前终端
- `syslog:server=address[,parameter=value]`:发送给 syslog 服务器
- `memory:size` （大量并发时性能更佳）
	+ 打开缓冲：写入内存，然后定期写入到磁盘上

- 日志级别：
	+ debug依赖于configure时的`--with-debug`模块选项;

## 事件相关的配置

#### worker_connections number;
- 每个worker进程所能够并发打开的最大连接数: 65535
- 依赖于：`worker_rlimit_nofile`
- 最大并发连接数：`worker_processes * worker_connections`

#### use method;
- 指明并发了请求处理时使用的方法
- use epoll;  

#### accept_mutex on(default) 或 off;
- 启用时，表示用于让多个worker进程轮流的、序列化的响应新请求

## http配置
> 定义套接字相关功能

- 配置一个虚拟主机
`server {
	listen PORT;
	server_name HOSTNAME;
	root /PATH/TO/DOCUMENTROOT;
}`

- 基于**port**的虚拟主机
	+ listen 指令要使用不同的端口；
+ 基于 **hostname** 的虚拟主机；
	+ server_name指令指向不同的主机名
+ 基于 **ip** 的虚拟主机
	+ listen IP:PORT;

- listen address[:port][default_server][ssl][backlog=number][rcvbuf=size][sndbuf=size]
- listen port [default_server][ssl];
- listen unix:path [default_server][ssl];
	+ default_server: 默认虚拟主机
	+ ssl：限制只能通过 ssl 连接提供服务
	+ backlog：后援队列的长度
	+ rcvbuf: 接受缓冲区大小
	+ sndbuf：发送缓冲区大小

- server_name name
	+ 指明当前 server 的主机名;
	+ 后可跟一个或空白字符分隔的多个主机；
	+ 支持使用`*`任意长度的任意字符；
	+ 支持 ~ 起始的正则表达式模式字符串；

### 应用策略：主机名匹配优先级
1. 精确匹配
2. 左侧`*`通配符匹配 （`*`:任意长度任意字符，.:任意字符）
3. 右侧`*`通配符匹配
4. 正则表达式模式匹配

- www.lingyima.com

`server_name www.lingyima.com;
server_name *.lingyima.com
server_name www.lingyi.*;
server_name ~^.*\.lingyima\..*$;
mail.lingyima.com, www.lingyima.com`

#### tcp_nodelay on | off;
- 对 **keepalived** 模式下的连接是否启用 TCP_NODELAY 选项；
- 服务器将小数据多个报文合并起来发送一个，web客户端影响速率。
- 服务器不等待合并报文，直接发送小报文
- （请求小的报文，服务器不发送了。比如图片...）

#### sendfile on | off;
- 是否启用sendfile功能，默认off
- 在内核中直接包装响应报文

### 定义路径相关配置
#### root path;
- 设置web资源路径映射；
- 用于指明用户请求的URL所对应的本地文件系统上的文档所在目录路径； 
- Context: http,server,location,if in location
- `root html;` 相对于安装 nginx 的 prefix 配置路径

- 标准化（运维：稳定、标准化、自动化）
	+ OS 硬件配置标准化
	+ OS 标准化
	+ application 版本标准化
	+ 配置文件标准化
	+ 配置路径标准化
	
#### location [ = | ~ | ~* | ^~] uri {...}
- `location @name {...}`
- 根据用户请求的 URI 来匹配定义的 location，匹配到时，此请求将被相应的 location 块中的指令所处理

1. `=`：URI精确匹配
2. `^~`：对URI的左半部分匹配检查，不分区字符大小写
3. `~`：正则表达式模式匹配，区分字符大小写
4. `~*`：正则表达式模式匹配，不区分字符大小写

- 匹配优先级：`=、^~, ~/~*, 不带符号`
- 同一个优先级，匹配长的优先级更高~~

	server {
		location / {
			...
		}
		location ~*\.txt {
			gzip on;
		}
	}

#### alias path;
> 定义路径别名，文档映射的一种机制；仅能用于location上下文
	
`location /i/ {
	alias /web/v2/images/;
}`

- 注意：
	+ root 指令，给定的路径对应于 location 中的**/**uri/，左侧的/
	+ alias指令，给定的路径对应于location中的/uri**/**，右侧的/

#### index file ...
> 设置默认主页
- Context: http, server, location

#### error_page code ... [=response] uri;
> 根据用户请求的资源的http响应的状态码实现错误页重定向
- error_page 404 =200 /404.html;
- 404以200状态响应
- http://www.lingyima.com/hello.html ->因为资源不存在而被改为 
- http://www.lingyima.com/404.html

- error_page 404 /404.html;
	+ 客户端响应码为**404**

- error_page 404 =200 /404.html;
	+ 客户端响应码为**200**

#### try_files file ... uri;
> try_files file 尝试访问没有文件，则显示最后一个文件内容
- Context: server, location

`location /images/ {
	try_files $uri /images/default.gif;
}
location /test/ {
	try_files /web/host1/test/test1.html /web/host1/test/test2.html /web/host1/test/test3.html http://192.168.1.61/index.html;
}`

`# nginx -t `
`# nginx -s reload`

### 定义客户端请求的相关配置

#### keepalive_timeout timeout [header_timeout];
> 设定保持连接的超时时长，0 表示禁止长连接；默认为 75s;
- 客户端连接服务器nginx连接超时时长

#### keepalive_requests number;
> 在一次长连接上所允许请求的资源的最大数量，默认为100

#### keepalive_disable none | browser ...;
> 对哪种浏览器禁用长连接；

#### send_timeout time; 
> 向客户端发送响应报文的超时时长；特别的，是指两次写操作之间的间隔时长；

#### client_body_buffer_size size;
> 用于接受客户端请求报文的body部分的缓冲区大小；默认为16k；超时此文件时，其将被暂存到磁盘上；

#### client_body_temp_path path [level1 [ level2 [level3]]]
> 设定用于存储客户端请求报文的body部分的临时存储路径及子目录结构和数量， URI md5 首字符[0-f]
- /var/tmp/body/2 1 2
- 2个16个进制
- 2,00-ff = 256
- 1,00-0f = 15
- 2,00-ff = 256

### 对客户端请求进行限制的相关配置
#### limit_rate rate;
- limit_rate 0;
- Context: http, server, location, if in location

- 限制响应给客户端的传输速率，单位是bytes/second，0表示无限制；
- 示例：`location /donwload/ { limit_rate 20; }`

`# nginx -t`
`# nginx -s reload`
`# mkdir /web/host1/download`
`# dd if=/dev/zero of=/web/host1/donwload/test.img bs=1m count=50`
`# wget http://192.168.1.71/download/test.img`

#### limit_except method ... {...}
> 限制对指定的请求方法之外的其他方法的使用客户端
- Context: http,server,location if in location
`limit_except GET POST {
	allow 192.168.1.0/32;
	deny all;
}`	
- 表示除了GET和POST之外的其他方法仅允许192.168.1.0/32中主机使用
`# curl -X PUT http://host/donwload/index.html`

- 403 forbidden => 没有权限
- 405 Not Allowed：没有写权限

### 文件操作优化的配置
#### aio on | off | threads[=pool];
> 是否启用aio功能，默认off

#### directio size | off(default)
> 直接IO输入磁盘上，没有缓存到内存上
> 影响性能，数据可靠性增强

#### open_file_cache off;
> 打开的文件缓存
- open_file_cache max=N [inactive=time];

- nginx可以缓存一下三种信息：
	+ (1) 文件的描述符、文件大小和最近一次的修改时间
	+ (2) 打开的目录的结构
	+ (3) 没有找到的或没有权限访问的文件的相关信息

- max=N：可缓存的缓存项上限；达到上限后会使用LRU算法实现缓存管理（清除LRU条目）
- inactive=time：缓存项的超时时长，在此处指定的时长内未被命中的缓存项即为非活动项；
- LRU：最近最少使用算法

#### open_file_cache_errors on | off;
> 是否缓存查找是发送错误的文件一类的信息

#### open_file_cache_min_uses number;
> 在 open_file_cache 指令的 inactive 参数指定的时长内，至少命中此处指定的次数方可不被归类到非活动项

#### open_file_cache_valid time;
> (什么时候删除)缓存项有效性的检查频率；默认是60s;


## ngx_http_access_module模块：
> 实现基于ip的访问控制功能：

- http_access_module局限性：
	+ $remote_addr: proxy_ip
	+ $x_forwarded_for: client_ip, proxy_ip1, proxy_ip2,...
- http_access_module局限性 solution：
	+ 采用别http头信息控制访问，http_x_forward_for
	+ 结合geo模块
	+ http自定义变量传递

### allow address | CIDR | unix: | all;
> Context: http, server, location, limit_except

- CIDR: 网段
- unix: socket
- all:

### deny address | CIDR | unix: | all;
> Context: http, server, location, limit_except

## ngx_http_auth_basic_module模块:
> 实现基于用户的信任登录访问控制功能： 

### auth_basic string | off;
> 使用basic机制进行用户认证
`location / {
	auth_basic "closed site";
	auth_basic_user_file conf/htpasswd;
}`

### auth_basic_user_file file
> 认证用的账号密码文件

- 文件格式：明文密码
	+ name:password:comment

- 密码格式：httpd模块
	+ htpasswd命令

- 示例：-m=md5, -c=create file
`# yum -y install httpd-tools`
`# htpasswd -c -m /etc/nginx/.ngxpasswd tom`
`# htpasswd -m /etc/nginx/.ngxpasswd jerry`

- 认证
`location /admin/ {
	auth_basic "Admin Area";
	auth_basic_user_file /etc/nginx/.ngxpasswd;
}`


- solution
	+ Nginx结合Lua实现高效验证
	+ Nginx和LDAP打通，利用nginx-auth-ldap模块



## ngx_http_stub_status_module模块:
> 用于输出nginx的基本状态信息（脚本获取状态信息）
- Syntax: stub_status;
- Default: --
- Context: server, location


### stub_status
`location /status {
	stub_status;
}`

- 地址访问：https://ip/status

- Active connections: 1 活动的连接数
- Server accepts handled requests  服务器接受处理的请求数
- 155 155 298  (握手数|连接数|请求数)
- Reading:0 Writing:1 Waiting:0

- Active connections: 处于活动状态的客户端连接数量
- 请求、等待、响应等

- 服务器接受处理请求数量，过去的结果
	+ accepts：已经**接受**的客户端连接的总数
	+ handled：已经**处理完成**的客户端请求的总数
	+ request：客户端发来的**总的请求数**

- 当下结果
	+ Reading: 处于读取客户端**请求报文首部**的连接数量
	+ Writing: 处于向客户端发送**响应报文**过程中的连接数
	+ Waiting: 处于等待客户端发出请求的**空闲**连接数
		* 很多参数，keep-alive太长了


## [ngx_http_random_index_module 模块](http://nginx.org/en/docs/http/ngx_http_random_index_module.html)
> 目录中选择一个随机主页

- Syntax: `random_index on | off`;
- Default: `random_index off`;
- Context: `location`

- 实例代码
location /{
	root /usr/share/nginx/html;
	random_index on;
	#index index.html idnex.htm;
}
[零壹码博客](https://www.lingyima.com)中有[ngx_http_random_index_module模块详解](https://www.lingyima.com/ngx_http_random_index_module.html)


## Nginx 请求限制
### http协议的连接与请求
- HTTP协议/连接关系
- HTTP1.0/tcp 不能复用
- HTTP1.1/循序性TCP复用
- HTTP2.0/多路复用TCP复用

- http 请求建立在一次 TCP 连接基础上
- 一次 TCP 请求至少产生一次 HTTP 请求



### 连接频率限制(握手数量限制)：limit_conn_module
- Syntax: limit_conn_zone key zone=name:size;
- Default: -
- Context: http

- Syntax: limit_conn zone number; number并发连接
- Default: -
- Context: http, server, location

### 请求频率限制(发送数量限制)：limit_req_module
- Syntax: limit_req_zone key zone=name:size rate=rate;
- Default: -
- Context: http

- Syntax: limit_req zone=name [burst=number] [nodelay]
	+ burst
	+ nodelay
- Default: -
- Context: http, server, location

http {
	# 同一个客户端IP地址请求每秒1个请求
	# 1m: 空间
	# 1m 空间 $remote_addr 比$binary_remote_addr 多余10个字节
	limit_req_zone $binary_remote_addr zone=req_zone:1m rate=1r/s;

	server {
		location /{
			# 三个延迟执行，其他不响应
			limit_req zone=req_zone burst=3 nodelay;
			limit_req zone=req_zone;
		}	
	}
}

- 压力测试：
n:总重请求数，c:并发数
`# ab -n 40 -c 20 http://ip/1.html`
- Non-2xx reponses: 16 响应数量


## ngx_http_sub_module模块
--with-http_sub_module
> http 内容替换
- http响应体替换

### sub_filter
- Syntax: sub_filter string replacement
- Default: -
- Context: http, server, location

### sub_filter_last_modified
- Syntax: sub_filter_last_modified on `|` off;
	+ on: 判断是否更新
	+ off: 判断是否更新
- Default: sub_filter_last_modified off;
- Context: http, server, location

### sub_filter_once on `|` off;
- default: sub_filter_once on; 
	+ on: 仅匹配第一个
	+ off: 都匹配
- context: http, server, location

## ngx_http_referer_module模块
> 引用参考

### valid_referers none | blocked | server_names | string ...;
> 定义合法的referer数据

- none：请求报文首部没有referer首部
- blocked：请求报文首部的referer首部没有值
- server_names：其值是主机名，指定下面两个类型
- arbitrary string：直接字符串，可以使用`*`作为通配符
- regular expression：被指定的正则表达式模式匹配到的字符串
- 要使用~起始


- 示例：**防盗链**
`valid_referer none blocked server_names *.ligyima.com lingyima.* ~\.google\.;`
`if ($invalid_referer) {
	return 403;
}`

## ngx_http_ssl_module模块
> 一个IP对应一个https虚拟主机

### ssl on | off;
> 是否启用当前虚拟主机的ssl功能

### ssl_certificate file;
> 当前虚拟主机使用的PEM格式的证书文件

### ssl_certificate_key file;	
> 当前虚拟主机使用的证书文件中的公钥配对儿的私钥文件路径
- PEM格式

### ssl_protocol [SSLv2] [SSLv3] [TLSv1] [TLSv1.1] [TLSv1.2]
> SSL协议的版本

### ssl_session_cache off | none [builtin[:size]] [shared:name:size]
> ssl会话的缓存机制
- off 禁止使用会话
- none 
- builtin：使用openssl内建的缓存机制，此为各worker独有
- shared: 由各worker共享的缓存
	+ name：缓存空间的名称
	+ size：字节为单位的缓存空间的大小；每1MB内存空间可缓存4000个会话
- ssl_session_cache builtin:1000 shared:SSL:10m;

### ssl_session_timeout time
> ssl会话超时时长，指ssl session cache中缓存条目有效时长
- 默认为5m(分钟)

- 示例：
`# cd /etc/nginx`
`# (umask 077;openssl genrsa -out ssl/nginx.key 1024)`
`# ls -l ss/`
`# cd ssl/`

- 证书签署请求文件
`# openssl req -new -key nginx.key -out nginx.csr -days 365`
CN,Beijing,Beijng,Lingyima, Ops, www.lingyima.com,adminmaster@lingyima.com

- 生成私钥
`# cd /etc/pki/CA`
`# (umask 077;openssl genrsa -out primate/cakey.pem 2048)`
`# openssl req -new -x509 -key private/cakey.pem -out cacert.pem -days 365`
CN,Beijing,Beijng,Lingyima, Ops, ca.lingyima.com,camaster@lingyima.com
`# touch index.txt`
`# echo 01 > serial`
`# openssl ca -in /etc/nginx/ssl/nginx.csr -out /etc/nginx/ssl/nginx.crt -days 365`
`# cd /etc/nginx/ssl`
`# vim /etc/nginx.conf`
	server {
		listen 443 ssl;
		server_name www.lingyima.com;
		ssl_certificate /etc/nginx/ssl/nginx.crt;
		ssl_certificate_key /etc/nginx/ssl/nginx.key;

		ssl_session_cache shared:SSL:10m;
		ssl_session_timeout 5m;

		ssl_ciphers HIGH:!aNULL:!MD5;
		ssl_prefer_server_ciphers on; 倾向于use server ciphers
		location / {
			root html;
			index index.html index.htm;
		}
	}
`# nginx -t`
`# ss -tnl`
`# curl https://www.lingyima.com`

## ngx_http_log_module模块 **腾讯分析**

### access_log path [format[buffer=size[flush=time]][if=condition]] 缓存存放
### access_log path format gzip[=level] [buffer=size] [flush=time] [if=condition] 压缩存放
### access_log syslog:server=address[,parameter=value][format[if=condition]]
### access_log off
### Default: access_log logs/access.log combined;

### log_format name string ...;
- context: http
- Syntax: log_format name [escape=default|json] string ...;
- Default: log_format combined "...";

- http 变量：
	+ arg_PARAMETER：http请求参数
	+ `http_HEADER` 请求头
		* User-Agent => $http_user_agent
	+ http响应变量
		* `sent_http_HEADER` 响应头

- [内建变量](http://nginx.org/en/docs/http/ngx_http_log_module.html#access_log)
	+ $bytes_send 			客户端请求发送的字节数
	+ $connection 			连接的序列号
	+ $connection_requests 	连接请求
	+ $msec 				秒
	+ $pipe 				管道方式
	+ $request_length 		请求报文长度
	+ $request_time 		请求时间
	+ $status 				响应码
	+ $time_iso8601 		时间格式
	+ $time_local 			本地时间
	+ $remote_addr 			客户端IP
	+ $remote_user 			客户端用户名
	+ $http_referer 		引用地址
	+ $http_user_agent 		浏览器类型
	+ $gzip_ratio 			压缩比率

`# nginx -t -c /etc/nginx/nginx.conf`


### open_log_file_cache max=N[inactive=time] [min_uses=N] [valid=time];
> Default: open_log_file_cache off
	
- max：最大缓存条目
- inactive=time: 非活动时长
- min_uses：最少使用次数
- valid:验证缓存条目有效性的频率

## ngx_http_rewrite_module模块
### rewrite regex replacement [flags]
> 把用户请求的URI基于regex做检查，匹配到时将替换为replacement指定的字符串

- 在同一个location中存在的多个rewrite规则会自上而下逐个被检查(循环)；可以使用flag控制次循环功能；
	
- 如果replacement是以http://或https://开头，则替换结果以重定向方式返回给客户端

- regex：模式引用
- replacement：不能使用模式，但可是用反向应用$n

- http://server/iamges/1.jpg
- `(.*)\.jpg => $1.html`
- `(.*)\.html => $1.jpg`
- `http://server/hi.html`
- 死循环

- [flag]:
	+ last:（重启匹配）重写完成后停止对当前uri在当前location中的后续其他的重写操作，改为对新uri的新一轮处理；提前结束本轮，进入重新下一轮,continue（不返回客户端，从新开始匹配新的location）
	
	+ break: 重写完成后停止对当前uri在当前location中的后续其他的重写操作
	
	+ redirect：重写完成后以**临时重定向**方式直接返回重写后生成的新URL给客户端，由客户对新URL进行请求, 302
	
	+ permanent：重写完成后以**永久重定向**方式直接返回重写后生成的新U
	RL给客户端，由客户对新URL进行请求,301

	location / {
		root html;
		index index.html index.htm;
		rewrite (.*)\.txt$ $1.html;
	}
 
	location ~* \.html$ {
		root html;
		index index.html
		rewrite (.*)\.html $1.txt;
	}


### rewrite_log on | off
> 是否启用重写日志；启用时，日志信息被发往错误日志
- error_log日志中

### if (condition) {...}
> 条件判断机制，在条件满足时，执行配置快中的配置
- 引入了一个新的配置上下文

- Condition:
	+ compare expression: 
		* =, !=
		* ~：模式匹配，区分字母大小写
		* `~*`：模式匹配，不区分字母大小写
		* !~：模式不匹配，区分字母大小写
		* `!~*`：模式不匹配，不区分字母大小写

	+ 文件或目录存在性判断：
		* -f, !-f : file
		* -d, !-d: dir
		* -e, !-e：exists
		* -x, !-x：执行

### return code [text]
> return code URL
- return URL
- 条件判断机制
- return 403 "go away";

### set $variable value
> 用户自定义变量

## ngx_http_gzip_module模块:
> 过滤器，对指定类型的资源压缩传输以节约带宽；

- Request
	+ Accept-Encoding:gzip,deflate,sdch (压缩格式，sdch是google退出的压缩算法)
- Response
	+ Content-Encoding: gzip
	+ Content-Length: 203
	+ Transfer-Ecoding: chunked

### gzip on | off
> 启用或禁用gzip压缩响应报文

### gzip_comp_level level
> 压缩级别，1-9，默认1
- 推荐6（级别越高，压缩的越小，越消耗CPU计算资源）

### gzip_disable regex
> regex是匹配客户端浏览器的模式，表示对所有匹配到的浏览器不执行压缩响应

### gzip_min_length length (单位：KB)
> 触发启用压缩功能的响应报文的最小长度

### gzip_http_version 1.0 | 1.1(default);
> 设定启用压缩响应功能时，http协议的版本

### gzip_types mine-type ...;
> 指定仅执行压缩的资源内容类型；默认为text/html;

### gzip_proxied off | expired | no-cache | no-store | private | no_last_modified | no_etag | auth  | any ...;
> 对代理的请求基于何种属性判断其是否应该启用压缩功能
- 请求者是代理服务器，如何缓存内容

### gzip_buffers 32 4k | 16 8k 缓冲（压缩在内存中缓冲几块？每块多大？）

### gzip_vary on | off （是否传输gzip压缩标志）

- 示例：
http {
	gzip on;
	gzip_buffers 32 4k;
	gzip_http_version 1.0;
	gzip_comp_level  6;
	gzip_disable msie6;
	gzip_min_length 2;	kb
	gzip_types text/plain text/css  text/xml application/x-javascript application/xml application/json applicaiton/javascipt
}
`# cp /var/log/message /usr/local/nginx/html/message.html`
`# chmod 644 /usr/local/nginx/html/message.html`

- 注意：图片/MP3的二进制文件压缩比较小，不必压缩，而且压缩消耗CPU资源


## ngx_http_fastcgi_module模块
- LAMP(fpm):
	+ httpd+php:
		* Module
		* cgi
		* fastcgi (proxy_fastcgi_module)	
- LNMP
	+ nginx+php
		* fastcgi

	+ php: 编译时，支持fpm; (fastcgi进程管理器)
		* ./configure ... -enable-fpm ...
		* php-fpm工作方式（类似于httpd的prefork） 

`listen = 127.0.0.1:9000
listen.allowed_clients = 127.0.0.1
pm = dynamic | static
	pm.start_servers：启动fpm进程时启动的工作进程数量
	pm.min_spare_servers：最少空间进程数
	pm.max_spare_servers：最大空间进程数
	pm.max_children：最大工作进程数
user = UERNAME
group = GROUPNAME`

`# yum info php-fpm`
`# yum -y install php-fpm php-mysql php-mystring php-gd php-xml`
`# rpm -ql php-frpm | less`
`# cd /etc/php-fpm.d/`
`# vim www.conf`
`# systemctl stat php-fpm.service`

./configure --prefix=/usr/local/fastphp \
--with-mysql=mysqlnd \
--enable-mysqlnd \
--with-gd \
--enable-gd-native-ttf \
--enable-gd-jis-conv \
--enable-fpm

## nginx + php-fpm 结合
`# cd /etc/nginx/`
`# vim nginx.conf`
	location ~ \.php$ {
		root 			html;
		fastcgi_pass 	127.0.0.1:9000;
		fastcgi_index 	index.php;
		fastcgi_param	SCRIT_FILENAME /usr/local/nginx/html$fastcgi_script_name; 路径映射
		fastcgi_param	SCRIT_FILENAME $document_root$fastcgi_script_name; 路径映射
		include		fastcgi_params;
	}


## fastcgi模块指令
### fastcgi_pass address;
> address是fpm服务器监听的地址和端口
- 示例：fastcgi 127.0.0.1:90000;

### fastcgi_index name;
> fastcgi应用的主页名称

### fastcgi_param parameter value [if_not_empty];
> 传递给fpm服务器的参数和其值

- 刚缓存就，后端删除数据
	+ a.所以缓存及时清理删除
	+ b.同一个资源多次请求，命中率

- 内存中：保存缓存文件的元数据 (key)
- 磁盘上：对应元数据指向的内容数据 (value)
	+ 文件名：文件内容的md5校验码(128bit)
	+ 128/4 = 32  

### fastcgi_cache_path path [levels=levels] [key_zone=name:size];
> path：文件系统路径，用于存储缓存的文件数据；

- max_size=size 定义此路径下的多大空间用于存储缓存数据
- levels=#[:#[:#]] 缓存目录层级定义
- levels=1:2
- keys_zone=name:size 
	+ 内存中用于缓存k/v映射关系的空间名称及大小
- inactive=time
	+ 非活动时间

- 注意：只能定义在http上下文

### fastcgi_cache_key string;
> 定义要使用的缓存键
- 示例： fastcgi_cache_key $request_uri;

### fastcgi_cache zone | off;
> 是否启用cache，如果启用，数据缓存存于哪个zone

### fastcgi_cache_methods GET | HEAD | POST ...;
> 缓存哪些类型的请求的相关数据

### fastcgi_cache_min_uses number;
### fastcgi_cache_valid [code...] time
> 对不同响应码设定其可缓存时长

- 注意：调用缓存时，至少应该指定三个参数
	fastcgi_cache_valid 200 302 10m;
	fastcgi_cache_valid 301 1h;
	fastcgi_cache_valid any 1m;

- 示例：
http {
	fastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=fcgicache:10m;

	server {
		location ~ \.php$ {
			root 			html;
			fastcgi_cache			fcgicache;
			fastcgi_cache_key 		$request_uri;
			fastcgi_cache_valid 		200 302 10m;
			fastcgi_cache_valid 		301 1h;
			fastcgi_cache_valid 		any 1m;
			fastcgi_pass 	127.0.0.1:9000;
			fastcgi_index 	index.php;
			fastcgi_param	SCRIT_FILENAME /usr/local/nginx/html$fastcgi_script_name; 路径映射
			include		fastcgi_params;
		}
	}
}

`# ab -c 10 -n 100 https://192.168.1.71/info.php`
`# ls /var/cache/nginx/fastcgi/`

## 定时任务日志切割
`# vim /usr/local/nginx/nginx.conf`
	access_log logs/domain.com.access.log main;

`# vim /usr/local/nginx/sh/log.sh`
	LOGPATH=/usr/local/nginx/logs/domain.com.access.log
	BASEPATH=/data
	
	back=$BASEPATH/$(date -d yesterday +%Y%m%d%H%M).domain.com.access.log
	
	mv $LOGPATH $bak
	touch $LOGPATH

	kill -USR1 `cat /usr/local/nginx/logs/nginx.pid`

`# crontab -e`
	`*/1 * * * * sh /usr/local/nginx/sh/log.sh`

## 伪静态实战
- 批匹配模式包含{}时，必须使用双引号("模式")
- 模式匹配最长的优先重写
`location /ecshop {
	rewrite "goods-(\d{1,7})-.*\.html$" /ecshop/goods.php?id=$1; 
}`




# 静态资源Web服务

## 静态资源类型
- image/jpeg
- text/html

## 静态资源服务场景-CDN


## 文件读取
- Syntax: sendfile on `|` off;
- Default: sendfil off;
- Context: http, server, location, if in location

- **--with-file-aio** 异步文件读取

## tcp_nopush
> sendfile 开启的情况下，提高网络包的传输速率
- nopush 意思是多个包一次性发送包


- Syntax: tcp_nopush on `|` off;
- Default: tcp_nopush off;
- Context: http,server,location

## tcp_nodelay
> keepalive(长)连接下，提高网络包的传输实时性

- Syntax: tcp_nodelay on `|` off;
- Default: tcp_nodelay on;
- Context: http,server,location

## gzip 压缩

- Syntax: gzip on `|` off;
- Default: gzip off;
- Context: http,server,location, if in location

- 浏览器(解压) <-----> (解压)Nginx

### 压缩比率
- Syntax: gzip_comp_level level[1-9];
- Default: gzip_comp_level 1; 推荐6，占用 CPU 
- Context: http,server,location

### http 版本
- Syntax: gzip_http_version 1.0 or 1.1;
- Default: gzip_comp_level 1.1; 
- Context: http,server,location


## 扩展Nginx 压缩模块
- http_gzip_static_module - 预读 gzip 功能
- http_gunzip_module - 应用支持gunzip的压缩方式

- `# vim static_server.conf`
`server {
	listen 80;
	server_name IP or domain;
	location ~ .*\.(jpg|gif|png)$ {
		gzip on;
		gzip_http_version 1.1;
		gzip_comp_level 2;
		gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php images/jpeg image/gif image/png;
		root /data/www/images;
	}
	location ~ .*\.(txt|xml)$ {
		gzip on;
		gzip_http_version 1.1;
		gzip_comp_level 2;
		gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php images/jpeg image/gif image/png;	
		root /data/www/doc;	
	}
	location ~ ^/download {
		# 压缩文件test.img.gz
		# on 打开之后下载地址可以使test.img 自动识别
		gzip_static on;
		tcp_nopush on;
		root /data/www/code;
	}
}`


## 浏览器缓存
- http协议缓存机制（Expires; Cache-control等）
- 浏览器记录访问的页面进行缓存，并记录文件最后一次修改时间
- 如果在向服务器请求同一个文件，发送文件附带最后修改时间，服务器收到该文件后比较最后一次修改时间对比，相等，则304返回状态，客户端从本地读取该文件。



# 代理服务

# 负载均衡调度器 SLB

# 动态缓存

