angular.module('ITAApp')
.factory('jobService', function($http){
    var jobServiceAPI = {};

    // search sample
    jobServiceAPI.get_all_assay_names_keyed_by_toxicities = function() {
        return $http.get('/get_all_assay_names_keyed_by_toxicities');
    };

    jobServiceAPI.get_all_sample_types = function() {
        return $http.get('/get_all_sample_types');
    };

    jobServiceAPI.search_sample = function(start_time, end_time, type, assay, toxicity, cas){
        return $http.post('/search_sample', {
            start_time: start_time,
            end_time: end_time,
            type: type,
            assay: assay,
            toxicity: toxicity,
            cas: cas
        });
    };

    // search chemical
    jobServiceAPI.search_chemical = function(cas, type, assay, toxicity, smiles) {
        return $http.post('/search_chemical', {
            cas: cas,
            type: type,
            assay: assay,
            toxicity: toxicity,
            smiles: smiles
        });
    };

    // search assay
    jobServiceAPI.get_all_biological_process_targets_keyed_by_toxicities = function() {
        return $http.get('/get_all_biological_process_targets_keyed_by_toxicities');
    }

    jobServiceAPI.search_assay = function(biological_process_target, toxicity){
        return $http.post('/search_assay', {
            biological_process_target: biological_process_target,
            toxicity: toxicity
        });
    };

    // sample
    jobServiceAPI.sample_detail = function(sample_id){
        return $http.post('/sample_detail', {sample_id: sample_id});
    };

    jobServiceAPI.sample_assay = function(sample_id){
        return $http.post('/sample_assay', {sample_id: sample_id});
    };

    jobServiceAPI.sample_chemical = function(sample_id){
        return $http.post('/sample_chemical', {sample_id: sample_id});
    };

    jobServiceAPI.sample_chemical_component = function(sample_id){
        return $http.post('/sample_chemical_component', {sample_id: sample_id});
    };

    // chemical
    jobServiceAPI.chemical_detail = function(chemical_id){
        return $http.post('/chemical_detail', {chemical_id: chemical_id});
    };

    jobServiceAPI.chemical_assay = function(chemical_id){
        return $http.post('/chemical_assay', {chemical_id: chemical_id});
    };

    jobServiceAPI.chemical_sample = function(chemical_id){
        return $http.post('/chemical_sample', {chemical_id: chemical_id});
    };

    // assay
    jobServiceAPI.assay_detail = function(assay_id){
        return $http.post('/assay_detail', {assay_id: assay_id});
    };

    jobServiceAPI.assay_chemical = function(assay_id){
        return $http.post('/assay_chemical', {assay_id: assay_id});
    };

    jobServiceAPI.assay_component = function(assay_id){
        return $http.post('/assay_component', {assay_id: assay_id});
    };

    jobServiceAPI.assay_sample = function(assay_id){
        return $http.post('/assay_sample', {assay_id: assay_id});
    };

    jobServiceAPI.createUnregistered = function(smiles, captcha_id, captcha_code){
        return $http.post('/createUnregistered', {
            smiles: smiles,
            captcha_id: captcha_id,
            captcha_code: captcha_code
        });
    };

    jobServiceAPI.list = function(username, password){
        return $http.post('/list', {
            username: username,
            password: password
        });
    };

    jobServiceAPI.svg = function(id){
        return $http.post('/svg', {
            id: id
        });
    };

    jobServiceAPI.structure = function(smiles){
        return $http.post('http://202.127.19.75:5210/webservices/rest-v0/util/detail', {
            'structures' : [
                {'structure': smiles}
            ],
            'display': {
                'include': ['image']
            }
        });
    }

    return jobServiceAPI;
});
