document.addEventListener('DOMContentLoaded', function() {
  var username = document.getElementById('calendar-calendar').getAttribute('data-username');
  var events = [];

  async function fetchData() {
    const response = await fetch(`/${username}/calendar/data`);
    var dataPoints = await response.json();
    return dataPoints.events;
  }

  fetchData().then(dataPoints => {
    for (let i = 0; i < dataPoints.length; i++) {
      events.push(dataPoints[i]);
    }

    console.log('EVENTS',events)

    // Create calendar instance after data is fetched
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      themeSystem: 'bootstrap',
      initialView: 'dayGridMonth',
      eventColor: '#198754',
      selectable: true,
      headerToolbar: {
        start: 'dayGridMonth,timeGridWeek,timeGridDay',
        center: 'title'
      },
      events: events,
      select: function(info) {
        var myModal = new bootstrap.Modal(document.getElementById('createModal'));

        // Sets default start date and time
        startDate = document.getElementById('startDateInput')
        startDate.value = info.startStr
        startTime = document.getElementById('startTimeInput')
        startTime.value ='12:00'

        //Sets the deafult end date and time
        endDate =  document.getElementById('endDateInput')
        endDate.value = info.endStr
        endTime = document.getElementById('endTimeInput')
        endTime.value ='12:00'

        myModal.show();
      },
      eventClick: function(info) {
        var myModal = new bootstrap.Modal(document.getElementById('editModal'));
        var eventObj = info.event;

        console.log(eventObj._def.title)

        // Sets the title
        title = document.getElementById('titleInputEdit')
        title.value = eventObj._def.title

        // Sets the start date and time
        startDate = document.getElementById('startDateInputEdit')
        //startDate.value = info.startStr
        startTime = document.getElementById('startTimeInputEdit')
        startTime.value ='12:00'

        //Sets the end date and time
        endDate =  document.getElementById('endDateInputEdit')
       // endDate.value = info.endStr
        endTime = document.getElementById('endTimeInputEdit')
        endTime.value ='12:00'

        myModal.show();
      }
    });

    // Render the calendar after data is set

    calendar.render();

  });

  document.getElementById('submit').addEventListener('click', () =>{
    var title = document.getElementById('titleInput');
    var startDate = document.getElementById('startDateInput');
    var startTime = document.getElementById('startTimeInput');
    var endDate = document.getElementById('endDateInput');
    var endTime = document.getElementById('endTimeInput');
    var frequency = document.getElementById('frequencySelect');
    
    console.log(startTime.value)

    fetch(`/${username}/calendar/data`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        title: title.value,
        startDate: startDate.value,
        startTime: startTime.value,
        endDate: endDate.value,
        endTime: endTime.value,
        frequency: frequency.value
      }),
    })
  })

});