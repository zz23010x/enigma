from django.utils.deprecation import MiddlewareMixin
from public.LogHelper import logger

class commMiddleware(MiddlewareMixin):
    def process_request(self,request):
        logger().info('[{0}]-[{1}]-[{2}]'.format(request.get_host(), request.get_full_path(), request.method))

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('auth...')

    def process_exception(self, request, exception):
        logger().error('[{0}]-[{1}]-[{2}]'.format(request.get_host(), request.get_full_path(), exception))

    def process_response(self, request, response):
        logger().info('[{0}]-[{1}]-[{2}]'.format(request.get_host(), request.path, response.status_code))
        return response


# HttpRequest.path—不包括域的全路径，例如：”/music/bands/the_beatles/”
# HttpRequest.method—请求方法，常用的有GET和POST
# HttpRequest.encoding—请求的编码格式，很有用！
# HttpRequest.GET(POST)---见HttpRequest.method
# HttpRequest.REQUEST---类字典的对象，搜索顺序先POST再GET
# HttpRequest.COOKIES---标准的python字典对象，键和值都是字符串。
# HttpRequest.FILES---类字典对象。键是表单提交的name---<input type="file" name="" />而file是一个上传的对象，它的属性有：read,name,size,chunks
# HttpRequest.META---包括标准HTTP头的python字典。如下:
#     CONTENT_LENGTH
#     CONTENT_TYPE
#     HTTP_ACCEPT_ENCODING
#     HTTP_ACCEPT_LANGUAGE
#     HTTP_HOST — The HTTP Host header sent by the client.
#     HTTP_REFERER — The referring page, if any.
#     HTTP_USER_AGENT — The client’s user-agent string.
#     QUERY_STRING — The query string, as a single (unparsed) string.
#     REMOTE_ADDR — The IP address of the client.
#     REMOTE_HOST — The hostname of the client.
#     REMOTE_USER — The user authenticated by the web server, if any.
#     REQUEST_METHOD — A string such as "GET" or "POST".
#     SERVER_NAME — The hostname of the server.
#     SERVER_PORT — The port of the server.
# HttpRequest.user---当前登录的用户
# HttpRequest.session---一个可读写的类python字典
# HttpRequest.raw_post_data---在高级应用中应用，可以算是POST的一个替代，但是不建议使用。
# HttpRequest.urlconf---默认情况下，是没有定义的
# HttpRequest.get_host()—返回域名，例如：”127.0.0.1:8000″
# HttpRequest.get_full_path()—返回请求的全路径(但是不包括域名)，例如：”/music/bands/the_beatles/?print=true”
# HttpRequest.build_absolute_uri(location)—以上2者的结合
# HttpRequest.is_secure()—判断是否为https连接(没有用过)
# HttpRequest.is_ajax()—请求为XMLHttpRequest时，返回True

# HttpResponse.content—python string对象，尽量用unicode。
# HttpResponse.status_code—HTTP Status code
# HttpResponse.has_header(header)
# HttpResponse.set_cookie
# HttpResponse.delete_cookie
# HttpResponse.write(content)
# HttpResponse.flush()
# HttpResponse.tell()