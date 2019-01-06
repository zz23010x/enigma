var express = require('express');
var router = express.Router();
let request = require('request-promise');

/* GET users listing. */
router.get('/', async(req, res, next) =>{
  let enKeyWord = encodeURI(req.query.word)
  let result = {objURL : ''}
  await request('https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&pn=0&rn=10&word=' + enKeyWord + "&width=" + req.query.width + "&height=" + req.query.height, function(error, response, body){
    if(error){
      callback(error);
    }
    if (body != undefined && body[0] === '{'){
      let jsonData = JSON.parse(body)
      if (jsonData.data.length > 1){
        result = jsonData.data[Math.floor(Math.random()*(jsonData.data.length-1))]
      }
      if (result === undefined || result.objURL === undefined){
        console.log(result, jsonData)
      }
    }
  })
  res.header("Access-Control-Allow-Origin", "*");
  res.send(await objURLToIamge(result.objURL))
})

function objURLToIamge(objURL){
  var f = {w: "a",k: "b",v: "c",1: "d",j: "e",u: "f",2: "g",i: "h",t: "i",3: "j",h: "k",s: "l",4: "m",g: "n",5: "o",r: "p",q: "q",6: "r",f: "s",p: "t",7: "u",e: "v",o: "w",8: "1",d: "2",n: "3",9: "4",c: "5",m: "6",0: "7",b: "8",l: "9",a: "0",_z2C$q: ":","_z&e3B": ".",AzdH3F: "/"};
  var h = /(_z2C\$q|_z&e3B|AzdH3F)/g;
  var e = objURL.replace(h, function(t, e) { return f[e] });
  var s = /([a-w\d])/g;
  e = e.replace(s, function(t, e) { return f[e] });
  return e
}

module.exports = router;