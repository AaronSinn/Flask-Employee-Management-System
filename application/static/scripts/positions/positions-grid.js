import { Grid, h } from "https://unpkg.com/gridjs?module";

document.addEventListener('DOMContentLoaded', () => {

    var username = document.getElementById('positions-grid').getAttribute('data-username');

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
            { id: 'title', name: 'Title', resizable: true,'attributes': editableCellAttributes},
            { id: 'description', name: 'Description', sort: false, resizable: true,'attributes': editableCellAttributes},
            { id: 'basePay', name: 'Base Pay', formatter: (cell) => `$${cell}`, width: 200,resizable: true,'attributes': editableCellAttributes},
            
            //used to delete rows
            { id: 'delete', name: 'Delete', sort: false, width: 200,formatter: (cell, row) => {
                return h('button', {onClick: () =>{
                  console.log(row.cells[0]);
                  //DELETE
                  fetch(`/${username}/positions/data`, {
                    method: 'DELETE',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                      id: row.cells[0].data
                    }),
                  });
                  location.reload() //refreshes page to display changes
                }}, 'Delete');
                }
            }
        ], 
        //GET
        server: {
          url:`/${username}/positions/data`,
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
            fetch(`/${username}/positions/data`, {
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
          location.reload() //refreshes page to display changes
        }
    });

    //I hate this hack so much. Flask-wtf wants to route to the api and leave the page so now I gotta do this
    //POST
    document.getElementById("submit").addEventListener("click", () =>{
      var titleInput = document.getElementById('titleInput');
      var descriptionInput = document.getElementById('descriptionInput');
      var basePayInput = document.getElementById('basePayInput');

      fetch(`/${username}/positions/data`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          title: titleInput.value,
          description: descriptionInput.value,
          basePay: basePayInput.value
        }),
      });
  })
})