import random
from aishu.public.db_select import select

class date(object):

    #获取日志库ID
    def getLogwareHouseID(self):
        sql = 'SELECT id From LogWareHouse where len([id])=8'
        LogwareHouseID = select(sql)[0][0]
        return LogwareHouseID

    #获取日志库的类型
    def getdataType(self):
        sql = 'SELECT dataType From LogWareHouse where len([id])=8'
        dataType = select(sql)[0][0]
        return dataType

    #获取索引ID
    def getindexID(self):
        sql = 'SELECT id From IndexParams'
        indexID= select(sql)[0][0]
        return indexID

    #获取索引名字
    def getindexName(self):
        sql = 'SELECT indexName From IndexParams'
        indexName= select(sql)[0][0]
        return indexName

    #获取数据流名字
    def getstreamId(self):
        sql = 'SELECT name From DataStream'
        streamId= select(sql)[0][0]
        return streamId

    #获取日志分组ID
    def getLogGroupIdPare(self):
        sql = 'SELECT LogGroupIdPare From LogGroup where GroupName="所有日志"'
        LogGroupIdPare= select(sql)[0][0]
        return LogGroupIdPare

    #获取用户ID
    def getUserID(self):
        sql = 'SELECT userId From User where loginName ="admin"'
        UserID= select(sql)[0][0]
        return UserID

    #获取角色ID
    def getRoleId(self):
        sql = 'SELECT roleId From Role where roleName ="admin"'
        RoleId= select(sql)[0][0]
        return RoleId

    #获取标签组ID
    def gettagGroupID(self):
        sql = 'SELECT id From TagGroup'
        tagGroupID= select(sql)[0][0]
        return tagGroupID

    #获取标签ID
    def gettagID(self):
        sql = 'SELECT id From Tag'
        tagID= select(sql)[0][0]
        return tagID


