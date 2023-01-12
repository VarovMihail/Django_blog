console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

function singUp(e) {
  let form = $(this);
  e.preventDefault();
  console.log(form.serialize())
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
      $(".help-block").remove()

      if (data.responseJSON.first_name ) {
      $("#first_name_group").addClass('has-error');   // это <div id="first_name_group"
      $('#first_name_group').append('<div class="help-block">' + data.responseJSON.first_name + "</div>"
      )};

      if (data.responseJSON.last_name ) {
      $("#last_name_group").addClass('has-error');
      $('#last_name_group').append('<div class="help-block">' + data.responseJSON.last_name + "</div>"
      )};

      if (data.responseJSON.email ) {
      $("#email").addClass('has-error');
      $('#email').append('<div class="help-block">' + data.responseJSON.email + "</div>"
      )};

      if (data.responseJSON.password_1 ) {
      $("#password_1").addClass('has-error');
      $('#password_1').append('<div class="help-block">' + data.responseJSON.password_1 + "</div>"
      )};

      if (data.responseJSON.password_2 ) {
      $("#password_2").addClass('has-error');
      $('#password_2').append('<div class="help-block">' + data.responseJSON.password_2 + "</div>"
      )}


    }

  })
}
