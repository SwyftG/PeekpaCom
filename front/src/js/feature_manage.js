function CMSFeature() {

}

CMSFeature.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var feature_id = btn.attr('data-feature-id');
        peekpaajax.post({
            'url': '/cms/dashboard/feature/delete',
            'data': {
                'feature_id': feature_id
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

CMSFeature.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var feature = new CMSFeature();
    feature.run();
});