from python_helper.api.src.domain  import Constant as c
from python_helper.api.src.service import LogHelper, ObjectHelper, StringHelper, RandomHelper

MAXIMUN_ARGUMENTS = 20

UNKNOWN_TYPE_NAME = f'{c.UNKNOWN.lower()} type'
UNDEFINED = 'undefined'

METHOD_TYPE_NAME_LIST = [
    c.TYPE_METHOD,
    c.TYPE_BUILTIN_FUNCTION_OR_METHOD
]

def hasAttributeOrMethod(instance, name) :
    return False if ObjectHelper.isNone(instance) or ObjectHelper.isNone(name) else hasattr(instance, name)

def getAttributeOrMethod(instance, name, muteLogs=False) :
    attributeOrMethodInstance = None
    if ObjectHelper.isNotNone(instance) and ObjectHelper.isNotNone(name) :
        try :
            attributeOrMethodInstance = None if not hasattr(instance, name) else getattr(instance, name)
        except Exception as exception :
            if not muteLogs :
                LogHelper.warning(getAttributeOrMethod, f'Not possible to get "{name}" from "{getClassName(instance, typeClass=c.TYPE_CLASS, muteLogs=muteLogs) if ObjectHelper.isNotNone(instance) else instance}" instance', exception=exception)
    return attributeOrMethodInstance

def setAttributeOrMethod(instance, name, attributeOrMethodInstance, muteLogs=False) :
    if ObjectHelper.isNotNone(instance) and ObjectHelper.isNotNone(name) :
        try :
            setattr(instance, name, attributeOrMethodInstance)
        except Exception as exception :
            if not muteLogs :
                LogHelper.warning(setAttributeOrMethod, f'Not possible to set "{name}:{attributeOrMethodInstance}" to "{getClassName(instance, typeClass=c.TYPE_CLASS, muteLogs=muteLogs) if ObjectHelper.isNotNone(instance) else instance}" instance', exception=exception)

def getAttributeOrMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeOrMethodName
        for attributeOrMethodName in dir(objectNullArgsInstance)
        if isNotPrivate(attributeOrMethodName)
    ]

def isAttributeName(attributeName, objectNullArgsInstance) :
    return isNotPrivate(attributeName) and isNotMethod(objectNullArgsInstance, attributeName)

def getAttributeNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        attributeName
        for attributeName in dir(objectNullArgsInstance)
        if isAttributeName(attributeName, objectNullArgsInstance)
    ]

def getMethodNameList(instanceClass) :
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass)
    return [
        methodName
        for methodName in dir(objectNullArgsInstance)
        if isNotPrivate(methodName) and isMethod(objectNullArgsInstance, methodName)
    ]

def isMethodClass(methodClass) :
    return False if ObjectHelper.isNone(methodClass) else methodClass.__name__ in METHOD_TYPE_NAME_LIST

def isNotMethodClass(methodClass) :
    return False if ObjectHelper.isNone(methodClass) else not isMethodClass(methodClass)

def isMethodInstance(methodInstance) :
    return isMethodClass(type(methodInstance))

def isNotMethodInstance(methodInstance) :
    return not isMethodInstance(methodInstance)

def isMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isMethodInstance(getAttributeOrMethod(objectInstance, name))

def isNotMethod(objectInstance, name) :
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name) :
        return False
    return isNotMethodInstance(getAttributeOrMethod(objectInstance, name))

def instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=None, muteLogs=None) :
    if ObjectHelper.isNone(args) :
        args = []
    for _ in range(amountOfNoneArgs) :
        args.append(None)
    objectInstance = None
    for _ in range(MAXIMUN_ARGUMENTS) :
        try :
            objectInstance = targetClass(*args)
            break
        except :
            args.append(None)
    if not isinstance(objectInstance, targetClass) :
        raise Exception(f'Not possible to instanciate {getClassName(targetClass, typeClass=c.TYPE_CLASS, muteLogs=muteLogs)} with None as args constructor')
    return objectInstance

def getArgsOrder(targetClass) :
    noneArgs = []
    noneInstance = instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=noneArgs)
    strArgs = []
    for arg in range(len(noneArgs)) :
        strArgs.append(RandomHelper.string(minimum=10))
    try :
        instance = targetClass(*strArgs)
        instanceDataDictionary = getAttributeDataDictionary(instance)
        argsOrderDictionary = {}
        for key,value in instanceDataDictionary.items() :
            if StringHelper.isNotBlank(value) :
                argsOrderDictionary[strArgs.index(value)] = key
        argsOrder = [argsOrderDictionary[key] for key in sorted(argsOrderDictionary)]
    except Exception as exception :
        errorMessage = f'Not possible to get args order from "{getName(targetClass)}" target class'
        LogHelper.error(getArgsOrder, errorMessage, exception)
        raise Exception(errorMessage)
    return argsOrder

def isNotPrivate(attributeOrMethodName) :
    return StringHelper.isNotBlank(attributeOrMethodName) and (
        not attributeOrMethodName.startswith(f'{2 * c.UNDERSCORE}') and
        not attributeOrMethodName.startswith(c.UNDERSCORE) and
        not ObjectHelper.METADATA_NAME == attributeOrMethodName
    )

