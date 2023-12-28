document.addEventListener('DOMContentLoaded',function(){
    const ctx = document.getElementById('myChart');
    
    var username = document.getElementById('departments-chart').getAttribute('data-username');

    //creates the list of random colours for the chart
    // var colourList = [];
    // const randomBetween = (min, max) => min + Math.floor(Math.random() * (max - min + 1));
    // for(var i = 0; i < 20; i++){
    //   r = randomBetween(0,50);
    //   g = randomBetween(80,255);
    //   b = randomBetween(60,145);

    //   let colour = `rgb(${r}, ${g}, ${b})`
    //   colourList.push(colour);
    // }
    // console.log(colourList);

    var colourList = ['rgb(8, 124, 88)', 'rgb(2, 104, 95)', 'rgb(43, 227, 89)', 'rgb(14, 187, 116)', 'rgb(36, 172, 88)', 'rgb(26, 133, 143)', 'rgb(26, 206, 117)', 'rgb(32, 245, 143)', 'rgb(29, 112, 79)', 'rgb(14, 85, 144)', 'rgb(25, 84, 106)', 'rgb(9, 184, 126)', 'rgb(24, 188, 106)', 'rgb(35, 96, 82)', 'rgb(39, 207, 65)', 'rgb(34, 138, 90)', 'rgb(39, 87, 98)', 'rgb(26, 190, 79)', 'rgb(33, 171, 89)', 'rgb(43, 182, 62)'];
    async function fetchData(){
      const response = await fetch(`/${username}/departments/data`);
      var dataPoints = await response.json();
      console.log(dataPoints);
      return dataPoints.data
    }

    var departmentTitles = [];
    var empCounts = [];

    fetchData().then(dataPoints => {
      for(let i = 0; i < dataPoints.length; i++){
        departmentTitles.push(dataPoints[i].title);
        empCounts.push(dataPoints[i].employeeCount);
      }
      console.log(departmentTitles);
      console.log(empCounts);
      myChart.update(); //due to the async loading of the data, the chart renders before the data is loaded so I update it here so it renders the data. I hate this hack :(
    });

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: departmentTitles,
          datasets: [{
            label: 'Employee Count',
            data: empCounts,
            backgroundColor: colourList,
            hoverOffset: 4
          }]
        },
        options: {
            scales: {
                y: {
                  ticks: {
                    stepSize: 1, // Set the step size to 1 to display only integer values
                    beginAtZero: true
                  }
                }
            }
        }
    });

});