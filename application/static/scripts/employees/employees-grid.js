import { Grid, h } from "https://unpkg.com/gridjs?module";

document.addEventListener('DOMContentLoaded', () => {

    var username = document.getElementById('employees-grid').getAttribute('data-username');

    const editableCellAttributes = (data, row, col) => {
          if (row) {
            // return {contentEditable: 'true', 'data-element-id': row.cells[0].data};
            return {contentEditable: 'true', 'data-element-id': row.cells[0].data};
          }
          else {
            return {};
          }
      };

    new gridjs.Grid({
        columns: [
            { id: 'id', sort: false, 'hidden': true},
            { id: 'firstName', name: 'First Name', resizable: true,'attributes': editableCellAttributes},
            { id: 'lastName', name: 'Last Name', resizable: true,'attributes': editableCellAttributes},
            { id: 'position', name: 'Position', resizable: true,'attributes': editableCellAttributes},
            { id: 'department', name: 'Department', resizable: true,'attributes': editableCellAttributes},
            { id: 'email', name: 'Email', width: 325,resizable: true,'attributes': editableCellAttributes},
            { id: 'phoneNumber', name: 'Work Phone', resizable: true, width: 160,'attributes': editableCellAttributes},
            { id: 'salary', name: 'Salary', formatter: (cell) => `$${cell}`, width: 120, resizable: true,'attributes': editableCellAttributes},
            { id: 'dateHired', name: 'Date Hired', width: 160, resizable: true,'attributes': editableCellAttributes},
            { id: 'birthday', name: 'Birthday', width: 160, resizable: true,'attributes': editableCellAttributes},
            
            //used to delete rows
            { id: 'delete', name: 'Delete', sort: false, width: 150, formatter: (cell, row) => {
                return h('button', {onClick: () =>{
                  console.log(row.cells[0]);
                  fetch(`/${username}/employees/data`, {
                    method: 'DELETE',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                      id: row.cells[0].data, //row is hidden
                      department: row.cells[4].data
                    }),
                  });
                  location.reload() //refreshes page to display changes
                }}, 'Delete');
                }
            }
        ], 
        server: {
          url: `/${username}/employees/data`,
          method: 'GET',
          then: results => results.data,
          total: results => results.total,
        },
        search: true,
        sort: true,
        pagination: true,
        style: {
            th: {
                'background-color': '#198754',
                'color': 'white',
                'text-align': 'center'
            },
            td: {
            'text-align': 'center'
            }
        }
    }).render(document.getElementById('table'));

    let previousValue;

    table.addEventListener('focusin', ev => {
        if (ev.target.tagName === 'TD') {
          previousValue = ev.target.textContent;
        }
    });

    table.addEventListener('focusout', ev => {
        if (ev.target.tagName === 'TD') {
          if (previousValue !== ev.target.textContent) {
            // console.log(savedValue, ev.target.textContent);
            fetch(`/${username}/employees/data`, {
              method: 'PATCH',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                id: ev.target.dataset.elementId,
                [ev.target.dataset.columnId]: ev.target.textContent,
                previousValue: previousValue
              }),
            });
          }
          previousValue = undefined;
        }
        location.reload() //refreshes page to display changes T
                          //TODO: Update the chart by passing the new data to it rather than reloading
    });

    //I hate this hack so much. Flask-wtf wants to route to the api and leave the page so now I gotta do this
    document.getElementById("submit").addEventListener("click", () =>{
      var firstNameInput = document.getElementById('firstNameInput');
      var lastNameInput = document.getElementById('lastNameInput');
      var emailInput = document.getElementById('emailInput');
      var phoneNumberInput = document.getElementById('phoneNumberInput');
      var salaryInput = document.getElementById('salaryInput');
      var dateHiredInput = document.getElementById('dateHiredInput');
      var birthdayInput = document.getElementById('birthdayInput');
      var positionSelect = document.getElementById('positionSelect');
      var departmentSelect = document.getElementById('departmentSelect');

      fetch(`/${username}/employees/data`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          firstName: firstNameInput.value,
          lastName: lastNameInput.value,
          email: emailInput.value,
          phoneNumber: phoneNumberInput.value,
          salary: salaryInput.value,
          dateHired: dateHiredInput.value,
          birthday: birthdayInput.value,
          position: positionSelect.value,
          department: departmentSelect.value
        }),
      });
  })
});