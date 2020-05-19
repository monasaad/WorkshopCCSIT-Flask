// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Bar Chart - Frequent usage by category

var stacked = document.getElementById('MyBarChart-Freq').getContext("2d");

var data = {
    labels: ['Core','Service','Compliance'],
      datasets: [
  {label: 'Daily',
    data: [67,50,30],
    backgroundColor: "#3FBF3F",
   borderColor:"#3FBF3F"
  },
  {label: 'Weekly',
    data: [25,21,13],
    backgroundColor: "#3FBF7F",
   borderColor:"#3FBF7F"
  },
  {label: 'Monthly',
    data: [15,45,21],
    backgroundColor: "#3FBFBF", 
   borderColor:"#3FBFBF"
  },
  {label: 'Querterly',
    data: [19,45,21],
    backgroundColor: '#3F7FBF', 
   borderColor:'#3F7FBF'
  },
  {label: 'Yearly',
    data: [20,45,21],
    backgroundColor: '#3F3FBF', 
   borderColor:'#3F3FBF'
  }
]
    
};
var mybarChart = new Chart(stacked, {
  type: 'bar',
  data: data,
  options: {
      legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
  scales: {
    xAxes: [{barPercentage:0.5, stacked: true, ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{ stacked: true, ticks: {
          beginAtZero: true
        }
 }]
  }
}
});



// Line Chart - Release Date and platform
new Chart(document.getElementById("MyLineChart-platform"), {
  type: 'line',
  data: {
    labels: [2015,2016,2017,2018],
    datasets: [{ 
        data: [30,14,20,5],
        label: "SAP",
        backgroundColor:'#3F3FBF',
        borderColor: '#3F3FBF',
        fill: false
      }, { 
        data: [10,15,10,20],
        label: "Web App",
        backgroundColor: '#3F7FBF',
          borderColor: '#3F7FBF',
        fill: false
      }, { 
        data: [17,8,19,25],
        label: "Cloud",
        backgroundColor: "#3FBFBF",
          borderColor:"#3FBFBF",
        fill: false
      }, { 
        data: [34,12,7,18],
        label: "Mobile App",
         backgroundColor: "#3FBF7F",
        borderColor: "#3FBF7F",
        fill: false
      }
    ]},
  options: {
    
    legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
  }}
});


// Horizintal bar chart - HR Strategy
var hor = document.getElementById("myBarChart-HRstr");
var myHorBarChart = new Chart(hor, {
    type: 'horizontalBar',

    data: {
        
      datasets: [
        {
            label:'Talent Acquisition',
          backgroundColor: ['#3F3FBF'],
          data: [17],
        }, {
            label:'Talent Development',
          backgroundColor: ['#3F7FBF'],
          data: [20],
        }, {
            label:'Talent Retention',
          backgroundColor: ["#3FBFBF"],
          data: [30],
        }, {
            label:'Agility',
          backgroundColor: ["#3FBF7F"],
          data: [10],
        }
      ]
    },
    options: {
         legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
  },scales: {
    xAxes: [{ ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{
        
        scaleLabel: {
        display: true,
        labelString: 'Applications'
      }
 }]
  }
    }
});





// Vertical bar chart - Proponent
new Chart(document.getElementById("myVarBarChart-Pro"), {
    type: 'bar',
    data: {
      datasets: [
        {
            label:'HRSSD',
          backgroundColor: ['#3F3FBF'],
          data: [17],
        }, {
            label:'HR',
          backgroundColor: ['#3F7FBF'],
          data: [23],
        }, {
            label:'Personnel',
          backgroundColor: ["#3FBFBF"],
          data: [30],
        }, {
            label:'M&PDD',
          backgroundColor: ["#3FBF7F"],
          data: [10],
        }, {
            label:'OCD',
          backgroundColor: ["#3FBF3F"],
          data: [9],
        }, {
            label:'SSD',
          backgroundColor: ['#7FBF3F'],
          data: [14],
        }
      ]
    },
    options: {
      legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
  },scales: {
    xAxes: [{
        scaleLabel: {
        display: true,
        labelString: 'Proponent'
      }
        
        
        
       
 }],
    yAxes: [{
         ticks: {
          beginAtZero: true
        }
 }]
  }
    }
});




