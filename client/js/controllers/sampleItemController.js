angular.module('ITAApp')
.controller('sampleItemController', function($scope, $location, $window, $routeParams, $cookies, $anchorScroll, jobService){
    //$window.scrollTo(0, 0);
    $scope.scrollTo = function(id) {
        $location.hash(id);
        $anchorScroll.yOffset = 100;
        $anchorScroll();
    }
    jobService.sample_detail($routeParams.sid).success(function(res){
        $scope.sample_detail_info = res;
    });
    jobService.sample_assay($routeParams.sid).success(function(res){
        $scope.sample_assay_info = res;
    });
    jobService.sample_chemical_component($routeParams.sid).success(function(res){
        $scope.sample_chemical_component_info = res;
    });
});