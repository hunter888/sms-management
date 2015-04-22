'use strict';

app.controller('DraftCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Outbox', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Outbox, toaster) {
 
	$scope.reloadList = function () {
    Outbox.getDrafts().then(function(data){
      $scope.data_list = data; 
		});
	}

 	$scope.deleteOutbox = function(outbox){
		var modalInstance = $modal.open({
   	templateUrl: 'deleteModal',
   	controller: 'FailedDeleteModal',
   	resolve: {
   		outbox: function(){
     		return outbox;
   		}
   	}
   	});
   	modalInstance.result.then(function(){
      $window.location.reload();
   	});
	};


  $scope.reloadList();
}]);


app.controller('FailedDeleteModal',
  [       '$scope', '$rootScope', '$modalInstance', 'Outbox', 'outbox',
  function($scope,   $rootScope,   $modalInstance,   Outbox,   outbox){

      $scope.obj =  outbox;
      $scope.name = outbox.recipient_name;

      $scope.ok = function(obj){
        Outbox.delete(outbox.id);
        $modalInstance.close();
      };

      $scope.cancel = function(){
        $modalInstance.close();
      };


  }
]);



app.filter('propsFilter', function() {
    return function(items, props) {
        var out = [];

        if (angular.isArray(items)) {
          items.forEach(function(item) {
            var itemMatches = false;

            var keys = Object.keys(props);
            for (var i = 0; i < keys.length; i++) {
              var prop = keys[i];
              var text = props[prop].toLowerCase();
              if (item[prop].toString().toLowerCase().indexOf(text) !== -1) {
                itemMatches = true;
                break;
              }
            }

            if (itemMatches) {
              out.push(item);
            }
          });
        } else {
          // Let the output be the input untouched
          out = items;
        }

        return out;
    };
})

app.controller('CreateSMSCtrl', ['$scope', '$rootScope', '$http', 'toaster','Phonebook', function($scope, $rootScope, $http, toaster, Phonebook) {
  $scope.priority_error = "";
  $scope.recipient_error = "";
  $scope.message_error = "";

  $scope.clear = function() {
  	$scope.person.selected = undefined;
 	};


  $scope.priorities = [
      {name:'Normal', value: 'normal'},
      {name:'Low', value: 'low'},
      {name:'High', value: 'high'},
    ];
  $scope.priority = $scope.priorities[0];

	$scope.reloadList = function () {
    Phonebook.getAll().then(function(data){
      $scope.people = data; 
		});
	}

 $scope.person = {};

	$scope.reloadList();

  $scope.submitForm = function() {
    $scope.spinnerClass = "fa fa-spin fa-spinner show inline";

    $http({
      method: "POST",
      url: "/outbox/create",
      params: {
        priority : $scope.priority.value,
        recipient_id : $scope.person.selected.id,
        message : $scope.message,
      }
    }).
    success(function(data, status, headers, config) {
      var res = data;
      console.info(res);
      if(res.success == "true") {
        $scope.toaster = {
          type: 'success',
          title: 'Success',
          text: 'Successfully added to Outbox.'
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

