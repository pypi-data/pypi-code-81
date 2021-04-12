import datetime
import re

from django.db.models import Q
from django.http import JsonResponse, HttpRequest

from medicine.dto.dtos import PageDTO, ReturnDTO
from medicine.dto.params import QueryParam, MatchParam
from medicine.models import Medicine, Image, Instruction


def query_trend(request: HttpRequest):
    query_set = Medicine.objects.filter(data_completion=1).order_by("id")[0:5]
    return JsonResponse(ReturnDTO.success(data=[q.name for q in query_set]))


def query_medicine(request: HttpRequest):
    """
    查询药品 支持 通用名称/品牌/商品名称 的模糊，及首字母或拼音查询
    """
    param = QueryParam(request).validate()
    if isinstance(param, JsonResponse):
        return param

    page: int = int(param.page)
    page_size: int = int(param.page_size)
    name: str = param.name

    query_time_start = datetime.datetime.now()

    query = Q()
    query.add(Q(data_completion=1), Q.AND)

    subquery = Q()
    if name:
        subquery.add(Q(name__contains=name), Q.OR)
        subquery.add(Q(prod_name__contains=name), Q.OR)
        subquery.add(Q(brand__contains=name), Q.OR)
        if re.match(r'[a-zA-Z].+$', name):
            subquery.add(Q(abbreviation__icontains=name), Q.OR)
            subquery.add(Q(pinyin__icontains=name), Q.OR)
            subquery.add(Q(brand_abbreviation__icontains=name), Q.OR)
            subquery.add(Q(brand_pinyin__icontains=name), Q.OR)

    query.add(subquery, Q.AND)
    query_set = Medicine.objects.filter(query).order_by("id")
    total = query_set.count()
    query_set_slice = query_set[(page - 1) * page_size:page * page_size]

    qs_dicts = []
    medicine_ids = set()

    for qs in query_set_slice:
        medicine_ids.add(qs.id)
        qs_dicts.append(qs.to_dict())

    images = list(Image.objects.filter(medicine_id__in=medicine_ids))
    instructions = list(Instruction.objects.filter(medicine_id__in=medicine_ids))
    query_time_end = datetime.datetime.now()

    print(f"查询时间：{query_time_end - query_time_start}")

    calc_time_start = datetime.datetime.now()
    image_dicts = {}
    for image in images:
        mid = image.__dict__["medicine_id"]
        image_dict = image_dicts.get(str(mid), [])
        image_dict.append(image.to_dict())
        image_dicts[str(mid)] = image_dict

    instruction_dicts = {}
    for instruction in instructions:
        mid = instruction.__dict__["medicine_id"]
        instruction_dict = instruction_dicts.get(str(mid), [])
        instruction_dict.append(instruction.to_dict())
        instruction_dicts[str(mid)] = instruction_dict

    for qs_dict in qs_dicts:
        qs_dict["images"] = image_dicts.get(qs_dict["id"])
        qs_dict["instructions"] = instruction_dicts.get(qs_dict["id"])

    calc_time_end = datetime.datetime.now()
    print(f"计算时间: {calc_time_end - calc_time_start}")
    return JsonResponse(PageDTO.success(page, page_size, total, data=qs_dicts))


def match_medicine(request):
    """
    匹配药品数据 规则： 通用名称+品牌名称+规格
    """
    param = MatchParam(request).validate()
    if isinstance(param, JsonResponse):
        return param

    name: str = str(param.name)
    brand: str = str(param.brand)
    spec: str = str(param.spec)
    spec_regex = ''.join([i if i.isdigit() else ".*?" for i in spec])
    spec_regex = r"^%s" % spec_regex

    query = Q()
    query.add(Q(data_completion=1), Q.AND)
    query.add(Q(name__contains=name), Q.AND)

    brand_query = Q()
    brand_query.add(Q(manufacture__contains=brand), Q.OR)
    brand_query.add(Q(brand__contains=brand), Q.OR)
    query.add(brand_query, Q.AND)

    spec_query = Q()
    spec_query.add(Q(spec__regex=spec_regex), Q.OR)
    spec_query.add(Q(spec__contains=spec), Q.OR)
    query.add(spec_query, Q.AND)

    query_time_start = datetime.datetime.now()
    query_set = Medicine.objects.filter(query).order_by("id")
    if not query_set.exists():
        return JsonResponse(ReturnDTO.success(message="未查询到结果"))

    qs_dicts = []
    medicine_ids = set()

    for qs in query_set:
        medicine_ids.add(qs.id)
        qs_dicts.append(qs.to_dict())

    images = list(Image.objects.filter(medicine_id__in=medicine_ids))
    instructions = list(Instruction.objects.filter(medicine_id__in=medicine_ids))
    query_time_end = datetime.datetime.now()

    print(f"查询时间：{query_time_end - query_time_start}")

    calc_time_start = datetime.datetime.now()
    image_dicts = {}
    for image in images:
        mid = image.__dict__["medicine_id"]
        image_dict = image_dicts.get(str(mid), [])
        image_dict.append(image.to_dict())
        image_dicts[str(mid)] = image_dict

    instruction_dicts = {}
    for instruction in instructions:
        mid = instruction.__dict__["medicine_id"]
        instruction_dict = instruction_dicts.get(str(mid), [])
        instruction_dict.append(instruction.to_dict())
        instruction_dicts[str(mid)] = instruction_dict

    for qs_dict in qs_dicts:
        qs_dict["images"] = image_dicts.get(qs_dict["id"])
        qs_dict["instructions"] = instruction_dicts.get(qs_dict["id"])

    calc_time_end = datetime.datetime.now()
    print(f"计算时间: {calc_time_end - calc_time_start}")
    return JsonResponse(ReturnDTO.success(data=qs_dicts))
