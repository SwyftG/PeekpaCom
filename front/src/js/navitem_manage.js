function CMSNavItem() {

}

CMSNavItem.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var navitem_id = btn.attr('data-navitem-id');
        peekpaajax.post({
            'url': '/cms/dashboard/navitem/delete',
            'data': {
                'navitem_id': navitem_id
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

CMSNavItem.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var navItem = new CMSNavItem();
    navItem.run();
});