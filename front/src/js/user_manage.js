function CMSUser() {

}

CMSUser.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var user_id = btn.attr('data-user-id');
        peekpaajax.post({
            'url': '/cms/dashboard/user/delete',
            'data': {
                'user_id': user_id
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

CMSUser.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var user = new CMSUser();
    user.run();
});