$(function () {
    var submitBtn = $('#submit-comment-btn');
    var textarea = $(".comment-textarea");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id = submitBtn.attr('data-news-id');
        xfzajax.post({
            'url': '/add_comment/',
            'data': {
                'content': content,
                'news_id': news_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    console.log(result);
                    var comment = result['data'];
                    var tpl = template('comment-item',{"comment":comment});
                    var commentGroup = $(".comment-list-group");
                    commentGroup.prepend(tpl);
                    textarea.val('');
                }else{
                    window.messageBox.showError(result['message']);
                }
            }
        });
    });
});