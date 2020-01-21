// JavaScript Document
$(document).ready(function () {
	"use strict";
	$("#addParticipateButton1").click(function () {
		$("#inputParticipate1").show();
		$(this).prop("id", "addParticipateButton2");
		$("#addParticipateButton2").click(function () {
			$("#inputParticipate2").show();
			$(this).prop("id", "addParticipateButton3");
			$("#addParticipateButton3").click(function () {
				$("#inputParticipate3").show();
				$(this).hide();
			});
		});
	});
	$("#inputProjectLeader").change(function () {
		if ($(this).prop("checked")) {
			$("#inputProjectIDPanel").show();
		}
		if (!$(this).prop("checked")) {
			$("#inputProjectIDPanel").hide();
		}

	});
/*	$("#inputNotes").change(function () {
		if (getByteLen($("#inputNotes").text()) >= 100) {
			$("#noteAlert").show();
			$("#submitButton").prop("id", "notReady");
		} else {
			$("#noteAlert").hide();
			$("#notReady").prop("id", "submitButton");
		}
	});*/
	$(".comments-response-button-reply").click(function () {
		$(this).parent().siblings(".comments-response-card").show();
		$(this).hide();
	});
	
	$(".comments-response-button-edit").click(function () {
		$(this).parent().next().hide();
		$(this).parent().siblings(".comments-edit-card").show();
		$(this).hide();
	});
	/*$(".form_datetime").datetimepicker({                format: "yyyy-mm-dd hh:ii:ss",                linkField: "mirror_field",                linkFormat: "yyyy-mm-dd hh:ii"                });*/

});
/*
function getByteLen(val) {
	"use strict";
	var len = 0;
	for (var i = 0; i < val.length; i++) {
		var a = val.charAt(i);
		if (a.match(/[^\x00-\xff]/ig) !== null) {
			len += 2;
		} else {
			len += 1;
		}
	}
	return len;
}
*/