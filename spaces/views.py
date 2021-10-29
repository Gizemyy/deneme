from django.contrib.auth.models import User
from django.shortcuts import render
from spaces.forms import SpaceForm, SpaceQuestionForm,CommentForm
from django.shortcuts import render, Http404
from django.shortcuts import HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from spaces.models import Spaces
from accounts.models import Profile
from ask.models import SpaceQuestion


from django.urls import reverse
def space_create(request):
    if not request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        form = SpaceForm(request.POST, request.FILES)
        if form.is_valid():
            space = form.save(commit=False)#commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
            space.author = request.user
            space.save()
            return redirect('home')
    else:
        form = SpaceForm()
    context = {
        'form': form,
    }
    return render(request, 'create_space.html', context)


def space_index(request):
    space_list = Spaces.objects.all()
    context = {
        'space_list': space_list
    }
    return render(request, 'space_list.html', context)


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



def space_question_create(request, slug):
    my_profile = Profile.objects.get(user=request.user)
    space = get_object_or_404(Spaces, slug=slug)
    questions = SpaceQuestion.objects.filter(category_id=Spaces.objects.get(slug=slug).id).order_by('-publishing_date')
    if not request.user.is_authenticated:
        raise Http404()
    if request.method == "POST":
        form = SpaceQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)#commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
            question.user = request.user
            question.category_id = Spaces.objects.get(slug=slug).id
            question.save()
            return HttpResponseRedirect('/spaces/' + slug)
    else:
        form = SpaceQuestionForm()
    if space in my_profile.following.all():
        follow = True
    else:
        follow = False
    context = {
        'form': form,
        'questions': questions,
        'space': space,
        'follow': follow
    }
    return render(request, 'space_questions.html', context)

def space_question_detail(request, slug):
    question = get_object_or_404(SpaceQuestion, slug=slug)
    form = CommentForm(request.POST or None)
    question_comments = question.spacecomments.all().order_by('-created_date')
    profile = Profile.objects.get(user=request.user)
    upvotings = profile.upvotingsq.all()
    downvotings = profile.downvotingsq.all()
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()

    if form.is_valid():
        comment = form.save(commit=False) # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/spaces/qdetail/' + slug + '/')

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
        'question_comments': question_comments,
        'upvote': upvote,
        'downvote': downvote,
        'up_count': up_count,
        'down_count': down_count,
    }
    return render(request, 'space_question_detail.html', context)


def space_detail(request, slug):
    my_profile = Profile.objects.get(user=request.user)
    space = get_object_or_404(Spaces, slug=slug)
    if space in my_profile.following.all():
        follow = True
    else:
        follow = False
    context = {
            'space': space,
            'follow': follow
        }
    return render(request, 'space_detail.html', context)


def space_question_delete(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    question = get_object_or_404(SpaceQuestion, slug=slug)
    if question.user == request.user:
        question.delete()
    return redirect('ask:home')


def space_question_update(request, slug):
    if not request.user.is_authenticated:
        raise Http404()
    question = get_object_or_404(SpaceQuestion, slug=slug)
    form = SpaceQuestionForm(request.POST, request.FILES, instance=question)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(question.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'ask_question.html', context)


def upvote_question(request,slug):
    profile = Profile.objects.get(user=request.user)
    question = get_object_or_404(SpaceQuestion, slug=slug)
    question_comments = question.spacecomments.all().order_by('-created_date')
    upvotings = profile.upvotingsq.all()
    downvotings = profile.downvotingsq.all()
    user = User.objects.get(id=request.user.id)
    form = CommentForm(request.POST or None)
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()
    if form.is_valid():
        comment = form.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/spaces/qdetail/' + slug + '/')

    if question in downvotings:
        downvote = True

    else:
        downvote = False


    if question in upvotings:
        upvote = False
        profile.upvotingsq.remove(question.id)
        question.upvoters.remove(user)
    else:
        upvote = True
        profile.upvotingsq.add(question.id)
        question.upvoters.add(user)

        if question in downvotings:
            profile.downvotingsq.remove(question.id)
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
        'question_comments': question_comments
    }
    return render(request, 'space_question_detail.html', context)

def downvote_question(request,slug):
    profile = Profile.objects.get(user=request.user)
    question = get_object_or_404(SpaceQuestion, slug=slug)
    question_comments = question.spacecomments.all().order_by('-created_date')
    downvotings = profile.downvotingsq.all()
    upvotings = profile.upvotingsq.all()
    user = User.objects.get(id=request.user.id)
    form = CommentForm(request.POST or None)
    up_count = question.upvoters.count()
    down_count = question.downvoters.count()
    if form.is_valid():
        comment = form.save(commit=False)  # commit=false o nesneyi veri tabanına eklemez ama save methodu formdan aldığı bilgilerle o nesneyi bize geri döndürür.
        comment.question = question
        comment.user = request.user
        comment.save()
        return HttpResponseRedirect('/spaces/qdetail/' + slug + '/')

    if question in upvotings:
        upvote = True

    else:
        upvote = False

    if question in downvotings:
        downvote = False
        profile.downvotingsq.remove(question.id)
        question.downvoters.remove(user)
    else:
        downvote = True
        profile.downvotingsq.add(question.id)
        question.downvoters.add(user)
        if question in upvotings:
            profile.upvotingsq.remove(question.id)
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
        'question_comments': question_comments
    }
    return render(request, 'space_question_detail.html', context)


