function CMSPost() {

}

CMSPost.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var post_id = btn.attr('data-post-id');
        peekpaajax.post({
            'url': '/cms/dashboard/post/delete',
            'data': {
                'post_id': post_id
            },
            'success': function (result) {
                if(result['code'] === 200){
                    window.location = window.location.href;
                    // window.location.reload()
                }
            }
        });
    });
};

CMSPost.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var post = new CMSPost();
    post.run();
});