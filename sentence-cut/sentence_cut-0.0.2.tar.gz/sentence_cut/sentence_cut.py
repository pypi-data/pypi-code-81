import re
import pandas as pd
from copy import  copy

class sentence_cut:
    '''
    句子切分，可以把几种类型的排比句切分为单句，便于后续的句子成分分析。
    '''
    def __init__(self):
        '''
        初始化设置
        timerange_pattern1检测 ”2020-2022年xxx分别为xx、xx、xx“ 类型的表述
        timerange_pattern1检测 ”10月、11月和12月的xxx分别为xx、xx、xx“ 类型的表述
        year_detect_pattern 检测年月日和季度等时间信息
        value_pattern 检测货币、百分比、重量等数值类型
        combine_lst deep_cut中使用的连接词表，识别到连接词，触发deep cut
        '''
        time_type1 = "([0-9]+(年|月|日|季度)??)([\-,至,到,~])([0-9]+(年|月|日|季度)?)"
        time_type2 = "([HQ][0-9])([\-,至,到,~])([HQ][0-9])"
        self.timerange_pattern1 = r"({})|({})".format(time_type1, time_type2)

        time_type3 = "([0-9]+(年|月|日|季度)??)(/[0-9]+(年|月|日|季度)?)+(年|月|日|季度)"
        time_type4 = "([HQ][0-9])(/[HQ][0-9])+"
        time_type5 = "([0-9]+(年|月|日|季度)??)(/[0-9]+[HQ][0-9])"
        self.timerange_pattern2 = r"({})|({})|({})".format(time_type3, time_type4, time_type5)

        self.year_detect_pattern = "([0-9]+(年|月|日|季度))"
        # self.year_detect_pattern = "(年|月|日|季度)?"

        self.combine_lst = ["增加", "增长", "减少", "上升", "下降",
                       "增速", "降速", "提升", "增幅", "降幅", "同比", "环比"]
        currency_pattern = '[+\-]?(([1-9]\d*[\d,，]*\.?\d*)|(0\.[0-9]+))(百|千|百万|千万|亿|万|亿)?元'
        percent_pattern = '[+\-]?(([1-9]\d*[\d,，]*\.?\d*)|(0\.[0-9]+))%'
        other_pattern = '[+\-]?(([1-9]\d*[\d,，]*\.?\d*)|(0\.[0-9]+))(百|千|百万|千万|亿|万|亿)?(吨|千克|斤)'
        self.value_pattern = '({})|({}|{})'.format(
            currency_pattern, percent_pattern, other_pattern)

    def res_clean_space(self,res):
        '''
        句子切分过程中可能会产生多余的空格或者重复的逗号，在这里数据清洗
        '''
        new_res = []
        for item in res:
            if item:
                item = item.replace(' ', '')
                item = item.replace("，，", '，')
                new_res.append(item)
        return new_res

    def preprocess(self,text):
        '''
        文本预处理
        清除源文本中的空格，和英文逗号（一般出现在较大的数额中）
        处理切分标识符（【SEP】）
        '''
        text = text.replace(' ', '')
        text = text.replace(',', '')
        text = re.sub(r"（(.+)）", "", text)

        # text = re.sub("至|到|~", '-', text)
        text = re.sub("和|、", '/', text)

        text_lst = text.split('，')
        clean_res = []
        for text_i in text_lst:
            if "分别" in text_i:
                text_i = re.sub("分别为|分别是|分别", '[SEP]', text_i)


            if '为' in text_i or '是' in text_i:
                tmp_split_res = re.split("为|是", text_i)
                if '/' in tmp_split_res[0] or '/' in tmp_split_res[1]:
                    text_i = re.sub("为|是", '[SEP]', text_i)
            clean_res.append(text_i)
        text = '，'.join(clean_res)

        return text

    def check_semicolon(self, text):
        '''
        默认得到的句子是以句号分割的完整句意的句子
        但是句子中可能会有分号，分号前后的句子可能存在句意联系，也可能无关
        这里根据经验进行判断，决定分号是否切分
        '''
        if '；' not in text:
            return [text]
        res = []
        pre_text = ""
        split_lst = text.split('；')
        for text_item in split_lst:
            if '[SEP]' not in text_item:
                pre_text += text_item
                pre_text += '，'
            else:
                tmp_split_res = text_item.split("[SEP]")
                L_count = len(re.findall('/',tmp_split_res[0])) + len(re.findall('-',tmp_split_res[0]))
                R_count = len(re.findall('/', tmp_split_res[1]))
                if L_count == 0 and R_count != 0:
                    pre_text += text_item
                    pre_text += '，'
                else:
                    if pre_text != "":
                        res.append(pre_text)
                    pre_text = text_item + '，'
        if pre_text != "":
            res.append(pre_text)
        return res

    def event_split(self, event_text, time_length=2):
        '''
        对包含多个属性的分居进行切分，结果为单属性的短句
        “归母净利润为100、200、300” ——》 “归母净利润为100” “归母净利润为200” “归母净利润为300”
        '''
        if '/' not in event_text:
            return None
        event_text = event_text.replace('[SEP]','')
        i = 0
        #     print(event_text)
        for i in range(len(event_text)):
            #         print(i)
            if event_text[i] in "+-/.,0123456789%":
                break
        l = i
        i = len(event_text) - 1
        for i in range(len(event_text) - 1, -1, -1):
            if event_text[i] in "+-/.,0123456789%":
                break
        r = i
        event_pre = event_text[:l]
        event_value = ""
        for c in event_text[l:r + 1]:
            if c in "+-/.,0123456789%":
                event_value += c
        unit = event_text[r + 1:]
        res = []
        #     print(event_value)
        word_lst = re.split("/", event_value)
        item_lst = word_lst.copy()
        if len(word_lst) != time_length:
            item_lst = []
            for i in range(0, len(word_lst), 2):
                item_lst.append(word_lst[i] + '/' + word_lst[i + 1])

        for word in item_lst:
            s = event_pre + word + unit
            res.append(s)

        #     print(res)
        return res

    def time_split(self, time_text, type="range"):
        '''
        对timerange进行切分，得到分离的时间短语，两种type 分别对应以下
        “20—22年” ——》 “2020年” “2021年” ”2022年“
        ”10、11、12月“ ——》 ”10月“ ”11月“ ”12月“
        '''
        time_text = re.sub("至|到|~", '-', time_text)
        i = len(time_text) - 1
        for i in range(len(time_text) - 1, -1, -1):
            if time_text[i] in "HQ0123456789":
                break
        r = i
        unit = time_text[r + 1:]
        times = ""
        for c in time_text[:r + 1]:
            if c in "-/HQ0123456789":
                times += c
        res = []
        if not unit and "20" in times:
            unit = "年"
        if type == "parallel":
            word_lst = times.split('/')
            if unit == '年':
                for i in range(len(word_lst)):
                    if len(word_lst[i]) == 2:
                        word_lst[i] = "20" + word_lst[i]
            for word in word_lst:
                if 'H' in word or 'Q' in word:
                    res.append(word)
                else:
                    res.append(word + unit)
        elif type == "range":

            pattern_char = re.compile(r"[HQ]+")
            matches = pattern_char.search(times)
            pre = ""
            if matches:
                pre = matches.group()
                times = re.sub(r"[HQ]+", '', times)
                word_lst = re.split("-", times)
                start = int(word_lst[0])
                end = int(word_lst[1])
                i = start
                while (i <= end):
                    res.append(pre + str(i) + unit)
                    i += 1
            else:
                word_lst = re.split("-", times)
                word_lst[1] = str(int(word_lst[1]) + 1)
                if unit == '年':
                    for i in range(len(word_lst)):
                        if len(word_lst[i]) == 2:
                            word_lst[i] = "20" + word_lst[i]
                    #                 print(word_lst)
                    time_range = pd.date_range(word_lst[0], word_lst[1], freq='Y')
                    res = [item.strftime("%Y") + unit for item in time_range]
                elif unit == '月':
                    time_range = pd.date_range(
                        "2020-" + word_lst[0], "2020-" + word_lst[1], freq='M')
                    #                 print(time_range)
                    res = [item.strftime("%m") + unit for item in time_range]

        #     print(res)
        return res

    def time_range_split(self, text, time_match, type="range"):
        '''
        切分timerange类型的排比句（两种timerange）
        例子：
        "2020年Q1~Q4，公司单季度营业收入分别为 12.99/16.44/19.82/21.56 亿元，同比增长，归母净利润 0.32/0.80/1.25/0.94 亿元"——》
        ”2020年Q1，公司单季度营业收入为12.99亿元，同比增长，归母净利润0.32亿元“
        ”2020年Q2，公司单季度营业收入为16.44亿元，同比增长，归母净利润0.80亿元“
        ”2020年Q3，公司单季度营业收入为19.82亿元，同比增长，归母净利润1.25亿元“
        ”2020年Q4，公司单季度营业收入为21.56亿元，同比增长，归母净利润0.94亿元“
        '''
        try:
            time_pre = text[:time_match.start()]
            time_period = text[time_match.start():time_match.end()]
            events = text[time_match.end():]

            time_period = self.time_split(time_period, type)
            time_length = len(time_period)
            # print(time_length)
            #     print(time_pre)
            #     print(time_period)
            #     print(events)

            event_lst = re.split('，', events)
            split_res = []
            for i in range(len(time_period)):
                split_res.append(time_pre + time_period[i])
            text_post = ""
            for event in event_lst:
                if event:
                    event = event.replace('[SEP]','为')
                    res = self.event_split(event, time_length)
                    if res:
                        for i in range(len(split_res)):
                            split_res[i] += (res[i] + '，')
                    else:
                        for i in range(len(split_res)):
                            split_res[i] += (event + '，')
        except:
            split_res = [text]
        return self.res_clean_space(split_res)

    def aspect_single_split(self, text):
        '''
        对单句进行aspect切分，前边的处理中已经保证了该步骤接收的text只包含一个分隔符SEP
        识别出[SEP]的位置，分隔符左边为不同的属性，分隔符右边为相应的数值
        对于没有数值的短句，默认为number suggest，直接把该短句拼接在后边
        '''
        text_before, text_after = text.split('[SEP]')
        text_before_lst = re.split("，", text_before)
        text_pre = ''
        text_post = ''
        text_key = ''

        #找到text_pre 一般来说句子的前缀中会包含时间、公司名等关键信息
        for i in range(len(text_before_lst)):
            s = text_before_lst[i]
            if '/' in s:
                text_key = s
                break
            else:
                text_pre += (s + '，')

        for s in text_before_lst[i + 1:]:
            text_post += ('，' + s)
        if not text_post:
            text_post = ""

        #先找到key_lst 也就是句子中关注的属性，并且针对研报中常出现的一些用语做特殊处理，使得key lst定位更准确
        key_lst = text_key.split('/')
        if "实现" in key_lst[0]:
            s1, s2 = key_lst[0].split("实现")
            text_pre += s1
            key_lst[0] = s2

        time_matches = re.finditer(self.year_detect_pattern, key_lst[0])
        time_match = None
        for iter in time_matches:
            time_match = iter
        if time_match:
            time_end = time_match.end()
            text_pre += key_lst[0][:time_end]
            key_lst[0] = key_lst[0][time_end:]

        if '的' in key_lst[-1]:
            tmp = key_lst[-1].split('的')[-1]
            new_key_lst = []
            for item in key_lst:
                if tmp not in item:
                    new_key_lst.append(item + tmp)
                else:
                    new_key_lst.append(item)
            key_lst = new_key_lst

        split_res = []
        for i in range(len(key_lst)):
            split_res.append(text_pre + key_lst[i] + text_post)

        #调用event split 划分后边的句子成分
        text_after_lst = re.split("，", text_after)
        event_i = 0
        for event in text_after_lst:
            if event:
                res = self.event_split(event, len(key_lst))
                if event_i != 0:
                    for i in range(len(split_res)):
                        split_res[i] += '，'
                event_i += 1
                if res:
                    for i in range(len(split_res)):
                        split_res[i] +=  res[i]
                else:
                    for i in range(len(split_res)):
                        split_res[i] += event
        # final_res = text_pre + '，'.join(split_res)
        return text_pre, key_lst, split_res

    def aspect_split(self, text):
        '''
        处理 ”xxx和xxx分别为 xx、xx“ 这种类型的句子，但是考虑到研报中表述的可能情况，要先判断句中有几个分隔符[SEP]
        如 "贵州茅台2020年一季报、中报、三季报的营收分别为XX、XX、XX，去年同期分别为XX、XX、XX，去年同期中报的营业成本为，扣非为232。"
        "贵州茅台2020年的营收和净利润分别为XX、XX，管理、财务费用分别为XX、XX。"
        这两句话就要做不同的处理。
        '''
        try:
            split_res = []
            aspect_sentences = []
            tmp_text = ""
            text_lst = re.split('，', text)
            text_post = ""
            text_pre = ""
            flag = 0
            #按照句意完整度划分为两个aspect子句
            for text_i in text_lst:
                if text_i == "":
                    continue
                if '[SEP]' in text_i:
                    flag = 1
                    sep_before, sep_after = text_i.split('[SEP]')
                    if '/' in sep_before:
                        if tmp_text!="":
                            aspect_sentences.append(tmp_text)
                        tmp_text = text_i + '，'
                    else:
                        if '[SEP]' in tmp_text:
                            text_i = text_i.replace('[SEP]','')
                        tmp_text += (text_i + '，')
                else:
                    if '/' in text_i:
                        tmp_text += (text_i + '，')
                    else:
                        if flag:
                            text_post+=(text_i + '，')
                        else:
                            text_pre += (text_i + '，')
            if tmp_text != "":
                aspect_sentences.append(tmp_text)

            for s in aspect_sentences:
                text_pre, key_lst_s, split_res_s = self.aspect_single_split(text_pre + s)
                split_res.extend(split_res_s)
            if text_post!="":
                split_res.append(text_pre + text_post)
        except:
            split_res = [text]
        return self.res_clean_space(split_res)


    def cut(self,text):
        '''
        执行切句
        首先判断是否属于两类  timerange
        否则判断如果分隔符 [SEP] 出现在文本中，就执行aspect 切分
        如果以上三种pattern都没有发现，那么返回原句
        '''
        time_matches = re.finditer(self.timerange_pattern1, text)
        time_match1 = None
        for iter in time_matches:
            time_match1 = iter

        if time_match1:
            time_split_res = self.time_range_split(text, time_match1, type="range")
            return time_split_res

        time_matches = re.finditer(self.timerange_pattern2, text)
        time_match2 = None
        for iter in time_matches:
            time_match2 = iter

        if time_match2:
            time_split_res = self.time_range_split(text, time_match2, type="parallel")
            return time_split_res

        if '[SEP]' in text:
            aspect_split_res = self.aspect_split(text)
            return aspect_split_res
        return [text]


    def deep_cut(self, sentence):

        try:
            matches = re.findall(self.value_pattern, sentence)
            if len(matches) <= 1:
                return [sentence]
            number_pattern = re.compile(self.value_pattern)
            text_pre = ""
            tmp_pre = ""
            res = []
            s_lst = re.split("，", sentence)
            for s_i in s_lst:
                number_match = number_pattern.search(s_i)
                if number_match:
                    if any(i in s_i for i in self.combine_lst):
                        res.append(text_pre + tmp_pre + s_i)
                    else:
                        res.append(text_pre + s_i)
                        tmp_pre = s_i[:number_match.start()]
                else:
                    text_pre += (s_i + '，')
        except:
            res = [text]
        return res


    def cut_sentence(self,sentence, method="loose"):
        '''
        切句主函数，首先按照句号切分（虽然默认接收到的句子是不含句号的）
        然后判断是否需要切开分号，得到新的text list
        默认执行loose切分，即切分后的句子中可以包含描述同一事物不同属性的多个数值
        如果设置method为strict，那么对上述得到的分句执行deep_cut操作，把每个数值切分到单独的短句中
        '''
        try:
            s_lst = re.split("。", sentence)
            text_lst = []
            for s in s_lst:
                if s != "":
                    s = self.preprocess(s)
                    text_lst.extend(self.check_semicolon(s))
            res_loose = []
            for s in text_lst:
                if s:
                    res_loose.extend(self.cut(s))
            if method == "loose":
                return res_loose

            elif method == "strict":
                res_strict = []
                for s in res_loose:
                    if s:
                        res_strict.extend(self.deep_cut(s))
                new_res = list(dict.fromkeys(res_strict))
                return new_res
                # res_final = []
                # for s in res_strict:
                #     if s:
                #         res_final.extend(respect_split(s))
                # return res_final

            return res_loose

        except:
            return [sentence]


