'use strict';

app.controller('NavbarController', function($scope, $routeParams, $location) {
    if($routeParams.query < 2 | $routeParams > 50) {
        $location.path('/home');
        return;
    }

    $scope.$on('$routeChangeSuccess', function (event, current, previous) {
        $scope.query = current.pathParams.query;
     });

    $scope.go = function(query) {
        $location.path(query);
    };
});

app.controller('HomeController', function($rootScope, $scope, $location) {
    $scope.go = function(query) {
        $location.path(query);
    };

    $rootScope.is_homepage = function() {
        return true;
    }
});

app.controller('EmptyController', function($rootScope, $scope, $location) {
    $scope.go = function(query) {
        $location.path(query);
    };

    $rootScope.is_homepage = function() {
        return true;
    }
});

app.controller('SearchController', function($rootScope, $scope, $location, $routeParams, House) {
    if($routeParams.query < 2 | $routeParams > 50) {
        $location.path('/home');
        return;
    }

    House.search($routeParams.query, $routeParams.page_num, function(data) {
        if(!data.page_count)
            $location.path('empty');
        $scope.query = data.query;
        $scope.page_count = data.page_count;
        $scope.page_num = data.page_num;
        $scope.page_next = data.page_next;
        $scope.page_prev = data.page_prev;
        $scope.houses = data.result;
    });

    $rootScope.is_homepage = function() {
        return false;
    }
});
