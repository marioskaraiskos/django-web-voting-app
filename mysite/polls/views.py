from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .models import Question, Choice
from .forms import UserRegistrationForm

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

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        user_vote = request.POST.get("choice")  # match the form input
        if not user_vote:
            return HttpResponse("No vote provided.")
        # store in session
        request.session[f'user_vote_{question_id}'] = user_vote
        # redirect to GET to display vote
        return redirect('polls:vote', question_id=question_id)

    # GET request → display the vote result
    user_vote = request.session.get(f'user_vote_{question_id}')
    if not user_vote:
        return HttpResponse("You haven't voted yet.")

    try:
        choice_text = Choice.objects.get(id=user_vote).choice_text
    except Choice.DoesNotExist:
        choice_text = "Unknown choice"

    return HttpResponse(f"You voted: {choice_text}")
