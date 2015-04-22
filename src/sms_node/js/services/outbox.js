'use strict';

app.factory('Outbox', function ($http) {
  var data_list = { 
    getAll: function(){
        var promise = $http.get('/outbox/all').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    delete: function(_id){
        var promise = $http.get('/outbox/delete/' + _id).then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    edit: function(_id) {
       var promise = $http.post('/outbox/edit', { id: _id }).then(function(result) {
          return result.data;
        }); 
        return promise;

		},
   get: function(_id) {
       var promise = $http.get('/outbox/' + _id).then(function(result) {
          return result.data[0];
        }); 
        return promise;

		},

   getUnsent: function() {
       var promise = $http.get('/outbox/getWithStatus/0').then(function(result) {
          return result.data;
        }); 
        return promise;

		},

   getDrafts: function() {
       var promise = $http.get('/outbox/getWithStatus/1').then(function(result) {
          return result.data;
        }); 
        return promise;

		},

   getSent: function() {
       var promise = $http.get('/outbox/getWithStatus/2').then(function(result) {
          return result.data;
        }); 
        return promise;

		},

   getFailed: function() {
       var promise = $http.get('/outbox/getWithStatus/3').then(function(result) {
          return result.data;
        }); 
        return promise;

		},





  };  
  return data_list;
});
