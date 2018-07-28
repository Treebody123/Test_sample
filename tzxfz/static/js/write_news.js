// 将文件上传到我们自己的服务器的代码
/*
$(function () {
    var uploadBtn = $("#upload-btn");
    uploadBtn.change(function (event) {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('upfile', file);

        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    var thumbnailInput = $("input[name='thumbnail']");
                    thumbnailInput.val(url);
                }
            }
        });
    });
});
*/

$(function () {
    // progressGroup：用来控制整个进度条是否需要显示的
    var progressGroup = $("#progress-group");
    // progressBar：用来控制这个进度条的宽度
    var progressBar = $(".progress-bar");

    function progress(response) {
        var percent = response.total.percent;
        var percentText = percent.toFixed(0) + '%';
        console.log('****************');
        console.log(percent);
        console.log('****************');
        progressBar.css({"width":percentText});
        progressBar.text(percentText);
    }

    function error(err) {
        console.log('========');
        console.log(err);
        console.log('========');
        window.messageBox.showError(err.message);

        progressGroup.hide();
    }

    function complete(response) {
        // hash key
        var key = response.key;
        var domain = 'http://7xqenu.com1.z0.glb.clouddn.com/';
        var url = domain + key;
        var thumbnailInput = $("input[name='thumbnail']");
        thumbnailInput.val(url);

        progressGroup.hide();
        progressBar.css({"width":'0'});
        progressBar.text('0%');
    }

    var uploadBtn = $("#upload-btn");
    uploadBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    var key = file.name;
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg', 'image/gif','video/x-ms-wmv']
                    };
                    var config = {
                        useCdnDomain: true,
                        region: qiniu.region.z0
                    };
                    var observable = qiniu.upload(file,key,token,putExtra,config);
                    observable.subscribe({
                        'next': progress,
                        'error': error,
                        'complete': complete
                    });
                    progressGroup.show();
                }
            }
        });
    });
});


$(function () {
    window.ue = UE.getEditor('editor',{
        "initialFrameHeight": 400,
        'serverUrl': '/ueditor/upload/'
    });
});

$(function () {
    var submiBtn = $("#submit-btn");
    submiBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var title = $("input[name='title']").val();
        var desc = $("input[name='desc']").val();
        var category = $("select[name='category']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var news_id = btn.attr('data-news-id');
        var url = '';
        if(news_id){
            url = '/cms/edit_news/';
        }else{
            url = '/cms/write_news/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'desc': desc,
                'category': category,
                'thumbnail': thumbnail,
                'content': content,
                'pk':news_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('恭喜！新闻发表成功！',function () {
                        window.location.reload();
                    });
                }
            }
        });
    });
});