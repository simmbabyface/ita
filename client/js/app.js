var app = angular.module('ITAApp', ['ngRoute', 'ngCookies', 'angular-jqcloud', 'ui.bootstrap']);

app.config(function($routeProvider, $locationProvider) {
    if (window.history && history.pushState){
        $locationProvider.html5Mode(true);
    }
    $routeProvider.when('/', {
        templateUrl: 'views/home.html',
        controller: 'homeController'
    }).when('/signup', {
        templateUrl: 'views/signup.html',
        controller: 'signupController'
    }).when('/signin', {
        templateUrl: 'views/signin.html',
        controller: 'signinController'
    }).when('/sample', {
        templateUrl: 'views/sample.html',
        controller: 'sampleController'
    }).when('/chemical', {
        templateUrl: 'views/chemical.html',
        controller: 'chemicalController'
    }).when('/analyze', {
        templateUrl: 'views/analyze.html',
        controller: 'analyzeController'
    }).when('/assay', {
        templateUrl: 'views/assay.html',
        controller: 'assayController'
    }).when('/about', {
        templateUrl: 'views/about.html',
        controller: 'aboutController'
    }).when('/sampleItem/:sid', {
        templateUrl: 'views/sample_item.html',
        controller: 'sampleItemController'
    }).when('/chemicalItem/:cid', {
        templateUrl: 'views/chemical_item.html',
        controller: 'chemicalItemController'
    }).when('/assayItem/:aid', {
        templateUrl: 'views/assay_item.html',
        controller: 'assayItemController'
    }).otherwise({
        redirectTo: '/'
    });
});

