console.log('blog-detail')
const slug = decodeURI(window.location.href.split('/')[4])
$(function () {
  blogDetail();
  $('#comment-form').submit(commentCreate);
   $('#edit-form').submit(saveEditComment)
  commentsList();

});

function blogDetail() {
  $.ajax({
    url: `/api/v1/article/post/${slug}/`,
    type: 'GET',
    success: function (data) {
      console.log("success blogDetail", data)

      let div = $('#article')       // ПОЧЕМУ НЕ ДОСТАЕМ ЭЛЕМЕНТ ИЗ СПИСКА?
      const article = data
      const cTime = new Date(article.created)
      const createdTime = cTime.toLocaleString()
      const uTime = new Date(article.updated)
      const updatedTime = uTime.toLocaleString()

      let html = articleHtml(article.title,
        article.author.full_name,
        article.image,
        article.content,
        createdTime,
        updatedTime,
      )
      div.append(html)
    },
    error: function (data) {
      console.log("error blogDetail", data);
    }
  })
}

const articleHtml = (title, author, image, content, created, updated) => {
  return `
   <!-- the actual blog post: title/author/date/content -->
    <h1><a href="">${title}</a></h1>
    <p class="lead"><i class="fa fa-user"></i> by <a href="">${author}</a>
    </p>
    <hr>
    <p><i class="fa fa-calendar"></i> Posted on ${created}</p>
    <p><i class="fa fa-calendar"></i> Updated on ${updated}</p>
    <p><i class="fa fa-tags"></i> Tags: <a href=""><span class="badge badge-info">Bootstrap</span></a> <a
      href=""><span class="badge badge-info">Web</span></a> <a href=""><span class="badge badge-info">CSS</span></a>
      <a href=""><span class="badge badge-info">HTML</span></a></p>

    <hr>
    <img src="${image}" class="img-responsive">
    <hr>
    <p class="lead">${title}</p>
    <p>${content}</p>
    <br/>
    <div class="g-plusone" data-annotation="inline" data-width="300" data-href=""></div>
    <br/>
    <hr>
    <!-- the comment box -->

  `
}

function commentCreate(e) {
  console.log('commentCreate');
  e.preventDefault();
  let form = $(this);
  let mySlug = {
    'article': slug
  }
  $.ajax({
    url: form.attr('action'),
    type: form.attr('method'),
    dataType: 'json',
    data: form.serialize() + '&' + $.param(mySlug),
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
    },
    error: function (data) {
      console.log("error commentCreate", data.responseText);
      alert(data.responseText)
    }
  })

}

function commentsList() {
  $.ajax({
    url: `/api/v1/article/comment-list/${slug}/`,
    type: 'GET',
    success: updateComments,                          //function (data) {updateComments(data)}, ?? COLLBACK
    error: function (data) {
      console.log('error commentsList', data);
    }

  })
}

function updateComments(data) {
  console.log('success updateComments', data);
  const div = $('#all-comments');
  div.empty()
  let currentUserId
  try {
    currentUserId = JSON.parse(localStorage.currentUserId)
  }catch (err) {
    currentUserId = null
  }

  data.results.forEach(comment => {
    const commentId = comment.id
    const author = comment.author
    const uTime = new Date(comment.updated);
    const updated = uTime.toLocaleString();
    const content = comment.content;
    let commentCreator;

    try {
      commentCreator = comment.user.full_name
      commentCreatorId = comment.user.id                      //number но сравнение с "1" прошел
    } catch(err) {
      commentCreator = 'Anonimus'
      commentCreatorId = 0
    }
    // console.log(commentCreatorId)
    // console.log(typeof commentCreatorId)

    let html = commentHtml(
      commentId,
      commentCreator,
      commentCreatorId,
      updated,
      content,
      author,
      currentUserId
    );
    div.append(html);

    let editButtonId = `#edit${commentId}`
    if ($(editButtonId)[0]) {
      $(editButtonId)[0].onclick = editComment
    }
    let commentButtonId = `#comment${commentId}`
    if ($(commentButtonId)[0]) {
      $(commentButtonId)[0].onclick = commentComment
    }

  })
  if (data.next){
    div.append(`<br><a id="next" className="btn btn-read-more" href="${data.next}">Previous comments</a>&nbsp; &nbsp;`);
    $('#next')[0].onclick = UpDownCommentsList; // назначить действие на одну кнопку
    //$('#next').click(UpDownCommentsList);      // назначить действие на список состоящий из одной или нескольких кнопок

  }
  if (data.previous){
    div.append(`<a id="previous" className="btn btn-read-more" href="${data.previous}">Next comments</a>`);
    $('#previous')[0].onclick = UpDownCommentsList;
  }

}

function UpDownCommentsList(e) {
  e.preventDefault()
  const link = e.path[0].href;
  $.ajax({
    url: link,
    type: 'get',
    success: updateComments,
    error: function (data) {
      console.log('error pagination', data)
    }
  })

}

function commentHtml(commentId, commentCreator, commentCreatorId, updated, content, author, currentUserId) {
  let htmlList = `
      <div id="${commentId}">
        <h3><i class="fa fa-comment"></i > ${commentCreator}:
          <small> ${updated}</small>
        </h3>
        <h5>${content}</h5>
      </div>
  `
  const editButton = `<a id="edit${commentId}" className="btn btn-read-more" href="#" data-target="#pwdModal" data-toggle="modal">Edit</a>&nbsp; &nbsp;`
  const commentButton = `<a id="comment${commentId}" className="btn btn-read-more" href="#">Comment</a><br>`

  console.log(currentUserId, commentCreatorId)
  if (currentUserId == commentCreatorId) {
    htmlList += editButton

  }
  htmlList += commentButton

  return htmlList
}

function editComment(e) {
  const button = $(this)
  console.log(button, button.attr('id'))        // так тоже можно найти атрибут id
  const commentId = e.path[0].id.slice(4)            // найти id комментария edit153
  const text = $(`#${commentId} h5`)[0].innerText      // получить текст комментария
  $('#edit-form textarea')[0].innerText = text       // вставить текст в форму редактирования
  localStorage.setItem('commentId', commentId)       // сохранить id комментария для след функции
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
      setTimeout(commentsList, 500)
    },
    error: function (data) {
      console.log("error commentUpdate", data);
    }
  })
}


function commentComment(e) {
  prompt('Comment', 'default value')
}
