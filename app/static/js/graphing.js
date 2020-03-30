var canvas = document.getElementById("rackGraph");
var ctx = canvas.getContext("2d");
console.log('instantiated canvas and context');

// with (Chart.defaults.global.datasets.line){
//     steppedLine = true;
//     xAxisID = "Placement Size (mm)";
//     yAxisID = "Qty";
//     pointRadius = 0;
// }

var rack = new Chart(ctx,generateJson());

function generateJson() {
    var json = {
        type: "line",
        data: {
            labels: [],
            datasets: [{data:[],
                fill: true,
                pointRadius:0,
                pointHoverRadius:5,
                borderColor: 'rgba(184, 109, 60, 0.79)',
                backgroundColor: 'rgba(184, 109, 60, 0.5)',
                xAxisID: 'rack',
                steppedLine: true,
                spanGaps: true
            }]
        },
        options: {
            legend: { display: false },
            scales: {
                yAxes: [{
                    //gridLines:{
                    //    color: "black",
                    //    display: false
                //},
                    scaleLabel: {
                        display: true,
                        labelString: "# of Pieces",
                        fontColor: 'rgb(184, 109, 60)',
                    },
                    ticks: {
                        min: 0
                    }
                }],
                xAxes: [{
                    id: 'rack',
                    scaleLabel: {
                        display: true,
                        labelString: "Placement Size (mm)",
                        fontColor: 'rgb(184, 109, 60)',
                    },
                    ticks: {
                        min: 0,
                        suggestedMax: 200,
                        stepSize: 4
                    }
                }]
            }
            // title:{
            //     text:"My Rack",
            //     display:true
            // }
        }
    };
    console.log('in generatejson');
    for (var i = 0; i <= 3500; i++) {
        var zeroes = false;
        var temp = 0;
        for (piece in dataPy) {
            if ((i/10 >= dataPy[piece].lowFitMm) && (i/10 <= dataPy[piece].upFitMm)) {
                temp += qty[dataPy[piece].id];
            }
        }
        json.data.datasets[0].data[i] = temp;
        json.data['labels'].push(i/10);
    }
    console.log(json);
    return json;
}