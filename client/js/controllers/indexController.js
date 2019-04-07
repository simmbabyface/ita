angular.module('ITAApp')
.controller('indexController', function($scope, $rootScope, $cookies, $location, $window){
    $scope.redirect = function(path) {
    	$window.scrollTo(0, 0);
    	$location.path(path);
    };
    $scope.logout = function(){
        noty({text: 'Signout successful!', type:'success', timeout: 1000});
        delete $cookies.user;
        delete $cookies.pass;
        $rootScope.user = null;
        $location.path('/');
        return false;
    };
});