'use strict';

app.factory('Inbox', function ($http) {
  var inbox_list = { 
    getAll: function(){
        var promise = $http.get('/inbox/all').then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    deleteInbox: function(inbox_id){
        var promise = $http.get('/inbox/delete/' + inbox_id).then(function(result) {
          return result.data;
        }); 
        return promise;
      },  
    editInbox: function(inbox_id) {
       var promise = $http.post('/inbox/edit', { id: inbox_id }).then(function(result) {
          return result.data;
        }); 
        return promise;

		},
  getInbox: function(inbox_id) {
       var promise = $http.get('/inbox/' + inbox_id).then(function(result) {
          return result.data[0];
        }); 
        return promise;

		},

  };  
  return inbox_list;
});
