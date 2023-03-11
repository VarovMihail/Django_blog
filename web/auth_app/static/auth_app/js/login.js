console.log('login page')


$(function () {
  $('#loginForm').submit(login);
  $('#forgotPasswordForm').submit(resetPassword);
  $('#GithubLogin').click(GithubLogin);
  $('#VKLogin').click(VKLogin);
});

function GithubLogin() {
  console.log('GithubLogin')
  $.ajax({
    url: '/api/v1/auth/github/init/',
    type: 'GET',
    success: function (data) {
      console.log("success GithubLogin", data)
      let params = $.param(data)
      console.log(params)
      window.location.replace(`https://github.com/login/oauth/authorize?${params}`)
    },
    error: function (data) {
      console.log("error GithubLogin", data)
    }})

}

function VKLogin() {
  console.log('VKLogin')
  $.ajax({
    url: '/api/v1/auth/vk/init/',
    type: 'GET',
    success: function (data) {
      console.log("success VKLogin", data)
      let params = $.param(data)
      console.log(params)
      window.location.replace(`https://github.com/login/oauth/authorize?${params}`)
    },
    error: function (data) {
      console.log("error VKLogin", data)
    }})

}

function resetPassword(e) {
  let form = $(this);
   e.preventDefault();
  $.ajax({
    url: '/api/v1/auth/password/reset/',
    type: 'POST',
    data: form.serialize(),
    success: function (data) {
      console.log("success", data)
      $('#pwdModal h1').text('')
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

      localStorage.access_token_expiration = data.access_token_expiration
      localStorage.currentUserId = data.user.pk
      sessionStorage.currentUserId = data.user.pk

      location.reload();
      // $(function () {
      //    Toast.show(`Success login`, 'success')
      // })


    },
    error: function (data) {
      Toast.show(`${data.responseText}`, 'error')
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

