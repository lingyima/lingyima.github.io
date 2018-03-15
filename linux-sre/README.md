# Linux 运维架构-[零壹码博客](https://lingyima.com)
## [计算机入门 ComputersGetting started](./computerGetting-started/)
- [计算机概论](./computerGetting-started/computer-concepts/)
- [操作系统](./computerGetting-started/operating-system/)
- [计算机网络](./computerGetting-started/computer-network/)
- [程序设计语言](./computerGetting-started/programming-language/)

## Linux 基础管理
- Linux 安装与配置环境
- Linux 基础入门
- 文件系统
- 文件操作工具
- bash 特性
- 文本处理工具及正则表达式
- 用户管理工具
- Linux 编辑器
- 压缩打包工具

## Linux 系统管理
- 磁盘分区
- 文件系统管理工具
- 程序包管理
- 网络管理
- 进程管理
- Linux 启动流程
- 内核管理
- 安装系统

## SHELL 脚本编程

## 系统服务管理
- systemd
- 任务计划
- SELinux
- OpenSSL
- OpenSSH
- DNS
- IPTABLES
- tcp wrapper
- nss and pam

## 应用服务管理
- File Server
- FTP 
- NFS
- SMB
- Web Service
	+ Apache
	+ PHP
	+ Mariadb
	+ Cache
		* Memecache, varnish
	+ NoSQL
		* Redis
		* MongoDB
		* HBase
	+ tomcap
	+ session replication cluster
- [Nginx](./application-service/nginx/)

- 分布式存储系统
	+ MogileFS
	+ GlusterFS

## 集群服务构建
- LB Cluster(负载均衡)
	+ LVS
	+ Nginx
	+ haproxy
- HA Cluster(高可用集群)
	+ keepalived
	+ Corosync+Pacemaker
	+ pcc/crmsh
- MySQL Cluster
	+ HA Cluster
	+ MHA
	+ Read-Write splitting

## Linux 运维工具
- ansible(中小规模)
- puppet(大规模自动化工具，Ruby开发的)
- saltstack(Python开发的)
- cobbler

## Linux 监控
- zabbix

## 虚拟化
- Linux 操作系统原理
- 虚拟化技术原理
- KVM 虚拟化应用详解
- XEN 虚拟化
- 虚拟化网络
- SDN

## 云计算集群构建
- OpenStack 云栈
- Docker
- ELK Stack
	+ ElasticSearch(搜索引擎)
	+ Logstash
	+ Kibana

## 大数据集群构建
- Hadoop v2
- HBase
- Hive
- Storm
- Spark

## 系统优化

## 人工智能

## 区块链

## IT 技术岗位

### 研发技术
- 硬件：机器语言（二进制的指令和数据）开发的接口代码
- 软件：程序写的程序代码
	+ 低级语言：汇编语言(机器(CPU能够执行的指令)相关的指令)，汇编器
	+ 高级语言：C/C++, 编译器
		* 系统级别(接近机器，机器执行性能更好)：C/C++ 
			性能服务类程序：操作系统, 数据库
		* 应用级(接近人类，人类易于编写)：Java, Python, Go
			应用程序：ansible, puppet

### 应用技术
- 运维：Linux 生态圈中的各应用程序的应用
	+ Shell 脚本编程：某些应用工作能自动完成
	+ Python：专业编程语言
		* Ansible Openstack
- DevOps: 开发运维