$(document).ready(function(){
  // При загрузке страницы, запрашиваем все комментарии с сервера и отрисовываем страницу.
  $.ajax({
      url:'/all-comments',
      type:'POST',
      data: 'q=',
      dataType: 'json',
      success: function( json ) {
          $.each(json, function(i, value) {
              value.forEach((element) => {
              	let city = 'Город не указан'
              	if (element[4]) {
                  city = element[4]
              	}
                html = `<br><div class="card" id="comment-${element[0]}">`
	              html += `<div class="card-header">${city}</div>`
	              html += '<div class="card-body">'
	              html += `<h5 class="card-title">${element[1]} ${element[2]}</h5>`
	              html += `<p class="card-text">${element[3]}</p>`
	              html += `<a href="#" class="btn btn-primary" id="${element[0]}" onClick="deleteComment(this.id)">Удалить</a></div>`

                $("#main").append(html)
              })

              
          })
      }
  })

})


function deleteComment(obj) {
  // Функция получает id объекта который ее вызвал и отправляет запрос на сервер для удаления комментария.
  // При успешном выполнении скрывает div с удаленным комментарием.
  let id = obj
  const coment = $('#comment-' + id)
        
  $.ajax({
    url:'/delete-comment',
    type:'POST',
    data: 'comment_id=' + id,
    dataType: 'json',
    success: function( json ) {
      $.each(json, function(i, value) {
        if (value !== 'ok'){
          alert('Что-то пошло не так(:')
        } else {

          $(coment).hide()

        }
      })
    }
  })

}