# 电商数据库设计及架构优化实战

- 注册会员(用户模块) - 展示商品 - 加入购物车(购物车模块)-生成订单(订单模块)
- 商户入住(商户模块) - 发送货物(物流模块)

## 环境
- MySQL 5.7
- SQLyog: MySQL图形客户端程序


## 购物流程
用户登录->选购商品->加购物车->检车库存->提交订单
- 货到付款 	
	 + Y
	 + N => 订单付款
- 发货

## 用户模块
> 用户注册/登录验证/查找密码

## 商品模块
> 前后台商品管理和浏览

## 订单模块
> 订单/购物车的生成和管理 

## 仓配管理
> 仓库库存和物理的管理


## 数据结构设计
- 逻辑设计 -> 逻辑设计

- 实际工作：逻辑设计+物理设计


# 数据库设计规范
- 数据库命名规范
- 数据库基本设计规范
- 数据库索引设计规范
- 数据库字段设计规范
- 数据库 SQL 开发规范
- 数据库操作行为规范(运维)


## 数据库命名规范
- 所有数据库对象名称是**小写字母并用下划线分割**（Linux OS 区分大小写）
- 所有数据库对象名称禁止使用[MySQL保留关键字](https://dev.mysql.com/doc/refman/5.7/en/keywords.html)
- 所有数据库对象名称必须要**见名识义**，并且最好不超过32个字符
- 临时表：以tmp为前缀并以日期为后缀
- 备份表：以bak为前缀并以日期为后缀
- 所有存储**相同数据的列名和列类型必须一致**（不同列名影响性能）
-


- lym_userdb(零壹码网的用户数据库)
- user_account(用户账号表)

## 数据库基本设计规范
**MySQL 5.5 使用之前 MyISAM(默认存储引擎)**

- 所有表必须使用 **InnoDB** 存储引擎
	+ 5.6 + 默认引擎
	+ 支持事务，行级锁，更好恢复性，高并发下性能更好
- 数据库表和字符集统一使用UTF8
	+ 避免字符集转换乱码
	+ UTF—8字符集汉字占用3个字节
- 所有表和字段必须添加注释
	+ 便于以后数据字典的维护
- 尽量控制单表数据量大小，建议控制在500万以内
	+ 500万并不是 MySQL 数据库限制
	+ 存储多少万数据？取决于存储设置和文件系统
	+ 历史数据归档、分库分表(业务)等手段来控制数据量大小
- 谨慎使用 MySQL分区表
	+ 分区表在物理上表现为多个文件，在逻辑上表现为一个表
	+ 分区键，跨分区查询效率可能更低
	+ 建议才用物理分表的方式管理大数据

- 冷热数据分离，减少表的字段
	+ MySQL 限制做多存储4096列
	+ MySQL 每行不能超过65535字节
	+ 减少磁盘IO，保证热数据缓存命中率
	+ 利用更有效的利用缓存，避免读取无用的冷数据
	+ 经常一起使用的列放在一起

- 禁止在表中预留字段
	+ 见名识义
	+ 预留字段无法确认存储的数据类型，所有无法选择合适的类型
	+ 对预留字段类型的修改，会对表进行锁定
- 禁止存储图片/文件等二进制数据
- 禁止在线上做数据库压力测试（可以在开发环境测试）
- 禁止从开发环境，测试环境直连生产环境

## 索引设计规范
> 对查询性能非常重要

- 不要滥用索引
- 限制每张表的索引数量，建议单表索引不超过5个
	+ 与列数量成正比
	+ 索引提高效率同时可以降低效率
- InnoDB 表必须有一个主键
	+ 不适用更新频繁de列作为主键，不使用多列主键
	+ 不使用uuid,md5,hash,字符串列作为主键
- 使用自增ID值

- 常见索引列建议：
	+ select,update,delete语句的where从句中的列
	+ 包含在order by, group by, distinct中的字段
	+ 多表 join 的关联列

- 如何选择索引列的顺序
	+ 从左到右的顺序来使用
		* 区分度最高的列放在联合索引的最左侧
		* 尽量字段长度小的列放在联合索引的最左侧
		* 使用最频繁的列放到联合做引的左侧
	
- 避免建立冗余索引和重复索引
	+ index(a,b,c), index(a,b), index(a)

- 频繁查询有限考虑使用覆盖索引
	+ 覆盖索引：包含了素有查询字段的索引(where,order by, group by)
	+ 好处：
		* 避免innodb表进行索引的二次查找
		* 随机IO变为顺序IO加快查询效率

- 尽量避免使用外键
	+ 不建议使用外键约束
	+ 在业务端实现
	+ 外键影响父表和子表的写操作从而降低性能


## 数据库字段设计规范
- 优先选择符合存储需要的**最小的数据类型**
	+ inet_aton('255.255.255.255') = 4294967295
	+ inet_ntoa(4294967295) = '255.255.255.255'

	4 byte vs 15 byte	
- 选择非负整型数据选择无符号整型数据进行存储unsigned 类型
- varchar(n) n代表**字符数**，而不是字节数
	+ utf8汉字varchar(255) = 占用765 byte

- 过大的长度会消耗更多的内存
- 避免使用text(max 64k), blob数据类型
	+ tinytext
	+ text
	+ midumtext
	+ longtext
	+ 内存不支持text,blog 排序
	+ 需要二次查询
	+ 建议单独放到的扩展表中
	+ text/blog只能有前缀索引，没有默认值
- 避免使用enum数据类型
	+ 65535 中
	+ 字符串类型
	+ 修改enum值需要使用alter语句
	+ enum类型的order by 操作率低，需要额外的操作
	+ 禁止使用数值作为enum的枚举类型

- 尽可能吧所有列定义为NOT NULL
	+ 索引null列需要额外的空间来保存，所以要占用更多的空间
	+ 进行比较和计算时要对null值做特别的处理
- 使用timestamp(4 byte)或datetime(8 byte)类型存储时间
	+ timestamp 1970-01-01 00:00:01 ~ 2038-03-03 03:14:07
	+ timestamp占用 4 byte 和 int 相同，但比 int 可读性高
- 超出时间范围使用datetime
- 财务数据必须使用decimal
	+ 精准浮点数，在计算时不会丢失精度
	+ 占用空间由定义的宽度决定
		* 每4字节存储9位数据
	+ 存储比bigint更多的数据


## 数据库 SQL 开发规范
- **预编译语句**进行数据库操作
> prepare stmt1
> from 'select SQRT(POW(?,2) + POW(?,2)) AS hypotenuse';
> set @a=3;
> set @b=4;
> execute stmt1 USING @a, @b;
> deallocate prepare stmt1;

	+ 只传参数，比传递SQL语句更高效
	+ 相同语句可以一次解析，多次使用，提高处理效率

- 避免数据类型的隐式转换
	+ 隐式转换导致索引失效
	+ where id='1'

- 利用表上的已经存在的索引
	+ 避免使用双%好的查询条件：'%123%'
	+ 一个SQL只能利用到复合索引中的一列进行范围查询
	+ 使用 left join 和 not exists 来优化 not in 操作

- 不同的数据库使用不同的账号，禁止跨库查询
	+ 为数据库迁移和分库分表留出余地
	+ 降低业务耦合度
	+ 避免权限过大而产生的安全风险
- 禁止使用select*
	+ 消耗更多的CPU和IO以及网络带宽资源
	+ 无法使用覆盖索引
	+ 可以减少表结构变更带来的影响

- 禁止是不含字段列表的insert 语句
	+ insert int t value('a','b')
	+ insert into t(c1,c2) values('a','b')
	+ 可以减少结构变更带来的影响

- 禁止子查询，子查询优化位join操作
	+ 在查询结果集无法使用索引
	+ 产生临时表操作，如果子查询数据量大则严重影响效率
	+ 消耗过多的CPU和IO资源

- 避免使用join关联太多的表
	+ 每join一个表会多占用一部分内存(join_buffer_size)
	+ 会产生临时表操作，应影响查询效率
	+ MySQL 最多允许关联61个表，建议不超过5个

- 减少同数据库的交互次数
	+ 分页显示：不要提取 第一页结果
	+ 数据库更合适处理批量操作
	+ 合并多个相同的操作到一起，可以提高处理效果
	+ alter table t1 add column c1int, add. ...

- 使用 in 代替 or
	+ in 的值不要超过 500个
	+ in 操作可以有效的利用索引

- 禁止使用 order by rand() 进行随机排序
	+ 会把所有符合条件的数据装载到内存中进行排序
	+ 消耗大量的CPU和IO及内存资源
	+ 在程序中获取一个随机值，然后从数据库中获取数据

- where 从句中禁止对列进行函数转换和计算
	+ 导致无法使用索引
	+ where date(createtime) = '20160901'
	+ where createtime >= '20160901' and createtime < '20161010'

- 不会有重复值的使用union all ，而不是union
	+ union 把所有数据放到临时表中后再进行去重操作
	+ union all 不会再对结果集进行去重操作

- 拆分复杂的大 SQL 为多个小 SQL
	+ MySQL 一个 SQL 只能使用一个CPU进行计算
	+ 通过并行执行来提高处理效率

## 数据库操作行为规范(运维)
- 超 100万行的批量写操作，要分批多次进行操作
	+ 大批量操作可能造成严重的主从延迟
	+ binlog 日志为row格式时会产生大量的日志
	+ 避免产生大事务操作


- 对大表数据结构修改一定要谨慎，会造成严重的锁表操作。尤其是生产环境，是不能忍受的。 10分钟表锁，会出现在线延迟

- 对大表使用pt-online-schema-change修改表结构
	+ percona开发的工具
	+ 1. 新建表与原来表一样，并修改表结构
	+ 2. 复制数据到新表中，并在源表中增加触发器，把新增的数据也增加在新表中。在行的数据完成之后，在源表上加上事件锁

	+ 避免大表修改产生的主从延迟
	+ 避免在对表字段进行修改时进行锁表

- 禁止为程序程序使用的账号赋予super权限
	+ 当达到最大连接数限制时，还允许1个有super权限的用户连接
	+ super权限只能留给DBA 处理问题的账号使用

- 程序连接数据库账号，遵循权限最小原则
	+ 不准夸库
	+ 程序使用账号原则上不准有drop权限



# 数据库设计

## 用户模型设计

- 用户实体(下面是实体属性)
	+ 用户姓名
	+ 登录名
	+ 密码
	+ 手机号
	+ 证件类型
	+ 证件类型号码
	+ 邮箱
	+ 性别
	+ 邮政编码
	+ 省
	+ 市
	+ 区
	+ 地址
	+ 积分
	+ 注册时间
	+ 生日
	+ 用户状态（冻结[不能登陆和购物]|正常）
	+ 用户级别（优惠政策）
	+ 用户余额

- 用户表(customer)

### 所有数据字段保存在一个表上带来问题
- 数据插入异常
	+ PK：用户登录名
	+ 用户级别存储（会员级别/级别积分上限/级别积分下限，不需要插入主键）
	
- 数据更新异常
	+ 修改某一行的值时，不得不修改多行数据
		* 用户等级(青铜级)修改成其他名称(皇冠级)
		* 修改所有会员的用户级别数据时，表锁

- 数据删除异常	
	+ 删除某一数据时不得不同时删除另一数据
		* 删除用户等级名为皇冠级等级
		* delete from customer where level='皇冠';
	
- 数据存在冗余
	+ 每个用户的用户等级上限和下限
	+ 数据表过宽，会影响修改表结构的效率

### Solution

#### 满足数据库设计第三范式(3NF)
> 一个表中的**列**和**其他列**之间既不包含部分**函数依赖关系**也不包含传递函数依赖关系，那么这个表的设计就符合第三范式


- 级别积分上限/下限 依赖用户级别
- 用户级别依赖于登录名

- 拆分原用户表以符合第三范式
	+ 用户登陆表（登录名/密码/用户状态）
	+ 用户地址表（省名/市/区/地址/邮编）
	+ 用户信息表（用户姓名/证件类型/证件号码/手机号/邮箱/性别/积分/注册时间/生日/会员级别/用户余额）
	+ 用户级别信息（customer_level_info）
		* 会员级别
		* 级别积分下限
		* 级别积分上限

#### 数据表设计
- 用户登陆表：customer_login

`create table customer_login(
	customer_id int unsigned auto_increment not null '用户ID',
	login_name varchar(28) not null comment '用户登录名',
	password char(32) not null comment 'md5加密的密码',
	user_status tinyint not null default 1 comment '用户状态(1:正常,0:冻结)',
	modified_time timestamp not null default CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
primary key pk_customerid(customer_id)
) engine=innodb comment='用户登陆表';`

- 用户信息表：customer_info

`create table customer_info{
	customer_info_id int unsigned auto_increment not null comment '自增主键ID',
	customer_id int unsigned not null comment 'customer_login表的自增ID',
	customer_name varchar(20) not null comment '用户真实姓名',
	identity_card_type tinyint not null default 1 comment '证件类型(1:身份证，2:军官证，3:护照)'，
	identity_card_no varchar(20) comment '证件号码',
	mobile_phone int unsigned comment '手机号',
	customer_email varchar(50) comment '邮箱',
	gender char(1) comment '性别',
	user_point int not null default 0 comment '用户积分',
	register_time timestamp not null comment '注册时间',
	birthday datetime comment '会员生日',
	customer_level tinyint not null default 1 '会员级别（1：普通会员，2：青铜会员，3：白银会员，4：黄金会员，5：钻石会员）',
	user_money decimal(8,2) not null default 0.00 comment '用户余额',
	modified_time timestamp not null default current_timestamp on update current_timestamp comment '最后修改时间',
	primary key pk_customerinfoid(customer_info_id)
} engine=innodb comment '用户信息表'`


- 用户级别表(customer_level_info)

`create table customer_level_info(
	customer_level tinyint not null auto_increment comemnt '会员级别ID',
	level_name varchar(10) not null comment '会员级别名称',
	min_point int unsigned not null default 0 comment '级别最低积分',
	max_point int unsigned not null default 0 comment '级别最高积分',
	modified_time timestamp not null default current_timestamp 0 on update current_timestamp comment '最后修改时间',
	primary key pk_levelid(customer_level)
) engine=innodb comment '用户级别信息表'`


- 用户地址表(customer_addr)

`create table customer_addr(
	customer_addr_id int unsigned auto_increment not null comment '自增主键ID',
	customer_id int unsigned not null comment 'customer_login表的自增ID',
	zip smallint not null comment '邮编',
	province smallint not null comment '地区表中省份的ID',
	city smallint not null comment '地区表中城市的ID',
	district smallint not null comment '地区表中区的ID',
	address varchar(200) not null comment '具体的地址门牌号',
	is_default tinyint not null comment '是否默认',
	modified_time timestamp not null default current_timestamp on update current_timestamp comment '最后修改时间',
	primary key pk_customeraddid(customer_addr_id)
) engine=innodb comment '用户地址表'`


- 用户积分日志表(customer_point_log)
`create table customer_point_log(
	point_id int unsigned not null auto_increment comment '积分日志ID',
	customer_id int unsigned not null comment '用户ID',
	source tinyint unsigned not null comment '积分来源(0：订单，1：登录，2：活动)',
	refer_number int unsigned not null default 0 comment '积分来源相关编号',
	change_point smallint not null default 0 comment '变更积分数',
	create_time timestamp not null comment '积分日志生成时间',
	primary key pk_pointid(point_id)
) engine=innodb comment '用户积分日志表'`

- 用户余额变动表(customer_balance_log)
`create table customer_balance_log(
	balance_id int unsigned not null auto_inrement comment '余额日志ID',
	customer_id int unsigned not null comment '用户ID',
	source tinyint unsigned not null default 1 comment '记录来源（1：订单，2：退货单）',
	source_sn int unsigned not null comment '相关单据ID',
	create_time timestamp not null default current_timestamp comment '记录生成时间',
	amount decimal(8,2) not null default 0.00 comment '变动金额',
	primary key pk_balanceid (balance_id)
) engine=innodb comment '用户余额变动表'`

- 用户登录日志表（customer_login_log）
`create table customer_login_log(
	login_id int unsigned not null auto_increment comment '登录日志ID',
	customer_id int unsigned not null comment '登录用户ID',
	login_time timestamp not null comment '用户登录时间',
	login_ip int unsigned not null comment '登录IP',
	login_type tinyint not null comment '登录类型（0：未成功，1：成功）',
	primary key pk_loginid(login_id)
) engine=innodb comment '用户登录日志表'`


- 业务场景
	+ 用户每次登录都会记录 customer_login_log 日志
	+ 用户登录日志保存一年，一年后可以删除

- 登录日志表的分区类型及分区键
	+ 使用 range 分区
	+ login_time 作为分区键

`create table customer_login_log(
	login_id int unsigned not null auto_increment comment '登录日志ID',
	customer_id int unsigned not null comment '登录用户ID',
	login_time timestamp not null comment '用户登录时间',
	login_ip int unsigned not null comment '登录IP',
	login_type tinyint not null comment '登录类型（0：未成功，1：成功）',
	primary key pk_loginid(login_id)
) engine=innodb comment '用户登录日志表'
partitoin by range(year(lgin_time)) (
	partition p0 values less than(2015),
	partition p1 values less than(2016),
	partition p2 values less than(2017)
);`

insert 插入数据
`select * from customer_login_log;`
`select table_name, partition_name, partition_description, table_rows from infomation_shema.PARTITIONS where table_name='customer_login_log'`

`alter table customer_login_log add partition (partition p4 values less than(2018))`


- 删除分区表
`alter table customer_login_log drop partition p0;`

- 建立归档表
`create table arch_customer_login_log(
	login_id int unsigned not null auto_increment comment '登录日志ID',
	customer_id int unsigned not null comment '登录用户ID',
	login_time timestamp not null comment '用户登录时间',
	login_ip int unsigned not null comment '登录IP',
	login_type tinyint not null comment '登录类型（0：未成功，1：成功）',
	primary key pk_loginid(login_id)
) engine=innodb comment '用户登录日志归档表'`

- 分区迁移
`alter table customer_login_log exchange partition p2 with table arch_customer_login_log;`

- 分区迁移之后删除分区p2
`alter table customer_login_log drop partition p2;`

- 查看归档
`select * from customer_login_log;`

- 修改归档引擎(只能查找操作，不能写操作)
`alter table arch_customer_login_log engine=ARCHIVE`

## 分区表的注意事项
- 结合业务场景选择分区键，避免跨分区查询
- 对分区表进行查询最好在where从句中包含分区键
- 具有主键或唯一索引的表，主键或唯一索引必须是分区键的一部分



## 商品实体
- 商品名称
- 国条码
- 分类
- 供应商
- 品牌名称
- 销售价格
- 成本
- 上下架状态
- 颜色
- 重量
- 长度
- 宽度
- 高度

- 有效期
- 生产时间
- 描述
- 图片信息


- 品牌信息表(brand_info)
`create table brand_info(
	brand_id small int unsigned auto_increment not null comment ''品牌ID,
	brand_name varchar(50) not null comment '品牌名称',
	telephone varchar(50) not null comment '联系电话',
	brand_web varchar(100)  comment '品牌网站',
	brand_logo varchar(100) comment '品牌logo RUL',
	brand_desc varchar(150) comment '品牌描述', 
	brand_status tinyint not null default 0 comment '品牌状态（0：禁用，1：启用）',
	brand_order tinyint not null default comment '排序',
	modified_time timestamp not null default current_timestmap on update current_timestamp comment '最后修改时间',
	primary key pk_brandid(brand_id)
) engine=innodb comment="品牌信息表"`

- 分类信息表(product_category)
`create table product_category(
	category_id smallint unsigned auto_increment not null comment '分类ID',
	category_name varchar(10) not null comment '分类名称',
	category_code varchar(10) not null comment '分类编号',
	parent_id smallint unsigned not null default 0 comment '父分类ID',
	category_level tinyint not null default 1 comment '分类层级',
	category_status tinyint not null default 1 comment '分类状态',
	modified_time timestamp not null default current_timestmap on update current_timestamp comment '最后修改时间',
	primary key pk_categoryid(category_id)
) engine=innodb comment='商品分类表'`


- 供应商信息表(supplier_info)
`create table supplier_info(
	supplier_id int unsigned auto_increment not null comment '供应商ID',
	supplier_code char(8) not null comment '供应商编号',
	supplier_name char(50) not null comment '供应商名称',
	supplier_type tinyint not null comment '供应商类型（1：直营，2：平台）',
	link_man varchar(10) not null comment '供应商联系人',
	phone_number varchar(50) not null comment '联系电话',
	bank_name varchar(50) not null comment '供应商开户银行名称',
	bank_account varchar(50) not null comment '银行账号',
	address varchar(200) not null comment '供应商地址',
	supplier_status tinyint not null default 0 comment '状态（0：禁用，1：启用）',
	modified_time timestamp not null default current_timestmap on update current_timestamp comment '最后修改时间',
	primary key pk_supplierid(supplier_id)
) engine=innodb comment '供应商信息表';`

- 商品信息表(product_info)
`create table product_info(
	product_id int unsigned auto_increment not null comment '商品ID',
	product_code char(16) not null comment '商品编码',
	product_name varchar(20) not null comment '商品名称',
	bar_code varhcar(50) not null comment '国条码',
	brand_id int unsigned not null comment '品牌表的ID',
	one_category_id small int unsigned not null comment '一级分类ID',
	two_category_id  small int unsigned not null comment '二级分类ID',
	three_category_id  small int unsigned not null comment '三级分类ID',
	supplier_id int unsgined not null comment '商品的供应商ID',
	price decimal(8,2) not null comment '商品销售价格',
	average_cost decimal(8,2) not null comment '商品加权平均成本',
	publish_status tinyint not null default 0 comment '上下架状态（0:下架，1：上架）',
	audit_status tinyint not null default 0 comment '审核状态（0：未审核，1：已审核）',
	weight float comment '商品重量',
	length float comment '商品长度',
	height float comment '商品高度',
	width float comment '商品宽度',
	color_type enum('红','黄','蓝','黑'),
	production_date datetime not null comment '生产日期',
	shelf_life int not null comment '商品有效期',
	descript text not null comment '商品描述',
	indate timestamp not null default CURRENT_TIMESTAMP comment '商品录入时间',
	modified_time timestamp not null default current_timestmap on update current_timestamp comment '最后修改时间',
	primary key pk_productid(product_id)
) engine=innodb comment '商品信息表';`


- 商品图片表(product_pic_info)




# MySQL分区表
- 确认MySQL 服务器是否支持分区表
mysql> show plugins;
partition active 

## 分区表的特点
- 在逻辑为一个表，在物理上存储多个文件中
`create table customer_login_log(
	login_id int unsigned not null auto_increment comment '登录日志ID',
	customer_id int unsigned not null comment '登录用户ID',
	login_time timestamp not null comment '用户登录时间',
	login_ip int unsigned not null comment '登录IP',
	login_type tinyint not null comment '登录类型（0：未成功，1：成功）',
	primary key pk_loginid(login_id)
) engine=innodb comment '用户登录日志表'
partition by hash(customer_id)
partitions 4;`

- 非分区表的物理文件
	+ customer_login_log.frm
	+ customer_login_log.idb

- 分区表的物理文件
	+ customer_login_log.frm
	+ customer_login_log#p0.ibd
	+ customer_login_log#p1.ibd
	+ customer_login_log#p2.ibd
	+ customer_login_log#p3.ibd


## hash分区(hash)的特点
- 根据MOD（分区键，分区数）的值把数据行存储到表的不同分区内
- 数据可以平均的分布在各个分区中
- 分区的键值必须是一个int 类型的值，或是通过函数可转换为 int 类型



- 如何建立hash分区表
`create table customer_login_log(
customer_id int(10) unsigned not null,
login_time timestamp not null,
login_ip int(10) unsigned not null,
login_type tinyint(4) not null
) engine=innodb
partition by hash(customer_id)
partitions 4` 分区数量

`partition by hash(unix_timestamp(login_time))
partitions 4`

- 插入数据时跟正常插入数据方式一样的

## hash分区表可用的函数
- abs()
- dayofmonth()
- datediff()
- hour()
- mod()
- second()
- to_seconds()
- year()
- ceiling()
- dayofweek()
- extract()
- microsecond()
- month()
- time_to_sec()
- unix_timestamp()
- day()
- dayofyear()
- floor()
- minute()
- quarter()
- to_days()
- weekday()
- yearweek()





## 按范围分区(range)

- 根据分区键值的范围把数据行存储到表的不同分区中
- 多个分区的范围要连续，但不能重叠
- 默认情况下使用 values less than 属性，即每个分区不包括指定的那个值


- 如何范围分区

`create table customer_login_log(
customer_id int(10) unsigned not null,
login_time timestamp not null,
login_ip int(10) unsigned not null,
login_type tinyint(4) not null
) engine=innodb
partition by range (customer_id) (
	partition p0 values less than (10000),
	partition p1 values less than (20000),
	partition p2 values less than (30000),
	partition p3 values less than MAXVALUE
)`
- p0: 小于10000的customer_id，存储与p0， 0-9999
- p1: 小于20000的customer_id，存储与p0， 10000-19999
- p0: 大于30000的customer_id，存储与p3， > 30000 

- 使用场景
	+ 分区间为日期或是时间类型
	+ 所有查询中都包括分区键
	+ 定期按分区范围清理历史数据



## List 分区
- 按分区键的列表进行分区
- 同范围分区一样，各分区的列表值不能重复
- 每一行数据必须能找到对应的分区列表，否则数据插入失败

- 如何建立 li分区
`create table customer_login_log(
customer_id int(10) unsigned not null,
login_time timestamp not null,
login_ip int(10) unsigned not null,
login_type tinyint(4) not null
) engine=innodb
partition by list (login_type) (
	partition p0 values in (1,3,5,7,9),
	partition p1 values in (2,4,6,8)
)`
- insert into 插入login_type 10 出现错误代码：1526


## MySQL性能问题

### 超高的QPS/TPS
> QPS：每秒中处理的查询量
- 风险：效率底下的SQL

- CPU 10ms 处理 1个SQL
- 1s 处理 100个sql
- QPS <= 100

- 100ms 处理 1个sql
- QPS <= 10


### 大量的并发和超高的CPU使用
- 风险
- 大量的并发：数据库连接数被占满（MySQL：max_connection 默认100）
- 超高的CPU使用率：CPU 资源耗尽而出现宕机

- 并发量：同一时间数据库处理的业务适量
- 连接数：同一时间连接数据库


### 磁盘IO
- 风险：
	+ 磁盘IO性能突然下降（解决：使用更快的磁盘设备）
		* 更好的raid卡
		* SSD
		* fashion IO
	+ 其他大量消耗磁盘性能的计划任务（调整计划任务，做好磁盘维护）
		* 备份

### 网卡流量
- 风险: 网卡IO被占满（1000Mb/8 = 100MB）
- solution:
	+ 减少从服务器的数量
	+ 进行分级缓存
	+ 避免使用 `select *` 进行查询
	+ 分离业务网络和服务器网络


### 大表带来的问题


### 大事务带来的问题








- Web服务器横向发展
- 数据库服务器
	+ Master(1)/Slave(15)
		* Master 故障，没有高可靠性
- 数据库影响原因(CPU:64 core, Mem: 512GB)
	+ QPS(Query Per Second) & TPS(transaction per second)代表每秒执行的事务数量
	+ 并发请求/CPU idle
	+ 磁盘IO






- SQL 查询速度
- 服务器硬件（CPU/内存/磁盘IO/网卡流量）

## 数据库解决方案

## 如何对评论进行分页展示
`explain select customer_id, title, content from product_comment where audit_status=1 and product_id = 199727 limit 0,5;`
- SQL如何使用索引
- 连接查询的执行顺序
- 查询扫描的数据行数

### 执行计划 explain
- ID: 表示执行select语句的顺序
	+ ID 值相同时，执行顺序由上至下
	+ ID 值越大优先级越高，越先被执行

- select_type:
	+ simple : 不包含子查询或是union
	+ primary: 按主键查询
	+ subquery: select列表中的子查询
	+ dependent subquery: 依赖外部结果的子查询
	+ union：Union操作的第二个或是之后的值为union
	+ dependento union： 当union作为子查询时，第二或是第二个后的查询的select_type值
	+ union result: union产生的结果集
	+ derived: 出现在from子句中的子查询
primary > simple > subquery > dependent subquery

- table列
	+ 表的名称
	+ unionM,N: unicon产生结果集
	+ derivedN/subqueryN: 有id为N的查询产生结果

- partitions列
	+ 分区表的ID
	+ NULL：非分区表

- type:
	+ system：表中只有一行
	+ const: 表中有且只有**一个匹配的行**时使用，如对**主键或唯一索引的查询**，这是效率最高的连接方式
	+ eq_ref：**唯一索或主键引查找**，对于每个索引键，表中只有**一条记录与之匹配**
	+ ref：**非唯一索引查**找，返回匹配某个单独值得**所有行**
	+ ref_of_null：雷士ref，附加了对**null**值列的查询
	+ index_mer：索引**合并优化**方法
	+ ge
	+ range： **索引范围扫描**，between,<,>等查询条件
	+ index: Full index Scan **全索引扫描**，同ALL的区别是，遍历的是**索引树**
	+ all：**全表扫描**，效率最差

- possible_keys 可能索引优化查询
	 
- key 优化查询实际使用的索引
	+ NULL： 没有可用的索引
	+ 使用覆盖索引：则该索引金出现在key列中
- key_len 索引**字节数**
	+ 索引字段的最大可能长度
	+ 有字段定义计算而来，并非数据的实际长度

- ref: key索引查询时的来源
- rows 估算的读取的行数，统计抽样结果，并不准确
- filtered 返回结果的行数占需读取行数的百分比，值越大越好，依赖统计信息

- Extra
	+ Distinct : 优化distince操作，在找到第一匹配的元祖后即停止找同样值的动作
	+ Not exists: 使用not exists来优化查询。如 not in
	+ Using filesort ： 额外操作进行排序，如order by, group by 查询中
	+ Using index: 使用覆盖索引进行查询
	+ Using temporary : 临时表来处理查询，常见于排序、子查询、和分组查询
	+ Using where： where条件来过滤数据
	+ select tables optimized away: 索引来获得数据，不用访问表

- 无法展示存储过程，触发器/UDF对查询的影响
- 早期版本仅支持select

select count(distinct audit_status)/count(*) as audit_rate, 
count(distince product_id)/count(*) as product_rate from product_comment;
 
- 越接近1使用该字段放左侧，创建索引

create index idx_productid_auditStat on product_comment(product_id,audit_status)

- 进一步优化
select t.customer_id, t.title, t.content
from (
select comment_id from product_comment
where produt_id=199727 and audit_status=1 limit 0,15
) a join product_comment t
on a.comment_id = t.comment_id;



## 删除重复数据
- 同一订单同一商品的重复评论





