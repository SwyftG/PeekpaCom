
$(document).ready(function () {
    var loadingCircle = $('#loading-circle');
    var contentBlock = $('#content-block');
    var fid = location.search;
    getDataFromServer("/center/data/" + fid , loadingCircle, contentBlock, initPageAfterData);

});

function initPageAfterData(data, loadingCircle, contentBlock){
        var tpl = template('data-list', {'data': data} );
        contentBlock.append(tpl);

        var nextPageButton = $(".page-link");
        nextPageButton.click(function () {
            var btn = $(this);
            var url = btn.attr('href');
            getDataFromServer(url, loadingCircle, contentBlock, initPageAfterData )
        });

        var options = {
             'singleDatePicker': true,
            'showDropdowns': true,
            locale: {
            'format': 'YYYY-MM-DD',
            },
        };

        var searchButton = $(".search-button");
        var inputTime = $(".input-time");
        var inputSearchKey = $(".input-search-key");
        inputTime.daterangepicker(options);
        searchButton.click(function () {
            var btn = $(this);
            var inputTimeValue = inputTime.val();
            var inputSearchKeyValue = inputSearchKey.val();
            var url = btn.attr('href') + "&search=" + inputSearchKeyValue + "&day=" + inputTimeValue;
            getDataFromServer(url, loadingCircle, contentBlock, initPageAfterData )
        });
}

function getDataFromServer(url, loadingCircle, contentBlock, callback) {
    contentBlock.hide();
    contentBlock.empty();
    loadingCircle.show();
    $.ajax({
        url: url,
        type: "get",
        success: function (data) {
            console.log("data:", data)
            callback(data, loadingCircle, contentBlock);
            loadingCircle.hide();
            contentBlock.show();
        }
    })
}

