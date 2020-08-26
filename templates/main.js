$(document).ready(function(){
 
  function validateEmail(value) {
    // Функция валидирует email. Сопостовляет с регулярным выражением.
    if (value == ''){
      return true
    } else {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(value);
    }
  }


  function validateTel(value) {
    //Валидация номера телефона
    if (value == ''){
      return true
    } else {
    const re = /^[\+]?\d{2,}?[(]?\d{2,}[)]?[-\s\.]?\d{2,}?[-\s\.]?\d{2,}[-\s\.]?\d{0,9}$/im;
    return re.test(value);
    }
  }


  function validateRequiredField(value) {
    // Проверяем что заполнены обязательные поля.
    if (value == ''){
      return false
    } else {
      return true
    }
  }


  function validate() {
    // Основная функция валидатор. Запускается при клике по кнопке Отправить.
    // Поочередно вызывает несколько валидаторов и если все проверки прошли, отправляет форму.
    const form = document.getElementById("form-comment");
    const $result = $("#result");
    const $email = $("#email");
    const $tel = $("#tel");
    const $firstName = $("#first_name");
    const $lastName = $("#last_name");
    const $text = $("#text");
    const emailValue = $("#email").val();
    const telValue = $("#tel").val();
    const firstNameValue = $("#first_name").val();
    const lastNameValue = $("#last_name").val();
    const textValue = $("#text").val();
    let counter = 0;



    if (!validateEmail(emailValue)) {
      $email.css("border-color", "red");
      counter = 1;
    } else {
      if (emailValue != '') {
        $email.css("border-color", "green");
      }
    }

    if (!validateTel(telValue)) {
      $tel.css("border-color", "red");
      counter = 1;
    }  else { 
      if (telValue != '') {
        $tel.css("border-color", "green");
      }
    }

    if (!validateRequiredField(textValue)) {
      $text.css("border-color", "red");
      counter = 1;
    } else {
      $text.css("border-color", "green");
    }

    if (!validateRequiredField(firstNameValue)) {
      $firstName.css("border-color", "red");
      counter = 1;
    } else {
      $firstName.css("border-color", "green");
    }

    if (!validateRequiredField(lastNameValue)) {
      $lastName.css("border-color", "red");
      counter = 1;
    } else {
      $lastName.css("border-color", "green");
    }

    if (counter == 0) {
      form.submit();
    } else {
      $result.removeClass("d-none");
    }

    return false;
  }

  $("#validate").on("click", validate);


  // При загрузке страницы, получает от сервера список регионов и формирует селект.
  $.ajax({
      url:'/regions',
      type:'POST',
      data: 'q=',
      dataType: 'json',
      success: function( json ) {
          $.each(json, function(i, value) {

              value.forEach((element) => {
                $('#region').append($('<option>').text(element[1]).attr('value', element[0]));
              })

              
          });
      }
  });


  // Функция реагирует на изменение региона. Взависимости от региона, формирует селект с городами.
  const selectElement = document.querySelector('#region');
  selectElement.addEventListener('change', (event) => {
    
    let region = selectElement.value
    $.ajax({
      url:'/citys',
      type:'POST',
      data: 'region=' + region,
      dataType: 'json',
      success: function( json ) {
        $.each(json, function(i, value) {
          $('#city')[0].options.length = 0;
          $('#city').prop('disabled', false);
          value.forEach((element) => {
                  
            $('#city').append($('<option>').text(element[1]).attr('value', element[0]));
                  
          })      
        });
      }
    }); 
  });




 });