function singleNumberToDouble(minute){
  //input = 2
  //output = 02
  if(String(minute).length === 1){
    return '0' + minute
  }
  return minute
}

function singleHourToDouble(hour){
  //input = 2
  //output = 02

  if(hour >= 20){
    switch(hour){
      case 20:
        hour = 1
        break;
      case 21:
        hour = 2;
        break;
      case 22:
        hour = 3;
        break;
      case 23:
        hour = 4
        break;
      case 24:
        hour = 5
        break;
      default:
        break;
    }
    return '0' + hour
  }

  if(hour <= 4){
    return '0' + (hour +5)
  }
  return hour + 5
}

//returns the correct month in the correct format
function gerProperMonth(month){
  if(month <= 8){
    return '0' + (month + 1)
  }
  else{
    return + month + 1
  }
}

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
      themeSystem: 'bootstrap5',
      initialView: 'dayGridMonth',
      eventColor: '#198754',
      timeZone: 'America/Toronto',
      
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
        endTime.value ='13:00'

        myModal.show();
      },

      eventClick: function(info) {
        var myModal = new bootstrap.Modal(document.getElementById('editModal'));
        var eventObj = info.event;
        eventId = eventObj._def.publicId

        console.log(eventObj)
        // Sets the ID. It will be the same one as stored in the DB
        eventId = eventObj._def.publicId

        // Sets the title
        title = document.getElementById('titleInputEdit')
        title.value = eventObj._def.title

        // Sets the start date and time
        startDate = document.getElementById('startDateInputEdit')
        startDate.value = eventObj._instance.range.start.getFullYear() + '-' + gerProperMonth(eventObj._instance.range.start.getMonth()) + '-' + singleNumberToDouble(eventObj._instance.range.start.getDate()) 
        console.log(eventObj._instance.range.start.getFullYear() + '-' + (eventObj._instance.range.start.getMonth() + 1) + '-' + singleNumberToDouble(eventObj._instance.range.start.getDate()))
        startTime = document.getElementById('startTimeInputEdit')
        startTime.value = (singleHourToDouble(eventObj._instance.range.start.getHours())) + ':' + singleNumberToDouble(eventObj._instance.range.start.getMinutes()) // You haft to add 5 to the hour to get the correct time

        //Sets the end date and time
        endDate =  document.getElementById('endDateInputEdit')
        endDate.value = eventObj._instance.range.end.getFullYear() + '-' + gerProperMonth(eventObj._instance.range.end.getMonth()) + '-' + singleNumberToDouble(eventObj._instance.range.end.getDate())
        endTime = document.getElementById('endTimeInputEdit')
        endTime.value =(singleHourToDouble(eventObj._instance.range.end.getHours())) + ':' + singleNumberToDouble(eventObj._instance.range.end.getMinutes()) // You haft to add 5 to the hour to get the correct time

        myModal.show();
      }
    });

    // Render the calendar after data is set
    calendar.render();
  });

  //this is used to send the id of an event in a PUT or DELETE request
  var eventId;

  // for the create modal, POST requests
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

  // for the edit modal, PUT request
  document.getElementById('submitEdit').addEventListener('click', () =>{
    var title = document.getElementById('titleInputEdit');
    var startDate = document.getElementById('startDateInputEdit');
    var startTime = document.getElementById('startTimeInputEdit');
    var endDate = document.getElementById('endDateInputEdit');
    var endTime = document.getElementById('endTimeInputEdit');
    var frequency = document.getElementById('frequencySelectEdit');

    fetch(`/${username}/calendar/data`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        id: eventId,
        title: title.value,
        startDate: startDate.value,
        startTime: startTime.value,
        endDate: endDate.value,
        endTime: endTime.value,
        frequency: frequency.value
      }),
    })
  })

   // for the edit modal, DELETE request
   document.getElementById('deleteButton').addEventListener('click', () =>{
    fetch(`/${username}/calendar/data`, {
      method: 'DELETE',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        id: eventId,
      }),
    })
    location.reload() //refreshes page to display changes
  })

});