function CMSExchangeLink() {

}

CMSExchangeLink.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var exchangelink_id = btn.attr('data-exchangelink-id');
        peekpaajax.post({
            'url': '/cms/dashboard/exchangelink/delete',
            'data': {
                'exchangelink_id': exchangelink_id
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

CMSExchangeLink.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var exchangeLink = new CMSExchangeLink();
    exchangeLink.run();
});