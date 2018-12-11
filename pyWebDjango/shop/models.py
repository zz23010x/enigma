from django.db import models
import json

# Create your models here.
class ShopController:
    def __init__(self):
        self.__items_list = []

    def AddGoods(self, name, price):
        goods = Goods()
        goods.id = self.__GetMaxNum()
        goods.name = name
        goods.price = price
        self.__items_list.append(goods)

    def WriteToDB(self, goods=None):
        from public.sqlite3Helper import DataBaseServer   
        if goods is None:
            params = []
            for item in self.__items_list:
                params.append((item.id, item.name, item.price))
            DataBaseServer().InsertValues('replace into tab_shop_item_info values(?,?,?)', params)
        else:
            DataBaseServer().InsertValues('replace into tab_shop_item_info values({0},{1},{2})'.format(goods.id, goods.name, goods.price))


    def ReadFromDB(self):
        from public.sqlite3Helper import DataBaseServer
        datas = DataBaseServer().SelectTable('select * from tab_shop_item_info')
        for item in datas:
            goods = Goods()
            goods.id = item[0]
            goods.name = item[1]
            goods.price = item[2]
            self.__items.append(goods)

    def ListToJson(self):
        result = []
        for item in self.__items_list:
            result.append(item.__dict__)
        return json.dumps(result)

    def __GetMaxNum(self):
        max = 1
        for i in self.__items_list:
            if i.id >= max:
                max += i.id+1
        return max

class Goods:
    def __init__(self):
        self.id = None
        self.name = None
        self.price = None