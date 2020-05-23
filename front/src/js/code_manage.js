function CMSCode() {

}

CMSCode.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var code_id = btn.attr('data-code-id');
        peekpaajax.post({
            'url': '/cms/dashboard/code/delete',
            'data': {
                'code_id': code_id
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

CMSCode.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var codeItem = new CMSCode();
    codeItem.run();
});