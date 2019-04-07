angular.module('ITAApp')
.controller('assayController', function($scope, $cookies, $timeout, $location, jobService){
    var tox_biological_process_target_map;
    $scope.default = 'all';

    $scope.toxicity = $scope.default;
    $scope.biological_process_target = $scope.default;
    $scope.disable_toxicity = false;

    $scope.samples = Array();
    $scope.searched = false;
    
    jobService.get_all_biological_process_targets_keyed_by_toxicities().success(function(res){
        tox_biological_process_target_map = res;
        $scope.toxicities = [$scope.default].concat(Object.keys(res));
        $scope.biological_process_targets = [$scope.default].concat(Object.values(res).flat(1));
    });

    $scope.filter_biological_process_target = function() {
        if ($scope.toxicity != $scope.default) {
            $scope.biological_process_targets = [$scope.default].concat(tox_biological_process_target_map[$scope.toxicity]);
            $scope.biological_process_target = $scope.default;
        } else {
            $scope.biological_process_targets = [$scope.default].concat(Object.values(tox_biological_process_target_map).flat(1));
            $scope.biological_process_target = $scope.default;
        }
    }

    $scope.filter_toxicity = function() {
        if ($scope.biological_process_target != $scope.default) {
            for (var tox in tox_biological_process_target_map) {
                if (tox_biological_process_target_map[tox].includes($scope.biological_process_target)) {
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

    $scope.search_assay = function() {
        var biological_process_target = $scope.biological_process_target;
        var toxicity = $scope.toxicity;
        if (biological_process_target == $scope.default) {
            biological_process_target = '';
        }
        if (toxicity == $scope.default) {
            toxicity = '';
        }
        $scope.searched = true;
        jobService.search_assay(
            biological_process_target,
            toxicity
        ).success(function(res){
            console.log(res);
            $scope.assays = res;
        });
    };
});