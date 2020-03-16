from reverse import reverse_valence
# from retrieve import retrieveCommonSense
from rank import rankContext
import sys
utterance = sys.argv[1]
rov = reverse_valence(utterance)
# commonsense, extra = retrieveCommonSense(rov)
mostincongruent = rankContext(rov,'jealousy','')

sarcasm = rov+mostincongruent
print(sarcasm)
