angular.module('contact', ['restangular', 'ngRoute']).
  config(function($routeProvider, RestangularProvider) {
    $routeProvider.
      when('/', {
        controller:ListCtrl,
        templateUrl:'list.html'
      }).
      when('/edit/:contactId', {
        controller:EditCtrl,
        templateUrl:'detail.html',
        resolve: {
          contact: function(Restangular, $route){
            return Restangular.one('contacts', $route.current.params.contactId).get();
          }
        }
      }).
      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).
      otherwise({redirectTo:'/'});

      RestangularProvider.setBaseUrl('http://localhost:5000/api');
      RestangularProvider.setRestangularFields({
        id: '_id.$oid'
      });

      RestangularProvider.setRequestInterceptor(function(elem, operation, what) {

        if (operation === 'put') {
          elem._id = undefined;
          return elem;
        }
        return elem;
      })
  });


function ListCtrl($scope, Restangular) {
   $scope.contacts = Restangular.all("contacts").getList().$object;
}


function CreateCtrl($scope, $location, Restangular) {
  $scope.save = function() {
    Restangular.all('contacts').post($scope.contact).then(function(contact) {
      $location.path('/list');
    });
  }
}

function EditCtrl($scope, $location, Restangular, contact) {
  var original = contact;
  $scope.contact = Restangular.copy(original);


  $scope.isClean = function() {
    return angular.equals(original, $scope.contact);
  }

  $scope.destroy = function() {
    original.remove().then(function() {
      $location.path('/list');
    });
  };

  $scope.save = function() {
    $scope.contact.put().then(function() {
      $location.path('/');
    });
  };
}