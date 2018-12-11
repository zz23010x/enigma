// ==UserScript==
// @name         AddMagazineContent
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  add magazine content
// @author       zz
// @match        *://testcms.duzhe.com/*
// @grant        none
// @require       https://code.jquery.com/jquery-3.2.1.min.js
// @require       https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.0/clipboard.min.js
// ==/UserScript==


var $ = window.jQuery;
(function() {
    'use strict';
    // Your code here...
    var InputEnum = {
        TITLE : 0,
        AUTHOR : 1,
        TRANSLATOR : 2,
        ORIGIN : 3,
        COLUMNNUM : 7,
        CONTENTNUM : 8,
    }

    var FunctionPage = {
        ADDMAGAZINECONTENT : '/addMagazineContent?',
    }

    CreateSideTools()
    if (window.location.href.indexOf(FunctionPage.ADDMAGAZINECONTENT) != -1){
        AddMagazineContent()
    }
})();

function AddMagazineContent(){
    let btnRefresh = '<li><button id="btnPullArticle">Get One</button></li>'
    let btnTitle = '<li><button id="btnCTitle" class="btnCopy">Copy Title</button></li>'
    let btnAuthor = '<li><button id="btnCAuthor" class="btnCopy">Copy Author</button></li>'
    let btnTranslator = '<li><button id="btnCTranslator" class="btnCopy">Copy Translator</button></li>'
    let btnOrigin = '<li><button id="btnCOrigin" class="btnCopy">Copy Origin</button></li>'
    let btnIntroduction = '<li><button id="btnCIntroduction" class="btnCopy">Copy Introduction</button></li>'
    let btnContent = '<li><button id="btnCContent" class="btnCopy">Copy Content</button></li>'
    let btnImage = '<li></li><button id="btnCImage" class="btnCopy">Copy ImageSrc</button></li>'
    let divImageSearchTools = '<li><input id="inputWidth" type="text" style="width:120px">x<input id="inputHeight" type="text" style="width:120px"><br><input id="inputWord" type="text" style="width:120px"><button id="btnSearchImage">SearchImageByBaidu</button></li>'
    $('#ulFuncView').append(btnRefresh)
    $('#ulFuncView').append(btnTitle)
    $('#ulFuncView').append(btnAuthor)
    $('#ulFuncView').append(btnTranslator)
    $('#ulFuncView').append(btnOrigin)
    $('#ulFuncView').append(btnIntroduction)
    $('#ulFuncView').append(btnContent)
    $('#ulFuncView').append(btnImage)
    $('#ulFuncView').append(divImageSearchTools)
    $('.btnCopy').css({'white-space': 'nowrap', 'overflow': 'hidden', 'text-overflow': 'ellipsis'})

    $('#btnPullArticle').click(function (){
        $.ajax({
            type: "GET",
            url: "http://localhost:3000/reader/pull_article",
            success: function (data, textStatus, jqXHR) {
                console.log(data)
                $('#btnCTitle').attr('data-clipboard-text', data.title)
                $('#btnCAuthor').attr('data-clipboard-text', data.author)
                $('#btnCTranslator').attr('data-clipboard-text', data.translator)
                $('#btnCOrigin').attr('data-clipboard-text', data.origin)
                $('#btnCIntroduction').attr('data-clipboard-text', data.introduction)
                $('#btnCContent').attr('data-clipboard-text', data.content)

                if (data.translator === 'china_'){
                    $('#btnCTranslator').hide()
                }else{
                    $('#btnCTranslator').show()
                }

                $('.btnCopy').each(function(){
                    if ($(this).attr('data-clipboard-text') === ''){
                        $(this).hide()
                    }else{
                        $(this).show()
                    }
                })
                
                new ClipboardJS('.btnCopy');

                // var d = dialog({
                //     content: data.title,
                //     quickClose: true,// 点击空白处快速关闭
                //     align: 'top left',
                // });
                // d.show(document.getElementById('btnPullArticle'))
                // setTimeout(function () {
                //     d.close().remove();
                // }, 1000);
            },
            complete: function(jqXHR, textStatus){}
        })
    })

    $('#btnSearchImage').click(function (){
        $.ajax({
            type: "GET",
            url: "http://localhost:3000/reader/pull_image?word=" + $("#inputWord").val() + "&width=" + $("#inputWidth").val() + "&height=" + $("#inputHeight").val(),
            success: function (data, textStatus, jqXHR) {
                if (data != ''){
                    $("#spResultMsg").text('result:0')
                    setTimeout(function(e){
                        $("#spResultMsg").text('爬虫读者文章')                        
                    }, 2000)
                }
                $('#btnCImage').attr('data-clipboard-text', data)
                new ClipboardJS('#btnCImage');
            },
            complete: function(jqXHR, textStatus){}
        })
    })
}

function CreateSideTools(){
    $(document.body).append('<div id="floatTools" class="rides-cs"></div>')
    $('#floatTools').append('<div class="floatL" style="float:left"><a style="display:block;text-decoration:none;" id="aFloatTools_Show" class="btnOpen" href="javascript:void(0);">+</a><a style="display:none;text-decoration:none;" id="aFloatTools_Hide" class="btnCtn" href="javascript:void(0);">—</a></div>')
    $('#floatTools').append('<div id="divFloatToolsView" class="floatR" style="display:none;float:left;"></div>')
    $('#divFloatToolsView').append('<span id="spResultMsg">爬虫读者文章</span><ul id="ulFuncView" style="list-style:none"></ul>')

    $(".rides-cs").css({'position':'fixed','bottom':'20px', 'right':'20px'});
    
    $("#aFloatTools_Show").on("click",function(){
        $('#divFloatToolsView').animate({width:'show',opacity:'show'},100,function(){$('#divFloatToolsView').show();});
        $('#aFloatTools_Show').hide();
        $('#aFloatTools_Hide').show();		
    });
    $("#aFloatTools_Hide").on("click",function(){
        $('#divFloatToolsView').animate({width:'hide', opacity:'hide'},100,function(){$('#divFloatToolsView').hide();});
        $('#aFloatTools_Show').show();
        $('#aFloatTools_Hide').hide();	
    });
}
// $('#btnFillForm').click(function (){
//     $.ajax({
//         type: "GET",
//         url: "localhost:3000/reader/pull_article",
//         success: function (data, textStatus, jqXHR) {
//             console.log(data.content)
//             $('.el-input__inner').eq(InputEnum.TITLE).val(data.title)
//             $('.el-input__inner').eq(InputEnum.AUTHOR).val(data.author)
//             $('.el-input__inner').eq(InputEnum.TRANSLATOR).val(data.translator)
//             $('.el-input__inner').eq(InputEnum.ORIGIN).val(data.origin)
//             $('.el-input__inner').eq(InputEnum.COLUMNNUM).val('卷首语')
//             $('.el-input__inner').eq(InputEnum.CONTENTNUM).val(data.contentNum)
//             $('.el-textarea__inner').val(data.introduction)
//         },
//         complete: function(jqXHR, textStatus){}
//     })
// })