let cheerio = require('cheerio')
let request = require('request-promise');

class article{
  constructor(){
    this.author = '这是一个作者'
    this.content = '这是一个编辑内容'
    this.contentWithHTML = ''
    this.contentNum = (parseInt(Math.random()*99)+1).toString();
    this.introduction = '这是一个摘要'
    this.origin = '这是一个来源'
    this.title = '这是一个标题'
    this.translator = '这是一个译者'
  }

  async init(info){
    this.id = info.id
    this.title = info.title
    this.introduction = info.context
    this.url = 'http://www.duzhe.com' + info.url
    this.info = info
    await this.GetArticleDetailByUrl(this.url)
  }

  async GetArticleDetailByUrl(url){
    let details
    await request(url, function(error, response, body){
      if(error){
        callback(error);
      }
      details = body
    })

    let $ = cheerio.load(details)
    
    let author, origin
    let author_and_origin = $('span.iocn_warp').text().split(' ')
    for (let i in author_and_origin){
      if (author_and_origin[i].indexOf('作者') != -1){
        author = author_and_origin[i].trim().split('：')[1]
      }else if(author_and_origin[i].indexOf('来源' != -1)){
        origin = author_and_origin[i].trim().split('：')[1] == "暂无" ? '' : author_and_origin[i].trim().split('：')[1]
      }
    }
    this.author = author
    this.origin = origin

    this.translator = 'china_' + author
    if (author === ''){
      this.translator = ''
    }
    this.content = $('div.detail_con').eq(0).html()
    // this.content = $('div.detail_con').eq(0).text()
    this.contentWithHTML = $('div.detail_con').eq(0).html()

    if (this.author === undefined) {
      console.log('error..author is undefined.' + url)
    }

    this.detail = details
  }
}

module.exports = article;