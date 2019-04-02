odoo.define('avi_planner.dashboard_postura', function (require) {
"use strict";

var core = require('web.core');
var KanbanView = require('web_kanban.KanbanView');
var Model = require('web.Model');
var QWeb = core.qweb

var _t = core._t;
var _lt = core._lt;


var AviDashboardPosturaView = KanbanView.extend({
     // Here we are plotting bar,pie chart
    display_name: _lt('Dashboard Postura'),
    icon: 'fa-dashboard text-red',
    searchview_hidden: true,//  To hide the search and filter bar
    events: {
        'click .info-parvada': 'info_parvada',
        'click .ave-recibida': 'ave_recibida',
        'click .mortalidad-total': 'mortalidad_total',
        'click .kgs-enviados':'kgs_enviados',
    },
    init: function (parent, dataset, view_id, options) {
        this._super(parent, dataset, view_id, options);
        this.options.creatable = false;
        var uid = dataset.context.uid;
        var isFirefox = false;
        var self = this;
        var mortalidad_acum_data = [];
        var mortalidad_data = [];
        var consumo_acum_data = [];
        var consumo_data = [];
        var peso_data = [];
        var uniformidad_data = [];
        var produccion_data = [];

        var granja_id = 0;
        var parvada_id = 0;
    },
    render: function() {
        var super_render = this._super;
        var self = this;
        var avi_dashboard = QWeb.render('avi_planner.dashboard_postura', {
                    widget: self,
                });
                super_render.call(self);
                $(avi_dashboard).prependTo(self.$el);
                self.graph();
                self.graph_mortalidad();
                self.graph_cunsumo_acum();
                self.graph_cunsumo();
                self.graph_peso();
                self.graph_uniformidad();
                self.graph_produccion();

       var model_granjas  = new Model('avi.dashboard').call('get_granjas_postura',[]).then(function(result){
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
      self.granja_id = granja_id;
      self.parvada_id = parvada_id;
      if (granja_id != 'G' && parvada_id != 'P'){
          var model  = new Model('avi.dashboard').call('get_posturas_info',[{'parameters':{'granja_id':granja_id,'parvada_id':parvada_id}}]).then(function(result){
               document.getElementById("ave_recibida").innerHTML = result[0]['ave_recibida'];
               document.getElementById("mortalidad_total").innerHTML = result[0]['mortalidad_total'];
               document.getElementById("mortalidad_porcen_acum").innerHTML=result[0]['mortalidad_porcen_acum'];
               document.getElementById("alimento_enviado").innerHTML = result[0]['alimento_enviado'];
               document.getElementById("alimento_consumido").innerHTML = result[0]['alimento_consumido'];
               document.getElementById("grs_acum_consum_enviados").innerHTML = result[0]['grs_acum_consum_enviados'];
               document.getElementById("grs_acum_consum_servido").innerHTML = result[0]['grs_acum_consum_servido'];

               self.isFirefox = typeof InstallTrigger !== 'undefined';
               self.mortalidad_acum_data = result[0]['mortalidad_acum_info']
               self.mortalidad_data = result[0]['mortalidad_info']
               self.consumo_acum_data = result[0]['consumo_acum_info']
               self.consumo_data = result[0]['consumo_info']
               self.peso_data = result[0]['peso_info']
               self.uniformidad_data = result[0]['uniformidad_info']
               self.produccion_data = result[0]['produccion_info']

               return self.fetch_data().then(function(result){
                    self.graph();
                    self.graph_mortalidad();
                    self.graph_cunsumo_acum();
                    self.graph_cunsumo();
                    self.graph_peso();
                    self.graph_uniformidad();
                    self.graph_produccion();
                })
          });//termina el model
      }//termina el if

       
    },
    ave_recibida: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return this.do_action({
            name: _t("Ave Recibida"),
            type: 'ir.actions.act_window',
            res_model: 'bi.parvada.recepcion',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['granja_id','=',parseInt(self.granja_id,10)], ['parvada_id', '=',parseInt(self.parvada_id,10)]],
            target: 'new'
        })
    },
    mortalidad_total: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return this.do_action({
            name: _t("Mortalidad Total"),
            type: 'ir.actions.act_window',
            res_model: 'bi.parvada.mortalidad',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['granja_id','=',parseInt(self.granja_id,10)], ['parvada_id', '=',parseInt(self.parvada_id,10)]],
            target: 'new'
        })
    },
    kgs_enviados: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return this.do_action({
            name: _t("Kgs Enviados"),
            type: 'ir.actions.act_window',
            res_model: 'bi.registro.alimento',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['granja_id','=',parseInt(self.granja_id,10)], ['parvada_id', '=',parseInt(self.parvada_id,10)]],
            limit: 10000000000,
            target: 'new',
        })
    },
    graph: function() {
        $('#canva_mortalidad_acum').remove(); // this is my <canvas> element
        $('#graph-container-mortalidad-acum').append('<canvas id="canva_mortalidad_acum" height="150px"><canvas>');

        var self = this
        var ctx = this.$el.find('#canva_mortalidad_acum')
        var semanas_edad =[]
        var mortalidad_porcen_acum = []
        var mortalidad_porcen_acum_meta = []
        for (var i = 0; i < _.size(self.mortalidad_acum_data); i++ ) {
           semanas_edad.push(self.mortalidad_acum_data[i]['semena_edad_ave'])
           mortalidad_porcen_acum.push(self.mortalidad_acum_data[i]['mortalidad_porcen_acum'].toFixed(2))
           mortalidad_porcen_acum_meta.push(self.mortalidad_acum_data[i]['mortalidad_porcen_acum_meta'])
        }
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
        var mortalidad_acumulada_real = {
          label: "Real",
          data: mortalidad_porcen_acum,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var mortalidad_acumulada_meta = {
          label: "Meta",
          data: mortalidad_porcen_acum_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var mortalidad = {
          labels: semanas_edad,
          datasets: [mortalidad_acumulada_real,mortalidad_acumulada_meta]
        };
        var chartOptions = {
            title: {
            display: true,
            text: '% Mortalidad Acumulada'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "% Mortalidad Acumulada"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          },
            pan: {
      enabled: true,
      mode: "x",
      speed: 10,
      threshold: 10
    },
    zoom: { sensitivity:0.5, drag: true, enabled: true, mode: 'xy' }
        };
        var myChart = new Chart(ctx, {
            type: 'line',
            //data:mortalidad,
            options: chartOptions,
            responsive: true,
        });
        myChart.config.data = mortalidad;
        myChart.update();
    },//termina grafica de porcentajed de mortalida dacumulada
    graph_mortalidad: function() {
        $('#canva_mortalidad').remove(); // this is my <canvas> element
        $('#graph-container-mortalidad').append('<canvas id="canva_mortalidad" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_mortalidad')
        var semanas_edad =[]
        var mortalidad_porcen = []
        var mortalidad_porcen_meta = []
        for (var i = 0; i < _.size(self.mortalidad_data); i++ ) {
           semanas_edad.push(self.mortalidad_data[i]['semena_edad_ave'])
           mortalidad_porcen.push(self.mortalidad_data[i]['mortalidad_porcen'].toFixed(2))
           mortalidad_porcen_meta.push(self.mortalidad_data[i]['mortalidad_porcen_meta'])
        }
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
        var mortalidad_real = {
          label: "Real",
          data: mortalidad_porcen,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var mortalidad_meta = {
          label: "Meta",
          data: mortalidad_porcen_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var mortalidad_chart = {
          labels: semanas_edad,
          datasets: [mortalidad_real,mortalidad_meta]
        };
        var chartOptionsMortalidad = {
           title: {
            display: true,
            text: '% Mortalidad'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "% Mortalidad"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          },
        };
        var ChartMortalidad = new Chart(ctx, {
            type: 'line',
            data:mortalidad_chart,
            options: chartOptionsMortalidad,
            responsive: true,
        });
    },// termina grafica de mortalidad
    graph_cunsumo_acum: function() {
        $('#canva_consumo_grs_acum').remove(); // this is my <canvas> element
        $('#graph-container-consumo-acum').append('<canvas id="canva_consumo_grs_acum" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_consumo_grs_acum')
        var semanas_edad =[]
        var consumo_acum = []
        var consumo_acum_meta = []
        for (var i = 0; i < _.size(self.consumo_acum_data); i++ ) {
           semanas_edad.push(self.consumo_acum_data[i]['semena_edad_ave'])
           consumo_acum.push(self.consumo_acum_data[i]['consumo_alimento_grs_ave_acum'].toFixed(2))
           consumo_acum_meta.push(self.consumo_acum_data[i]['consumo_alimento_grs_ave_acum_meta'])
        }
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
        var consumo_acum_real = {
          label: "Real",
          data: consumo_acum,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var consumo_acum_meta = {
          label: "Meta",
          data: consumo_acum_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var consumo_acumulado = {
          labels: semanas_edad,
          datasets: [consumo_acum_real,consumo_acum_meta]
        };
        var chartOptions = {
           title: {
            display: true,
            text: '(Grs) Consumo de alimento acumulado por Ave'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "(Grs) Consumo de alimento acumulado por Ave"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        };
        var ChartConsumoAcumulado= new Chart(ctx, {
            type: 'line',
            data:consumo_acumulado,
            options: chartOptions,
            responsive: true,
        });
    },//termina grafica de consumo grs. acumulados
    graph_cunsumo: function() {
        $('#canva_consumo_grs').remove(); // this is my <canvas> element
        $('#graph-container-consumo').append('<canvas id="canva_consumo_grs" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_consumo_grs')
        var semanas_edad =[]
        var consumo = []
        var consumo_meta = []
        for (var i = 0; i < _.size(self.consumo_data); i++ ) {
           semanas_edad.push(self.consumo_data[i]['semena_edad_ave'])
           consumo.push(self.consumo_data[i]['consumo_alimento_grs_ave'].toFixed(2))
           consumo_meta.push(self.consumo_data[i]['consumo_alimento_grs_ave_meta'])
        }
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
        var consumo_real = {
          label: "Real",
          data: consumo,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var consumo_meta = {
          label: "Meta",
          data: consumo_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var consumo_chart = {
          labels: semanas_edad,
          datasets: [consumo_real,consumo_meta]
        };
        var chartOptions = {
           title: {
            display: true,
            text: '(Grs) Consumo de alimento por Ave'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "(Grs) Consumo de alimento por Ave"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        };
        var ChartConsumo= new Chart(ctx, {
            type: 'line',
            data:consumo_chart,
            options: chartOptions,
            responsive: true,
        });
    },//termina grafica de consumo grs. ave
    graph_peso: function() {
        $('#canva_peso').remove(); // this is my <canvas> element
        $('#graph-container-peso').append('<canvas id="canva_peso" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_peso')
        var semanas_edad =[]
        var peso = []
        var peso_meta = []
        for (var i = 0; i < _.size(self.peso_data); i++ ) {
           semanas_edad.push(self.peso_data[i]['semena_edad_ave'])
           peso.push(self.peso_data[i]['peso_real'].toFixed(2))
           peso_meta.push(self.peso_data[i]['peso_meta'])
        }
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
        var peso_real_chart = {
          label: "Real",
          data: peso,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var peso_meta_chart = {
          label: "Meta",
          data: peso_meta,
          borderColor: "#3e95cd",
          backgroundColor: "#3e95cd",
          fill:false,
        };
        var peso_chart = {
          labels: semanas_edad,
          datasets: [peso_real_chart,peso_meta_chart]
        };
        var chartOptions = {
           title: {
            display: true,
            text: '(Grs) Peso del Ave'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "(Grs) Peso del ave"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          }
        };
        var ChartPeso= new Chart(ctx, {
            type: 'line',
            data:peso_chart,
            options: chartOptions,
            responsive: true,
        });
    },//termina grafica de peso
    graph_uniformidad: function() {
        $('#canva_uniformidad').remove(); // this is my <canvas> element
        $('#graph-container-uniformidad').append('<canvas id="canva_uniformidad" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_uniformidad')
        var semanas_edad =[]
        var uniformidad_real = []
        var uniformidad_meta = []
        for (var i = 0; i < _.size(self.uniformidad_data); i++ ) {
           semanas_edad.push(self.uniformidad_data[i]['semena_edad_ave'])
           uniformidad_real.push(self.uniformidad_data[i]['uniformidad_real'].toFixed(2))
           uniformidad_meta.push(self.uniformidad_data[i]['uniformidad_meta'])
        }
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
        var uniformidad_real_chart = {
          label: "Real",
          data: uniformidad_real,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var uniformidad_meta_chart = {
          label: "Meta",
          data: uniformidad_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var uniformidad_chart = {
          labels: semanas_edad,
          datasets: [uniformidad_real_chart,uniformidad_meta_chart]
        };
        var chartOptions = {
           title: {
            display: true,
            text: '% Uniformidad'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "% Uniformidad"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          },
           zoom: {
            // Boolean to enable zooming
                enabled: true,

                // Zooming directions. Remove the appropriate direction to disable
                // Eg. 'y' would only allow zooming in the y direction
                mode: 'xy',
            }
        };
        var ChartUniformidad= new Chart(ctx, {
            type: 'line',
            data:uniformidad_chart,
            options: chartOptions,
            responsive: true,
        });
    },//termina grafica de uniformidad
    graph_produccion: function() {
        $('#canva_produccion').remove(); // this is my <canvas> element
        $('#graph-container-produccion').append('<canvas id="canva_produccion" height="150px"><canvas>');
        var self = this
        var ctx = this.$el.find('#canva_produccion')
        var semanas_edad =[]
        var produccion_real = []
        var produccion_meta = []
        console.log(self.produccion_data)
        for (var i = 0; i < _.size(self.produccion_data); i++ ) {
           semanas_edad.push(self.produccion_data[i]['semena_edad_ave'])
           produccion_real.push(self.produccion_data[i]['produccion_real'].toFixed(2))
           produccion_meta.push(self.produccion_data[i]['produccion_meta'])
        }
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
        var produccion_real_chart = {
          label: "Real",
          data: produccion_real,
          borderColor: "#c45850",
          backgroundColor:"#c45850",
          fill:false,
        };
        var produccion_meta_chart = {
          label: "Meta",
          data: produccion_meta,
          borderColor: "#3e95cd",
          backgroundColor:"#3e95cd",
          fill:false,
        };
        var produccion_chart = {
          labels: semanas_edad,
          datasets: [produccion_real_chart,produccion_meta_chart]
        };
        var chartOptions = {
           title: {
            display: true,
            text: '% Produccion'
          },
          scales: {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "% Produccion"
                  }
                }],
                xAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: "Edad del Ave (Semanas)"
                  }
                }]
            },
          legend: {
            display: true,
            position: 'top',
            labels: {
              boxWidth: 80,
              fontColor: 'black'
            }
          },
           zoom: {
            // Boolean to enable zooming
                enabled: true,

                // Zooming directions. Remove the appropriate direction to disable
                // Eg. 'y' would only allow zooming in the y direction
                mode: 'xy',
            }
        };
        var ChartProduccion= new Chart(ctx, {
            type: 'line',
            data:produccion_chart,
            options: chartOptions,
            responsive: true,
        });
    },//termina grafica de produccion
})
    // View adding to the registry
core.view_registry.add('avi_dashboard_postura_view', AviDashboardPosturaView);
return AviDashboardPosturaView
});

