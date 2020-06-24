function GetKeyByValue(json, val){
    for(var i in json){
        if (json[i] == val){
            return i
        }
    }
}

function arrRemoveByValue(arr, val) {
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == val) {
            arr.splice(i, 1);
            break;
        }
    }
}

function objCompare(obj1, obj2){
    for(var i in obj1){
        if(obj1[i] != obj2[i]){
            return false
        }
    }
    return true
}

function objCalcNumber(obj){
    var count = 0;
    for(var key in obj){
        count++
    }
    return count
}

function ExeSqliteStr(strsql) {
    var result;
    $.ajax({
        async: false,
        type: "POST",
        data:{
            strsql: strsql
        },
        url: def_serverurl + "/Public/ExeSqliteStr",
        success: function (data) {
            result = jQuery.parseJSON(data);
        }
    })
    return result
}

function GetRoleDataRequest(group, role) {
    var result;
    $.ajax({
        async: false,
        type: "POST",
        data: {
            "group":group,
            "roleid":role
        },
        url: def_serverurl + "/Public/GetRoleData",
        success: function(data){
            result = jQuery.parseJSON(data);
        }
    })
    return result 
}

function GetSignJobRequest(name){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        data: {"account":name},
        url: def_serverurl + "/Other/WorkSign",
        success: function(data){
            result = jQuery.parseJSON(data);
        }
    })
    return result 
}

function GetCurrentDateRequest(){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        url: def_serverurl + "/Other/DateQuery",
        success: function(data){
            result = jQuery.parseJSON(data);
        }
    })
    return result 
}

function getQueryString(name) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
    var r = window.location.search.substr(1).match(reg); 
    if (r != null) return unescape(r[2]); return null; 
} 

function TimeControl(current_date){
    $("#SelectTime").empty();
    $("#SelectTime").append('<select id="year" name="year"></select>年');
    for (var i=1900;i<2100;i++){
        $("#year").append('<option value="' + i + '">' + i + '</option>');
    }

    $("#SelectTime").append('<select id="month" name="month"></select>月');
    for (var i=1;i<13;i++){
        var str = String(i);
        if (i<10){
            str = "0" + str;
        }
        $("#month").append('<option value="' + str + '">' + i + '</option>');
    }

     $("#SelectTime").append('<select id="day" name="day"></select>日');
    for (var i=1;i<32;i++){
        var str = String(i);
        if (i<10){
            str = "0" + str;
        }
        $("#day").append('<option value="' + str + '">' + i + '</option>');    }

    $("#SelectTime").append('<select id="hour" name="hour"></select>时');
    for (var i=0;i<24;i++){
        var str = String(i);
        if (i<10){
            str = "0" + str;
        }
        $("#hour").append('<option value="' + str + '">' + i + '</option>');    }

    $("#SelectTime").append('<select id="min" name="min"></select>分');
    for (var i=0;i<60;i++){
        var str = String(i);
        if (i<10){
            str = "0" + str;
        }
        $("#min").append('<option value="' + str + '">' + i + '</option>');    }

    $("#SelectTime").append('<select id="second" name="second"></select>秒');
    for (var i=0;i<60;i++){
        var str = String(i);
        if (i<10){
            str = "0" + str;
        }
        $("#second").append('<option value="' + str + '">' + i + '</option>');    }

    if (current_date != undefined){
        $("#year").val(current_date.substring(0,4));
        $("#month").val(current_date.substring(5,7));
        $("#day").val(current_date.substring(8,10));
        $("#hour").val(current_date.substring(11,13));
        $("#min").val(current_date.substring(14,16));
        $("#second").val(current_date.substring(17,19));
    }
}

function GetStageConfigurationRequest(){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        url: def_serverurl + "/Public/GetStageConfiguration",
        success: function (data) {
            console.log(data)
            result = jQuery.parseJSON(data);
            console.log(result)
        }
    })
    return result 
}

function GetProtocolFileRequest(){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        url: def_serverurl + "/Public/GetProtocolFile",
        success: function(data){
            result = jQuery.parseJSON(data);
        }
    })
    return result; 
}

function GetActivityInfoRequest(){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        url: def_serverurl + "/Public/GetActivityInfo",
        success: function(data){
            result = jQuery.parseJSON(data);
        }
    })
    return result; 
}

function GetActivityInfo(){
    var obj = GetActivityInfoRequest();
    var activity = obj["activity_type"];
    var task = obj["task_type"];
    var sel = document.getElementById("SelectActivity");
    sel.options.length=0;
    for (var key in activity) {
        if (key > 8)
        {
            break;
        }
        sel.options.add(new Option(key + " " + activity[key], key));
    }

    return task;
}

