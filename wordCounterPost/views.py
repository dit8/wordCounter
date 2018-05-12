import json
import threading
import urllib

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from wordCounterPost import core


@csrf_exempt
@require_POST
def postData(request):
    if request.method == "POST":
        print('MAIN in thread {}'.format(threading.current_thread().name))

        param = request.body
        if not param:
            return HttpResponse(help())
        try:
            jsonParam = json.loads(param)
        except ValueError:
            return HttpResponse('Error: must pass JSON object.')
        keys = list(jsonParam)
        if not keys:
            return HttpResponse('Error: JSON is empty object.')
        methodType = keys[0]
        value = jsonParam.get(methodType)
        if methodType == 'string':
            core.countWordsFromString(value)
            return HttpResponse('string- ok')
        elif methodType == 'url':
            statusStr = url(value)
        elif methodType == 'file':
            statusStr = file(value)
        else:
            statusStr = 'Error: method {} not supported. \n'.format(value)
        if statusStr:
            return HttpResponseBadRequest('ERROR: {} \n{}'.format(statusStr, help()) )
        return HttpResponse('fin')


def help():
    return ('Documentation <br />  \
            Receives a text input and counts the number of appearances for each word in the input. <br />  <br /> \
            Possible responses: <br /> \
            status 200 - success <br /> \
            status 400 - invalid request <br /> <br /> \
            usage: <br /> \
            - A simple string sent in the request. <br /> \
              eg. wordcounter?string=my totally cool string <br /> <br />\
            - A file path (the contents of the file will be used as input). <br /> \
              eg. wordcounter?file=filePath <br /> <br />\
            - A URL (the data returned from the URL will be used as input). <br /> \
              eg.wordcounter?url = my.url.com ')


def url(url):
        if not url:
            return 'ERROR: missing url in body.'
        validate = URLValidator(schemes=('http', 'https')) #'ftp', 'ftps'
        try:
            validate(url)
        except ValidationError as e:
            print(str(e))
            return 'ERROR: invalid url provided. {}'.format(url)
        print('got valid url: {} . start fetching'.format(url))
        buffer = getUrlContent(url)
        print('got content. sending to processing')

        core.countWordsFromString(buffer)

        print('finished')
        return ''


def getUrlContent(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return response.read().decode("utf-8")


# validate file is readable, if so enqueue to backgound process the filepath
def file(filePath):
        if not filePath:
            return 'ERROR: missing filePath in body.'
        tupleIsValid = core.isPathValidForRead(filePath)
        if not tupleIsValid[0]: #boolean
            return 'ERROR: {}  {}'.format(tupleIsValid[1], filePath)

        core.queue.put(item=filePath)
        print('finished')
        return ''