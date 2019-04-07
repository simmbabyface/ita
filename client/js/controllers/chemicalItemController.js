angular.module('ITAApp')
.controller('chemicalItemController', function($scope, $window, $routeParams, $cookies, $anchorScroll, jobService){
    $window.scrollTo(0, 0);
    jobService.chemical_detail($routeParams.cid).success(function(res){
        $scope.chemical_detail_info = res;
    });
    jobService.chemical_assay($routeParams.cid).success(function(res){
        $scope.chemical_assay_info = res;
    });
    jobService.chemical_sample($routeParams.cid).success(function(res){
        $scope.chemical_sample_info = res;
    });
});