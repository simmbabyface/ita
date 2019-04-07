angular.module('ITAApp')
.controller('assayItemController', function($scope, $window, $routeParams, $cookies, $anchorScroll, jobService){
    $window.scrollTo(0, 0);
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