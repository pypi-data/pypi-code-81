import xml.etree.cElementTree as ET


# xml字符串 -> xml对象
def xmlString_to_Object(xmlString):
    return ET.fromstring(xmlString)


# xml对象 -> xml字符串
def xmlObject_to_string(xmlObject):
    return ET.tostring(xmlObject, encoding="utf-8", method="xml").decode()

# xml文件 -> xml对象
def xmlFile_to_Object(xmlFile):
    tree = ET.ElementTree()
    tree.parse(xmlFile)
    return tree

# 创建节点对象
def create_node(tag, propertyMap, text):
    node = ET.Element(tag, propertyMap)
    node.text = text
    return node

# 获取节点对象
def get_node(root, path):
    return root.find(path)

# 获取节点对象（当有多个同名节点时）
def get_nodes(root, path):
    return root.findall(path)


# 删除父节点下的所有子节点
def remove_children(parent):
    children = parent.getchildren()
    for child in children:
        parent.remove(child)
    return parent


# 给父节点添加单个子节点
def add_child(parent, child):
    parent.append(child)


# 给父节点添加多个子节点
def add_children(parent, childrenMap):
    for tag in childrenMap:
        if type(childrenMap[tag]) is str:
            childnode = create_node(tag, {}, childrenMap[tag])
            add_child(parent, childnode)
        elif type(childrenMap[tag]) is int or type(childrenMap[tag]) is float:
            childnode = create_node(tag, {}, str(childrenMap[tag]))
            add_child(parent, childnode)
        elif type(childrenMap[tag]) is dict:
            childnode = create_node(tag, {}, "")
            childnode = add_children(childnode, childrenMap[tag])
            add_child(parent, childnode)
    return parent


# 设置节点文本
def set_node_text(node, text):
    if type(text) is not str:
        node.text = str(text)
    else:
        node.text = text


# 给节点添加属性值
def add_properties(node, propertiesMap):
    for key in propertiesMap:
        key_node = get_node(node, key)
        properties = propertiesMap.get(key)
        for property in properties:
            key_node.set(property, str(properties[property]))


if __name__ == '__main__':
    mystr = "<pc><eid>1</eid><pid>1</pid><pn>PATH 1</pn><pd>2</pd><pltr><bd><s>1</s><r>9000</r><t>3</t></bd><bg><s>1</s><lu>0</lu><bs>0</bs></bg><ql><qd>16</qd><qdt>2</qdt></ql><md><cs>0</cs></md><m><s>1</s><n>1500</n></m><fo><t>1</t><r>24</r></fo><d><s>1</s><co><de>0.0</de></co></d><l><s>1</s><ra><r>0.000</r></ra></l><cor><ber>0</ber><beri>14</beri></cor><reo><s>1</s><p>0.000</p><dmi>0.1</dmi><dma>0.5</dma></reo><du><s>2</s><shake type_id = \"6\"><max>10</max><min>0</min><cycle>60</cycle><proportion>0.5</proportion></shake type_id = \"6\"></du></pltr><prtl><bd><s>1</s><r>10000</r><t>3</t></bd><bg><s>1</s><lu>0</lu><bs>0</bs></bg><ql><qd>16</qd><qdt>2</qdt></ql><md><cs>0</cs></md><m><s>1</s><n>1500</n></m><fo><t>1</t><r>24</r></fo><d><s>1</s><co><de>0.0</de></co></d><l><s>1</s><ra><r>0.000</r></ra></l><cor><ber>0</ber><beri>14</beri></cor><reo><s>1</s><p>0.000</p><dmi>0.1</dmi><dma>0.5</dma></reo><du><s>1</s><p>0.000</p></du></prtl></pc>"
    print(mystr)