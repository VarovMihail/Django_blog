$(function () {
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(resetPassword);
});



function resetPassword(e) {
  console.log('reset_Password')
  let form = $(this);
   e.preventDefault();
  $.ajax({
    url: '/api/v1/auth/password/reset/',
    type: 'POST',
    data: form.serialize(),
    success: function (data) {
      console.log("success", data)
      $('.modal-body').html('<h1>Check your inbox. We\'ve emailed you instructions for setting your password.</h1>')
      // $('#pwdModal h1').text("Check your inbox. We've emailed you instructions for setting your password.")
    },
    error: function (data) {
      console.log("error", data)
       $('#pwdModal h1').text('User does not exist')

    }


  })

}


function login(e) {
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
}

