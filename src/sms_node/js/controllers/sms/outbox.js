'use strict';

app.controller('OutboxCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Outbox', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Outbox, toaster) {
 
	$scope.reloadList = function () {
    Outbox.getUnsent().then(function(data){
      $scope.data_list = data; 
		});
	}

 	$scope.deleteOutbox = function(outbox){
		var modalInstance = $modal.open({
   	templateUrl: 'deleteModal',
   	controller: 'OutboxDeleteModal',
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


app.controller('OutboxDeleteModal',
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

