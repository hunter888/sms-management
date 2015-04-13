'use strict';

/* Controllers */
  // signin controller
app.controller('SigninFormController', ['$scope', '$http', '$state', function($scope, $http, $state) {
    $scope.user = {};
    $scope.authError = null;
    $scope.login = function() {
      $scope.authError = null;
      // Try to login
      $http.post('../login', {email: $scope.user.email, password: $scope.user.password})
      .then(function(response) {
        console.log(response.data)
        if ( !response.data.user ) {
          $scope.authError = 'Email or Password not right';
        }else{
          //$state.go('app.dashboard-v1');
          $state.go('app.inbox');
        }
      }, function(x) {
        $scope.authError = 'Server Error';
      });
    };
  }])
;
