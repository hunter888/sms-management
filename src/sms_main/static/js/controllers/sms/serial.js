'use strict';

app.controller('SerialCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Serial', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Serial, toaster) {
 
	$scope.reloadList = function () {
    Serial.getAll().then(function(data){
      $scope.data_list = data; 
		});
	}

	
  $scope.addAsModem = function(_data, network) {
    $scope.spinnerClass = "fa fa-spin fa-spinner show inline";
    $http({
      method: "POST",
      url: "/serial/addAsModem",
      params: {
        id : _data.id,
        name : _data.name,
        network : network,
      }
    }).

    success(function(data, status, headers, config) {
      var res = data;
      console.info(res);
      if(res.success == "true") {
        $scope.toaster = {
          type: 'success',
          title: 'Success',
          text: 'Successfully added as modem for ' + network + ' network.'
        };

        toaster.pop($scope.toaster.type, $scope.toaster.title, $scope.toaster.text);

        // CLEAR ERROR CLASSES AND FORMS
        $scope.spinnerClass = "fa fa-spin fa-spinner hide";



      }
      else {
      }
    }).
    error(function(data, status, headers, config) {
    });
    }


  $scope.reloadList();
}]);


app.controller('SerialDeleteModal',
  [       '$scope', '$rootScope', '$modalInstance', 'Serial', 'serial',
  function($scope,   $rootScope,   $modalInstance,   Serial,   serial){

      $scope.obj =  serial;
      $scope.name = serial.name;

      $scope.ok = function(obj){
        Serial.delete(serial.id);
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
});

