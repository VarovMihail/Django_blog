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

