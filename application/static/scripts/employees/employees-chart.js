document.addEventListener('DOMContentLoaded',function(){
    const ctx = document.getElementById('myChart');
    
    var username = document.getElementById('employees-chart').getAttribute('data-username');

    async function fetchData(){
      const response = await fetch(`/${username}/employees/data`);
      var dataPoints = await response.json();
      console.log(dataPoints);
      return dataPoints.data
    }

    var empNames = [];
    var salaries = [];

    fetchData().then(dataPoints => {
      for(let i = 0; i < dataPoints.length; i++){
        empNames.push(dataPoints[i].firstName + " " + dataPoints[i].lastName);
        salaries.push(dataPoints[i].salary);
      }
      // console.log(empNames);
      // console.log(salaries);
      myChart.update(); //due to the async loading of the data, the chart renders before the data is loaded so I update it here so it renders the data. I hate this hack :(
    });

    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: empNames,
          datasets: [{
            label: 'Salary',
            data: salaries,
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