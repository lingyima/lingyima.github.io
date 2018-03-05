// 配置模块加载位置，给模块起个别名
require.config({
    paths : {
    	//远程cdn库没有加载成功，可以加载本地的库
        "jquery" : ["https://cdn.bootcss.com/jquery/3.3.1/jquerys", "jquery"],
        "stack" : ["core/stack"],
        "util" : ["helper/util"],
    },
    shim: {
        "stack": {
        	exports: "stack"
        },
        "util": {
        	exports: "util"
        }
        /*
        "underscore" : {
            exports : "_";
        },
        "jquery.form" : {
            deps : ["jquery"]
        }
        */
    }
})

requirejs(["stack","util","jquery"], function(stack, util, $) {

	$('body').append("<p>调用jQuery</p>")
	var stack = new stack();

	// 入栈
	stack.push("唐僧");
	stack.push("孙悟空");
	stack.push("沙僧");
	util.echo(stack.push("猪八戒"));


	util.echo(stack.stdout());

	

	util.echo('获取栈元素大小：' + stack.size())
	
	util.echo('弹栈：' + stack.pop());
	util.echo('栈元素列表：' + stack.stdout());

	util.echo('获取栈大小：' + stack.size());
	
	util.echo('获取顶栈：' + stack.top());
	util.echo('获取底栈：' + stack.bottom());
	
	util.echo('清空栈：' + stack.clear());
	util.echo('栈元素列表：' + stack.stdout());

	util.echo('栈元素是否为空：' + stack.isEmpty())

});