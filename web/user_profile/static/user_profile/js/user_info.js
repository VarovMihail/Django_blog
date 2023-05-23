//import followersApi from "./profile";
//import { followersApi } from 'user_profile/static/user_profile/js/profile'
//import { followersApi } from './profile'
//import * as profile from 'user_profile/static/user_profile/js/profile'
console.log('user info')
let userPk = window.location.href.split('/')[5]
$(function () {
  fillOutPage();
  $('#subscribe').click(subscribe)
  $('#message').click(message)
  $('#followersButton').click(followersApi)
  $('#followingButton').click(followersApi)

});

function fillOutPage () {
  /** Заполнить страницу */
  console.log('fillOutPage', userPk)
  $.ajax({
    url: `/api/v1/user-profile/user-info/${userPk}/`,
    type: 'GET',
    success: function (data) {
      console.log('success fillOutPage', data)
      $('.col-sm-10 h1').text(`${data.full_name}`)

      if (data.avatar) {
        $('#avatar').attr('src', data.avatar)
      } else {
        $('#avatar').remove()
        $('#Layer_1').removeAttr('hidden')
      }

      if (data.first_name) {$('#first_name').attr('value', data.first_name)}
      if (data.last_name) {$('#last_name').attr('value', data.last_name)}
      if (data.email) {$('#email').attr('value', data.email)}
      if (data.birthday) {$('#birthday').attr('value', data.birthday)}
      $('#followersButton').text(`Followers (${data.followers_count})`)
      $('#followersButton').attr('data-href', `/api/v1/action/followers-following-button/${data.id}/`)
      $('#followingButton').text(`Following (${data.following_count})`)
      $('#followingButton').attr('data-href', `/api/v1/action/followers-following-button/${data.id}/`)

      addSubscribeMessageButton(data.subscribe_status)


    },
    error: function (data) {
      $('.container').empty()
      $('.container').append("Page Not Found")
    }

  })
}

function subscribe () {
  /** Нажать кнопку подписки */
  console.log('subscribe button')
  let data = {
    'content_maker_id': userPk,
  }
  $.ajax({
    url: '/api/v1/action/subscribe-button/',
    type: 'post',
    data: data,
    success: function (data) {
            console.log('success subscribe', data)
      addSubscribeMessageButton(data.subscribe_status)
      $('#followersButton').text(`Followers (${data.followers_count})`)
      $('#followingButton').text(`Following (${data.following_count})`)
    },
    error: function (data) {
      console.log('error subscribe', data)
    }
  })
}

function message(e) {
  let data = {
    'user_id': userPk,
  }
  $.ajax({
    url: '/api/v1/chat/open/',
    type: 'get',
    data: data,
    success: function (data) {
            console.log('success message', data)
      window.open(data.url, '_blank').focus()
    },
    error: function (data) {
      console.log('error message', data)
    }
  })
}



function addSubscribeMessageButton(subscribeStatus) {
  let subscribeButton = $('#subscribe')
  let messageButton = $('#message')

  if (subscribeStatus == 0) {
    subscribeButton.remove()
  } else if (subscribeStatus == 2) {
    subscribeButton.remove()
    messageButton.remove()
  } else if (subscribeStatus == 1) {
    subscribeButton.text('Unsubscribe')
    subscribeButton.attr('class', 'btn btn-lg btn-error')
    subscribeButton.attr('data-id', '-1')
  } else if (subscribeStatus == -1) {
    subscribeButton.text('Subscribe')
    subscribeButton.attr('class', 'btn btn-lg btn-success')
    subscribeButton.attr('data-id', '1')
  }
}




/** НАДО ВЫНЕСТИ В ОТДЕЛЬНЫЙ ФАЙЛ - ЭТО ЕСТЬ ЗДЕСЬ И В profile.js */

function followersApi(){
  /**Нажатие на кнопку Followers и Following */
  let button = $(this)
  let button_name = button.attr('id')
  let apiUrl = button.data('href') + `?button_name=${button_name}`
  console.log(button.data('href'))
  console.log(apiUrl)
   $.ajax({
    type: 'GET',
    url: apiUrl,
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
  console.log('renderModal')
  /** modal_followers.html */
  $('#followModalTitle').text(button.text())
  followBodyRender(data, button)

}

function followBodyRender(data, button) {
  console.log('followBodyRender start')
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
     console.log('followBodyRender end')
}

function followMe () {
  alert('followMe')
}