if __name__ == "__main__":
    # text = "2019年矿产金xxx，矿产铜"
    # res = split_for_completion(text)
    # text = "预计20、21、22年归母净利为48.3/56.8/64.6亿元，EPS为0.62/0.73/0.82元，PE为8.9/7.5/6.6x。"
    text = "报告期内，公司主要产品产量保持平稳，生产矿产金11.18吨、精炼金33.10吨、冶炼金17.90吨，与上年同期比较分别减少了4.53%、10.65%、13.66%；生产矿山铜9,380吨、电解铜143,984吨，与上年同期比较分别增加了7.12%、1.62%。"
    # text = "20年公司前三季度实现收入/归母净利润为695.7/338.3亿元，同比+9.6%/11.1%"
    # text = "20Q3单季度实现收入/归母净利润为239.4/112.3亿元，同比+7.2%/6.9%，公司业绩延续上半年稳健增长态势，"
    # res = split_text(text,method="strict")
    # text = "报告期内，公司主要产品产量保持平稳，生产矿产金11.18吨，与上年同期比较减少了4.53%，与上年同期比较增加了7.12%。"
    text = "20年公司前三季度实现收入/归母净利润为695.7/338.3亿元，同比+9.6%/11.1%；20Q3单季度实现收入/归母净利润为239.4/112.3亿元，同比+7.2%/6.9%；公司业绩延续上半年稳健增长态势，中秋国庆双节传统旺季带动需求快速增长，商超等直营渠道拓展稳步推进，产品结构持续优化，我们预计公司20-22年EPS为37.04/42.65/50.14元，维持“买入”。"
    # text = "20H1公司销售铜精矿约4.1万吨，内蒙古矿业业绩承诺19-21年度经审计的矿业权口径净利润合计数分别不低于人民币7.46亿元、7.34亿元和6.91亿元；中原冶炼厂19年和20H1净利润分别约4.48亿元和1.36亿元。"
    # text = "20年公司前三季度实现收入/归母净利润为695.7/338.3亿元"
    # text = "2020年上半年公司起重机械销售收入126.9亿，同比增长10.6%"
    # text = "我们下调公司20-22年起重机销售预测至0.49/0.63/0.71元，以反映当期汇兑损失以及疫情对海外市场的影响。"
    # text = "去年贵州茅台2020年一季报、中报、三季报分别为：XX、XX、XX，去年同期中报的营业成本为XX，扣非为XX.XX。"
    # text = "2020Q1~Q4，公司单季度营业收入分别为 12.99/16.44/19.82/21.56 亿元，同比-15.16%/-6.78%/+4.41%/+15.97%；归母净利润 0.32/0.80/1.25/0.94 亿元，同比-53.36%/-25.40%/+6.07%/433.74%；扣非归母净利润分别为 0.28/0.79/1.19/0.94 亿元，同比-59.23%/-27.48%/+4.17%/+691.53%。"
    # res = split_text(text, method="loose")
    # text = "报告期内，公司主要产品产量保持平稳，生产矿产金11.18吨、精炼金33.10吨、冶炼金17.90吨，与上年同期比较分别减少了4.53%、10.65%、13.66%；生产矿山铜9,380吨、电解铜143,984吨，与上年同期比较分别增加了7.12%、1.62%。"
    # text = "2020Q1~Q4，公司单季度营业收入分别为 12.99/16.44/19.82/21.56 亿元，同比增长，归母净利润 0.32/0.80/1.25/0.94 亿元"
    # text = "贵州茅台2020年一季报、中报、三季报的营收分别为，去年同期分别为：，去年同期中报的营业成本为，扣非为232。"
    # text = "中金黄金的2020年中报披露日期为12，上半年公司营业收入为123，上年同期为22，上半年实现归母净利润为22，扣非净利润为22。"
    # text = "徐工机械2020年三季报表现同比大增，费用率控制较好，其中管理、财务费用为，去年同期分别为：21、22，整体利润总金额为22，对比与贵州茅台利润总额33，公司仍有一定差距。"
    SC = sentence_cut()
    res = SC.cut_sentence(text)
    print(res)

#['据一季报，20年Q1 实现营收 73.18亿元', '据一季报，20年Q1 实现营收 同比下降16.87%', '据一季报，20年Q1 归母净利润 1.60亿元', '据一季报，20年Q1 归母净利润 同比下降22.40%', '据一季报，20年Q1 扣非后归母净利润 为0.4亿元', '据一季报，20年Q1 扣非后归母净利润 同比增长7.61%']
