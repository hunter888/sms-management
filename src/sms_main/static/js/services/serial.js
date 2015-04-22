'use strict';

app.factory('Serial', function ($http) {
  var data_list = { 

	  
    getAllDevices: function(){
        var promise = $http.get('/serial/getAllDevices').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    getAll: function(){
        var promise = $http.get('/serial/all').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    delete: function(_id){
        var promise = $http.get('/serial/delete/' + _id).then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    edit: function(_id) {
       var promise = $http.post('/serial/edit', { id: _id }).then(function(result) {
          return result.data;
        }); 
        return promise;

		},
   get: function(_id) {
       var promise = $http.get('/serial/' + _id).then(function(result) {
          return result.data[0];
        }); 
        return promise;

		},

  };  
  return data_list;
});
