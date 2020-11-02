function CenterCode() {

}

CenterCode.prototype.listenDeleteEvent = function () {
    var submitBtns = $(".submit-btn");
    var formInput = $("#form-code");
    submitBtns.click(function () {
        var form_code = formInput.val()
        peekpaajax.post({
            'url': '/validate/',
            'data': {
                'form-code': form_code
            },
            'success': function (result) {
                if(result['code'] === 200){
                    window.location.href = "/center/"
                }
            }
        });
    });
};

CenterCode.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var centerCode = new CenterCode();
    centerCode.run();
});
