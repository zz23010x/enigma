

THIS IS A DUCUMENT..HEHE

前言
    欢迎入坑
    这个文件用来说明 packby3k.py 相关的巴拉巴拉

工具目的
    - 为了简化日常打包APK的流程
    - 扔掉IDE，回归下朴实、简单的命令行
    - 呵呵、我写不出来了，你猜吧

一些术语
    - 版本资源：
        用于打包的、带有版本标识的游戏资源文件们
        比如 乱舞.android svn 里的 _v104、_v105、_vtrunk

what it DOES??
    - 将版本资源、指定渠道的android工程、(.libs里的)游戏.so和.jar、 打包成 android-apk
    - 将生成的android-apk和androidmanifest.xml改名拷贝至输出目录，
      比如乱舞工程里的 .output

what it NOT DOES??
    - 不处理so的编译过程，只拷贝
    - 不处理资源文件的加密，请确认版本资源是已经加密过的
    - 不自带android sdk、ant，请确保已经安装，并且相关设置正确
    - 不对渠道所带的android库工程进行检测或者编译，请确保渠道所带的android库工程已经编译

怎么用??
    - 一些前提
        1. 编写者用的 python3.4，你懂的
        2. 配置下 .toolchain 里的 env.ini
           脚本里的环境变量是通过这个文件读取的

    - 最基本的 python packby3k.py CHANNEL -v 104
        说明一下
        1.  CHANNEL 是指定的渠道的目录名
        2.  "python packby3k.py " 这个在一般的电脑上直接 " packby3k.py " 就可以
        3.  packby3k.py 里有一个默认的版本 default_version，如果和你打算拷贝的资源一致，
            可以不写，直接写成 " python packby3k CHANNEL"
        4.  有一些资源目录名比较奇葩的话，比如 _v104.googleplay，淡定，直接照写就ok，
            -> "python packby3k.py CHANNEL -v 104.googleplay"
        5.  如果不想重复拷贝资源，去掉 "-v xxx"，改成 " -n "
            如 "python packby3k.py CHANNEL -n"


额外的使用??
    呵呵，是的，还有一些参数
    首先，最后的 apk的文件名是这样滴 C#smartspace_S#test_V#102_T#1512181133_P#test.apk
    C -> 渠道名
    S -> 服务器别名(就是说明下用的是测试服还是正式服，手动的哦，不是根据资源判定的)
    V -> 所用的资源版本
    T -> 打包时间：年月日时分，1512181133：15年12月18日11时33分
    P -> purpose，打包用途：commit、test二选一

    然后，其中S、P是可以用参数修改的
    S：python packby3k CHANNEL -s servername，最后生成的就是 xxx_S#servername_xxx.apk
    P：默认是test，加上-c之后就是commit了
       如 python packby3k CHANNEL -c，最后生成的就是 xxx_P#commit.apk


这是个结尾 -，=！
    大概就是这些了，有遗漏在补充。。
    祝你用的愉快，啊哈哈


version 1, By z-suzon @ 2015.12.18

