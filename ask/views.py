from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from django.shortcuts import render, Http404
from .forms import QuestionForm, CommentForm
from ask.models import Question,SpaceQuestion
from spaces.models import Spaces
from django.contrib.auth.models import User
from spaces.forms import SpaceForm
from accounts.models import Profile
from django.db.models import Q
from itertools import chain
from operator import attrgetter

def question_create(request):
    if not request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)#commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
            question.user = request.user
            question.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        form = QuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'ask_question.html', context)


def question_detail(request, slug):
    question = get_object_or_404(Question, slug=slug)
    form = CommentForm(request.POST or None)
    profile = Profile.objects.get(user=request.user)
    upvotings = profile.upvoting.all()
    downvotings = profile.downvoting.all()
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()
    question_comments = question.comments.all().order_by('-created_date')

    if form.is_valid():
        comment = form.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/question/' + slug + '/')

    if question in upvotings:
        upvote = True

    else:
        upvote = False


    if question in downvotings:
        downvote = True

    else:
        downvote = False

    context = {
        'question': question,
        'form': form,
        'upvote': upvote,
        'downvote': downvote,
        'up_count': up_count,
        'down_count': down_count,
        'question_comments': question_comments
    }
    return render(request, 'question_detail.html', context)

def question_index(request):
    question_list = Question.objects.all()
    space_list = Spaces.objects.all()
    space_question_list = SpaceQuestion.objects.all()
    combined_question = sorted(
        chain(question_list, space_question_list),
        key=attrgetter('publishing_date'), reverse=True)

    users = User.objects.all()
    profiles = Profile.objects.all()
    query = request.GET.get('q')
    if query:
        question_list = question_list.filter(
            Q(question__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
        space_question_list = space_question_list.filter(
            Q(question__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()
        context = {
            'question_list': question_list,
            'space_question_list': space_question_list
        }
        return render(request, 'searched.html', context)


    if not request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)

        form2 = SpaceForm(request.POST, request.FILES)
        if form.is_valid():

            question = form.save(commit=False)#commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
            question.user = request.user
            question.save()

            return HttpResponseRedirect(question.get_absolute_url())
        if form2.is_valid():
            space = form2.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
            space.author = request.user
            space.save()
            return redirect('home')
    else:
        form = QuestionForm()
        form2 = SpaceForm()

    context = {
        'form': form,
        'form2': form2,
        'question_list': question_list,
        'space_list': space_list,
        'users': users,
        'profiles': profiles,
        'combined_question': combined_question,
        'space_question_list': space_question_list
    }
    return render(request, 'home.html', context)



def profile_questions_list(request):
    my_questions = Question.objects.filter(user=request.user)
    my_space_questions = SpaceQuestion.objects.filter(user=request.user)
    combined_question = sorted(
        chain(my_questions, my_space_questions),
        key=attrgetter('publishing_date'), reverse=True)
    return render(request, 'my_questions.html', {'combined_question': combined_question})

def question_delete(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    question = get_object_or_404(Question, slug=slug)
    if question.user == request.user:
        question.delete()
    return redirect('ask:home')


def question_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    question = get_object_or_404(Question, slug=slug)
    form = QuestionForm(request.POST, request.FILES, instance=question)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(question.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'ask_question.html', context)


def space_index(request):
    space_list = Spaces.objects.all()

    context = {
        'space_list': space_list
    }
    return render(request, 'space_list.html', context)

def upvote_question(request,slug):
    profile = Profile.objects.get(user=request.user)
    question = get_object_or_404(Question, slug=slug)
    question_comments = question.comments.all().order_by('-created_date')
    upvotings = profile.upvoting.all()
    downvotings = profile.downvoting.all()
    user = User.objects.get(id=request.user.id)
    form = CommentForm(request.POST or None)
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()
    if form.is_valid():
        comment = form.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/question/' + slug + '/')
    if question in downvotings:
        downvote = True
    else:
        downvote = False
    if question in upvotings:
        upvote = False
        profile.upvoting.remove(question.id)
        question.upvoters.remove(user)
    else:
        upvote = True
        profile.upvoting.add(question.id)
        question.upvoters.add(user)

        if question in downvotings:
            profile.downvoting.remove(question.id)
            question.downvoters.remove(user)
            downvote = False
    context = {
        'question': question,
        'upvotings': upvotings,
        'upvote': upvote,
        'form': form,
        'downvote': downvote,
        'up_count': up_count,
        'down_count': down_count,
        'question_comments': question_comments,

    }
    return render(request, 'question_detail.html', context)

def downvote_question(request,slug):
    profile = Profile.objects.get(user=request.user)
    question = get_object_or_404(Question, slug=slug)
    question_comments = question.comments.all().order_by('-created_date')
    downvotings = profile.downvoting.all()
    upvotings = profile.upvoting.all()
    user = User.objects.get(id=request.user.id)
    form = CommentForm(request.POST or None)
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()

    if form.is_valid():
        comment = form.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/question/' + slug + '/')

    if question in upvotings:
        upvote = True

    else:
        upvote = False

    if question in downvotings:
        downvote = False
        profile.downvoting.remove(question.id)
        question.downvoters.remove(user)
    else:
        downvote = True
        profile.downvoting.add(question.id)
        question.downvoters.add(user)

        if question in upvotings:
            profile.upvoting.remove(question.id)
            question.upvoters.remove(user)
            upvote = False

    context = {
        'question': question,
        'downvotings': downvotings,
        'downvote': downvote,
        'form': form,
        'upvote': upvote,
        'up_count': up_count,
        'down_count': down_count,
        'question_comments': question_comments,

    }
    return render(request, 'question_detail.html', context)


def follow_space(request, slug):
    profile = Profile.objects.get(user=request.user)
    space = get_object_or_404(Spaces, slug=slug)
    following = profile.following.all()
    user = User.objects.get(id=request.user.id)

    if space in following:
        follow = False
        profile.following.remove(space.id)
        space.followers.remove(user)
    else:
        follow = True
        profile.following.add(space.id)
        space.followers.add(user)
    context = {
        'space': space,
        'following': following,
        'follow': follow,
    }
    return render(request, 'space_detail.html', context)


