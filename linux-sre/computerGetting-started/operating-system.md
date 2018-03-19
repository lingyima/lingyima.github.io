# 操作系统-[零壹码博客](https://lingyima.com)
## 操作系统发展史
- Multi tasks(Bell, MIT, GE) => Multics
- KenThompson: Space Travel
- DEC: PDP-11, VAX(VMS系统)
	+ PDP-7: 汇编语言
	+ 1969: Unics => Unix
	+ Unix: 1971, nroff
	+ 1972: Unix, 10台
	+ B：Dennis Ritch, C
	+ 《美国计算机通信》：1974,开发发布 Unix 1.0版本

	+ AT&T: System v, 1979
	+ 1978， SCO公司包装发行Unix, C编译器
	+ 1980， Microsoft , Xenix(Unix)系统
	+ Berkeley: 
		* Ken in Berkeley
		* Student: Bill Joy
		* Build **BSRG**
		* 1977, BSRG distribution BSD(Berkeley System Distribution) 
	+ 1980, DARPA => 实现 TCP/IP 
		* 本来 VMS 系统上实现（商业）
		* BSD 上实现
		* 1983 => Unix in TCP/IP
	+ 1981, Microsoft, Bill Gate
		* SCP 公司 程序员研发小系统 QDOS(Quick and Dirty Operating System)
		* IBM 发售 PC 机
		* DOS 2.0 => CP/M
		* 1990: Unix 开发环境
		* VMS 领导入职微软 => 开发 Windows NT(New Technolegy)

	+ SUN： Bill Joy
		* workstation： 非常复杂的任务
		* BSD 系统：Solaris
	+ Apple
		* Xerox: park(star图形界面)
		* 卖给 乔布斯
		* Bill Gates复制park系统(上成代码) => Windows(蓝屏问题)
	+ 1985: Unix 商业化
		* 一份拷贝4万美元
	+ MIT: Richard Stallman 
		* GNU: GNU is Not Unix
		* GPL: General Pulibc License(freedom 自由软件)
		* FSF：Free Software Foundation
		* X-Window: GPL
		* gcc: GNU C Compiler
		* vi: Visual interface

- Andrew: Minix, 4000+行

- System V(Bell Lab)
	+ AIX(IBM)
	+ Solaris(SUN->Oracle)
	+ HP-UX(HP)
- BSD(Berkeley System Distribution), BSRG 组织研发
	+ NetBSD
	+ OpenBSD
	+ FreeBSD

- System V vs BSD
	+ 1990, BSD 完全独立
		* Jolitz, BSD 移植到 X86, 商业化后，推出项目
		* 386-BSD
	+ 1991-8: Linus Torvalds 宣布成立 Linux
		* GPL
	+ Larry Wall => diff, patch
	
- 完整的OS
	+ Kernel + Application
	+ 狭义上的OS: Kernel
	+ GNU/Linux
- OS的接口: 仅是应用程序
	+ GUI: Graphic User Interface
		* GNome: C, gtk图形库
		* [KDE](https://www.kde.org/)：C++, QT图形库
		* [xfce](https://xfce.org)
	+ GLI: Command Line Interface
		* bash
		* zsh
		* sh
		* csh
		* tcsh
		* ksh
- OS 的功能
	+ 驱动程序
	+ 进程管理
	+ 安全
	+ 网络协议栈
	+ 内存管理
	+ 文件系统

- API：Application Program Interface 程序员面对的编程接口
	+ POSIX: Portable Operating System
- ABI：Application Binary Interface 程序应用者面对运行程序的接口
- GNU:
	+ 源码：编译为二进制格式
	+ gcc, glibc, vi, linux
	+ Linux 发行版：数百种之多
		* RedHat
			RedHat 9.0
				RHEL: RedHat Enterprise Linux
					CentOS: Community Enterprise OS
				Fedora Core: 6个月
		* Debian
			Ubuntu 
				Mint
			Knopix
		* Slackware
			S.u.S.E(Novel)
				SLES: Suse Linux Enterprise System
				OpenSUSE
		* Gentoo
		* ArchLinux
- 软件程序：版本号
	+ major(架构).minor(功能).release(bug)-compile time
		* major: 主版本号，有结构性变化才更改
		* minor: 次版本号，新增功能是才变化，一般奇数表示测试版，偶数表示开发板
		* release: 对次版本的修订次数或补丁包数
		* compile time: 编译次数
	+ Linux 0.99, 2.2, 2.4, 2.6
		* Linux 3.0, 3.2, 3.4
		* Linux 4.0, 4.3
		* el: Enterprise Linux
		* pp: 测试版
		* fc: fedora core
		* rc: 候选版本
		* x86_64: 64位
	+ GNU:
		* vi: 
		* gcc:

- 发行版有自己的版本号
	+ RHEL: 5.x, 6.x, 7.x
		* Fedora 23
	+ Debian: 8.x
	+ OpenSuSE: 13.x

- GPL, BSD, Apache, MIT
- GPL: General Public License
	+ copyright, copyleft
	+ LGPL: Lessor GPL
	+ GPLv2, GPLv3
	+ FSF: Ree
- BSD:
- Apache: 不以原作者名义宣传代码
	+ ASF: Apache Software Foundation

- 双线授权：
	+ Community: 遵循开源协定
	+ Enterprise: 商业授权，附加功能
- 程序管理
	+ 程序组成部分
		* 二进制程序
		* 配置文件
		* 库文件
		* 帮助文件
	+ X, Y, Z 程序包
	+ 程序包管理器：X
		* 程序的组成文件打包成一个或有限几个文件
		* 安装
		* 卸载
		* 查询

- Debian: dpkg(.deb), apt-get
- RedHat: rpm, yum -> dnf
- S.u.S.E: rpm, zypper
- ArchLinux: port
- LFS: Linux From Scratch



## 什么是操作系统
## 操作系统分类
## Unix 操作系统

### UNIX 简史
### 什么是 UNIX
### UNIX 结构
### UNIX 特性
### UNNIX 标准
### UNIX 发行版

## Linux 操作系统
### Linux 发展简史
### GNU/Linux
### Linux 特性
### Linux 组成
### Linux 子系统
### Linux 版本号
### Linux 发行版
### Linux 哲学思想
### Linux 启动程序
### Linux 程序包管理器
### Linux 接口

