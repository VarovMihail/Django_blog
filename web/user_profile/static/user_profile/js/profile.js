console.log('profile')
$(function () {
  // document.addEventListener("DOMContentLoaded", () => Toast.init());
  fillOutHome();
  $('#fileUpload').on('change', uploadPhoto);
  //$('#fileUpload').change(uploadPhoto);
  $('#changePasswordForm').submit(changePassword);
  $('#registrationForm').submit(changeRegistrationData);
  $('#followersButton').click(followersApi)
  $('#followingButton').click(followersApi)

});


const error_class_name = "has-error"

function changeRegistrationData (e) {
  console.log('changeRegistrationData');
  e.preventDefault();
  let form = $(this);
  $.ajax({
    url: '/api/v1/user-profile/fill-out/',
    type: 'PUT',
    data: form.serialize(),
    success: function (data) {
      console.log('success changeRegistrationData', data)
      Toast.show('Success updated', 'success')
      $('.help-block').remove()
    },
    error: function (data) {
      console.log('error', data)
      Toast.show(`Error data`, 'error')
      $('.help-block').remove()
      if (data.responseJSON.first_name) {
        $('#first_name_div').addClass('has-error')
        $('#first_name_div').append('<div class="help-block">' + data.responseJSON.first_name + '</div>')
      }
      if (data.responseJSON.last_name) {
        $('#last_name_div').addClass('has-error')
        $('#last_name_div').append('<div class="help-block">' + data.responseJSON.last_name + '</div>')
      }

    }
  })

}

function fillOutHome () {
  console.log('fillOutHome')
  $.ajax({
    url: '/api/v1/user-profile/fill-out',
    type: 'GET',
    success: function (data) {
      console.log('success fillOutHome', data)
      Toast.show('Success enter', 'success')
      //Toast.show('hello')
      //document.getElementById('avatar').src = data.avatar  // тоже работает
      //if (data.avatar) {$('#avatar').attr('src', data.avatar)}
      if (data.avatar) {
        $('#avatar').attr('src', data.avatar)
      } else {
        $('#avatar').remove()
        $('#Layer_1').removeAttr('hidden')
      }
        // $('#avatar-div').append(svgAvatar)}
      // data.avatar
      //   ? $('#avatar').attr('src', data.avatar)
      //   :
      if (data.first_name) {$('#first_name').attr('value', data.first_name)}
      if (data.last_name) {$('#last_name').attr('value', data.last_name)}
      if (data.email) {$('#email').attr('value', data.email)}
      if (data.birthday) {$('#birthday').attr('value', data.birthday)}
      if (data.gender) {$(`input[value=${data.gender}]`)[0].checked = true}

    },
    error: function (data) {
      console.log('error', data)
      Toast.show(`${data}`, 'error')
    }

  })
}

function followersApi(){
  let button = $(this)
   $.ajax({
    type: 'GET',
    url: button.data('href'),
    success: function (data) {
        renderModal(data, button)
        $('#followerModal').modal('show');
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}


function uploadPhoto(e) {
  console.log('uploadPhoto')
  e.preventDefault()
  let data = new FormData();
  let files = $(this)[0].files;
  console.log('files', files, files.length)
  if (files.length) {                            //Если выбрана новая аватарка, а не нажата отмена
    data.append('avatar', files[0]);
    $.ajax({
      type: 'POST',
      url: $(this).data('href'),
      data: data,
      contentType: false,
      processData: false,
      success: function (data) {
        console.log('success uploadPhoto', data)
        Toast.show('Success upload photo', 'success')
        $("#avatar").attr("src", data.avatar)
      },
      error: function (data) {
        console.log('error', data)
      }
    })
  }
}

function changePassword(e) {
  e.preventDefault()
  console.log('changePassword')
  let form = $(this)
  console.log(form.serialize())

  $.ajax({
    type: 'PUT',//form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (data) {
      console.log('success changePassword', data)
      Toast.show('Success change Password', 'success')
    },
    error: function (data) {
      $(".help-block").remove()
      Toast.show('Error changePassword', 'error')
      let groups = ['#oldPasswordForm', '#newPassword1Form', '#newPassword2Form']
      //  groups это три <div id=...>
      for (let group of groups) {
        $(group).removeClass(error_class_name);
      }
      if (data.responseJSON.old_password) {
        help_block("#oldPasswordForm", data.responseJSON.old_password)
      }
      if (data.responseJSON.new_password1) {
        help_block("#newPassword1Form", data.responseJSON.new_password1)
      }
      if (data.responseJSON.new_password2) {
        help_block("#newPassword2Form", data.responseJSON.new_password2)
      }
    }
  })

}

function help_block(group, variable) {
  $(group).addClass(error_class_name);
  $(group).append('<div class="help-block">' + variable + "</div>");
}


function renderModal(data, button) {
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
   var templateString = `
      <div class="user">
        <p>
          <img src="${user_list[i].avatar}" class="avatar img-circle img-thumbnail" width=50px>
          <a href='${user_list[i].profile_url}'> ${user_list[i].full_name} </a>
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

const svgAvatar = `
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
  <defs>
    <style>.cls-1{fill:#b3b3b3;fill-rule:evenodd;}.cls-2{fill:#fff;}</style>
  </defs>
  <title>no-profile-picture</title>
  <polygon className="cls-1" points="0 0 122.88 0 122.88 122.88 0 122.88 0 0 0 0"/>
  <path className="cls-2"
        d="M48.64,77.72c.65-1.48,1.24-3.1,1.61-4.19a52.43,52.43,0,0,1-4.22-6L41.76,60.7a12.55,12.55,0,0,1-2.43-6.21,4.94,4.94,0,0,1,.43-2.23,4.1,4.1,0,0,1,1.47-1.71,4.73,4.73,0,0,1,1-.52,107.7,107.7,0,0,1-.2-12.23A16.87,16.87,0,0,1,42.58,35a16.39,16.39,0,0,1,7.22-9.2,22.79,22.79,0,0,1,6.05-2.69c1.37-.39-1.15-4.72.25-4.87,6.79-.7,17.77,5.5,22.51,10.62A16.63,16.63,0,0,1,82.8,39.37l-.27,11.1h0a3.06,3.06,0,0,1,2.25,2.32c.35,1.36,0,3.25-1.18,5.84h0a.37.37,0,0,1-.07.14l-4.87,8a41.6,41.6,0,0,1-6,8.24c.23.32.45.63.66.94,8.25,12.11,19.38,5.88,32.32,15.36l-.38.51v12.82H17.22V91.47h.24a1.14,1.14,0,0,1,.56-.61C26.4,86,45.72,84.35,48.64,77.72Z"/>
</svg>`
