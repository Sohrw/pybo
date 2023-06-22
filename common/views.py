from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm
from django.db.models import Q
from pybo.models import Question, Answer, Comment

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


def profile(request):
    user = request.user
    question_list = Question.objects.order_by('-create_date')
    answer_list = Answer.objects.order_by('create_date')
    comment_list = Comment.objects.order_by('create_date')

    question_list = question_list.filter(
        Q(author__username__icontains=user.username)
    )

    answer_list = answer_list.filter(
        Q(author__username__icontains=user.username)
    )

    comment_list = comment_list.filter(
        Q(author__username__icontains=user.username)
    )

    context = {
        'user': user,
        'question_list': question_list,
        'answer_list': answer_list,
        'comment_list': comment_list,
    }

    return render(request, 'common/profile.html', context)
