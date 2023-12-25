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

    fetchData().then(dataPoints => {
      for(let i = 0; i < dataPoints.length; i++){
        empNames.push(dataPoints[i].firstName + dataPoints[i].lastName);
      }
      console.log(empNames);
    });

    new Chart(ctx, {
        type: 'pie',
        data: {
          labels: [
            'Red',
            'Blue',
            'Yellow'
          ],
          datasets: [{
            label: 'My First Dataset',
            data: [300, 50, 100],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)'
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