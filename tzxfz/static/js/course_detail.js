
$(function () {
    var span = $(".video-container span");
    var video_url = span.attr("data-video-url");
    var cover_url = span.attr('data-cover-url');
    var course_id = span.attr('data-course-id');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: video_url,
        image: "http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.jpg",
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        tokenEncrypt: "true",
        // AccessKey
        ak: '42455a8c985649aeaa4ca86b50482d78'
    });
    player.on("beforePlay",function (e) {
        if(!/m3u8/.test(e.file)){
            return;
        }

        xfzajax.get({
            'url': '/course/course_token/',
            'data': {
                'video_url': video_url,
                'course_id': course_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    player.setToken(e.file,token);
                }else{
                    window.messageBox.showError(result['message']);
                    player.stop();
                }
            }
        });
    });
});