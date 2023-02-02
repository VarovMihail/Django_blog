console.log('all_users_list')
allUsersList()
// $(function () {
//   allUsersList()
// })



function allUsersList() {
  $.ajax({
    url: '/api/v1/user-profile/all-users-list/',
    type: 'get',
    success: printUserList,
    error: function (data) {
      console.log('error allUsersList', data)
    }
  })
}

function printUserList (data) {
  console.log('success allUsersList printUserList', data)
  let div = $('.row').first()
  //div.empty()
  //div.append('ul')
  for (user of data.results) {
    let avatar = (user.avatar == null) ? "https://oir.mobi/uploads/posts/2022-08/1661385261_40-oir-mobi-p-standartnii-fon-vatsap-instagram-56.png" : user.avatar
    //let avatar = (user.avatar == null) ? "http://localhost:8008/media/default.jpg" : user.avatar

    div.append(`
       <li>
          <div class="comment-main-level">
              <div class="comment-avatar"><img src=${avatar} width="150" height="150" alt=""></div>
              <div class="comment-box">
                  <div class="comment-head">
                      <h3 class="comment-name by-author"><a href="http://localhost:8008/profile/user-list/${user.id}">${user.first_name} ${user.last_name}</a></h3>
                      <span></span>


                  </div>
              </div>
          </div>
       </li>`)
  }

}
