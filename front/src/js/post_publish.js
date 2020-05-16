function Post() {

}

Post.prototype.initDatePicker = function () {
    var startPicker = $("#publish_time_show");

    var options = {
        'singleDatePicker': true,
        'showDropdowns': true,
        locale: {
        'format': 'YYYY-MM-DD',
        },
    };
    startPicker.daterangepicker(options);
};

Post.prototype.run = function() {
    this.initDatePicker();
};

$(function () {
    var post = new Post();
    post.run()
});