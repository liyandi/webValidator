# -*- coding: utf-8 -*-
#!/usr/bin/python                        
##################################################
# AUTHOR : Yandi LI
# CREATED_AT : 2015-12-06
# LAST_MODIFIED : 2015-12-06 21:51:23
# USAGE : python core.py column
# PURPOSE : TODO
##################################################
import math
import unicodedata
import pkgutil

class Hans(object):
  """ Check if a chinese sentence is correctly encoded. 
  ===============================================
  * Training
    - In the 'training' phase, we extract title and summary part from news over the 
      last five months. 
    - We count the document frequencies and filter those characters with 
      less than 1000 document occurrences, besides some quick fixes. 
    - After all, our dictionary consists of around 5000 unique chinese characters.
  ===============================================
  * Predict
    - For a given text sentence, assume that characters appears independently given the sentence.
      So we can easily compute the likelihood based on historical frequenciies .
    - For unknown characters, we treat them as if they appear once in the history. 
    - Romain characters, symbols, numbers are neglected.
    - For empty strings, we assume they are valid.
  """

  @staticmethod
  def _config():
    file_path = 'conf/common_chars.conf'
    charcnt = {}
    try:
      data = pkgutil.get_data("webValidator", file_path)
      for line in data.decode('utf-8').splitlines():
        try:
          char, cnt = line.split(' ')
          charcnt[char] = int(cnt)
        except:
          raise 
    except IOError:
      raise ValueError(
            "Stoplist %s for Chinese is missing. "
            "and feel free to contribute by your own stoplist." % 'common_chars.conf'
            )

    # compute log-probabilities of each character
    _TOTAL_CHAR_PROB = math.log10(sum(charcnt.itervalues()))
    _CHARDF = dict((char, math.log10(cnt) - _TOTAL_CHAR_PROB) for char,cnt in charcnt.iteritems())
    _MIN_CHAR_PROB = math.log10(min(charcnt.itervalues())) - _TOTAL_CHAR_PROB # minimum log-prob
    _MAX_CHAR_PROB = math.log10(max(charcnt.itervalues())) - _TOTAL_CHAR_PROB # maximum log-prob
    return _CHARDF, _MIN_CHAR_PROB, _MAX_CHAR_PROB, _TOTAL_CHAR_PROB

  _CHARDF, _MIN_CHAR_PROB, _MAX_CHAR_PROB, _TOTAL_CHAR_PROB = _config.__get__(None, object)()# _config.__func__()  #in python2.7     


  @classmethod
  def _likelihood(cls, sentence, smooth=1):
    """ Compute the log-likelihood of a sentence assuming that characters are independent
    @Parameters
    ------------------------
    | smooth: default count for a unknown character, take value > 0
    @Returns
    ------------------------
    | log-likelihood of the sentence 
    >>> _likelihood(u"沈阳：大二大三忙创业 毕业转身去择业") # good
    -3.022006128864273
    >>> _likelihood(u"銝箸隞砌飽銝敺憭") # bad
    -7.507283853858208
    >>> _likelihood(u"甇瘨衣")  # bad
    -7.375815184206794
    >>> _likelihood(u"【公　告】") # good
    -2.692653943384265
    >>> _likelihood(u"梢▼撠")  # bad
    -5.815355635777318
    >>> _likelihood(u"") # empty string, use maximal count as prior
    -1.5816035211996278
    >>> _likelihood(u"Revelation") # empty string, use maximal count as prior
    -1.5816035211996278
    """
    assert smooth > 0
    log_smooth = math.log10(smooth) - cls._TOTAL_CHAR_PROB
    log_like = 0.0
    alphabets = [c for c in cls._alphabetic(sentence)]
    for c in alphabets:
      log_like += cls._CHARDF.get(c, log_smooth)
    log_like = log_like / len(alphabets) if alphabets else cls._MAX_CHAR_PROB
    return log_like

  
  @staticmethod
  def _alphabetic(sentence):
    """ generate alphabetic characters in the sentence
    >>> for i in _alphabetic(u"我们是？abcДφŌ§<《偬兟◢"): print i,
    我 们 是 偬 兟
    """
    ALPHABETIC = ['Lm', 'Lo'] # 'Lu', 'Lo', 'Lt' -> romain letters, 'Nl'-> number letter, etc.
    for c in sentence:
      if unicodedata.category(c) in ALPHABETIC:
        yield c


  @classmethod
  def validate(cls, sentence, return_prob=False, MIN_LOG_LIKE=-5):
    """ Main, check if a text string has been rightly encoded. 
    Romain characters, symbols, numbers are neglected.
    @Parameters
    ----------------------
    | sentence: a unicode string
    | MIN_LOG_LIKE: threshold of the log-likelihood. Sentences with higher likelihood will validate. 
    |               The default value -5 is a good one, as the minimal likelihood of a 
    |               single valid char is around -6, itself being more or less on the boundary
    | return_prob: whether to return the value of log-likelihood
    @Returns
    ----------------------
    | True/False, log-likehood
    >>> core.Hans.validate(u"我们是？abcДφŌ§<《偬兟◢", return_prob=True)
    (False, -5.2000414461180196)
    >>> core.Hans.validate(u"我们是？bcДφŌ§<《◢", return_prob=True)
    (True, -2.5054545978898513)
    """
    assert isinstance(sentence, unicode)
    prob = cls._likelihood(sentence)
    if return_prob:
      return prob > MIN_LOG_LIKE, prob
    else:
      return prob > MIN_LOG_LIKE
    


if __name__ == "__main__":
  
  import sys

  fname = sys.argv[1]
  f = open(fname)
  fout = open(fname + '_out', 'w')

  for line in f:
    line = line.rstrip('\r\n')
    r, p = Hans.validate(line.decode('utf-8'), return_prob=True)
    fout.write(line + '\t' + str(r) + '\t' + str(p) + '\n')





