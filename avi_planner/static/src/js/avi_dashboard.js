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
    events: {
        'click .info-parvada': 'info_parvada',
    },
    init: function (parent, dataset, view_id, options) {
        this._super(parent, dataset, view_id, options);
        this.options.creatable = false;
        var uid = dataset.context.uid;
        var isFirefox = false;
        var self = this;
        var mortalidad_acum_data = [];
    },
    render: function() {
        var super_render = this._super;
        var self = this;
        var avi_dashboard = QWeb.render('avi_planner.dashboard', {
                    widget: self,
                });
                super_render.call(self);
                $(avi_dashboard).prependTo(self.$el);
                self.graph();

       var model_granjas  = new Model('avi.dashboard').call('get_granjas',[]).then(function(result){
            for (var i = 0; i < result.length; i++) {
                var opt = document.createElement('option');
                opt.appendChild(document.createTextNode(result[i]['name']));
                opt.value = result[i]['id'];
                document.getElementById("granjas").appendChild(opt);
             }
        });
        var model_parvadas  = new Model('avi.dashboard').call('get_parvadas',[]).then(function(result){
            for (var i = 0; i < result.length; i++) {
                var opt = document.createElement('option');
                opt.appendChild(document.createTextNode(result[i]['name']));
                opt.value = result[i]['id'];
                document.getElementById("parvadas").appendChild(opt);
             }
        });

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
    fetch_data: function() {
		// Overwrite this function with useful data
		return $.when();
	},
    info_parvada: function(){
      var self = this;
      var granja_id = document.getElementById("granjas").value;
      var parvada_id = document.getElementById("parvadas").value;
      if (granja_id != 'G' && parvada_id != 'P'){
          var model  = new Model('avi.dashboard').call('get_granjas_info',[{'parameters':{'granja_id':granja_id,'parvada_id':parvada_id}}]).then(function(result){
               document.getElementById("ave_recibida").innerHTML = result[0]['ave_recibida'];
               document.getElementById("ave_enviada").innerHTML = result[0]['ave_enviada'];
               document.getElementById("mortalidad_total").innerHTML = result[0]['mortalidad_total'];
               document.getElementById("mortalidad_porcen_acum").innerHTML = result[0]['mortalidad_porcen_acum'];
               document.getElementById("diff_aves").innerHTML = result[0]['diff_aves'];
               document.getElementById("mortalidad_al_cierre").innerHTML = result[0]['mortalidad_al_cierre'];
               document.getElementById("alimento_enviado").innerHTML = result[0]['alimento_enviado'];
               document.getElementById("alimento_consumido").innerHTML = result[0]['alimento_consumido'];
               document.getElementById("grs_acum_consum_enviados").innerHTML = result[0]['grs_acum_consum_enviados'];
               document.getElementById("grs_acum_consum_servido").innerHTML = result[0]['grs_acum_consum_servido'];
               self.isFirefox = typeof InstallTrigger !== 'undefined';
               self.mortalidad_acum_data = result[0]['mortalidad_acum_info']
               return self.fetch_data().then(function(result){
                    self.graph();
                })


          });//termina el model
      }//termina el if

       
    },
    graph: function() {
        var self = this
        var ctx = this.$el.find('#Chetos')
        var semanas_edad =[]
        var mortalidad_porcen_acum = []
        var mortalidad_porcen_acum_meta = []
        for (var i = 0; i < _.size(self.mortalidad_acum_data); i++ ) {
           semanas_edad.push(self.mortalidad_acum_data[i]['semena_edad_ave'])
           mortalidad_porcen_acum.push(self.mortalidad_acum_data[i]['mortalidad_porcen_acum'])
           mortalidad_porcen_acum_meta.push(self.mortalidad_acum_data[i]['mortalidad_porcen_acum_meta'])
        }
        console.log('consumo',mortalidad_porcen_acum)
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
        var dataFirst = {
          label: "% Mortalidad Acum Real",
          data: mortalidad_porcen_acum,
        };
        var dataSecond = {
          label: "% Mortalidad Acum Meta",
          data: mortalidad_porcen_acum_meta,
        };
        var speedData = {
          labels: semanas_edad,
          datasets: [mortalidad_porcen_acum, mortalidad_porcen_acum_meta]
        };
        var chartOptions = {
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        };
        var myChart = new Chart(ctx, {
            type: 'line',
            data:speedData,
            options: chartOptions,
            responsive: true,
        });
    },      
})
    // View adding to the registry
core.view_registry.add('avi_dashboard_view', AviDashboardView);
return AviDashboardView
});

