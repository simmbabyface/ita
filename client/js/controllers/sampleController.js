angular.module('ITAApp')
.controller('sampleController', function($scope, $cookies, $timeout, $location, jobService){
    var tox_assay_map;
    $scope.default = 'all';

    $scope.type = $scope.default;
    $scope.toxicity = $scope.default;
    $scope.assay = $scope.default;
    $scope.disable_toxicity = false;

    $scope.samples = Array();
    $scope.searched = false;
    
    jobService.get_all_assay_names_keyed_by_toxicities().success(function(res){
        tox_assay_map = res;
        $scope.toxicities = [$scope.default].concat(Object.keys(res));
        $scope.assays = [$scope.default].concat(Object.values(res).flat(1));
    });

    jobService.get_all_sample_types().success(function(res){
        $scope.types = [$scope.default].concat(res['sample_type']);
    });

    $scope.filter_assay = function() {
        if ($scope.toxicity != $scope.default) {
            $scope.assays = [$scope.default].concat(tox_assay_map[$scope.toxicity]);
            $scope.assay = $scope.default;
        } else {
            $scope.assays = [$scope.default].concat(Object.values(tox_assay_map).flat(1));
            $scope.assay = $scope.default;
        }
    }

    $scope.filter_toxicity = function() {
        if ($scope.assay != $scope.default) {
            for (var tox in tox_assay_map) {
                if (tox_assay_map[tox].includes($scope.assay)) {
                    $scope.toxicity = tox;
                    $scope.disable_toxicity = true;
                    break;
                }
            }
        } else {
            $scope.disable_toxicity = false;
        }
    }

    $scope.reset = function() {
        $scope.disable_toxicity = false;
    }

    $scope.search_sample = function() {
        var start_time = '';
        var end_time = '';
        var sample_type = $scope.type;
        var assay = $scope.assay;
        var toxicity = $scope.toxicity;
        if ($scope.start_time instanceof Date && !isNaN($scope.start_time)) {
            start_time = $scope.start_time.toISOString().split('T')[0];
        }
        if ($scope.end_time instanceof Date && !isNaN($scope.end_time)) {
            end_time = $scope.end_time.toISOString().split('T')[0];
        }
        if (sample_type == $scope.default) {
            sample_type = '';
        }
        if (assay == $scope.default) {
            assay = '';
        }
        if (toxicity == $scope.default) {
            toxicity = '';
        }
        $scope.searched = true;
        jobService.search_sample(
            start_time,
            end_time,
            sample_type,
            assay,
            toxicity,
            $scope.cas
        ).success(function(res){
            console.log(res);
            $scope.samples = res;
        });
    };
});