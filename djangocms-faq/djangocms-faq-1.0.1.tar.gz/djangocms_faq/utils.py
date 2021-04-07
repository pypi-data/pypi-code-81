from djangocms_faq.models import QuestionFaqPluginModel

def get_answers(question, search_in):

    if not len(question):
        return

    # answers from question text
    answers_questions = QuestionFaqPluginModel.objects.exclude(
        placeholder__page__publisher_is_draft=True
    ).filter(
        parent__id__in=[id for id in search_in.split()]
    ).filter(
        question__icontains=question
    )

    # answers from keywords list
    answers_keywords = QuestionFaqPluginModel.objects.exclude(
        placeholder__page__publisher_is_draft=True
    ).filter(
        parent__id__in=[id for id in search_in.split()]
    ).filter(
        keywords__keyword__icontains=question
    )

    # all answers
    answers = answers_questions | answers_keywords

    return answers.distinct()
