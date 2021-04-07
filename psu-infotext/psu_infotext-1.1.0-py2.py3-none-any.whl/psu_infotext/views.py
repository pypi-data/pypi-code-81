from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from psu_infotext.models import Infotext
from psu_base.classes.Log import Log
from psu_base.services import utility_service, error_service
from psu_base.decorators import require_authority
from django.db.models import Q
from collections import OrderedDict

log = Log()

# ToDo: Error Handling/Messages


@require_authority(['admin', 'infotext', 'developer'])
def infotext_index(request):
    """
    Search page for locating infotext to be edited
    """
    log.trace()
    keywords = request.GET.get("keywords")

    text_instances = Infotext.objects.filter(app_code=utility_service.get_app_code())
    if keywords:
        text_instances = text_instances.filter(
            Q(text_code__icontains=keywords) | Q(content__icontains=keywords) | Q(group_title__icontains=keywords)
        )
    text_instances = text_instances.order_by('group_title', 'text_code')

    # Group results by group_title
    results = OrderedDict()
    ungrouped = []
    if text_instances:
        for ii in text_instances:
            if ii.group_title:
                if ii.group_title in results:
                    results[ii.group_title].append(ii)
                else:
                    results[ii.group_title] = [ii]
            else:
                ungrouped.append(ii)

    if results and ungrouped:
        results['Other Infotext'] = ungrouped
    elif ungrouped:
        results['Infotext'] = ungrouped

    log.end('infotext/index')
    return render(
        request, 'infotext_index.html',
        {
            'results': results,
            'keywords': keywords,
        }
    )


@require_authority(['admin', 'infotext', 'developer'])
def infotext_update(request):
    """
    Update a given infotext instance
    """
    text_id = request.POST.get('id')
    text_content = request.POST.get('content')
    log.trace([text_id])

    text_instance = get_object_or_404(Infotext, pk=text_id)
    try:
        text_instance.set_content(text_content)
        text_instance.save()
        return HttpResponse(text_instance.content)
    except Exception as ee:
        error_service.unexpected_error("Unable to save infotext", ee)
        return HttpResponseForbidden()
