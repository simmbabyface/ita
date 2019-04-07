angular.module('ITAApp')
.controller('sampleItemController', function($scope, $window, $routeParams, $cookies, $anchorScroll, jobService){
    $window.scrollTo(0, 0);
    jobService.sample_detail($routeParams.sid).success(function(res){
        $scope.sample_detail_info = res;
    });
    jobService.sample_assay($routeParams.sid).success(function(res){
        $scope.sample_assay_info = res;
    });
    jobService.sample_chemical($routeParams.sid).success(function(res){
        $scope.sample_chemical_info = res;
    });
});