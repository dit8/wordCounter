from django.http import HttpResponse, HttpResponseBadRequest
from wordCounterPost import core

def index(request):
    word = request.GET.get('word', '')
    if not word:
        return HttpResponseBadRequest('ERROR: missing argument word in request.<br /> ' + help())
    return HttpResponse(word + ' ' + str(core.getFromDBCount(word)))

## limitation of 100 chars is set in class (DB) definition of wordInfo
def help():
    return('Documentation <br /> \
            Receives a word and returns the number of times the word appeared so far (in all previous inputs). <br /> \
            word should not exceed length of 100 chars <br /> \
            usage: wordStstistics?word=myRequestedWord')