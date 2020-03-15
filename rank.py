import torch
import numpy
from sentence_retriever import getSentences
from grammar import correct_grammar

roberta = torch.hub.load('pytorch/fairseq', 'roberta.large.mnli')

def getContradictionScores(sentences,rov):
	scores = []
	for sent in sentences:
		sent = correct_grammar(rov,sent)
		tokens = roberta.encode(rov, sent)
		value = roberta.predict('mnli', tokens).detach().numpy()
		value = round(value[0].tolist()[0],3)
		scores.append((value,sent))

	return scores


def rank_sentences_based_on_contradiction(sentences,rov):
	scores = getContradictionScores(sentences,rov)
	scores.sort(key = lambda x: x[0],reverse=True) 
	for s in scores:
		print(s)
	return scores[0] #for NSI return a random index




def rankContext(rov,commonsense,extra=''):
	sentences = getSentences(commonsense,rov)
	if extra!='':
		for i in range(len(sentences)):
			sentences[i] = sentences[i].replace(commonsense,commonsense+' '+extra)
	mostcontradictory = rank_sentences_based_on_contradiction(sentences,rov)
	return mostcontradictory[1]



rankContext("Tacobell got my order wrong again.","angry")




	