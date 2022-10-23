console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log('here')
  $.ajax({
    url: '/api/v1/auth/sign-up/',
    type: "POST",
    data: form.serialize(),
    success: function (data) {
      console.log("success", data);
      $('#signUpForm').html('<h1>На ваш email-адрес было отправлено письмо.</h1>')


    },
    error: function (data) {
      console.log("error", data);
       alert('ERROR ' + data.responseText)
    }

  })
}
