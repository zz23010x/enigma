var express = require('express');
var router = express.Router();
let request = require('request-promise');
let article = require('./article')
let cheerio = require('cheerio')

/* GET users listing. */
router.get('/', async(req, res, next) =>{
  let list = await GetArticleList()
  let num = Math.floor(Math.random()*list.length)
  let filter_article = new article()
  await filter_article.init(list[num])
  res.header("Access-Control-Allow-Origin", "*");
  res.send(filter_article)
})

function StrToJson(str){
  var p = new Promise(function(resolve, reject){
    var result = JSON.parse(str)
    resolve(result)
  })
  return p
}

async function GetArticleList(){
  let page = new Date().getSeconds()
  let result = new Array()
  let list

  // async.series([
  //   function(callback){
  //     request('http://www.duzhe.com/search.php/fall/' + page, function(error, response, body){
  //       if(error){
  //           callback(error);
  //       }
  //       // if(Object.prototype.toString.call(body) === '[object Array]'){
  //       //   // list = StrToJson(body).then(function(a){
  //       //   //   console.log(a)
  //       //   // }).catch(function(error){
  //       //   //   console.log(error)
  //       //   // })
  //       //   console.log(123123)
  //       // }
  //     })
  //   }
  // ])
  
  page = Math.ceil(page/3)
  await request('http://www.duzhe.com/index.php?v=listing&cid=39&page=' + page, function(error, response, body){
    if(error){
      callback(error);
    }
    let $ = cheerio.load(body)
    $('.bignewsbox').each(function(){
      let one = {}
      let a = $(this).find('a').eq(0)
      one.title = a.text()
      one.url = a.attr('href')
      let arrurl = one.url.split('id=')
      one.id = arrurl[arrurl.length-1]
      let p = $(this).find('p').eq(0).text().substr(3)
      one.context = p
      result.push(one)
    })
  })

  // list.forEach(element => {
  //   if (element.type === 'text'){
  //     result.push(element)
  //   }
  // });

  return result
}

module.exports = router;