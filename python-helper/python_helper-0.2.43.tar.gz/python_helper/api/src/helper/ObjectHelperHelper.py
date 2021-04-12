from python_helper.api.src.service import ObjectHelper, ReflectionHelper, LogHelper

def generatorInstance() :
    while True :
        yield False
        break

def leftEqual(left, right, visitedIdInstances, muteLogs=True) :
    if ObjectHelper.isNone(left) or ObjectHelper.isNone(right) :
        return left is None and right is None
    isEqual = True
    leftIsCollection = ObjectHelper.isCollection(left)
    rightIsCollection = ObjectHelper.isCollection(right)
    if leftIsCollection and rightIsCollection :
        if len(left) == len(right) :
            for itemLeft, itemRight in zip(left, right) :
                if isEqual :
                    isEqual = isEqual and ObjectHelper.equals(itemLeft, itemRight, visitedIdInstances=visitedIdInstances, muteLogs=muteLogs)
                else :
                    break
            return isEqual
        else :
            return False
    elif (leftIsCollection and not rightIsCollection) or (not leftIsCollection and rightIsCollection) :
        return False
    else :
        attrinuteDataList = ReflectionHelper.getAttributeDataList(left)
        if not muteLogs :
            LogHelper.prettyPython(leftEqual, f'{left} data list', attrinuteDataList, logLevel=LogHelper.DEBUG, condition=not muteLogs)
        if 0 == len(attrinuteDataList) :
            return False
        for value, name in attrinuteDataList :
            if isEqual :
                isEqual = isEqual and ObjectHelper.equals(value, ReflectionHelper.getAttributeOrMethod(right, name), visitedIdInstances=visitedIdInstances, muteLogs=muteLogs)
            else :
                break
        return isEqual
