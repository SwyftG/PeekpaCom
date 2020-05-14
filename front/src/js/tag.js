function CMSTag() {

}

CMSTag.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var tag_id = btn.attr('data-tag-id');
        peekpaajax.post({
            'url': '/cms/dashboard/tag/delete',
            'data': {
                'tag_id': tag_id
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

CMSTag.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var tag = new CMSTag();
    tag.run();
});