'use strict';

app.factory('Users', function ($http) {
  var users = { 
    getAll: function(){
        var promise = $http.get('/users/all').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    deleteUsers: function(users_id){
        var promise = $http.post('/users/delete', { id: users_id }).then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    editUser: function(user_id) {
       var promise = $http.post('/users/edit', { id: users_id }).then(function(result) {
          return result.data;
        }); 
        return promise;

		},
  getUser: function(user_id) {
       var promise = $http.get('/users/' + user_id).then(function(result) {
          return result.data[0];
        }); 
        return promise;

		},

  };  
  return users;
});