function GetActivityInfoNew(){
    var obj = GetActivityInfoRequest();
    var activity = obj["activity_type"];
    var sel = document.getElementById("SelectActivity");
    sel.options.length=0;
    for (var key in activity) {
        if (key > 8 && key != 41)
        {
            sel.options.add(new Option(key + " " + activity[key], key));
        }
    }
}

function GetTaskListRequest(group){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        data:{
            group: group
        },
        url: def_serverurl + "/Public/GetTaskLua",
        success: function (data) {
            result = jQuery.parseJSON(data);
        }
    })
    return result;
}

function GetItemListRequest(){
    var result;
    $.ajax({
        async: false,
        type: "POST",
        url: def_serverurl + "/Public/GetItemList",
        success: function (data) {
            result = jQuery.parseJSON(data);
            for (var i in result["items"]) {
                result["items"][i]["label"] = result["items"][i]["id"] + " " + result["items"][i]["name"];
            }
        }
    })
    return result["items"];
}

function GetGroupUnion(arr_union) {
    var text = document.getElementById("TextUnion");
    var unionlist = [];
    for (var key in arr_union) {
        unionlist.push({ title: arr_union[key].union_name, result: arr_union[key].union_id });
    }

    $("#TextUnion").bigAutocomplete({
        width: 543,
        data: unionlist,
        callback: function (data) {
            text.value = data.result;
        }
    });
}

function GetGroupRole(arr_role) {
    var text = document.getElementById("TextRole");
    var rolelist = [];
    for (var key in arr_role) {
        rolelist.push({ title: arr_role[key].role_name, result: arr_role[key].role_id });
    }

    $("#TextRole").bigAutocomplete({
        width: 543,
        data: rolelist,
        callback: function (data) {
            text.value = data.result;
        }
    });
}

function GetGameGroupRequest(){
	var result;
	$.ajax({
		async: false,
		type: "POST",
		url: def_serverurl + "/Public/GetGameGroup",
		success: function(data){
			result = jQuery.parseJSON(data);
		}
	})
	return result;
}

function GetGameGroup(){
    var obj = GetGameGroupRequest();
    var sel = document.getElementById("SelectGroup");
    sel.options.length = 0;
    var group_server = {
        info :{},
        open: {},
        close: []
    };

    for (var key in obj.center_group) {
        for (var num in obj.center_group[key]["groups"]) {
            var val = obj.center_group[key]["groups"][num];
            group_server.info[val.group_id] = val;
            if (val.isOpen)
            {
                if (!group_server.open[val.the_center] && group_server.open[val.the_center] != '') {
                    group_server.open[val.the_center] = [];
                }
                group_server.open[val.the_center].push(val.group_id);
            } else {
                group_server.close.push(val.group_name);
            }
        }
    }

    for (var key in group_server["open"]) {
        $("#SelectGroup").append('<option disabled="" style="background-color:#ADD8E6;color:#000000;">' + key + '</<option>');
        for (var num in group_server["open"][key]) {
            var val = group_server.info[group_server["open"][key][num]];
            sel.options.add(new Option(val.group_name, val.group_id));
        }
	}
    for (var key in group_server["close"]) {
        $("#SelectGroup").append('<option disabled="">' + group_server["close"][key] + '</<option>');
	}
	for (key in sel.options){
		if ("4122" == sel.options[key].value){
			sel.options[key].selected = true;
			break;
		}
	}

	return group_server;
}

function MakeForm(PARAMS, URL) { 
    var temp = document.createElement("makeform");
    temp.id = "makeform";
    temp.action = URL;        
    temp.method = "post";        
    temp.style.display = "none";        
    for (var x in PARAMS) {        
        var opt = document.createElement("textarea");        
        opt.name = x;        
        opt.value = PARAMS[x];        
        temp.appendChild(opt);        
    }        
    document.body.appendChild(temp);       
	return temp;        
}

function ShowDialog(url) 
{ 
    if(document.all)
    { 
        feature="dialogWidth:300px;dialogHeight:200px;status:no;help:no";
        window.showModalDialog(url, null, feature); 
    } 
    else 
    { 
        feature ="width=300,height=200,menubar=no,toolbar=no,location=no,"; 
        feature+="scrollbars=no,status=no,modal=yes";
        window.open(url, null, feature); 
    } 
}