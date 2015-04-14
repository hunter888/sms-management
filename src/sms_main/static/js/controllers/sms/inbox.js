'use strict';

app.controller('InboxCtrl', ['$scope', '$rootScope','$state', '$http', '$modal','$window', 'Inbox', 'toaster', function($scope, $rootScope, $state, $http, $modal,$window, Inbox, toaster) {
  var inbox_id = $rootScope.$stateParams.inbox_id;
  var exportCSV = $rootScope.$stateParams.exportCSV;
 $scope.username = $rootScope.username ;
 
	$scope.reloadList = function () {
    Inbox.getAll().then(function(data){
      $scope.data_list = data; 
		});
	}

 	$scope.deleteInbox = function(inbox){
		var modalInstance = $modal.open({
   	templateUrl: 'deleteModal',
   	controller: 'InboxDeleteModal',
   	resolve: {
   		inbox: function(){
     		return inbox;
   		}
   	}
   	});
   	modalInstance.result.then(function(){
      $window.location.reload();
   	});
	};

  if(inbox_id) {
 

  } else {

  $scope.reloadList();
  }
}]);


app.controller('InboxDeleteModal',
  [       '$scope', '$rootScope', '$modalInstance', 'Inbox', 'inbox',
  function($scope,   $rootScope,   $modalInstance,   Inbox,   inbox){

      $scope.obj =  inbox;
      $scope.name = inbox.sender_name;

      $scope.ok = function(obj){
        Inbox.deleteInbox(inbox.id);
        $modalInstance.close();
      };

      $scope.cancel = function(){
        $modalInstance.close();
      };


  }
]);

