$(function(){
	"use strict";
	getUser(getUserCallBack);//载入用户信息,getUserCallBack可自定义
	var setPageLang(getLangCookie());//与用户名无关的页面语言部分
	$("#navLang").click(toggleLang);//语言切换按钮
});

//取得用户信息后的回调函数
function getUserCallBack(data){
	"use strict";
	var name = null;
	if(null!==data) {name = data.truename;}
	if("en" === getLangCookie()){
		setLoginLang_en(name);
	}else{
		setLoginLang_zh_CN(name);
	}
}

function setLoginLang_zh_CN(name){
	"use strict";
	if(null===name){
		$("#login").text("登录");
	}else{
		$("#userid").text(name+" 欢迎光临");
		$("#login").text('工作台');
		$("#logout").text('退出');
	}
}

function setLoginLang_en(name){
	"use strict";
	if(null===name){
		$("#login").text("Login");
	}else{
		$("#userid").text(name+" welcome");
		$("#login").text("Dashboard");
		$("#logout").text("Logout");
	}
}

function toggleLang() {
	"use strict";
	var language=getLangCookie();
	if (language==="zh_CN"){
		setLangCookie('en');
	}else{
		setLangCookie('zh_CN');
	}
	location.reload();
}

/**
 * 从Cookie中取得当前页面使用的语言 
 * @returns
 */
function getLangCookie(){
	"use strict";
	var lang = getCookie('locale');
	if(null==lang) return 'zh_CN';
	return lang;
}

function setLangCookie(lang){
	document.cookie='locale='+lang+'; path=/; domain=.china-vo.org';
}

function getUser(callbackfunc){
   $.ajax({
        url: "http://astrocloud.china-vo.org/security/user/current", 
        type: "GET",
        async: false, 
        cache: false,
        dataType: "jsonp",
		jsonpCallback: "xxx_callbackfunc_xxx_name",
        success: function(json){
        	callbackfunc(json);
        },
        error: function(text){
        	callbackfunc(null);
        }
    });
}
