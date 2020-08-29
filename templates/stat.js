$(document).ready(function(){
  // При загрузке страницы, запрашиваем регионы с сервера и формируем таблицу.
  $.ajax({
      url:'/stat-regions',
      type:'POST',
      data: 'q=',
      dataType: 'json',
      success: function( json ) {
          $.each(json, function(i, value) {
              $i = 1
              value.forEach((element) => {
                $('#region-table > tbody:last-child').append(
                	`<tr>
                	   <th scope="row">${i}</th>
                	     <td><a href="#" id="${element[0]}" onClick="showCity(this.id)">${element[1]}</a></td>
                	     <td>${element[2]}</td>
                	 </tr>
                	`)
                $i++
              })

              
          })
      }
  })


})

 function showCity(obj) {
 	// Функция получает id вызвавшего ее объекта, 
 	// запрашивает все города по id региона с сервера и выводит их в виде таблицы.
        let id=obj;
        const region = $(id);
        const $cityTable = $('#city-table')
        
            $.ajax({
		      url:'/stat-city',
		      type:'POST',
		      data: 'region=' + id,
		      dataType: 'json',
		      success: function( json ) {
		      	// Выводим таблицу с городами региона, предварительно очищаем ее.
		      	  $cityTable.removeClass("d-none")
		      	  let tableHeaderRowCount = 1
				  let table = document.getElementById('city-table')
				  let rowCount = table.rows.length
				  for (var i = tableHeaderRowCount; i < rowCount; i++) {
					table.deleteRow(tableHeaderRowCount)
				  }

		          $.each(json, function(i, value) {
		              $i = 1
		              // Обходим json и отрисовываем табличку на основе полученны данных.
		              value.forEach((element) => {
		                $('#city-table > tbody:last-child').append(
		                	`<tr><th scope="row">${i}</th><td>${element[1]}</td><td>${element[2]}</td></tr>`)
		                $i++
		              })
		          })
		      }
		    })

   }