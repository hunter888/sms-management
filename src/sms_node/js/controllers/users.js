'use strict';

app.controller('UsersCtrl', ['$scope', '$rootScope','$state', '$http', 'Users', 'toaster', function($scope, $rootScope, $state, $http, Users, toaster) {
  var users_id = $rootScope.$stateParams.users_id;
  var exportCSV = $rootScope.$stateParams.exportCSV;
 
     $scope.editUser = function(user){
        $state.go("app.edit_user", { "user_id": user.id });
      };


  if(users_id) {
 

  }
  else if(exportCSV) {
    var url = '/users/export';
    window.location = url;
    toaster.pop("wait", "Export", "Downloading your CSV..");
    
    $scope.users = []; 
    Users.getAll().then(function(data){
      $scope.users = data; 
    }); 
  }
  else {
    $scope.users = []; 
    Users.getAll().then(function(data){
      $scope.users = data; 
    }); 
  }

}]);



app.controller('NewUsersCtrl', ['$scope', '$rootScope', '$http', 'toaster', function($scope, $rootScope, $http, toaster) {
  $scope.firstname_error = "";
  $scope.lastname_error = "";
  $scope.username_error = "";
  $scope.email_error = "";
  $scope.form_success = "";
  $scope.role_error = "";


  $scope.roles = [
      {name:'Select One', value: ''},
      {name:'Admin', value: 'admin'},
      {name:'User', value: 'user'},
    ];
  $scope.role = $scope.roles[0];

  $scope.change = function() {
    if($scope.password == $scope.confirm_password) {
      $scope.form_success = "has-success";
    }
    else {
      $scope.form_success = "has-error";
    }
  }

  $scope.submitForm = function() {
    $scope.spinnerClass = "fa fa-spin fa-spinner show inline";

    $http({
      method: "POST",
      url: "/users/create",
      params: {
        firstname : $scope.firstname,
        lastname : $scope.lastname,
        username : $scope.new_username,
        email : $scope.email,
        password : $scope.password,
        confirm_password : $scope.confirm_password,
        role: $scope.role.value,
      }
    }).

    success(function(data, status, headers, config) {
      var res = data;
      console.info(res);
      if(res.success == "true") {
        $scope.toaster = {
          type: 'success',
          title: 'Success',
          text: 'Successfully created a new Account.'
        };

        toaster.pop($scope.toaster.type, $scope.toaster.title, $scope.toaster.text);

        // CLEAR ERROR CLASSES AND FORMS
        $scope.spinnerClass = "fa fa-spin fa-spinner hide";

        $scope.firstname_error = "";
        $scope.lastname_error = "";
        $scope.username_error = "";
        $scope.email_error = "";
        $scope.form_success = "";
        $scope.role_error = "";
        // FORMS
        $scope.firstname = "";
        $scope.lastname = "";
        $scope.new_username = "";
        $scope.email = "";
        $scope.password = "";
        $scope.confirm_password = "";


        $scope.error_message = "";

      }
      else {
        $scope.error_message = res.message;
        if(res.field == "firstname") {
          $scope.firstname_error = "has-error";
        }
        else if(res.field == "lastname") {
          $scope.lastname_error = "has-error";
        }
        else if(res.field == "username") {
          $scope.username_error = "has-error";
        }
        else if(res.field == "email") {
          $scope.email_error = "has-error";
        }

        else {
          $scope.firstname_error = "has-error";
          $scope.lastname_error = "has-error";
          $scope.username_error = "has-error";
          $scope.email_error = "has-error";
          $scope.form_success = "has-error";
        }
      }
    }).
    error(function(data, status, headers, config) {
    });

  }
}]);






