from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, DeepThought, Question
from .forms import DeepThoughtForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def deepThoughts(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # # create a form instance and populate it with data from the request:
        # form = DeepThoughtForm(request.POST.get())
        # # check whether it's valid:
        # if form.is_valid():
        #     # process the data in form.cleaned_data as required
        #     # ...
        #     # redirect to a new URL:
        #     return HttpResponseRedirect('/list/')
        t = request.POST.get('deepthought_title')
        d = request.POST.get('deepthought_description')
        DeepThought.objects.create(deepthought_title=t, deepthought_description=d)
        return HttpResponseRedirect('list/')

    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = DeepThoughtForm()

    return render(request, 'polls/deepthoughts.html')


def listDeepThoughts(request):
    thoughts = DeepThought.objects.all()
    context = {'thoughts' : thoughts}
    return render(request, 'polls/listdeepthoughts.html', context)