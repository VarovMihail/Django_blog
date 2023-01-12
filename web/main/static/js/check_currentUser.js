$(function () {
  check_currentUser()
})


function check_currentUser() {
  console.log('check_currentUser')

  today = new Date()
  expirationTime = new Date(localStorage.access_token_expiration)
  delta = expirationTime - today

  console.log('delta', delta)

  if ( delta <  0 ) {
    localStorage.removeItem('access_token_expiration')
    localStorage.removeItem('currentUserId')
  }
}
