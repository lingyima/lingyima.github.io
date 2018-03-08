# MongoDB-[零壹码博客](https://lingyima.com)
- NoSQL: Not Only SQL 非关系型数据库
- 内存级读写（毫秒级）

## 为什么出现NoSQL
> 随着访问量的上升，网站的数据库性能出现问题

## 优点
- 高可扩展性
- 分布式计算
- 低成本
- 架构的灵活性，半结构化数据
- 没有复杂的关系

## 缺点
- 没有标准化
- 有限查询功能

## 分类
- 列存储：Hbase, Cassndra, Hypertable
- 文档存储：MongoDB, CouchDB
- key-value存储：Tokyo Cabinet /Tyrant, Berkeley DB, MemcacheDB
- 图存储：Neo4J, FlockDB
- 对象存储：db4o, Versant
- xml数据库：Berkeley DB XML, BaseX

## 用户浏览过程
- user -> application ->redis/mongodb -> mysql

## What [MongoDB](https://mongodb.com)
> 分布式文档存储的NoSQL数据库

- C++语言编写，运行稳定、性能高
- Web 应用提供可扩展的高性能数据存储解决方案

## MongoDB Features
- 模式自由：不同结构的文档存储在同一个数据库里
- 面向集合的存储：适合存储 JSON 风格文件的形式
- 完整的索引支持：对任何属性可索引
- 复制和高可用性：支持主从撇脂
- 自动分片
- 丰富的查询
- 快速的更新
- 高效的传统存储方式：支持二进制数据及大型对象（图片等）

## 名词对比
- 解释/SQL/MongoDB
- 数据库/database/database 
- 表,集合/table/collection
- 记录,文档/row/document
- 字段,域/column/field
- 索引/index/index
- 表连接/join/无
- 主键/primary key/primary key

- 三元素：数据库/集合/文档
	+ 集合就是关系数据库中的表，存储多个文档
	+ 文档对应着关系数据库中的行
	+ 文档，就是一个对象，有键值对构成，是json的扩展BSON形式

## 服务端 mongod

- 开启验证模式
`# mongod -f /etc/mongod.conf --fork --auth`

## 客户端 mongo


## 创建用户
use admin
db.createUser({
	user:'admin',
	pwd:'adminpwd',
	roles:[{role:'userAdminAnyDatabase', db:'admin'}]
})
db.auth('admin','adminpwd')

use test
db.createUser({
	user:'test',
	pwd:'testpwd',
	roles:[{role:'readWrite',db:'test'}]
})
db.auth('test','testpwd')


## MongoDB GUI
- [Robo](https://robomongo.org)

## 数据类型
- Object ID：文档ID (12byte 16机制)
	+ 4 byte timestamp
	+ 3 byte 机器id
	+ 2 byte mongodb的服务进程id
	+ 3 byte 增量值
- String
- Boolean
- Integer
- Double
- Arrays
- Object
- Null
- Timestamp
- Date


## 数据库操作

- 查看当前数据库：db
- 查看所有数据库：show dbs
- 切换数据库：use test
- 删除当前数据库:db.dropDatabase()
- 创建数据库：use test
	+ show dbs 不现实当前数据库

## 集合操作

- create: db.createCollection(name, options)
	+ db.createCollection("stu", {capped:true, size:10})
		* capped 覆盖


- view: show collections
- delete: db.集合名.drop()

## 文档操作

- 插入：
	+ db.集合名称.insert({...})
- 查询:
	+ db.集合.find()
- 更新：
	+ db.集合.update({条件}, {修改数据})
	+ db.集合.update({name:'hr',{$set:{name:'hys'}}}) $set 不修改文档结构
	+ db.集合.update({name:'hr',{$set:{name:'hys'}}}, {multi:true}) 修改多行，默认修改一行
- 删除：
	+ db.集合.remove({条件}, {justOne:false}) 默认删除所有
	+ db.集合.remove({}) 全部删除


## 查询
- db.集合.find()
- db.集合.find(条件)
- db.集合.find().pretty()
- db.集合.findOne()


## 比较运算符
- 等于
	+ db.stu.find({name:'gj'})
- $lt
- $lte
- $gt
- $gte
	+ db.stu.find({age:{$gte:18}})
- $ne


- $or (大于)
	+ db.stu.find({$or:[{age:{$gt:18}},{gender:1}]})

## 范围运算符
- $in, $nin
- db.stu.find({age:{$in:[18,28]}})

## 正则表达式
- // or $regex
`db.stu.find({name:/^ad/})`
`db.tu.find({name:{$regex:'^ad'}})`

## 自定义查询
`db.stu.find({$where: function(){return this.age>20}})`


## limit
`db.stu.find().limit(2)`

## skip 跳过指定数量
`db.stu.find().skip(2) 第三条开始`

## 投影
`db.stu.find({}, {_id:0,字段名:1,...})`
- 1:显示，0:不显示

## 排序
- 1:升序
- -1:降序
`db.stu.find().sort({字段:1})`


## 统计个数
`db.stu.find(条件).count()`
`db.stu.count({条件})`

## 消除重复
`db.stu.distinct(去重字段, {条件})`




