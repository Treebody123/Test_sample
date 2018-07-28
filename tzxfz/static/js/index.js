// 加载更多新闻的事件
$(function () {
    var loadBtn = $('.load-more-btn');
    loadBtn.click(function () {
        var li = $(".list-tab-group li.active");
        var category_id = li.attr('data-category-id');
        var page = parseInt(loadBtn.attr('data-page'));
        console.log("category_id:",category_id);
        console.log('page:',page);
        xfzajax.get({
            'url': '/list/',
            'data': {
                'p': page,
                'category_id': category_id
            },
            'success': function (result) {
                var newses = result['data'];
                if(newses.length > 0){
                    var tpl = template("news-item",{"newses":newses});
                    var newsListGroup = $(".news-list-group");
                    newsListGroup.append(tpl);
                    // ‘2’+‘1’
                    page += 1;
                    loadBtn.attr('data-page',page);
                }else{
                    window.messageBox.showInfo('没有更多数据了...');
                }
            }
        })
    });
});

$(function () {
    var categoryUl = $(".list-tab-group");
    var liTags = categoryUl.children();
    var loadBtn = $('.load-more-btn');
    liTags.click(function () {
        var li = $(this);
        var categoryId = li.attr('data-category-id');
        xfzajax.get({
            'url': '/list/',
            'data': {
                'category_id': categoryId
            },
            'success': function (result) {
                var newses = result['data'];
                var tpl = template("news-item",{"newses":newses});
                var newsListGroup = $(".news-list-group");
                // empay：可以将newsListGroup下所有的标签都清除掉
                newsListGroup.empty();
                newsListGroup.append(tpl);
                li.addClass('active').siblings().removeClass('active');
                loadBtn.attr('data-page',2);
            }
        });
    });
});