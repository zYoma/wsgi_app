//Взаимодействие с сервером по AJAX без использования библиотеки jQwery

function sendRequest(method, url, body = null) {
    return new Promise( (resolve, reject) => {
      const xhr = new XMLHttpRequest()
      xhr.open(method, url)
      xhr.responseType = 'json'
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
      xhr.onload = () => {
        if (xhr.status >= 400) {
          reject(xhr.response)
        } else {
          resolve(xhr.response)
        }
      }
      xhr.onerror = () => {
        reject(xhr.response)
      }
      xhr.send(body)
    })
  }


document.addEventListener("DOMContentLoaded", function(event){
  // При загрузке страницы, запрашиваем все комментарии с сервера и отрисовываем страницу.

  const requestURL = '/all-comments'
  const body = null
  sendRequest('POST', requestURL, body)
    .then(data => {
      const commentList = data['result']
      commentList.forEach((element) => {
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
      let new_elem = document.createElement('div')
      new_elem.innerHTML = html
      document.querySelector('#main').appendChild(new_elem)
    })

  })
  .catch(err => console.log(err))

})


function deleteComment(obj) {
  // Функция получает id объекта который ее вызвал и отправляет запрос на сервер для удаления комментария.
  // При успешном выполнении скрывает div с удаленным комментарием.
  let id = obj
  const coment = document.querySelector('#comment-' + id)
  const requestURL = '/delete-comment'
  const body = 'comment_id=' + id
  sendRequest('POST', requestURL, body)
    .then(data => {
      const result = data['result']
      if (result !== 'ok'){
        alert('Что-то пошло не так(:')
      } else {
        coment.style.display = 'none'
      }

    })
  .catch(err => console.log(err))

}