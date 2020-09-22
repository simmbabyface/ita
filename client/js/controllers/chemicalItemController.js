angular.module('ITAApp')
.controller('chemicalItemController', function($scope, $location, $window, $routeParams, $cookies, $anchorScroll, jobService){
    //$window.scrollTo(0, 0);
    $scope.scrollTo = function(id) {
        $location.hash(id);
        $anchorScroll.yOffset = 100;
        $anchorScroll();
    }
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