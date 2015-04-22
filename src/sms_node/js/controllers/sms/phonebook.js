'use strict';

app.controller('PhonebookCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Phonebook', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Phonebook, toaster) {
 
	$scope.reloadList = function () {
    Phonebook.getAll().then(function(data){
      $scope.data_list = data; 
		});
	}

 	$scope.deletePhonebook = function(phonebook){
		var modalInstance = $modal.open({
   	templateUrl: 'deleteModal',
   	controller: 'PhonebookDeleteModal',
   	resolve: {
   		phonebook: function(){
     		return phonebook;
   		}
   	}
   	});
   	modalInstance.result.then(function(){
      $window.location.reload();
   	});
	};


  $scope.reloadList();
}]);


app.controller('PhonebookDeleteModal',
  [       '$scope', '$rootScope', '$modalInstance', 'Phonebook', 'phonebook',
  function($scope,   $rootScope,   $modalInstance,   Phonebook,   phonebook){

      $scope.obj =  phonebook;
      $scope.name = phonebook.name;

      $scope.ok = function(obj){
        Phonebook.delete(phonebook.id);
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

app.controller('CreatePhonebookCtrl', ['$scope', '$rootScope', '$http', 'toaster','Phonebook', function($scope, $rootScope, $http, toaster, Phonebook) {
  $scope.department_error = "";
  $scope.name_error = "";
  $scope.mobile_number_error = "";
  $scope.rank_error = "";
  $scope.designation_error = "";
  $scope.home_address_error = "";

  $scope.submitForm = function() {
    $scope.spinnerClass = "fa fa-spin fa-spinner show inline";

    $http({
      method: "POST",
      url: "/phonebook/create",
      params: {
        department : $scope.department,
        name : $scope.name,
        mobile_number : $scope.mobile_number,
        rank : $scope.rank,
        designation : $scope.designation,
        home_address : $scope.home_address,
      }
    }).
    success(function(data, status, headers, config) {
      var res = data;
      console.info(res);
      if(res.success == "true") {
        $scope.toaster = {
          type: 'success',
          title: 'Success',
          text: 'Successfully added to Phonebook.'
        };

        toaster.pop($scope.toaster.type, $scope.toaster.title, $scope.toaster.text);

        // CLEAR ERROR CLASSES AND FORMS
        $scope.spinnerClass = "fa fa-spin fa-spinner hide";

  			$scope.department_error = "";
  			$scope.name_error = "";
  			$scope.mobile_number_error = "";
  			$scope.rank_error = "";
  			$scope.designation_error = "";
  			$scope.home_address_error = "";

  			$scope.department = "";
  			$scope.name = "";
  			$scope.mobile_number = "";
  			$scope.rank = "";
  			$scope.designation = "";
  			$scope.home_address = "";


        $scope.error_message = "";

      }
      else {
        $scope.error_message = res.message;
        $scope.spinnerClass = "fa fa-spin fa-spinner hide";
        if(res.field == "department") {
          $scope.department_error = "has-error";
        }
        else if(res.field == "name") {
          $scope.name_error = "has-error";
        }
        else if(res.field == "mobile_number") {
          $scope.mobile_number_error = "has-error";
        }
        else if(res.field == "rank") {
          $scope.rank_error = "has-error";
        } else {
          $scope.department_error = "has-error";
          $scope.name_error = "has-error";
          $scope.mobile_number_error = "has-error";
          $scope.rank_error = "has-error";
          $scope.designation_error = "has-error";
          $scope.home_address_error = "has-error";
        }
      }
    }).
    error(function(data, status, headers, config) {
    });

  }
}]);

