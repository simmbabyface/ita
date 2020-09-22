angular.module('ITAApp')
.controller('assayItemController', function($scope, $location, $window, $routeParams, $cookies, $anchorScroll, jobService){
    //$window.scrollTo(0, 0);
    $scope.scrollTo = function(id) {
        $location.hash(id);
        $anchorScroll.yOffset = 100;
        $anchorScroll();
    }
    jobService.assay_detail($routeParams.aid).success(function(res){
        $scope.assay_detail_info = res;
    });
    jobService.assay_sample($routeParams.aid).success(function(res){
        $scope.assay_sample_info = res;
    });
    jobService.assay_chemical($routeParams.aid).success(function(res){
        $scope.assay_chemical_info = res;
    });
});