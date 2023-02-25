console.log('blog-detail')
const slug = decodeURI(window.location.href.split('/')[4])
$(function () {
  $('#comment-form').submit(commentCreate);
  $('#edit-form').submit(saveEditComment)
  $(window).on('load', localStorage.removeItem('commentId')) // удалить если перезагрузили страницу
  commentsList();

});

// СОЗДАНИЕ КОММЕНТАРИЯ

function commentCreate(e) {
  console.log('commentCreate');
  e.preventDefault();
  let form = $(this);
  console.log('form = ', form )
  let mySlug = {
    'article': slug
  }
  const parent = {
    'parent': localStorage.getItem('commentId')
  }
  console.log('parent = ', parent)

  console.log(form.serialize() + '&' + $.param(mySlug) + '&' + $.param(parent))
  $.ajax({
    url: form.attr('action'),
    type: form.attr('method'),
    dataType: 'json',
    data: form.serialize() + '&' + $.param(mySlug) + '&' + $.param(parent),
    success: function (data) {
      console.log("success commentCreate", data)

      let textarea = document.getElementById('textarea')  //объект DOM
      console.log('1 ', textarea)

      textarea = $('#textarea')                    // объект jQuery - список из одного элемента
      console.log('2 ', textarea)                  // не работают свойства textarea.value и textarea.placeholder

      textarea = $('#textarea')[0]                  //объект DOM
      console.log('3 ',textarea)

      textarea.value = ''
      textarea.placeholder = 'Ваш комментарий отправлен'

      setTimeout(commentsList, 500)
      localStorage.removeItem('commentId')
    },
    error: function (data) {
      console.log("error commentCreate", data.responseText.detail);
      //Toast.show('Error comment', 'error')
      Toast.show(`${data.responseJSON.detail}`, 'error')
    }
  })

}

// ОБНОВЛЕНИЕ СПИСКА КОММЕНТАРИЕВ

function commentsList() {
  $.ajax({
    url: `/api/v1/article/comment-list/${slug}/`,        // `/api/v1/article/comment-list/${slug}/?page=2`,
    type: 'GET',
    success: updateComments,
    error: function (data) {
      console.log('error commentsList', data);
    }

  })
}

function updateComments(data) {
  console.log('success updateComments', data);
   let currentUserId
  try {
    currentUserId = JSON.parse(localStorage.currentUserId)
  }catch (err) {
    currentUserId = -1
  }

  const div = $('#all-comments');     // находится в comments.html
  div.empty()

// ДИНАМИЧЕСКОЕ СОЗДАНИЕ ЭЛЕМЕНТА - $('<ul class="comments-list">') ИЛИ  $('<div class="comments-container">').append

  let ul = $('<ul class="comments-list">')
    //$('#commentList').append($('<div class="comments-container">').append(
  div.append(
    $('<div class="comments-container">').append(
      $('<h1>').text(`Comments ${data.count}`)).append(ul))

  console.log(ul)

  for (let comment of data.results) {

    // html - ПОЛНЫЙ СПИСОК КОММЕНТАРИЕВ И ДОЧЕРНИХ КОММЕНТАРИЕВ
    let html = commentHtml(comment, currentUserId)
    ul.append(html)

  }
  $('.fa-pencil').click(editComment)
  $('.fa-heart').click(likeDislikeComment)
  $('.fa-heart-o').click(likeDislikeComment)

  if (data.next){
    console.log('data.next', data.next)
    div.append(`<br><a id="next" className="btn btn-read-more" href="${data.next}">Next comments</a>&nbsp; &nbsp;`);
    //div.append(`<br><a id="next" className="btn btn-read-more" onclick="nextPrevComments()" href="${data.next}">Previous comments</a>&nbsp; &nbsp;`);

    $('#next')[0].onclick = nextPrevComments; // назначить действие на одну кнопку

    //$('#next').click(nextPrevComments);      // назначить действие на список состоящий из одной или нескольких кнопок
    //$('#next').on('click', nextPrevComments);      // тоже самое
    //$('#next')[0].addEventListener('click', nextPrevComments)

  }
  if (data.previous){
    div.append(`<a id="previous" className="btn btn-read-more" href="${data.previous}">Previous comments</a>`);
    $('#previous')[0].onclick = nextPrevComments;
  }

}

