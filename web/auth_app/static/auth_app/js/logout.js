$(function () {
  $('#logoutSubmit').click(logout);
});


function logout(e) {
  e.preventDefault();
  $.ajax({
    url: $('#logoutForm').attr("action"),
    type: "POST",
    dataType: 'json',
    success: function (data) {
      localStorage.removeItem('currentUserId')
        //location.reload();
      location.href = '/'
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}
