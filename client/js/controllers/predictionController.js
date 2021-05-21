angular.module('ITAApp')
.controller('predictionController', function($scope, $cookies, $timeout, $location, jobService){
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

    $scope.finished = false;
    $scope.shouldDisableButton = false;

    $scope.predict_chemical = function() {
        var smiles = $scope.smiles;
        if (smiles == null || smiles == '') {
        	return;
        }
        $scope.shouldDisableButton = true;
        jobService.predict_chemical(
            $scope.smiles
        ).success(function(res){
            $scope.finished = true;
            $scope.shouldDisableButton = false;
            $scope.image_path1 = 'img/estrogen_activity_prediction/' + $scope.smiles + '_1.png';
            $scope.image_path2 = 'img/estrogen_activity_prediction/' + $scope.smiles + '_2.png';
        });
    };



});