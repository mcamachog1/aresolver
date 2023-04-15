
  document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#fecha-asistencia')) {
      const dt = new Date();
      console.log(dt)
      const dateFormat = dt.getFullYear() + "-" +((dt.getMonth()+1).length != 2 ? "0" + (dt.getMonth() + 1) : (dt.getMonth()+1)) + "-" + (dt.getDate()< 10 ?"0" + dt.getDate() : dt.getDate());
      console.log(dateFormat)
      document.getElementById('fecha-asistencia').value = dateFormat  
    
      const alumnos = document.querySelector('#alumnos');
      alumnos.addEventListener('change', (event) => asistencias_alumno(event.target.value))
      
    }
    
    else if (document.querySelector("#btn-asistencia-manual")){
      const btn_asistencia_manual = document.querySelector("#btn-asistencia-manual")
      const alumno_id = document.querySelector("#alumno-id").value
      console.log(alumno_id)
      btn_asistencia_manual.addEventListener('click', () => asistencias_alumno(alumno_id))
      
    }
    // fetch con get
    function asistencias_alumno(id) {
      console.log(id, "dentro de la funcion")
      // funciones auxiliares
      function addTable() {
          // create a new table element
          const newTable = document.createElement("table");
          newTable.innerHTML = `
            <table>
              <thead>
                <tr>
                  <th scope="col">Nombre</th>
                  <th scope="col">Fecha de asistencia</th>
                  <th scope="col">Tutor</th>
                  <th scope="col">Academia</th>
                  <th scope="col">Acción</th>
                </tr>
              </thead>
              <tbody id='table-body'>
              </tbody>                
            </table>
            `
          newTable.classList.add("table")
          // add the newly created element and its content into the DOM
          // const currentDiv = document.getElementById("titulo");
          document.body.appendChild(newTable)
      }
        
      document.querySelector('table').remove();
      addTable()

      tableBody = document.querySelector('#table-body')
      const ruta = `api/asistencias/${id}`
      console.log(ruta)
      fetch(ruta)
      .then(response => response.json())
      .then(json => {
        json.asistencias.forEach((asistencia) => {
          tableBody.innerHTML += 
          `<tr>
            <td>${ asistencia.nombre }</td>
            <td>${ asistencia.fecha }</td>
            <td>${ asistencia.tutor }</td>
            <td>${ asistencia.academia }</td>
            <td><a href='asistencia_delete/${ asistencia.id }'>Eliminar</a></td>
          </tr>`
        })
      })
    };
  });
