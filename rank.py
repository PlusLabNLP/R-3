import torch
import numpy
from sentence_retriever import getSentences
from grammar import correct_grammar
from loadconfig import loadConfig


roberta = torch.hub.load('pytorch/fairseq', 'roberta.large.mnli')
roberta.eval()
correct_phrase = loadConfig('Rank')

def getContradictionScores(sentences,rov):
	scores = []
	gender = ''
	for sent in sentences:
		sent,gender = correct_grammar(rov,sent,gender)
		tokens = roberta.encode(rov, sent)
		value = roberta.predict('mnli', tokens).detach().numpy()
		value = round(value[0].tolist()[0],3)
		scores.append((value,sent))

	return scores


def rank_sentences_based_on_contradiction(sentences,rov):
	scores = getContradictionScores(sentences,rov)
	scores.sort(key = lambda x: (x[0],-len(x[1].split())),reverse=True) 
	return scores[0] #for NSI return a random index




def rankContext(rov,commonsense,extra=''):
	sentences = getSentences(commonsense,rov)
	if extra!='':
		for i in range(len(sentences)):
			if commonsense in correct_phrase:
				replacement = commonsense+' '+extra
			else:
				replacement = extra+' '+commonsense
			if replacement not in sentences[i]:
				sentences[i] = sentences[i].lower().replace(commonsense,replacement).capitalize()
	print("Rov is",rov)
	mostcontradictory = rank_sentences_based_on_contradiction(sentences,rov)
	return mostcontradictory[1]



# rankContext("Flu is great.","accident")




	