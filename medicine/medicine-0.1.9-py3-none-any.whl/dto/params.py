from django.http import JsonResponse

from medicine.dto.dtos import ReturnDTO


class QueryParam:

    def __init__(self, request):
        self.name = request.GET.get("name")
        self.page: str = request.GET.get("page", "1")
        self.page_size: str = request.GET.get("page_size", "50")

    def validate(self):
        if not self.page.isdigit():
            return JsonResponse(ReturnDTO.fail(message="参数[page]错误"))

        if not self.page.isdigit():
            return JsonResponse(ReturnDTO.fail(message="参数[page_size]错误"))

        if int(self.page) < 1:
            return JsonResponse(ReturnDTO.fail(message="page不能小于1"))

        if int(self.page_size) < 1:
            return JsonResponse(ReturnDTO.fail(message="page_size不能小于1"))

        return self


class MatchParam:

    def __init__(self, request):
        self.name = request.GET.get("name")
        self.brand: str = request.GET.get("brand")
        self.spec: str = request.GET.get("spec")

    def validate(self):
        if not self.name:
            return JsonResponse(ReturnDTO.fail(message="缺少[name]参数"))

        if not self.brand:
            return JsonResponse(ReturnDTO.fail(message="缺少[brand]参数"))

        if not self.spec:
            return JsonResponse(ReturnDTO.fail(message="缺少[spec]参数"))

        return self
