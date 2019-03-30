odoo.define('avi_planner.dashboard', function (require) {
"use strict";

var core = require('web.core');
var KanbanView = require('web_kanban.KanbanView');
var Model = require('web.Model');
var QWeb = core.qweb

var _t = core._t;
var _lt = core._lt;


var AviDashboardView = KanbanView.extend({
     // Here we are plotting bar,pie chart
    display_name: _lt('Dashboard'),
    icon: 'fa-dashboard text-red',
    searchview_hidden: true,//  To hide the search and filter bar

    init: function (parent, dataset, view_id, options) {
        this._super(parent, dataset, view_id, options);
        this.options.creatable = false;
        var uid = dataset.context.uid;
        var isFirefox = false;
        var self = this;
        //Here we can bind any functions to be called before or after render.
        //_.bindAll(this, 'render', 'graph');
        //var _this = this;
        //this.render = _.wrap(this.render, function(render) {
        //    render();
        //    _this.graph();
        //    return _this;
        //});
    },
    // Here we are calling a function 'get_employee_info' from model to retrieve enough data
    render: function() {
        var super_render = this._super;
        var self = this;
        var avi_dashboard = QWeb.render('avi_planner.dashboard', {
                    widget: self,
                });
                super_render.call(self);
                $(avi_dashboard).prependTo(self.$el);
        self.graph();
    },
      // Function which gives random color for charts.
    getRandomColor: function () {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },
    graph: function() {
        console.log("papaya de celaya----- aqui ando en chinga")
        var self = this
        var ctx = this.$el.find('#Chetos')
        console.log("papaya de celaya----- aqui ando en chinga", ctx)
        // Fills the canvas with white background
        Chart.plugins.register({
          beforeDraw: function(chartInstance) {
            var ctx = chartInstance.chart.ctx;
            ctx.fillStyle = "white";
            ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
          }
        });


        var bg_color_list = []
        for (var i=0;i<=12;i++){
            bg_color_list.push(self.getRandomColor())
        }
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                //labels: ["January","February", "March", "April", "May", "June", "July", "August", "September",
                // "October", "November", "December"],
                labels: ["Africa", "Asia", "Europe", "Latin America", "North America"],
                datasets: [{
                    label: 'Granjas',
                    data: [2478,5267,734,784,433],
                    backgroundColor: bg_color_list,
                    borderColor: bg_color_list,
                    borderWidth: 1,
                    pointBorderColor: 'white',
                    pointBackgroundColor: 'red',
                    pointRadius: 5,
                    pointHoverRadius: 10,
                    pointHitRadius: 30,
                    pointBorderWidth: 2,
                    pointStyle: 'rectRounded'
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            min: 1000,
                            max: 10000,
                          }
                    }]
                },
                responsive: true,
                maintainAspectRatio: true,
                animation: {
                    duration: 100, // general animation time
                },
                hover: {
                    animationDuration: 500, // duration of animations when hovering an item
                },
                responsiveAnimationDuration: 500, // animation duration after a resize
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'black'
                    }
                },
            },
        });
    },      
})
    // View adding to the registry
core.view_registry.add('avi_dashboard_view', AviDashboardView);
return AviDashboardView
});

