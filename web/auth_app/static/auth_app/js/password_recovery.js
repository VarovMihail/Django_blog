console.log('password')
$(function () {
  $('#passwordResetForm').submit(passwordReset);
});

function passwordReset(e) {
  let form = $(this);
  const urlSearchParams = new URLSearchParams(window.location.search);
  let uidtoken = {
    'uid': urlSearchParams.get('uid'),
    'token': urlSearchParams.get('token'),
  }

  e.preventDefault();
  console.log('Reset')

  $.ajax({
    url: '/api/v1/auth/password/reset/confirm/',
    type: "POST",
    data: form.serialize() + '&' + $.param(uidtoken),
    success: function (data) {
      console.log("success", data)
      window.location.replace('/login/')
      alert('Пароль успешно изменен')
    },
    error: function (data) {
      console.log("error", data)
      $('#passwordResetForm h4').text('error ' + data.responseText)
    }

  })
}
