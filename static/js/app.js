/**
 * AngularJS 1.8 Application Logic for LPG Distribution & Consumer Management System
 * Module: lpgApp
 * Controllers: MainCtrl, StockCtrl, OrdersCtrl, BookingCtrl, ConsumersCtrl, RoutesCtrl
 * Custom Filter: inrCurrency (Formats values with Indian Rupee ₹ symbol and Indian numbering system)
 */

(function () {
  'use strict';

  var app = angular.module('lpgApp', []);

  // Configure CSRF cookie handling and template interpolation symbols for Django integration
  app.config(['$httpProvider', '$interpolateProvider', function ($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

    // Avoid collision with Django template tags {{ ... }}
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

  /**
   * Bespoke Indian Rupee (₹) Currency Filter
   * Formats numbers according to Indian numbering system (Lakhs and Crores).
   * Example: 903 -> ₹903.00, 1825 -> ₹1,825.00, 154200 -> ₹1,54,200.00
   */
  app.filter('inrCurrency', function () {
    return function (input, decimals) {
      if (input === null || input === undefined || isNaN(input)) {
        return '₹0.00';
      }
      decimals = (decimals !== undefined) ? decimals : 2;
      var num = parseFloat(input);
      var isNegative = num < 0;
      num = Math.abs(num);

      var fixedStr = num.toFixed(decimals);
      var parts = fixedStr.split('.');
      var integerPart = parts[0];
      var decimalPart = parts.length > 1 ? '.' + parts[1] : '';

      // Indian numbering format regex: last 3 digits, then groups of 2
      var lastThree = integerPart.substring(integerPart.length - 3);
      var otherNumbers = integerPart.substring(0, integerPart.length - 3);
      if (otherNumbers !== '') {
        lastThree = ',' + lastThree;
      }
      var formattedInt = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;

      return (isNegative ? '-₹' : '₹') + formattedInt + (decimals > 0 ? decimalPart : '');
    };
  });

  /**
   * Root / Main Dashboard Controller
   * Manages global view navigation, notification toasts, and top KPI ribbon.
   */
  app.controller('MainCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.activeTab = 'overview'; // 'overview', 'stock', 'booking', 'orders', 'consumers', 'routes'
    $scope.loading = false;
    $scope.toast = { show: false, message: '', type: 'info' };
    $scope.highVisibility = (localStorage.getItem('lpg_high_visibility') === 'true');

    // Apply saved high visibility preference on init
    if ($scope.highVisibility) {
      document.body.classList.add('high-visibility-mode');
    }

    $scope.toggleHighVisibility = function () {
      $scope.highVisibility = !$scope.highVisibility;
      if ($scope.highVisibility) {
        document.body.classList.add('high-visibility-mode');
        localStorage.setItem('lpg_high_visibility', 'true');
        $scope.showToast('High-Visibility Mode Enabled: Maximum contrast active', 'info');
      } else {
        document.body.classList.remove('high-visibility-mode');
        localStorage.setItem('lpg_high_visibility', 'false');
        $scope.showToast('Standard Warm Theme Restored', 'info');
      }
    };

    var baseMetrics = {
      total_consumers: 0,
      active_consumers: 0,
      total_godown_stock: 0,
      total_available_stock: 0,
      total_reserved_stock: 0,
      today_bookings: 0,
      today_revenue: 0,
      pending_deliveries: 0,
      delivered_today: 0,
      active_routes: 0,
      low_stock_alerts: 0
    };
    $scope.metrics = (window.INITIAL_METRICS) ? angular.extend({}, baseMetrics, window.INITIAL_METRICS) : baseMetrics;

    $scope.switchTab = function (tabName) {
      $scope.activeTab = tabName;
      if (tabName === 'overview') {
        $scope.fetchMetrics();
        $rootScope.$broadcast('refreshAll');
      }
    };

    $scope.showToast = function (message, type) {
      $scope.toast.message = message;
      $scope.toast.type = type || 'success';
      $scope.toast.show = true;
      setTimeout(function () {
        $scope.$apply(function () {
          $scope.toast.show = false;
        });
      }, 4500);
    };

    $scope.fetchMetrics = function () {
      $http.get('/api/stats/')
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            $scope.metrics = response.data.metrics;
          }
        }, function (error) {
          console.error('Failed to load KPIs:', error);
        });
    };

    // Listen for broadcasted notification requests
    $rootScope.$on('notify', function (event, data) {
      $scope.showToast(data.message, data.type);
    });

    // Listen for global data refresh requests
    $rootScope.$on('dataUpdated', function () {
      $scope.fetchMetrics();
    });

    // Initial KPI fetch
    $scope.fetchMetrics();
  }]);

  /**
   * Stock Inventory Controller
   * Real-time monitoring of domestic and commercial cylinder stock levels.
   */
  app.controller('StockCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.stocks = [];
    $scope.summary = {};
    $scope.loading = false;

    $scope.loadStock = function () {
      $scope.loading = true;
      $http.get('/api/stock/')
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            $scope.stocks = response.data.stocks;
            $scope.summary = response.data.summary;
          }
          $scope.loading = false;
        }, function (error) {
          $scope.loading = false;
          console.error('Stock fetch error:', error);
        });
    };

    $scope.getBadgeClass = function (cylinderType) {
      if (!cylinderType) return 'badge-domestic';
      if (cylinderType.indexOf('14.2kg') !== -1) return 'badge-domestic';
      if (cylinderType.indexOf('19kg') !== -1) return 'badge-commercial';
      return 'badge-mini';
    };

    $scope.getMeterClass = function (percentage) {
      if (percentage < 25) return 'meter-danger';
      if (percentage < 50) return 'meter-warning';
      return 'meter-healthy';
    };

    $scope.quickBookCylinder = function (stock) {
      $rootScope.$broadcast('preselectCylinder', stock);
    };

    $rootScope.$on('refreshAll', function () {
      $scope.loadStock();
    });

    $rootScope.$on('dataUpdated', function () {
      $scope.loadStock();
    });

    // Initial load
    $scope.loadStock();
  }]);

  /**
   * Orders Controller
   * Manages booking records, delivery status tracking, and inline status updates.
   */
  app.controller('OrdersCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.orders = [];
    $scope.totalOrders = 0;
    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.totalPages = 1;
    $scope.statusFilter = 'ALL';
    $scope.searchQuery = '';
    $scope.loading = false;

    $scope.loadOrders = function (page) {
      $scope.loading = true;
      $scope.currentPage = page || $scope.currentPage;

      var params = {
        page: $scope.currentPage,
        page_size: $scope.pageSize
      };
      if ($scope.statusFilter && $scope.statusFilter !== 'ALL') {
        params.status = $scope.statusFilter;
      }
      if ($scope.searchQuery && $scope.searchQuery.trim() !== '') {
        params.q = $scope.searchQuery.trim();
      }

      $http.get('/api/orders/', { params: params })
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            $scope.orders = response.data.orders;
            $scope.totalOrders = response.data.total_count;
            $scope.totalPages = response.data.num_pages;
          }
          $scope.loading = false;
        }, function (error) {
          $scope.loading = false;
          console.error('Orders fetch error:', error);
        });
    };

    $scope.filterByStatus = function (status) {
      $scope.statusFilter = status;
      $scope.currentPage = 1;
      $scope.loadOrders(1);
    };

    $scope.onSearch = function () {
      $scope.currentPage = 1;
      $scope.loadOrders(1);
    };

    $scope.clearFilter = function () {
      $scope.statusFilter = 'ALL';
      $scope.searchQuery = '';
      $scope.currentPage = 1;
      $scope.loadOrders(1);
    };

    $scope.updateOrderStatus = function (order, newStatus) {
      $http.post('/api/orders/' + order.order_id + '/status/', { status: newStatus })
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            order.delivery_status = newStatus;
            order.delivery_status_display = response.data.order.delivery_status_display;
            $rootScope.$broadcast('notify', {
              message: 'Order #' + order.order_id + ' marked as ' + response.data.order.delivery_status_display,
              type: 'success'
            });
            $rootScope.$broadcast('dataUpdated');
          }
        }, function (error) {
          var msg = (error.data && error.data.message) ? error.data.message : 'Status update failed';
          $rootScope.$broadcast('notify', { message: msg, type: 'danger' });
        });
    };

    $scope.getStatusBadgeClass = function (status) {
      switch (status) {
        case 'BOOKED': return 'badge-status-booked';
        case 'DISPATCHED': return 'badge-status-dispatched';
        case 'OUT_FOR_DELIVERY': return 'badge-status-transit';
        case 'DELIVERED': return 'badge-status-delivered';
        case 'CANCELLED': return 'badge-status-cancelled';
        default: return 'badge-status-booked';
      }
    };

    $rootScope.$on('refreshAll', function () {
      $scope.loadOrders(1);
    });

    $rootScope.$on('dataUpdated', function () {
      $scope.loadOrders($scope.currentPage);
    });

    // Initial load
    $scope.loadOrders(1);
  }]);

  /**
   * Refill Booking Controller
   * High-usability form with consumer auto-lookup, live pricing calculation, and DAC generation.
   */
  app.controller('BookingCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.stocks = [];
    $scope.selectedStock = null;
    $scope.consumerSearchResults = [];
    $scope.verifiedConsumer = null;
    $scope.isSearchingConsumer = false;
    $scope.submitting = false;
    $scope.latestConfirmedBooking = null;

    $scope.form = {
      consumer_query: '',
      consumer_id: '',
      cylinder_type_id: '',
      quantity: 1,
      payment_status: 'CASH_ON_DELIVERY',
      payment_reference: '',
      notes: ''
    };

    $scope.loadStocks = function () {
      $http.get('/api/stock/')
        .then(function (response) {
          if (response.data && response.data.stocks) {
            $scope.stocks = response.data.stocks;
            if ($scope.stocks.length > 0 && !$scope.form.cylinder_type_id) {
              $scope.selectStock($scope.stocks[0]);
            }
          }
        });
    };

    $scope.selectStock = function (stock) {
      $scope.selectedStock = stock;
      $scope.form.cylinder_type_id = stock.id;
    };

    // Live search consumers as staff types ID, phone, or name
    $scope.searchConsumer = function () {
      var query = $scope.form.consumer_query;
      if (!query || query.trim().length < 2) {
        $scope.consumerSearchResults = [];
        return;
      }
      $scope.isSearchingConsumer = true;
      $http.get('/api/consumers/', { params: { q: query.trim(), page_size: 5 } })
        .then(function (response) {
          $scope.isSearchingConsumer = false;
          if (response.data && response.data.consumers) {
            $scope.consumerSearchResults = response.data.consumers;
          }
        }, function () {
          $scope.isSearchingConsumer = false;
        });
    };

    $scope.pickConsumer = function (c) {
      $scope.verifiedConsumer = c;
      $scope.form.consumer_id = c.consumer_id;
      $scope.form.consumer_query = c.consumer_id + ' - ' + c.name + ' (' + c.region + ')';
      $scope.consumerSearchResults = [];

      // Auto pick cylinder type matching connection
      if (c.connection_type_code === 'COMMERCIAL') {
        var comm = $scope.stocks.filter(function (s) { return s.cylinder_type.indexOf('19kg') !== -1; })[0];
        if (comm) $scope.selectStock(comm);
      } else if (c.connection_type_code === 'FTL_5KG') {
        var mini = $scope.stocks.filter(function (s) { return s.cylinder_type.indexOf('5kg') !== -1; })[0];
        if (mini) $scope.selectStock(mini);
      } else {
        var dom = $scope.stocks.filter(function (s) { return s.cylinder_type.indexOf('14.2kg') !== -1; })[0];
        if (dom) $scope.selectStock(dom);
      }
    };

    $scope.clearPickedConsumer = function () {
      $scope.verifiedConsumer = null;
      $scope.form.consumer_id = '';
      $scope.form.consumer_query = '';
      $scope.consumerSearchResults = [];
    };

    // Live calculation methods
    $scope.getUnitPrice = function () {
      return $scope.selectedStock ? $scope.selectedStock.price : 0;
    };

    $scope.getSubtotal = function () {
      var qty = parseInt($scope.form.quantity) || 1;
      return $scope.getUnitPrice() * qty;
    };

    $scope.getSubsidy = function () {
      if (!$scope.selectedStock || !$scope.verifiedConsumer) return 0;
      if ($scope.verifiedConsumer.connection_type_code === 'PMUY_UJJAWALA' || $scope.verifiedConsumer.connection_type_code.indexOf('DOMESTIC') !== -1) {
        return ($scope.selectedStock.subsidy_amount || 0) * (parseInt($scope.form.quantity) || 1);
      }
      return 0;
    };

    $scope.submitBooking = function () {
      if (!$scope.form.consumer_id) {
        $rootScope.$broadcast('notify', { message: 'Please search and select a valid consumer first.', type: 'danger' });
        return;
      }
      if (!$scope.form.cylinder_type_id) {
        $rootScope.$broadcast('notify', { message: 'Please select a cylinder variant.', type: 'danger' });
        return;
      }
      if ($scope.form.quantity <= 0) {
        $rootScope.$broadcast('notify', { message: 'Booking quantity must be at least 1.', type: 'danger' });
        return;
      }

      $scope.submitting = true;
      var payload = {
        consumer_id: $scope.form.consumer_id,
        cylinder_type_id: $scope.form.cylinder_type_id,
        quantity: $scope.form.quantity,
        payment_status: $scope.form.payment_status,
        payment_reference: $scope.form.payment_reference,
        notes: $scope.form.notes
      };

      $http.post('/api/orders/', payload)
        .then(function (response) {
          $scope.submitting = false;
          if (response.data && response.data.status === 'success') {
            $scope.latestConfirmedBooking = response.data.order;
            $rootScope.$broadcast('notify', {
              message: 'Refill Booking Confirmed! DAC Code: ' + response.data.order.delivery_dac,
              type: 'success'
            });
            $rootScope.$broadcast('dataUpdated');
            // Reset form
            $scope.form.quantity = 1;
            $scope.form.notes = '';
            $scope.form.payment_reference = '';
            $scope.clearPickedConsumer();

            // Trigger modal display if Bootstrap is available
            var modalElem = document.getElementById('bookingReceiptModal');
            if (modalElem && window.bootstrap) {
              var modal = new window.bootstrap.Modal(modalElem);
              modal.show();
            }
          }
        }, function (error) {
          $scope.submitting = false;
          var msg = (error.data && error.data.message) ? error.data.message : 'Failed to submit booking. Check stock.';
          $rootScope.$broadcast('notify', { message: msg, type: 'danger' });
        });
    };

    // Listen for preselection from stock cards or consumer table
    $rootScope.$on('preselectCylinder', function (event, stock) {
      $scope.selectStock(stock);
    });

    $rootScope.$on('bookForConsumer', function (event, consumer) {
      $scope.pickConsumer(consumer);
    });

    // Initial stocks load
    $scope.loadStocks();
  }]);

  /**
   * Consumers Controller
   * Search, filter, and pagination across 22,000+ local consumers in Kanpur & Hamirpur.
   */
  app.controller('ConsumersCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.consumers = [];
    $scope.totalCount = 0;
    $scope.currentPage = 1;
    $scope.pageSize = 20;
    $scope.totalPages = 1;
    $scope.searchQuery = '';
    $scope.regionFilter = 'ALL';
    $scope.statusFilter = 'ALL';
    $scope.loading = false;

    $scope.regions = [
      'ALL',
      'Kanpur Nagar',
      'Kanpur Dehat',
      'Hamirpur City',
      'Hamirpur Rural',
      'Ghatampur',
      'Rath',
      'Maudaha',
      'Sumerpur'
    ];

    $scope.loadConsumers = function (page) {
      $scope.loading = true;
      $scope.currentPage = page || $scope.currentPage;

      var params = {
        page: $scope.currentPage,
        page_size: $scope.pageSize
      };
      if ($scope.searchQuery && $scope.searchQuery.trim() !== '') {
        params.q = $scope.searchQuery.trim();
      }
      if ($scope.regionFilter && $scope.regionFilter !== 'ALL') {
        params.region = $scope.regionFilter;
      }
      if ($scope.statusFilter && $scope.statusFilter !== 'ALL') {
        params.status = $scope.statusFilter;
      }

      $http.get('/api/consumers/', { params: params })
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            $scope.consumers = response.data.consumers;
            $scope.totalCount = response.data.total_count;
            $scope.totalPages = response.data.num_pages;
          }
          $scope.loading = false;
        }, function (error) {
          $scope.loading = false;
          console.error('Consumers fetch error:', error);
        });
    };

    $scope.onFilterChange = function () {
      $scope.currentPage = 1;
      $scope.loadConsumers(1);
    };

    $scope.clearFilters = function () {
      $scope.searchQuery = '';
      $scope.regionFilter = 'ALL';
      $scope.statusFilter = 'ALL';
      $scope.currentPage = 1;
      $scope.loadConsumers(1);
    };

    $scope.bookRefill = function (consumer) {
      $rootScope.$broadcast('bookForConsumer', consumer);
      // Switch to booking tab
      var scopeMain = angular.element(document.querySelector('[ng-controller="MainCtrl"]')).scope();
      if (scopeMain) {
        scopeMain.switchTab('booking');
      }
    };

    $rootScope.$on('refreshAll', function () {
      $scope.loadConsumers(1);
    });

    // Initial load
    $scope.loadConsumers(1);
  }]);

  /**
   * Routes & Logistics Controller
   * Monitoring delivery routes, drivers, vehicle numbers, and assigned quantities.
   */
  app.controller('RoutesCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {
    $scope.routes = [];
    $scope.loading = false;
    $scope.selectedRegion = 'ALL';

    $scope.loadRoutes = function () {
      $scope.loading = true;
      var params = {};
      if ($scope.selectedRegion && $scope.selectedRegion !== 'ALL') {
        params.region = $scope.selectedRegion;
      }
      $http.get('/api/routes/', { params: params })
        .then(function (response) {
          if (response.data && response.data.status === 'success') {
            $scope.routes = response.data.routes;
          }
          $scope.loading = false;
        }, function (error) {
          $scope.loading = false;
          console.error('Routes fetch error:', error);
        });
    };

    $scope.getRouteStatusClass = function (status) {
      switch (status) {
        case 'SCHEDULED': return 'badge-status-booked';
        case 'IN_TRANSIT': return 'badge-status-transit';
        case 'COMPLETED': return 'badge-status-delivered';
        default: return 'badge-status-booked';
      }
    };

    $rootScope.$on('refreshAll', function () {
      $scope.loadRoutes();
    });

    $rootScope.$on('dataUpdated', function () {
      $scope.loadRoutes();
    });

    // Initial load
    $scope.loadRoutes();
  }]);

})();
