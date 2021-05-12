angular.module('ITAApp')
.controller('analyzeController', function($scope, $cookies, $timeout, $location, jobService){
	var marvinSketcherInstance;
    angular.element(document).ready(function () {
        MarvinJSUtil.getEditor("#sketch").then(function(sketcherInstance) {
            marvinSketcherInstance = sketcherInstance;
            addSmilesListener();
        }, function(error) {
            alert("Loading of the sketcher failed"+ error);
        });
    });

    var addSmilesListener = function(){
        marvinSketcherInstance.on('molchange', function(){
            marvinSketcherInstance.exportStructure("smiles").then(function(source) {
                $scope.$apply(function(){
                    $scope.smiles = source;
                });
            });
        });
    };

    var FILE_NAME = 'plot';
    $scope.finished = false;
    $scope.shouldDisableButton = false;

    $scope.analyze_chemical = function() {
        var smiles = $scope.smiles;
        if (smiles == null || smiles == '') {
        	return;
        }
        $scope.shouldDisableButton = true;
        jobService.analyze_chemical(
            smiles,
            FILE_NAME
        ).success(function(res){
            $scope.finished = true;
            $scope.shouldDisableButton = false;
        });
    };



});