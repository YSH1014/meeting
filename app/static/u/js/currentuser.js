$(function(){
	"use strict";
	getUser(getUserCallBack);//�����û���Ϣ,getUserCallBack���Զ���
	var setPageLang(getLangCookie());//���û����޹ص�ҳ�����Բ���
	$("#navLang").click(toggleLang);//�����л���ť
});

//ȡ���û���Ϣ��Ļص�����
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
		$("#login").text("��¼");
	}else{
		$("#userid").text(name+" ��ӭ����");
		$("#login").text('����̨');
		$("#logout").text('�˳�');
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
 * ��Cookie��ȡ�õ�ǰҳ��ʹ�õ����� 
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
