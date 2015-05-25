'use strict';

app.factory('House', function($http) {
    var debug = false;

    if(debug) var api = 'http://127.0.0.1:8090/apis';
    else var api = 'http://182.92.159.73/apis';

    return {
        search: function(query, page_num, callback) {
            var uri = api + '/search/' + query;
            if(page_num == undefined) uri += '/1';
            else uri += '/' + page_num;
            return $http.get(uri).success(callback);
        },
    };
});
