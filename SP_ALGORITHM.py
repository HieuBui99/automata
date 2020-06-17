def RemovingPrefixOfWord(setOfPrefixs, w):
  for p in setOfPrefixs:
    if w.startswith(p):
      yield w[len(p):]
  return 

def CodeWordPrefix(setOfPrefixs, ws):
  """Trả về tập các suffix của tất cả các từ trong ws sau khi 
  sử dụng phép cắt trái (RemovingPrefixOfWord) trong tập setofPrefixs"""
  setOfSuffixs = set()
  for w in ws:
    for q in RemovingPrefixOfWord(setOfPrefixs, w):
      if q != '':
        setOfSuffixs.add(q)
        #print(q)
  if setOfSuffixs:
    print("Set Of Suffixs = ", str(setOfSuffixs))

  return setOfSuffixs

def SPAlgorithm(X):
  """Kiểm định mã sử dụng thuật toán Sardinas-Patterson (SP Algorithm)"""
  NL, i = len(str(X)) * len(str(max(len(x) for x in X))), 1
  U = CodeWordPrefix(X, X) # U1 = X^-1.X \ {epsilon}
  U.discard('')
  if len(U) == 0:
    print("X là mã!")
    return True
  while '' not in U and len(U & X) == 0:
    t = CodeWordPrefix(X, U) | CodeWordPrefix(U, X)
    if t == U or i > NL + 1:
      print("X là mã!")
      return True
    U = t
    i += 1
  if '' in  U:
    print("Dangling empty suffix!!")
  for x in U & X:
    print("X không phải là mã. Bởi vì nó chứa Dangling suffix: {}".format(x))
  return False

if __name__ == '__main__':
    SetOfCodewords = {'xyx', 'xxxy', 'xyyx', 'yyxx', 'xxxyy', 'xxyyx', 'yyyyx', 'yxyxyy'}
    print('The Set of Codewords', SetOfCodewords)
    SPAlgorithm(SetOfCodewords)

# OUTPUT:

#The Set of Codewords {'xxxy', 'xxyyx', 'yyyyx', 'xyx', 'yyxx', 'xyyx', 'yxyxyy', 'xxxyy'}
#Set Of Suffixs =  {'y'}
#Set Of Suffixs =  {'xyxyy', 'yyyx', 'yxx'}
#Set Of Suffixs =  {'yy'}
#Set Of Suffixs =  {'yyx', 'xx'}
#Set Of Suffixs =  {'yyx', 'x', 'xy', 'xyy'}
#Set Of Suffixs =  {'xyyx', 'yyx', 'xxyy', 'xxy', 'x', 'yx'}
#X không phải là mã. Bởi vì nó chứa Dangling suffix: xyyx