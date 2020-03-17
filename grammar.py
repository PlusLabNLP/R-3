import requests, json

def correct_grammar(utterance1,utterance2,sex):
	print(utterance2)
	utterance1 = utterance1.split()
	utterance2 = utterance2.split()
	if sex=='':
		potential_name = utterance1[0]
		sex = getGenders(potential_name)[0][0]
		print(sex)
	

	if utterance1[0].lower() in ['i','my']:
		if utterance2[0].lower() in ['his','her']:
			utterance2[0]='My'
		if utterance2[0].lower() in ['he','she'] and utterance2[1] in ['is','was']:
			utterance2[0]='I'
			utterance2[1] = 'am'
		if utterance2[0].lower() in ['he','she']:
			utterance2[0]='I'
	elif sex == 'male' and utterance2[0].lower() in ['her','my']:
		utterance2[0]='his'
	elif sex == 'male' and utterance2[0].lower()=='i' and utterance2[1].lower()=='am':
		utterance2[0]='he'
		utterance2[1]='is'
	elif sex == 'male' and utterance2[0].lower()in ['she','i']:
		utterance2[0]='he'
	elif sex == 'female' and utterance2[0].lower() in ['his','my','him']:
		utterance2[0]='her'
	elif sex == 'female' and utterance2[0].lower()=='i' and utterance2[1].lower()=='am':
		utterance2[0]='she'
		utterance2[1]='is'
	elif sex == 'female' and utterance2[0].lower() in ['he','i']:
		utterance2[0]='she'
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
				if utterance2[i] in ['his','her'] and utterance2[i+1]!='to':
					utterance2[i]='my'
				elif utterance2[i] in ['his','her'] and utterance2[i+1]=='to':
					utterance2[i]='me'
	

	return ' '.join(utterance2).capitalize(),sex




def getGenders(names):
	url = ""
	cnt = 0
	if not isinstance(names,list):
		names = [names,]
	
	for name in names:
		if url == "":
			url = "name[0]=" + name
		else:
			cnt += 1
			url = url + "&name[" + str(cnt) + "]=" + name
		

	req = requests.get("https://api.genderize.io?" + url)
	results = json.loads(req.text)
	
	retrn = []
	for result in results:
		if result["gender"] is not None and result["probability"]>0.8:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			retrn.append((u'None',u'0.0',0.0))
	return retrn

