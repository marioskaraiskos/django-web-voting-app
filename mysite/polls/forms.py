# polls/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Question, Choice
from django.forms.models import inlineformset_factory



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': 'Your Question',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': (
                    'w-full px-4 py-3 rounded-lg border border-gray-300 '
                    'focus:border-green-500 focus:ring-2 focus:ring-green-200 '
                    'placeholder-gray-400 text-gray-800 shadow-sm transition-all'
                ),
                'placeholder': 'Type your question here…'
            }),
        }

ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=('choice_text',),
    extra=3,
    can_delete=True,
    widgets={
        'choice_text': forms.TextInput(attrs={
            'class': (
                'w-full px-4 py-3 rounded-lg border border-gray-300 '
                'focus:border-green-500 focus:ring-2 focus:ring-green-200 '
                'placeholder-gray-400 text-gray-800 shadow-sm transition-all'
            ),
            'placeholder': 'Type a choice…'
        }),
    }
)

def create_question(request):
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('polls:index')
    else:
        question_form = QuestionForm()
        # Pass a new Question instance so the formset knows the parent
        formset = ChoiceFormSet(instance=Question())

    return render(request, 'polls/create_question.html', {
        'question_form': question_form,
        'formset': formset
    })

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={
            'placeholder': 'Type a choice',
            'class': 'choice-input'})
        }