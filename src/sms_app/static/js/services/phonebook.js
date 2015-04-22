'use strict';

app.factory('Phonebook', function ($http) {
  var data_list = { 
    getAll: function(){
        var promise = $http.get('/phonebook/all').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    delete: function(_id){
        var promise = $http.get('/phonebook/delete/' + _id).then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    edit: function(_id) {
       var promise = $http.post('/phonebook/edit', { id: _id }).then(function(result) {
          return result.data;
        }); 
        return promise;

		},
   get: function(_id) {
       var promise = $http.get('/phonebook/' + _id).then(function(result) {
          return result.data[0];
        }); 
        return promise;

		},

  };  
  return data_list;
});