// Horizintal bar chart - Integration IN1 - top
var IntIN1 = document.getElementById("myBarChart-IntIN1");
var myHorBarChartIN1 = new Chart(IntIN1, {
    type: 'horizontalBar',

    data: {
        
      datasets: [
        {
            label:'App1',
          backgroundColor: ['#3F3FBF'],
          data: [100],
        }, {
            label:'App2',
          backgroundColor: ['#3F7FBF'],
          data: [90],
        }, {
            label:'App3',
          backgroundColor: ["#3FBFBF"],
          data: [80],
        }, {
            label:'App4',
          backgroundColor: ["#3FBF7F"],
          data: [70],
        }, {
            label:'App5',
          backgroundColor: ["#3FBF3F"],
          data: [60],
        }, {
            label:'App6',
          backgroundColor: ['#3F3FBF'],
          data: [40],
        }, {
            label:'App7',
          backgroundColor: ['#3F7FBF'],
          data: [30],
        }, {
            label:'App8',
          backgroundColor: ["#3FBFBF"],
          data: [20],
        }, {
            label:'App9',
          backgroundColor: ["#3FBF7F"],
          data: [10],
        }, {
            label:'App10',
          backgroundColor: ["#3FBF3F"],
          data: [5],
        }
      ]
    },
    options: {
         legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 3,
        right: 3,
        top: 3,
        bottom: 0
      }
  },scales: {
    xAxes: [{ ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{
        
        scaleLabel: {
        display: true,
        labelString: 'No. of Applications'
      }
 }]
  }
    }
});


// Horizintal bar chart - Integration IN2 - bottom
var IntIN2 = document.getElementById("myBarChart-IntIN2");
var myHorBarChartIN2 = new Chart(IntIN2, {
    type: 'horizontalBar',

    data: {
        
      datasets: [
        {
            label:'App1',
          backgroundColor: ['#3F3FBF'],
          data: [5],
        }, {
            label:'App2',
          backgroundColor: ['#3F7FBF'],
          data: [10],
        }, {
            label:'App3',
          backgroundColor: ["#3FBFBF"],
          data: [20],
        }, {
            label:'App4',
          backgroundColor: ["#3FBF7F"],
          data: [30],
        }, {
            label:'App5',
          backgroundColor: ["#3FBF3F"],
          data: [40],
        }, {
            label:'App6',
          backgroundColor: ['#3F3FBF'],
          data: [50],
        }, {
            label:'App7',
          backgroundColor: ['#3F7FBF'],
          data: [60],
        }, {
            label:'App8',
          backgroundColor: ["#3FBFBF"],
          data: [70],
        }, {
            label:'App9',
          backgroundColor: ["#3FBF7F"],
          data: [80],
        }, {
            label:'App10',
          backgroundColor: ["#3FBF3F"],
          data: [90],
        }
      ]
    },
    options: {
         legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 3,
        right: 3,
        top: 3,
        bottom: 0
      }
  },scales: {
    xAxes: [{ ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{
        
        scaleLabel: {
        display: true,
        labelString: 'No. of Applications'
      }
 }]
  }
    }
});




