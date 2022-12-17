console.log('here')

$(function () {
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(resetPassword);
});



function resetPassword(e) {
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
  console.log('login')
  let form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      console.log("success", data);
      console.log(data.user.first_name);
      localStorage.currentUserId = data.user.pk

      location.reload();


    },
    error: function (data) {
      console.log("error", data);
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );

    }
  })
}

