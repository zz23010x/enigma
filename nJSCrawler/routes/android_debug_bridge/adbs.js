var express = require('express');
var router = express.Router();
var cmd = require('node-cmd');
var async = require("async");
let request = require('request-promise');

var tikrapp = {
  1 : 'PEOPLESDAILY',
  2 : 'READER'
}

var com = {
  package : {
    PEOPLESDAILY : 'com.peopleapp.en',
    READER : 'com.readers.mobile'
  }
}

var pgyer = {
  PEOPLESDAILY : 'https://www.pgyer.com/pdnewsandroid',
  READER : 'https://www.pgyer.com/readersAndroid'
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('shell_adb');
});

router.get('/keyboard_input', function(req, res, next){
  cmd.get(
    'adb shell input text "' + req.query.keyword + '"',
    function(err, data, stderr){
      res.header("Access-Control-Allow-Origin", "*");
      res.send(err)
    }
  );
});

router.get('/get_device_info', function(req, res, next){
  async.series({
    get_device: function(callback){
      cmd.get(
        'adb devices',
        function(err, data, stderr){
          let device_name = data.trim().split('\r\n')
          if (device_name.length>1){
            device_name = device_name[1].split('\t')[0]
          }
          callback(null, device_name)
        }
      );
    },
    get_andriod_version: function(callback){
      cmd.get(
        'adb shell getprop ro.build.version.release',
        function(err, data, stderr){
          callback(null, data.trim())
        }
      );
    },
    get_phone_madein: function(callback){
      cmd.get(
        'adb shell getprop ro.product.manufacturer',
        function(err, data, stderr){
          callback(null, data.trim())
        }
      );
    },
    get_phone_model: function(callback){
      cmd.get(
        'adb shell getprop ro.product.model',
        function(err, data, stderr){
          callback(null, data.trim())
        }
      );
    },
    get_phone_resolution: function(callback){
      cmd.get(
        'adb shell wm size',
        function(err, data, stderr){
          let resolution_size = data.trim().split(' ')
          if (resolution_size.length>2){
            resolution_size = resolution_size[2]
          }
          callback(null, resolution_size)
        }
      );
    },
  },function(error, results){
    let cjstr = ''
    for (let i in results){
      cjstr += results[i] + ' '
    }
    let phone_info = {
      '设备ID' : results.get_device,
      '手机型号' : results.get_phone_madein + ' ' + results.get_phone_model,
      'Android版本' : results.get_andriod_version,
      '分辨率' : results.get_phone_resolution,
      // 'copy word' : cjstr
    }
    console.log(cjstr)
    res.header("Access-Control-Allow-Origin", "*");
    res.send(phone_info)
  })
});

router.get('/ScreenShots', function(req, res, next){
  let file_name = GetTimeFormatYYYYMMddHHmmss() + '.png'
  cmd.get(
    'adb shell screencap -p /sdcard/' + file_name + ' && adb pull /sdcard/' + file_name + ' ' + req.query.filepath + ' && adb shell rm -f /sdcard/' + file_name,
    function(err, data, stderr){
      res.header("Access-Control-Allow-Origin", "*");
      res.send(req.query.filepath + '/' + file_name)
    }
  );
});

router.get('/OpenBrowser', function(req, res, next){
  cmd.get(
    'adb shell am start -a android.intent.action.VIEW -d ' + pgyer[tikrapp[req.query.appid]],
    function(err, data, stderr){
      res.header("Access-Control-Allow-Origin", "*");
      res.send(err)
    }
  );
});

router.get('/ClearPackageData', function(req, res, next){
  cmd.get(
    'adb shell pm clear ' + com.package[tikrapp[req.query.appid]],
    function(err, data, stderr){
      res.header("Access-Control-Allow-Origin", "*");
      res.send(err)
    }
  );
});

function GetTimeFormatYYYYMMddHHmmss(){
  let date = new Date();
  let year = date.getFullYear();
  let month = date.getMonth()+1;
  let day = date.getDate();
  let hour = date.getHours();
  let minute = date.getMinutes();
  let second = date.getSeconds();
  return ''+year+month+day+hour+minute+second
}

module.exports = router;