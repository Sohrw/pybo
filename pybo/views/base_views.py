from django.shortcuts import render, get_object_or_404
from ..models import Question, Answer
from django.core.paginator import Paginator
from django.db.models import Q


def index(request, category_id=None):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    question_list = Question.objects.order_by('-create_date')

    if category_id is not None:
        question_list = question_list.filter(category_id=category_id)

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(question_answer__content__icontains=kw) |
            Q(author__username__icontains=kw)|
            Q(question_answer__author__username__icontains=kw)
        ).distinct()
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    page = request.GET.get('page', '1')
    answer_list = question.question_answer.order_by('create_date')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)

    context = {'answer_list': page_obj, 'question': question}
    return render(request, 'pybo/question_detail.html', context)

