// 配置模块加载位置，给模块起个别名
require.config({
    paths : {
    	//远程cdn库没有加载成功，可以加载本地的库
        "jquery" : ["https://cdn.bootcss.com/jquery/3.3.1/core", "helper/jquery"],
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