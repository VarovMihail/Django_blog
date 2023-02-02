function followersApi(){
  /**Нажатие на кнопку Followers */
  let button = $(this)
  console.log('followersApi', button.data('href'))
   $.ajax({
    type: 'GET',
    url: button.data('href'),
    success: function (data) {
      console.log('success followersApi', data)
        renderModal(data, button)
        $('#followerModal').modal('show');
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function renderModal(data, button) {
  /** modal_followers.html */
  $('#followModalTitle').text(button.text())
  followBodyRender(data, button)

}

function followBodyRender(data, button) {
  user_list = data.results
  let body = $('#followModalBody')
  let followUrl = button.data('follow-actions')

  body.empty()
  $.each(user_list, function(i){
   let isShowFollowButton = !!user_list[i].follow
   console.log(isShowFollowButton)

    //let avatar = (user_list[i].avatar == null) ? "https://oir.mobi/uploads/posts/2022-08/1661385261_40-oir-mobi-p-standartnii-fon-vatsap-instagram-56.png" : user_list[i].avatar
    let avatar = (user_list[i].avatar == null) ? "http://localhost:8008/media/default.jpg" : user_list[i].avatar

   var templateString = `
      <div class="user">
        <p>
          <img src="${avatar}" class="avatar img-circle img-thumbnail" width=50px>
          <a href='/profile/user-list/${user_list[i].id}'> ${user_list[i].full_name} </a>
          ${isShowFollowButton ? `
            <button class="btn btn-primary followMe" data-id="${user_list[i].id}" data-href='${followUrl}'> ${user_list[i].follow} </button>
          ` : ''}

        </p>
      </div>
   `
   body.append(templateString);
  })
   $(".followMe").click(followMe);

}

function followMe () {
  alert('followMe')
}