// Horizintal bar chart - Integration OUT1 - top
var Out1 = document.getElementById("myBarChart-Out1");
var myHorBarChartOut1 = new Chart(Out1, {
    type: 'horizontalBar',

    data: {
        
      datasets: [
       {
            label:'App1',
          backgroundColor: ['#3F3FBF'],
          data: [100],
        }, {
            label:'App2',
          backgroundColor: ['#3F7FBF'],
          data: [90],
        }, {
            label:'App3',
          backgroundColor: ["#3FBFBF"],
          data: [80],
        }, {
            label:'App4',
          backgroundColor: ["#3FBF7F"],
          data: [70],
        }, {
            label:'App5',
          backgroundColor: ["#3FBF3F"],
          data: [60],
        }, {
            label:'App6',
          backgroundColor: ['#3F3FBF'],
          data: [40],
        }, {
            label:'App7',
          backgroundColor: ['#3F7FBF'],
          data: [30],
        }, {
            label:'App8',
          backgroundColor: ["#3FBFBF"],
          data: [20],
        }, {
            label:'App9',
          backgroundColor: ["#3FBF7F"],
          data: [10],
        }, {
            label:'App10',
          backgroundColor: ["#3FBF3F"],
          data: [5],
        }
      ]
    },
    options: {
         legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 3,
        right: 3,
        top: 3,
        bottom: 0
      }
  },scales: {
    xAxes: [{ ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{
        
        scaleLabel: {
        display: true,
        labelString: 'No. of Applications'
      }
 }]
  }
    }
});


// Horizintal bar chart - Integration IN2 - bottom
var Out2 = document.getElementById("myBarChart-Out2");
var myHorBarChartOut2 = new Chart(Out2, {
    type: 'horizontalBar',

    data: {
        
      datasets: [
        {
            label:'App1',
          backgroundColor: ['#3F3FBF'],
          data: [5],
        }, {
            label:'App2',
          backgroundColor: ['#3F7FBF'],
          data: [10],
        }, {
            label:'App3',
          backgroundColor: ["#3FBFBF"],
          data: [20],
        }, {
            label:'App4',
          backgroundColor: ["#3FBF7F"],
          data: [30],
        }, {
            label:'App5',
          backgroundColor: ["#3FBF3F"],
          data: [40],
        }, {
            label:'App6',
          backgroundColor: ['#3F3FBF'],
          data: [50],
        }, {
            label:'App7',
          backgroundColor: ['#3F7FBF'],
          data: [60],
        }, {
            label:'App8',
          backgroundColor: ["#3FBFBF"],
          data: [70],
        }, {
            label:'App9',
          backgroundColor: ["#3FBF7F"],
          data: [80],
        }, {
            label:'App10',
          backgroundColor: ["#3FBF3F"],
          data: [90],
        }
      ]
    },
    options: {
         legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 3,
        right: 3,
        top: 3,
        bottom: 0
      }
  },scales: {
    xAxes: [{ ticks: {
          beginAtZero: true
        }
 }],
    yAxes: [{
        
        scaleLabel: {
        display: true,
        labelString: 'No. of Applications'
      }
 }]
  }
    }
});


// Bar Chart multiple axis - user group
var barChartData = {
  labels: [
    "Group A",
    "Group B",
    "Group C"
  ],
  datasets: [
    {
      label: "Core",
      backgroundColor: '#3F7FBF',
      borderColor: '#3F7FBF',
      borderWidth: 1,
      data: [3, 5, 6]
    },
    {
      label: "Service",
      backgroundColor: "#3FBFBF",
      borderColor: "#3FBFBF",
      borderWidth: 1,
      data: [4, 7, 3]
    },
    {
      label: "Compliance",
      backgroundColor: "#3FBF7F",
      borderColor:"#3FBF7F",
      borderWidth: 1,
      data: [10,9,2]
    }
  ]
};

var chartOptions = {
    
     legend: {
                  position: 'bottom',
                  display: true
              },
      maintainAspectRatio: false,
    layout: {
      padding: {
        left: 40,
        right: 40,
        top: 25,
        bottom: 0
      }
  },  scales: {
      
        xAxes: [{
            barPercentage: 0.5
        }],
      
    yAxes: [{
      ticks: {
        beginAtZero: true
      }
    }]
  }
}

window.onload = function() {
  var UserGroupBarChart = document.getElementById("BarChartUserGroup").getContext("2d");
  window.myBar = new Chart(UserGroupBarChart, {
    type: "bar",
    data: barChartData,
    options: chartOptions
  });
};