function nextPrevComments(e) {
  e.preventDefault()      // это будет ошибка если назначить функцию через onclick="nextPrevComments()"
  //const link = e.path[0].href;
  let link = $(this).attr('href')
  console.log('link', link)
  $.ajax({
    url: link,
    type: 'get',
    success: updateComments,
    error: function (data) {
      console.log('error pagination', data)
    }
  })

}

function addChildToComment (commentId, commentCreator) {
  $('#textarea')[0].innerText = `${commentCreator}, `
  $('.well')[0].scrollIntoView(true)
  localStorage.setItem('commentId', commentId)
}


// СОЗДАЕМ ПОЛНЫЙ СПИСОК КОММЕНТАРИЕВ И ДОЧЕРНИХ КОММЕНТАРИЕВ
function commentHtml(comment, currentUserId) {

  const updated = (new Date(comment.updated)).toLocaleString()
  let commentCreator = (comment.user == null) ? 'Anonymous' : comment.user.full_name
  let commentCreatorId = (commentCreator == 'Anonymous') ? 0 : comment.user.id
  let avatar = (comment.user == null) ? "http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" :
    (comment.user.avatar == null) ? "https://oir.mobi/uploads/posts/2022-08/1661385261_40-oir-mobi-p-standartnii-fon-vatsap-instagram-56.png" : comment.user.avatar

  let childHtmlList = ''                     // ЗДЕСЬ БУДУТ ВСЕ ДОЧЕРНИЕ КОММЕНТАРИИ
  for (let child of comment.children) {
    childHtmlList += childCommentHtml(child, currentUserId) // childHtmlList - ВСЕ ДОЧЕРНИЕ КОММЕНТАРИИ СОБИРАЕМ И ВСТАВЛЯЕМ В КОНЕЦ
  }
  let htmlList = `

        <li>
            <div class="comment-main-level">
                <div class="comment-avatar"><img src=${avatar} alt=""></div>
                <div class="comment-box">
                    <div class="comment-head">
                        <h6 class="comment-name by-author"><a href="#">${commentCreator}</a></h6>
                        <span>${updated}</span>
                        <a href="#formReview" onclick="addChildToComment('${comment.id}', '${commentCreator}')"><i class="fa fa-reply"></i></a>

                        `
  let htmlListEnd = `
                    </div>
                    <div id="${comment.id}" class="comment-content">${comment.content}</div>
                </div>
            </div>
            <ul class="comments-list reply-list">${childHtmlList}</ul>
        </li>

  `
  let likeButtonBlack = `<i class="fa fa-heart commentLike" data-id=${comment.id} data-vote=-1 data-type="comment"> ${comment.likes}</i>`
  let likeButtonWhite = `<i class="fa fa-heart-o commentLike" data-id=${comment.id} data-vote=1 data-type="comment"> ${comment.likes}</i>`
  if (comment.like_status == 1) {htmlList += likeButtonBlack} else {htmlList += likeButtonWhite}

  let editButton = ` <i class="fa fa-pencil" aria-hidden="true"  data-comment-id=${comment.id}></i>`
  if (currentUserId == commentCreatorId) {
  htmlList += editButton
  }



  htmlList += htmlListEnd
  return htmlList
}

