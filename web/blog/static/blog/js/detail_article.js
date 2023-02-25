console.log('detail-article')
const slug = decodeURI(window.location.href.split('/')[4])
$(function () {
  blogDetail();
});



function blogDetail() {
  $.ajax({
    url: `/api/v1/article/post/${slug}/`,
    type: 'GET',
    success: function (data) {
      console.log("success blogDetail", data)
      let div = $('#article')       // ПОЧЕМУ НЕ ДОСТАЕМ ЭЛЕМЕНТ ИЗ СПИСКА?
      let html = articleHtml(data)
      div.append(html)
      // if (localStorage.currentUserId) {}
        $('#article-like-dislike').append(
          `<br>

            <i id="finger-like" class="fa fa-thumbs-up" action="article-like" data-id="${data.id}"> ${data.likes}</i><br>
            <i id="finger-dislike" class="fa fa-thumbs-down" action="article-dislike" data-id="${data.id}"> ${data.dislikes}</i>`
        )
      let likeButton = $('#finger-like')
      let dislikeButton = $('#finger-dislike')

      likeButton.click(likeDislikeArticle)
      dislikeButton.click(likeDislikeArticle)


      if (data.like_status == 1) {likeButton.attr('class',"fa fa-thumbs-o-up")}
      if (data.like_status == -1) {dislikeButton.attr('class',"fa fa-thumbs-o-down")}
    },
    error: function (data) {
      console.log("error blogDetail", data);
         //Toast.show(`${data.responseText}`, 'error')
         Toast.show(`${data.responseJSON.detail}`, 'error')
      $('.container').empty()
      $('.container').append("Too Many Requests")
    }
  })
}

const articleHtml = (data) => {
  let div = $('#article')       // ПОЧЕМУ НЕ ДОСТАЕМ ЭЛЕМЕНТ ИЗ СПИСКА?
  const article = data
  const cTime = new Date(article.created)
  const createdTime = cTime.toLocaleString()
  const uTime = new Date(article.updated)
  const updatedTime = uTime.toLocaleString()
  return `
   <!-- the actual blog post: title/author/date/content -->
    <h1><a href="">${article.title}</a></h1>
    <p class="lead" id="article-like-dislike">
    <i class="fa fa-user"></i> by <a href="">${article.author.full_name}</a>
    </p>
    <hr>
    <p><i class="fa fa-calendar"></i> Posted on ${createdTime}</p>
    <p><i class="fa fa-calendar"></i> Updated on ${updatedTime}</p>
    <p><i class="fa fa-tags"></i> Tags: <a href=""><span class="badge badge-info">Bootstrap</span></a> <a
      href=""><span class="badge badge-info">Web</span></a> <a href=""><span class="badge badge-info">CSS</span></a>
      <a href=""><span class="badge badge-info">HTML</span></a></p>

    <hr>
    <img src="${article.image}" class="img-responsive">
    <hr>
    <p class="lead">${article.title}</p>
    <p>${article.content}</p>
    <br/>
    <div class="g-plusone" data-annotation="inline" data-width="300" data-href=""></div>
    <br/>
    <hr>
    <!-- the comment box -->

  `
}

// почему console.log($(this).attr('action')) пишет article-like при $('.fa-thumbs-up').click(likeDislikeArticle)
// и пишет undefined когда  <i class="fa fa-thumbs-up" action="article-like" onclick="likeDislikeArticle()">

function likeDislikeArticle () {
  console.log('likeDislike')
  console.log('$(this)', $(this))
  console.log('this action = ', $(this).attr('action'))
  if (localStorage.currentUserId) {
  let vote = ($(this).attr('action') == 'article-like') ? 1 : -1
  let objectId = $(this).attr('data-id')
  //let dataJson = JSON.stringify({ 'vote': vote, 'object_id': 1, 'model': 'article'})
  let data = {'vote': vote, 'object_id': objectId, 'model': 'article'}
  console.log(data)

  $.ajax({
    url: `/api/v1/action/like/`,
    method: 'POST',
    dataType: 'json',
    data: data,
    success: function (data) {
      console.log('success likeDislike', data)
      //parseData = JSON.parse(data) // Почему надо здесь парсить, а через сериалайзер не надо?
      //console.log('success likeDislike', parseData)

      Toast.show(`${data.result} ${data.like_status}`, 'success')

      let likeButton = $('#finger-like')
      let dislikeButton = $('#finger-dislike')

      likeButton.text(` ${data.likes}`)
      dislikeButton.text(` ${data.dislikes}`)

      if (data.like_status == 0) {
        likeButton.attr('class', "fa fa-thumbs-up")
        dislikeButton.attr('class', "fa fa-thumbs-down")
      }
      if (data.like_status == 1) {
        likeButton.attr('class', "fa fa-thumbs-o-up")
        dislikeButton.attr('class', "fa fa-thumbs-down")
      }
      if (data.like_status == -1) {
        dislikeButton.attr('class', "fa fa-thumbs-o-down")
        likeButton.attr('class', "fa fa-thumbs-up")
      }

    },
    error: function (data) {
      console.log('error likeDislike', data)
      Toast.show(`${data.responseJSON.detail}`, 'error')
    }
  })
  } else {Toast.show('Please sing in', 'error')}
}
