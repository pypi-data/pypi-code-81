import requests


class API(object):

    def __init__(self):
        pass

    def query_exchange(self, key):
        """返回常用汇率"""
        url = "http://op.juhe.cn/onebox/exchange/query"
        res = requests.get(
            url,
            params={
                "key": key,
            },
        )
        res.raise_for_status()
        data = {}
        for item in res.json()["result"]["list"]:
            data[item[0]] = {
                "货币名称": item[0],
                "交易单位": item[1],
                "现汇买入价": item[2],
                "现钞买入价": item[3],
                "现钞卖出价": item[4],
                "中行折算价": item[5],
            }
        return data

    def get_jokes(self, key):
        """
        返回笑话
        [
            "高中一班主任陈老师，因其身高比较矮，同学给起了个外号叫“武大郎”，后来被老师得知，要求同学带家长，同学跟家里说了原委，家长带着同学到老师办公室致歉，该同学家长进门就说:“武老师，小孩子不懂事，还忘您能海涵”，后来同学告诉我们班主任当时那表情都抽搐了，足足让我们笑了一学期。",
            "…给闺女买了一双小皮鞋，花了两张毛爷爷，小鞋很结实，闺女穿了好多天后要我给她买鞋，说不喜欢了，我就各种教育，比如要穿破之后买，要知道省钱……等等。今天再回去的时候，姑娘左手拎着残破的鞋子，右手拿着剪刀，跑过来说:爸爸，现在可以买新的鞋子了吧！来，过来，爸爸保证不打你，我的亲闺女。",
        ]
        """
        url = "http://v.juhe.cn/joke/randJoke.php"
        res = requests.get(
            url,
            params={
                "key": key
            },
        )
        res.raise_for_status()
        return [
            x["content"]
            for x in res.json()["result"]
            if x["content"].strip().strip('　')
        ]
