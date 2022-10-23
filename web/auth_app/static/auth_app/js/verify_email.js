console.log('verify')
$(function () {
verifyToken()
});

function verifyToken() {
  console.log('email');
  const urlSearchParams = new URLSearchParams(window.location.search);
  let data = {'key': urlSearchParams.get('key')}
  console.log(data)

    $.ajax({
    url: '/api/v1/auth/sign-up/verify/',
    type: "POST",
    data: data,
    success: function (data) {
      console.log("success", data);
      window.location.replace("/login/");

    },
    error: function (data) {
      console.log("error", data);
      $('div h1').text('ERROR ' + data.responseText)
      // alert('ERROR ' + data.responseText)
    }

  })
}
