document.addEventListener('DOMContentLoaded', () =>{
    const ctx = document.getElementById('myChart');
    
    var username = document.getElementById('positions-chart').getAttribute('data-username');

    async function fetchData(){
      const response = await fetch(`/${username}/positions/data`);
      var dataPoints = await response.json();
      console.log(dataPoints);
      return dataPoints.data
    }

    var empTitles = [];
    var basePays = [];

    fetchData().then(dataPoints => {
      for(let i = 0; i < dataPoints.length; i++){
        empTitles.push(dataPoints[i].title);
        basePays.push(dataPoints[i].basePay);
      }
      console.log(empTitles);
      console.log(basePays);
      myChart.update(); //due to the async loading of the data, the chart renders before the data is loaded so I update it here so it renders the data. I hate this hack :(
    });

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: empTitles,
          datasets: [{
            label: 'Base Pay',
            data: basePays,
            backgroundColor: [
              'rgb(25, 135, 84)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(155, 202, 36)'
            ],
            hoverOffset: 4
          }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
});