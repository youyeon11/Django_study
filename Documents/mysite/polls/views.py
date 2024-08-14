from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Question, Choice

from django.http import Http404

from django.db.models import F
from django.urls import reverse

from django.views import generic

# Create your views here.
"""
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list" : latest_question_list,
               }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist: # 요청된 질문의 ID가 없을 때 오류를 반환
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk = question_id)
#    return render(request, "polls/detail.html", {"question" : question})    


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
"""

# 일반적인 장고의 뷰(generic.ListView를 사용)
# class 생성을 통하여 처리하기
class IndexView(generic.ListView):
    template_name= "polls/index.html" #index.html에 대하여 적용
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name="polls/results.html"

# vote() 함수를 가상으로 생성
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form(다시 투표 화면 띄우기)
        return render(request,
                      "polls/detail.html",
                      {
                          "question": question,
                          "error_message": "You didn't select a choice.",
                      },
                      )
    else:
        selected_choice.votes = F("votes") +1
        selected_choice.save()
        # POST요청 성공적으로 처리 후에 항상 HttpResponseRedirect 반환
        # back 버튼을 누를시에 다시 로드
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
