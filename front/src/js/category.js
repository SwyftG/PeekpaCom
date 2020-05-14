function CMSCategory() {

}

CMSCategory.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var category_id = btn.attr('data-category-id');
        peekpaajax.post({
            'url': '/cms/dashboard/category/delete',
            'data': {
                'category_id': category_id
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

CMSCategory.prototype.run = function () {
    this.listenDeleteEvent();
};

$(function () {
    var category = new CMSCategory();
    category.run();
});