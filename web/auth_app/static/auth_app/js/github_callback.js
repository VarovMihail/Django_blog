$(function () {
  githubCallback()
})

function githubCallback() {
  console.log('githubCallback')
  //const params = new URL(window.location.href).searchParams;
  const params = new URLSearchParams(window.location.search);
  let code = params.get('code');
  let state = params.get('state');
  $.ajax({
    url: `/api/v1/auth/github/callback/`,
    type: 'POST',
    data: {'code': code, 'state': state},
    success: function (data) {
      console.log("success githubCallback", data)
      console.log(params, code, state)

    },
    error: function (data) {
      console.log("error githubCallback", data)
    }})
}








