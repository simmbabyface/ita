angular.module('ITAApp')
.controller('homeController', function($scope, $location, $window){
    // parallax
    var initialHeight = angular.element('.jumbotron').outerHeight();
    angular.element($window).on('scroll', function(){
        var scrolled = angular.element($window).scrollTop();
        angular.element('.bg').css('height', (initialHeight - scrolled) + 'px');
    });

    $scope.redirect = function(path) {
    	$location.path(path);
    };

});