// ДЕЛАЕМ 1 ДОЧЕРНИЙ КОММЕНТАРИЙ
const childCommentHtml = (child, currentUserId) => {

  let updated = (new Date(child.updated)).toLocaleString()
  let commentCreator = (child.user == null) ? 'Anonymous' : child.user.full_name
  let commentCreatorId = (commentCreator == 'Anonymous') ? 0 : child.user.id
  let avatar = (child.user == null) ? "http://i9.photobucket.com/albums/a88/creaticode/avatar_1_zps8e1c80cd.jpg" :
    (child.user.avatar == null) ? "https://oir.mobi/uploads/posts/2022-08/1661385261_40-oir-mobi-p-standartnii-fon-vatsap-instagram-56.png" : child.user.avatar

  let htmlList = `
    <li>
<!--        <div class="comment-avatar"><img src="http://localhost:8008/media/default.jpg" alt=""></div>-->
        <div class="comment-avatar"><img src=${avatar} alt=""></div>
        <div class="comment-box">
            <div class="comment-head">
                <h6 class="comment-name"><a href="#"> ${commentCreator}</a></h6>
                <span>${updated}</span>

                `
  let htmlListEnd = `
            </div>
            <div id="${child.id}" class="comment-content">${child.content}</div>
        </div>
    </li>
  `
  let likeButtonBlack = `<i class="fa fa-heart commentLike" data-id=${child.id} data-vote=-1 data-type="comment"> ${child.likes}</i>`
  let likeButtonWhite = `<i class="fa fa-heart-o commentLike" data-id=${child.id} data-vote=1 data-type="comment"> ${child.likes}</i>`
  if (child.like_status == 1) {htmlList += likeButtonBlack} else {htmlList += likeButtonWhite}

  let editButton = ` <i class="fa fa-pencil" aria-hidden="true" data-comment-id=${child.id}></i>`
  if (currentUserId == commentCreatorId) {
  htmlList += editButton
  }
  htmlList += htmlListEnd

  return htmlList
}

function editComment() {
  console.log('editComment')
  let commentId = $(this).attr('data-comment-id')
  const text = $(`#${commentId}`)[0].innerText      // получить текст комментария
  $('#edit-form textarea')[0].innerText = text       // вставить текст в форму pwdModal
  localStorage.setItem('commentId', commentId)       // сохранить id комментария для saveEditComment()
  console.log($('#edit-form textarea')[0].innerText)
  $('#pwdModal').modal('show')
}

function saveEditComment(e) {
  //e.preventDefault()
  console.log('saveEditComment')
  let form = $(this);
  const commentId = localStorage.commentId
  $.ajax({
    url: `/api/v1/article/comment-update/${commentId}/`,
    type: 'patch',
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      console.log("success commentUpdate", data)
      setTimeout(commentsList, 400)
      localStorage.removeItem('commentId')
    },
    error: function (data) {
      console.log("error commentUpdate", data);
    }
  })
}


function likeDislikeComment () {
  console.log('likeDislike')
  console.log($(this).attr('data-id'))
  console.log('vote', $(this).attr('data-vote'))

  localStorage.dataId = $(this).attr('data-id')
  let vote = $(this).attr('data-vote')
  let objectId = $(this).attr('data-id')
  let data = { 'vote': vote, 'object_id': objectId, 'model': 'comment'}
  console.log(data)

  $.ajax({
    url: `/api/v1/action/like/`,
    type: 'POST',
    data: data,
    success: function (data) {
      //parseData = JSON.parse(data)
      console.log('success likeDislike', data)
      //Toast.show(`${data.result} ${data.like_status}`, 'success')
      dataId = localStorage.dataId
      likeButton = $(`[data-id = ${dataId}]`)
      likeButton.text(` ${data.likes}`)
      if (data.like_status == 1) {
        likeButton.attr('class', 'fa fa-heart commentLike');
        likeButton.attr('data-vote', '-1');
      } else {
        likeButton.attr('class', 'fa fa-heart-o commentLike');
        likeButton.attr('data-vote', '1');
      }
    },
    error: function (data) {
      console.log('error likeDislike', data)
      Toast.show(`${data.responseJSON.detail}`, 'error')
    }
  })
}

