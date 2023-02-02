console.log('blog-list')
$(function () {
blogList()
});

// получить список статей
function blogList() {
  $.ajax({
    url: '/api/v1/article/posts/',
    type: 'GET',
    success: updateArticleList,
    error: function (data) {
      console.log("error", data);
    }
  })
}

function updateArticleList(data) {
  console.log("success blogList", data)
  const div = $('#articleList')
  div.empty()
  // for (let article of data.results) {
  data.results.forEach(article => {
    const uTime = new Date(article.updated)
    //const updatedTime = uTime.getFullYear() + '-' + uTime.getMonth() + '-' + uTime.getDate()
    const updatedTime = `${uTime.getFullYear()}-${uTime.getMonth()}-${uTime.getDate()}`
    let html = articleHtml(article.title,
                          article.author.full_name,
                          article.image,
                          article.short_content,
                          updatedTime,
                          article.url,
                          article.comment_set.length,
                          article.likes
      )
    div.append(html)
  })
 if (data.next){
    div.append(`<br><a id="next" className="btn btn-read-more" href="${data.next}">Next articles</a>&nbsp; &nbsp;`);
  }
  if (data.previous){
    div.append(`<a id="previous" className="btn btn-read-more" href="${data.previous}">Previous articles</a>`);
  }
  if (document.querySelector('#next')){
    document.querySelector('#next').onclick = UpDownArticleList;
  }
  if (document.querySelector('#previous')){
    document.querySelector('#previous').onclick = UpDownArticleList;
  }
}

function UpDownArticleList(e) {
  e.preventDefault()
  const link = $(this).attr('href')
  $.ajax({
    url: link,
    type: 'get',
    success: updateArticleList,
    error: function (data) {
      console.log('error pagination', data)
    }
  })

}


// заполняем одну статью
const articleHtml = (title, author, image, content, updated, url, commentsCount, likes) => {
  return `
   <div class="row">
      <div class="col-md-12 post">
        <div class="row">
          <div class="col-md-12">
            <h4>
              <strong>
                <a href="${ url }" class="post-title">${title}</a>
              </strong>
            </h4>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 post-header-line">
            <span class="glyphicon glyphicon-user"></span>by <a href="#">${author}</a> |
            <span class="glyphicon glyphicon-calendar"></span> ${updated}
            <span class="glyphicon glyphicon-comment"></span><a href="#"> ${commentsCount} Comments</a> |
            <i class="icon-share"></i><a href="#">${likes} Likes</a> |
            <span class="glyphicon glyphicon-tags"></span> Tags: <a href="#">
            <span class="label label-info">Snipp</span></a> <a href="#">
            <span class="label label-info">Bootstrap</span></a> <a href="#">
            <span class="label label-info">UI</span></a> <a href="#">
            <span class="label label-info">growth</span></a>
          </div>
        </div>
        <div class="row post-content">
          <div class="col-md-3">
            <a href="#">
              <img class="img-responsive" src="${image}">
            </a>
          </div>
          <div class="col-md-9">
            <p>
               ${content}

            </p>
            <p>
              <a class="btn btn-read-more" href="${url}">Read more</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  `
}

