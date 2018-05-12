import asyncio
import os
import re
import threading
from datetime import datetime
from queue import Queue
from django.conf import settings
from wordStatistics.models import wordInfo

queue = Queue()


def background():
    while True:
        if not queue.empty():
            fileName = queue.get()
            # we validate filepath upon receiving of request,
            # however the file could be deleted while waiting in queue, this is why we revalidate now.
            if isPathValidForRead(fileName):
                print('background: start {}'.format(fileName))
                countWordsFromFile(fileName)


t = threading.Thread(target=background)
t.daemon = True
t.start()
# TODO: need to join thread on exit

def countWordsFromFile(validFilePath):
    t1 = datetime.now()
    with open(validFilePath, 'r', encoding="utf8") as f:
        for line in f:
            # print('entering countWordsFromString with buffer size: {}'.format(len(line)))
            countWordsFromString(line)
    fileSize = os.stat(validFilePath).st_size
    t2 = datetime.now()
    timeDiff = t2 - t1
    print('finished handling file request. '
          'file size:{} KB time(seconds): {}'.format(fileSize//1024, timeDiff.total_seconds()))


# call this function either with small buffer or on background
def countWordsFromString(buffer):
    lst = re.split(regexForSupportedLetters(), buffer)
    print(lst)
    for word in lst:
        if len(word) > 1:
            addWordToDB(word)
    if settings.DEBUG:
        print(wordInfo.objects.all())
    print('in string func')

# for new supported language please edit the regex here
# currently support English and Hebrew. word is defined as two or more letters having no non alphanumeric characters
# eg. "it's" would be understood as "it"
def regexForSupportedLetters():
    return '[^a-zA-Zא-ת]'


#######  DB stuff ################
def addWordToDB(word):
    word = word.lower()
    querySet = wordInfo.objects.filter(word=word)
    if not querySet:
        wordInfo(word=word, count=1).save()
    else:
        wordinfo = querySet.get()
        wordinfo.count += 1
        wordinfo.save()


def getFromDBCount(word):
    word = word.lower()
    querySet = wordInfo.objects.filter(word=word)
    if not querySet:
        return 0
    else:
        return querySet.get().count


#######  end DB stuff #############

# return tuple of boolean which indicate whether path is valid and an error string
def isPathValidForRead(filePath):
    if not os.path.exists(filePath):
        return False, 'file does not exist'
    try:
        open(filePath, 'r').close()
        return True, ''
    except PermissionError as e:
        return False, 'no permissions to read file {}'.format(e)
    except Exception as e:
        return False, str(e)
