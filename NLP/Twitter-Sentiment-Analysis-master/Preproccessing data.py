import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
import pickle
stop_words= set(stopwords.words("english"))
from nltk.corpus import wordnet

neg_rev=open("/Users/pushkarsingh/Desktop/negative.txt","rb").read()
pos_rev=open("/Users/pushkarsingh/Desktop/positive.txt","rb").read()

pos=[]
neg=[]

for rev in pos_rev.splitlines():
    pos.append(rev)

for rev in neg_rev.splitlines():
    neg.append(rev)

pos_words=[]
neg_words=[]    

for pos_line in pos:
    pos_words.append(word_tokenize(str(pos_line)))

for neg_line in neg:
    neg_words.append(word_tokenize(str(neg_line)))


pos_words_new=[]
neg_words_new=[]    

for line in pos_words:
    for words in line:
        pos_words_new.append(words)

for line in neg_words:
    for words in line:
        neg_words_new.append(words)

pos_words_new_stopwords=[]
neg_words_new_stopwords=[]
        
for words in pos_words_new:
    if words not in stop_words:
        pos_words_new_stopwords.append(words)

for words in neg_words_new:
    if words not in stop_words:
        neg_words_new_stopwords.append(words)


tagged_pos=[]
tagged_neg=[]
pos_adj=[]
neg_adj=[]
tagged_pos.append(nltk.pos_tag(pos_words_new_stopwords))
for i in range(len(tagged_pos[0])):
    if tagged_pos[0][i][1]=="JJ":
        try:
            pos_adj.append((tagged_pos[0][i][0]))
        except Exception as e:
            print(str(e))
            
tagged_neg.append(nltk.pos_tag(neg_words_new_stopwords))
for i in range(len(tagged_neg[0])):
    if tagged_neg[0][i][1]=="JJ":
        neg_adj.append((tagged_neg[0][i][0]))


        
for i in pos_adj:
    if i in neg_adj:
        pos_adj.remove(i)
        neg_adj.remove(i)
        
pos_syn=[]
neg_syn=[]

for words in pos_adj:
    for syn in wordnet.synsets(words):
        for syn_word in syn.lemmas():
            pos_syn.append(syn_word.name())

for words in neg_adj:
    for syn in wordnet.synsets(words):
        for syn_word in syn.lemmas():
            neg_syn.append(syn_word.name())

pos_syn= list(set(pos_syn))
neg_syn= list(set(neg_syn))

for words in pos_adj:
    pos_syn.append(words)

for words in neg_adj:
    neg_syn.append(words)
        
pos_adj_FreqDist=dict(nltk.FreqDist(pos_syn))
neg_adj_FreqDist=dict(nltk.FreqDist(neg_syn))


pos_dict={}
neg_dict={}
count=0

for key1, value1 in pos_adj_FreqDist.items():
    for key2, value2 in neg_adj_FreqDist.items():
        if key1==key2:
            count+=1
            if(value1>value2):
                value1=value1-value2
                value2=0
                pos_dict.update({key1:value1})
            elif (value2>value1):
                value2=value2-value1
                value1=0
                neg_dict.update({key2:value2})

tagged_neg_dict=[]
tagged_pos_dict=[]
tagged_neg_dict_list=[]
tagged_pos_dict_list=[]


tagged_pos_dict.append(nltk.pos_tag(pos_dict.keys()))
for i in range(len(tagged_pos_dict[0])):
    if tagged_pos_dict[0][i][1]=="JJ":
        tagged_pos_dict_list.append(tagged_pos_dict[0][i][0])
        
tagged_neg_dict.append(nltk.pos_tag(neg_dict.keys()))
for i in range(len(tagged_neg_dict[0])):
    if tagged_neg_dict[0][i][1]=="JJ":
        tagged_neg_dict_list.append((tagged_neg_dict[0][i][0]))


pos_dict_updated={}
neg_dict_updated={}

for key1, value1 in pos_dict.items():
    for i in range(len(tagged_pos_dict_list)):
        if key1==tagged_pos_dict_list[i]:
            pos_dict_updated.update({key1:value1})

for key1, value1 in neg_dict.items():
    for i in range(len(tagged_neg_dict_list)):
        if key1==tagged_neg_dict_list[i]:
            neg_dict_updated.update({key1:value1})


            
pickle_in=open("/Users/pushkarsingh/Desktop/twitter/pos-yy_adj.pickle","wb")
pickle.dump(pos_dict_updated,pickle_in)
pickle_in.close()

pickle_in=open("/Users/pushkarsingh/Desktop/twitter/neg-yy_adj.pickle","wb")
pickle.dump(neg_dict_updated,pickle_in)
pickle_in.close()        
