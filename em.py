import util
x=26+1
startProbs=[1.0/k for h in range(k)]
rawText=util.toIntSeq(util.readText("lm.train"))
transitioncounts=[[0 for h2 in range(k)] for h1 in range(k)]
for i in range(1,len(rawText)):
  h1=rawText[i-1]
  h2=rawText[i]
  transitionCounts[h1][h2]+=1
transitionProbs=[util.normalize(transitionCounts[h1])for h1 in range(k)]
emissionProbs=[[1.0/k for e in range(k)] for h in range(k)]
observations=util.toIntSeq(util.readText('ciphertext'))
n=len(observations)

for t in range(200):
  q=util.forwardBackward(observations,startProbs,transitionProbs,emissionProbs)
  print(util.toStrSeq([util.argmax(q[i]) for i in range(n)]))
  print('')
  emissionCounts=[[0 for e in range(k)]for h in range(k)]
  for i in range(n):
    for h in range(k):
      emissionCounts[h][observations[i]]+=q[i][h]
  emissionProbs=[util.normalize(emissionCounts[h]) for h in range(k)]