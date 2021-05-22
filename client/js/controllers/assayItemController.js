angular.module('ITAApp')
.controller('assayItemController', function($scope, $sce, $location, $window, $routeParams, $cookies, $anchorScroll, jobService){
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
    jobService.assay_component($routeParams.aid).success(function(res){
        $scope.assay_component_info = res;
    });
    jobService.assay_chemical($routeParams.aid).success(function(res){
        $scope.assay_chemical_info = res;
    });
    var trusted = {};
    $scope.getPopoverContent = function(content) {
        var available_curves = ["C0000001", "C0000002", "C0000003", "CP0000011", "S0000001"]; // TODO: Change hardcoded value
        if (available_curves.includes(content.trim())) {
            var generated_html = '<div><img src="img/' + content.trim() + '-assaycurve.png" class="img-responsive"></div>';
            return trusted[generated_html] || (trusted[generated_html] = $sce.trustAsHtml(generated_html));     
        }
    }
});