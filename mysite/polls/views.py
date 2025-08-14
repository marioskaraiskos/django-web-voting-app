from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .models import Question, Choice, Vote
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

# ---------------------------
# Generic Views
# ---------------------------

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pk")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# ---------------------------
# User Auth Views
# ---------------------------

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'polls/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('polls:index')

# ---------------------------
# Voting View
# ---------------------------
@login_required(login_url='polls:login')  # Redirect to login if not authenticated
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        choice_id = request.POST.get("choice")
        if not choice_id:
            return HttpResponse("No vote provided.")

        choice = get_object_or_404(Choice, id=choice_id, question=question)

        Vote.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'choice': choice}
        )

        return redirect('polls:vote', question_id=question_id)

    # GET → Display vote results
    try:
        user_vote = Vote.objects.get(user=request.user, question=question)
        user_choice_text = user_vote.choice.choice_text
    except Vote.DoesNotExist:
        return HttpResponse("You haven't voted yet.")

    all_votes = Vote.objects.filter(question=question).select_related('user', 'choice')

    choice_counts = {
        c.choice_text: Vote.objects.filter(question=question, choice=c).count()
        for c in question.choice_set.all()
    }

    context = {
        'question': question,
        'user_choice_text': user_choice_text,
        'all_votes': all_votes,
        'choice_counts': choice_counts
    }

    return render(request, 'polls/vote.html', context)
    # GET → Display vote results
    try:
        user_vote = Vote.objects.get(user=request.user, question=question)
        user_choice_text = user_vote.choice.choice_text
    except Vote.DoesNotExist:
        return HttpResponse("You haven't voted yet.")

    # All votes for this question
    all_votes = Vote.objects.filter(question=question).select_related('user', 'choice')

    # Count votes per choice
    choice_counts = {
        c.choice_text: Vote.objects.filter(question=question, choice=c).count()
        for c in question.choice_set.all()
    }

    context = {
        'question': question,
        'user_choice_text': user_choice_text,
        'all_votes': all_votes,
        'choice_counts': choice_counts
    }

    return render(request, 'polls/vote.html', context)