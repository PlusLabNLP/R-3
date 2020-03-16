def correct_grammar(utterance1,utterance2):
	utterance1 = utterance1.split()
	utterance2 = utterance2.split()
	if utterance1[0].lower() in ['i','my']:
		if utterance2[0].lower() in ['his','her']:
			utterance2[0]='My'
		if utterance2[0].lower() in ['he','she'] and utterance2[1] in ['is','was']:
			utterance2[0]='I'
			utterance2[1] = 'am'
		if utterance2[0].lower() in ['he','she']:
			utterance2[0]='I'
	else:
		if utterance1[0].lower() not in ['his','her']:
			if utterance2[0].lower() in ['his','her']:
				utterance2[0]='My'
		if utterance1[0].lower() not in ['he','she']:
			if utterance2[0].lower() in ['he','she'] and utterance2[1] in ['is','was']:
				utterance2[0]='I'
				utterance2[1] = 'am'
			if utterance2[0].lower() in ['he','she']:
				utterance2.pop(0)
			for i in range(1,len(utterance2)):
				if utterance2[i] in ['his','her']:
					utterance2[i]='my'
	return ' '.join(utterance2).capitalize()
