webValidator
===============================
Intended to provide a tool to identify main text part on a webpage

This work is done primarily for creating a universal framework for my recent project, 
called [Weibo Toutiao](https://play.google.com/store/apps/details?id=com.sina.app.weiboheadline), 
a news provider that collects data shared by users on weibo.com. 

---
To install, simply do `python setup.py install --user`
    
Then to use the module:

    >>> import webValidator as W

---

#### 1. Hans
判定一段文字是否是乱码。Check if a Chinese sentence is correctly encoded. 

**Training**

  - In the 'training' phase, we extract title and summary part from news over the 
    last five months. 
  - We count the document frequencies, filter those characters that appears in 
    less than 1000 documents, besides some manual quick fixes. 
  - After all, the whole dictionary consists of around 5000 unique Chinese characters.

**Predict**

  - For a given text sentence, assume that each characters appears independently.
    We can easily compute the joint likelihood based on our historical frequenciies .
  - For unknown characters, treat them as if they appear just once in the history. 
  - Romain characters, symbols, numbers are neglected.
  - For empty strings, we assume they are valid.

We use some examples to demonstrate the basic use of these units.


    >>> W.Hans.validate(u"我们是？abcДφŌ§<《偬兟◢", return_prob=True) # bad case
    (False, -5.2000414461180196)
    >>> W.Hans.validate(u"我们是？bcДφŌ§<《◢", return_prob=True) # good case
    (True, -2.5054545978898513)
    >>> W.Hans.validate(u'u"銝箸隞砌飽銝敺憭"',True) # bad case
    (False, -7.507283853858208)
    >>> W.Hans.validate(u'梢▼撠',True) # bad case
    (False, -5.815355635777318)
    >>> W.Hans.validate(u'',True) # good case, if empty
    (True, -1.5816035211996278)                        
    >>> W.Hans.validate(u"Revelation",True) # good case, if no chinese characters
    (True, -1.5816035211996278)                        
    >>> W.Hans.validate(u"【公　告】",True) # good case, short
    (True, -2.692653943384265)

The threshold of the log-likelihood has been chosen as -5.
Sentences with higher likelihood will validate. 
I choose this number mainly based on some trial and errors. As an addition justification,
the minimal log likelihood of a single character in my dictionary is around -6, 
thus the threshold -5 is probably a nice guess of the boundary.

You are free to play around with the threshold to suit your own case.

To be continued...

