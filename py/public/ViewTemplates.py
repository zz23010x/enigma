from django.shortcuts import render
from django import urls
from copy import deepcopy
import re

# Create your views here.
def index(request):
    return render(request, 'index.html', {'data': WebPage.GetAllCatalogue()})

class WebPage:
    id = 0
    name = None
    path = None
    url = None
    isIndex = False

    @staticmethod
    def GetAllUrls():
        urlsDic = {}
        for item in urls.get_resolver().url_patterns:
            if isinstance(item, urls.URLResolver):
                for pattern in item.url_patterns:
                    if str(item.pattern) == 'admin/':
                        continue
                    page = WebPage()
                    page.name = re.search(re.compile('\'.*?\''),str(pattern)).group().strip('\'')
                    page.path = str(item.pattern)
                    page.url = str(item.pattern) + re.search(re.compile('\'.*?\''),str(pattern)).group().strip('\'')
                    if 'index' in pattern.lookup_str:
                        page.isIndex = True
                    if str(item.pattern) in urlsDic:
                        urlsDic[str(item.pattern)].append(page)
                    else:
                        urlsDic[str(item.pattern)] = [page]
        return urlsDic

    @staticmethod
    def GetAllCatalogue():
        urlsDic = WebPage.GetAllUrls()
        result = deepcopy(urlsDic)
        for index, data in urlsDic.items():
            for i in range(len(data)-1, -1, -1):
                if not data[i].isIndex:
                    data.pop(i)
                    result[index].pop(i)
            if len(data) == 0:
                result.pop(index)
        return result