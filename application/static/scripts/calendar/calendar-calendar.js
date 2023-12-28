document.addEventListener('DOMContentLoaded', function() {
  var username = document.getElementById('calendar-calendar').getAttribute('data-username');
  var birthdays = [];

  async function fetchData() {
    const response = await fetch(`/${username}/calendar/birthdays`);
    var dataPoints = await response.json();
    console.log(dataPoints);
    return dataPoints.birthdays;
  }

  fetchData().then(dataPoints => {
    for (let i = 0; i < dataPoints.length; i++) {
      birthdays.push(dataPoints[i]);
    }
    console.log('array', birthdays);
    console.log('title', birthdays[1].title);

    // Create calendar instance after data is fetched
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      themeSystem: 'Minty',
      selectable: true,
      headerToolbar: {
        start: 'dayGridMonth,timeGridWeek,timeGridDay',
        center: 'title'
      },
      events: birthdays
    });

    // Render the calendar after data is set
    calendar.render();
  });
});