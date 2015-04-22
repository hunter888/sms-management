'use strict';

app.controller('UserEditCtrl',
  [       '$scope', '$rootScope','$log', '$state', 'toaster', 'Users',
  function($scope,   $rootScope,$log,   $state,   toaster,   Users){

    var user_id = $rootScope.$stateParams.user_id;
    $log.info("test");
    if ( user_id ){

    $log.info("test user_id" + user_id);
      // GET OBJECT
      Users.getUser(user_id).then(function(response){
        $log.info("response" + response.id);
        if (response.id){

             $log.info("test ok");
          // VARIABLES
          $scope.user = response;

          // FUNCTIONS

        } else {

          // NO OBJECT FOUND
          $state.go("app.users");

        }
      });

    } else {

      // NO SESSION
      $state.go("access.signin");

    }

  }
]);
