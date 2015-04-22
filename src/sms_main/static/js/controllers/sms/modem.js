'use strict';

app.controller('ModemCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Serial', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Serial, toaster) {
 
	$scope.reloadList = function () {
    Serial.getAllDevices().then(function(data){
      $scope.data_list = data; 
		});
	}

	$scope.deleteModem = function(serial){
		var modalInstance = $modal.open({
   	templateUrl: 'deleteModal',
   	controller: 'ModemDeleteModal',
   	resolve: {
   		serial: function(){
     		return serial;
   		}
   	}
   	});
   	modalInstance.result.then(function(){
  		$scope.reloadList();
   	});
	};



  $scope.reloadList();
}]);


app.controller('ModemDeleteModal',
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

