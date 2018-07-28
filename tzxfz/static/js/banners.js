
// 这个函数是用来给这个关闭按钮添加关闭事件的
function addCloseBannerEvent(bannerItem) {
    var closeBtn = bannerItem.find('.close-btn');
    var bannerId = bannerItem.attr('data-banner-id');
    closeBtn.click(function () {
        if(bannerId){
            xfzalert.alertConfirm({
                'text': '您确定要删除这个轮播图吗？',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/delete_banner/',
                        "data": {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if(result['code'] === 200){
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功！');
                            }
                        }
                    });
                }
            });
        }else{
            bannerItem.remove();
        }
    });
}

// 这个函数是用来绑定选择图片的事件的
function addImageSelectEvent(bannerItem) {
    var image = bannerItem.find(".banner-image");
    var imageSelect = bannerItem.find(".image-select");
    image.click(function () {
        imageSelect.click();
    });

    imageSelect.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('upfile',file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if(result['code'] === 200){
                    var url = result['data']['url'];
                    image.attr("src",url);
                }
            }
        });
    });
}

function addSaveBannerEvent(bannerItem) {
    var saveBtn = bannerItem.find(".save-btn");
    var image = bannerItem.find(".banner-image");
    var priorityInput = bannerItem.find("input[name='priority']");
    var linktoInput = bannerItem.find("input[name='link_to']");
    var bannerId = bannerItem.attr('data-banner-id');
    var url = '';
    if(bannerId){
        url = '/cms/edit_banner/';
    }else{
        url = '/cms/add_banner/';
    }
    saveBtn.click(function () {
        var image_url = image.attr('src');
        var priority = priorityInput.val();
        var link_to = linktoInput.val();

        xfzajax.post({
            'url': url,
            'data': {
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId
            },
            'success': function (result) {
                if(result['code'] === 200){
                    if(!bannerId){
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('轮播图添加成功！');
                    }else{
                        window.messageBox.showSuccess('轮播图修改成功！');
                    }
                    var prioritySpan = bannerItem.find('.priority-span');
                    prioritySpan.text("优先级："+priority);
                }
            }
        });
    });
}

function createBannerItem(banner) {
    var tpl = template("banner-item",{'banner':banner});
    var bannerListGroup  =$(".banner-list-group");
    var bannerItem = null;
    if(banner){
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find('.banner-item:last');
    }else{
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find('.banner-item:first');
    }
    addCloseBannerEvent(bannerItem);
    addImageSelectEvent(bannerItem);
    addSaveBannerEvent(bannerItem);
}

// 网页加载完毕后就执行获取轮播图列表的事件
$(function () {
    xfzajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if(result['code'] === 200){
                var banners = result['data']['banners'];
                console.log(banners);
                for(var i=0; i<banners.length; i++){
                    var banner = banners[i];
                    createBannerItem(banner);
                }
            }
        }
    });
});


// 绑定添加轮播图按钮的点击事件
$(function () {
    var addBtn = $('#add-banner-btn');
    var bannerListGroup = $(".banner-list-group");
    addBtn.click(function () {
        var length = bannerListGroup.children().length;
        if(length >= 6){
            window.messageBox.showInfo('最多只能添加6个轮播图！');
        }else{
            createBannerItem();
        }
    });
});