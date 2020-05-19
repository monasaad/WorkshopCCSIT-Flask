// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Doughnut Chart - Application Category
var AppCate = document.getElementById("myDoughChart-AppCate");
var myDoughChartAppCate = new Chart(AppCate, {
  type: 'doughnut',
  data: {
    labels: ["Core", "Service", "Compliance"],
    datasets: [{
      data: [26, 40, 30],
      backgroundColor: ['#3F7FBF', "#3FBFBF", "#3FBF7F"],
      hoverBackgroundColor: ['#3F7FBF', "#3FBFBF", "#3FBF7F"],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 60,
  },
});

// Pie Chart - Heavey Used Systems - here
var Heavey = document.getElementById("myPieChart-Heavey");
var MypieChartHeavey = new Chart(Heavey, {
  type: 'pie',
  data: {
    labels: ["system 1", "system 2", "system 3","system 4","system 5"],
    datasets: [{
      data: [26, 40, 30, 15, 10],
      backgroundColor: ["#3FBF3F", "#3FBF7F", "#3FBFBF", '#3F7FBF', '#3F3FBF'],
      hoverBackgroundColor: ["#3FBF3F", "#3FBF7F", "#3FBFBF", '#3F7FBF', '#3F3FBF'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 0,
  },
});
