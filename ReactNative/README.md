# ReactNative 跨开发 APP

## 软件开发流程
- 需求分析
- UI界面设计
- 编码开发
- 测试
- 上线

## 需求分析
- 为什么要开发这款 APP
	+ https://github.com/trending
- App 要具有哪些功能？基本功能
	+ Trending 的客户端
	+ 能搜素 Github 上的项目
	+ 有离线缓存
- 扩展功能
	+ 支持 50 多种编程语言
	+ 订阅
		* 排序
		* 取消
		* 收藏 -> 分享
	+ 主题
	+ 统计

## 技术分解
### 技术栈
- ES5/ES6
- React
- Flexbox
- AsyncStorage
- Fetch
- Native Modules(扫描/分享)
- Android & iOS

### 第三方库
- @react-native-check-box(复选框)
- @react-native-easy-toast(提示框)
- @react-native-splash-screen(启动屏)
- @react-native-htmlview(html渲染)
- @react-native-scrollable-tab-view(标签切换)
- @react-native-sortable-listview(列表排序)
- @react-native-tab-navigator(底部导航)
- @react-native-parallax-scroll-view(视差滚动)
- 分享 SDK

### 自定义组件
- 自定义 NavigationBar
- 自定义 MoreMenu
- 自定义 启动屏
- 自定义 复选框
- 自定义 提示框

### 高层封装
- Native 模块封装
- BaseCommon封装
- 网络操作封装
- 数据库操作封装
- 数据解析封装
- Promise 封装
- 其他工具封装

## react-native 项目结构
- index.ios.js
- index.android.js
- andorid/ 项目
- ios/ 项目
- res/ 全局资源（图片、音视频等）
- doc/ 文档说明
- js/
	+ common 	可服用的组件（非完整页面）
	+ expand	扩展
	+ page 		完整页面
	+ config 	配置项（常量、接口地址、路由、多语言化等预置数据）
	+ util		工具类（非UI组件）




