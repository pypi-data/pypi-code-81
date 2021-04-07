from django.core import serializers
from django.http import HttpResponse
from djangocms_faq.utils import get_answers
from json import dumps

def AnswerView(request):
    if "question" in request.GET:
        question = request.GET['question']

        if "search_in" in request.GET:
            search_in = request.GET["search_in"]
        else:
            search_in = ""

        answers = get_answers(question, search_in)

        jsondata = []

        if answers:
            for answer in answers:
                # look mom I'm creating ugly json!
                jsondata.append({
                    "question": answer.question,
                    "slug": answer.slug,
                    "url": answer.get_full_url,
                    "keywords": [str(keyword) for keyword in answer.keywords.all()]
                })

        return HttpResponse(dumps(jsondata), content_type='application/json')

    return HttpResponse("{}", content_type='application/json')
