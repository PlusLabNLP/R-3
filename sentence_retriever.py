import os
from urllib.parse import quote
import nltk

words = []

def islenPermissible(rov,retrieved):
	tokens = nltk.word_tokenize(rov)
	tokens1 = nltk.word_tokenize(retrieved)
	if len(tokens1)>2*len(tokens):
		return False
	return True

def getAllConcepts():
    for line in open('./data/concept.txt'):
        words.append(line.strip())
    return words


def updateConcept(concept):
    f = open('./data/concept.txt','a')
    f.write('\n')
    f.write(concept+'\n')


def filterSentences(keyword,sentences,utterance):
	s = []
	for sent in sentences:
		sent = sent.lower()
		if sent.startswith(keyword) or sent.endswith(keyword) or sent.endswith(keyword+'.') or sent.endswith(keyword+'?'):
			if islenPermissible(utterance,sent):
				s.append(sent.capitalize())
	return s


def isPageInValid(f):
    elem = f.split('<div id="all">')
    if len(elem)==1:
        return True
    return False

def getLast(f):
    if '>last<span style=' in f:
        elem = f.split('>last<span style=')
        last = int(elem[0].split('a href="')[-1].split('_')[1].replace('.html"',''))
        return last
    else:
        return 1

def getSentencesOnline(keyword):
    f1 = open('./data/corpus.txt','a')
    flag = True
    if keyword in words:
        flag = False
    keyword = quote(keyword)
    originalurl = '"https://sentencedict.com/'+keyword+'.html"'
    url = originalurl
    command = 'wget '+originalurl+' -q -nv -O ./comet-commonsense/temp/sent.txt'
    os.system(command)
    f = open('./comet-commonsense/temp/sent.txt','r',encoding ='ISO-8859-1').read()
    c = 1
    if isPageInValid(f):
        return []
    else:
        s = []
        while True:
            if c>1:
                elem = f.split('<div id="all">')
                sentences = elem[1].split('</div></div>')[0]
                sentences = sentences.split('</div><div>')
                for line in sentences:
                    line = line.replace('<em>','')
                    line = line.replace('</em>','')
                    if len(line.split(', '))==2:
                        line = line.split(', ')[1]
                        if '</div>' in line:
                            continue
                        s.append(line)
                    elif len(line.split('. '))==2:
                        line = line.split('. ')[1]
                        if '</div>' in line:
                            continue
                        s.append(line)
                url = originalurl.replace(keyword,keyword+'_'+str(c))
                os.system('wget '+url+' -q -nv -O ./comet-commonsense/temp/sent'+str(c)+'.txt')
                f = open('./comet-commonsense/temp/sent'+str(c)+'.txt','r',encoding ='ISO-8859-1').read()
                if c>getLast(f):
                    break
            c = c+1
        if flag:
            f1.write('\n')
            for line in s:
                if 'Sentencedict' in line or 'nbsp' in line or 'href' in line:
                    continue
                f1.write(line+'\n')
        return s


def getSentences(keyword,utterance):
    concepts = getAllConcepts()
    if keyword in concepts:
        retrieval_corpus = open('./data/corpus.txt')
        sentences = [sent.strip() for sent in retrieval_corpus.readlines()]
        s = filterSentences(keyword,sentences,utterance)
        if len(s)>0:
            return s
    else:
        print("Entering here")
        sentences = getSentencesOnline(keyword)
        if len(sentences)>0:
            updateConcept(keyword)
        return filterSentences(keyword,sentences,utterance)











	