def getAttributePointerList(instance) :
    return [
        getattr(instance, instanceAttributeOrMethodName)
        for instanceAttributeOrMethodName in dir(instance)
        if isNotPrivate(instanceAttributeOrMethodName)
    ]

def getAttributeDataList(instance) :
    return [
        (getattr(instance, instanceAttributeName), instanceAttributeName)
        for instanceAttributeName in dir(instance)
        if isAttributeName(instanceAttributeName, instance)
    ]

def getAttributeDataDictionary(instance) :
    instanceDataDictionary = {}
    for name in dir(instance) :
        if isAttributeName(name, instance) :
            instanceDataDictionary[name] = getattr(instance, name)
    return instanceDataDictionary

def overrideSignatures(toOverride, original, forceName=None, forceModuleName=None) :
    try :
        if ObjectHelper.isNotNone(original) :
            toOverride.__name__ = original.__name__ if ObjectHelper.isNone(forceName) else set(forceName)
            toOverride.__qualname__ = original.__qualname__ if ObjectHelper.isNone(forceName) else set(forceName)
            toOverride.__module__ = original.__module__ if ObjectHelper.isNone(forceName) else set(c.NOTHING)
        else :
            toOverride.__name__ = forceName if ObjectHelper.isNotNone(forceName) else set(toOverride.__name__)
            toOverride.__qualname__ = forceName if ObjectHelper.isNotNone(forceName) else set(toOverride.__qualname__)
            toOverride.__module__ = forceModuleName if ObjectHelper.isNotNone(forceModuleName) else set(toOverride.__module__)
    except Exception as exception :
        LogHelper.error(overrideSignatures, f'''Not possible to override signatures of {toOverride} by signatures of {original} method''', exception)
        raise exception

def getClass(thing, typeClass=None, muteLogs=False) :
    thingClass = None
    try :
        if ObjectHelper.isEmpty(thing) :
            thingClass = typeClass
        else :
            thingClass = thing.__class__ 
    except Exception as exception :
        thingClass = type(None)
        if not muteLogs :
            LogHelper.warning(None, f'Not possible to get class of {thing}. Returning {thingClass} insted', exception=exception)
    return thingClass

def getName(thing, typeName=None, muteLogs=False) :
    name = None
    try :
        if ObjectHelper.isEmpty(thing) :
            name = getUndefindeName(typeName)
        else :
            name = thing.__name__
    except Exception as exception :
        name = getUndefindeName(typeName)
        if not muteLogs :
            LogHelper.warning(None, f'Not possible to get name of {thing}. Returning {name} insted', exception=exception)
    return name

def getClassName(thing, typeClass=None, muteLogs=False) :
    name = None
    try :
        if ObjectHelper.isEmpty(thing) :
            name = getUndefindeName(typeClass)
        else :
            name = getName(getClass(thing, muteLogs=muteLogs), muteLogs=muteLogs)
    except Exception as exception :
        name = getUndefindeName(typeClass)
        if not muteLogs :
            LogHelper.warning(None, f'Not possible to get class name of {thing}. Returning {name} insted', exception=exception)
    return name

def getMethodClassName(instanceClass):
    return instanceClass.__qualname__.split(c.DOT)[0]

def getModuleName(thing, typeModule=None, muteLogs=False) :
    name = None
    try :
        if ObjectHelper.isEmpty(thing) :
            name = getUndefindeName(typeModule)
        else :
            name = thing.__module__.split(c.DOT)[-1]
    except Exception as exception :
        name = getUndefindeName(typeModule)
        if not muteLogs :
            LogHelper.warning(None, f'Not possible to get module name of {thing}. Returning {name} insted', exception=exception)
    return name

def getMethodModuleNameDotName(instance) :
    return f'{getModuleName(instance)}{c.DOT}{getName(instance)}'

def getUndefindeName(typeThing) :
    if ObjectHelper.isEmpty(typeThing) :
        return f'({UNDEFINED})'
    else :
        return f'({typeThing} {UNDEFINED})'

def getItNaked(it) :
    printDetails(it)
    printClass(it)
    try :
        LogHelper.prettyPython(getAttributeDataDictionary, 'getAttributeDataDictionary', getAttributePointerList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeAndMethodNameList, 'getAttributeAndMethodNameList', getAttributeAndMethodNameList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeNameList, 'getAttributeNameList', getAttributeNameList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeDataList, 'getAttributeDataList', getAttributeDataList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeDataDictionary, 'getAttributeDataDictionary', getAttributeDataDictionary(it), logLevel=LogHelper.DEBUG)
    except : pass

def printDetails(toDetail) :
    print(f'{2 * c.TAB}printDetails({toDetail}):')
    try :
        print(f'{2 * c.TAB}type({toDetail}).__name__ = {getName(type(toDetail), typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__ = {type(toDetail).__class__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__module__ = {type(toDetail).__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__name__ = {getName(type(toDetail).__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__name__ = {getName(toDetail.__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__module__ = {toDetail.__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__qualname__ = {toDetail.__class__.__qualname__}')
    except :
        pass

def printClass(instanceClass) :
    print(f'{2 * c.TAB}printClass({instanceClass}):')
    try :
        print(f'{2 * c.TAB}{instanceClass}.__name__ = {getName(instanceClass, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__module__ = {instanceClass.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__qualname__ = {instanceClass.__qualname__}')
    except :
        pass
