###################################################################################
# File_name : IndusNLPTookit.py             #Autor_name: Nikhil Malhotra
#Authoring Start date: 6/9/2023
# Change markers
# M0001 : Putting a code for replacing . with पूर्ण विराम (|)
##################################################################################
import os
import re
import string
import numpy as np

import nltk
from nltk.corpus import indian
from nltk.tag import tnt
import string

from logging import raiseExceptions


class Toolkit:


  # Init function
  def __init__(self):
    #List of punctuations that are available in the language
    # पूर्ण विराम (|) , अल्प विराम (,) , अर्ध विराम (;) , प्रशनवाचक चिन्ह (?)
    # विस्मयादिवाचक चिन्ह (!) , योजक (‐) , उद्धरण चिन्ह (” “), विवरण चिन्ह (:-)
    self.hindi_punctuations = ['।',',',';','?','!','-','"',':-','#','.']
    self.numbers = ['१','२','३','४','५','६','७','८','९']
    #List of dialect data
    # hi: Hindi, do: Dogri, ki:Kinnauri,ka:Kangri,ch:Chambeali,gh:Garhwali , ku:Kumaoni
    # ja: Jaunsari,bb: Brij Bhasha, kn: Kannauji, bu:Bundeli,ba:Bagheli,aw:Awadhi,
    # bh: Bhojpuri, ma:Magahi,ml:Maithili,an:Angika,na:Nagpuri,kh:Khortha,km:Kurmali
    # mu: Mundari, pp: Panch Pargania,ch:Chattisgarhi,su:Surgujja,ni:Nimadi,mv: Malvi,
    # mr:Marwari, dh: Dhundhari,ha: Harauti,wa: Wagdi,sh:Shekhawati,da:Hyderabadi Dakhni,
    # mhi : Mumbai hindi
    self.dialects = [
                        'hi','do','ki','ka','ch','gh','ku','ja','bb','kn','bu',
                         'ba','aw','bh','ma','ml','an','na','kh','km','mu','pp',
                         'ch','su','ni','mv','mr','dh','ha','wa','sh','da','mhi']

    #To be changed as per requirement.Directory is where we keep all dialect files
    self.dir_path = "Data/stopwords/"


  # THis function helps to remove english words and converts numbers to 
  # hindi format from a text
  def clean_text(self,text):
    english_text = re.findall("[a-zA-Z]", text)
    english_numbers = re.findall("[1-9]", text)
    for char in english_text:
        text = text.replace(char,"#")
    for number in english_numbers:
        text = text.replace(number,self.numbers[int(number)-1])
    return (text , english_text)  


  # THis function helps find stopwords in a language and doalect
  def find_stopwords(self,dialect):
    _arrstopwords = []
    if dialect in self.dialects:
      #Figure out the stop words file
      try:
        file_name = dialect + "_stopwords.txt"
        file_path = os.path.join(self.dir_path,file_name)
        with open(file_path,'r' , encoding="UTF-8") as f:
          txt = f.readlines()
        for item in txt:
          _arrstopwords.append(item.replace("\n",""))
      except:
        raise FileNotFoundError("File not found")
    else:
      print("Sorry! The intended dialet is not available")
    return _arrstopwords


  # This function tokenizes given text into words
  def word_tokenize(self,input_text):
    #Remove punctuations if they occur in the text
    for punc in self.hindi_punctuations:
      if punc != "-":
        input_text = input_text.replace(punc,"")
    #White space tokenization
    _word_list = input_text.split(' ')
    return _word_list


  #This function tokenizes given text into sentences
  def sent_tokenize(self,input_text):
    #Purna Viram tokenization
    #### M0001 starts ###################
    #Use this if necessary..........
      #_sent_list_temp = input_text.replace('.','।')
      #_sent_list = _sent_list_temp.split('।')
    #Use this if necessary.........
    _sent_list = input_text.split('।')
    #### M0001 ends
    for sentence in _sent_list:
      if '\n' in sentence:
        _temp = sentence
        print(_temp)
        _sent_list.remove(sentence)
        _sec_sent_list = sentence.split('\n')
        _sent_list.append(_sec_sent_list)
    return _sent_list



  #This funtion provides word freuency
  def word_freq(self,input_text):
    _tokenized_word_list = self.word_tokenize(input_text)
    _frequency_tuple = []
    for word in _tokenized_word_list:
      matches = [match for match in _tokenized_word_list if word in match]
      _frequency_tuple.append((word,len(matches)))
    return _frequency_tuple

  
  #This function maps words to id and id to tokens
  def mapping(self, tokens):
    word_to_id = {}
    id_to_word = {}

    for i, token in enumerate(set(tokens)):
        word_to_id[token] = i
        id_to_word[i] = token
    return word_to_id, id_to_word


  #Function to train for POS
  def tagger_train(self):
    taggedSet = "hindi.pos"
    wordSet = indian.sents(taggedSet)
    count = 0
    print(wordSet[0])
    for sen in wordSet:
        count = count + 1
        sen = "".join(
            [
                " " + i if not i.startswith("'") and i not in string.punctuation else i
                for i in sen
            ]
        ).strip()
        #print(count, sen, "sentences")
    #print("Total sentences in the tagged file are", count)

    trainPerc = 0.9

    trainRows = int(trainPerc * count)
    testRows = trainRows + 1

    data = indian.tagged_sents(taggedSet)
    train_data = data[:trainRows]
    test_data = data[testRows:]

    print("Training dataset length: ", len(train_data))
    print("Testing dataset length: ", len(test_data))

    pos_tagger = tnt.TnT()
    pos_tagger.train(train_data)
    print("Accuracy: ", pos_tagger.evaluate(test_data))
    return pos_tagger

  #This function helps find POS tags
  def pos_tags(self,input_text):
    tokens = self.word_tokenize(input_text)
    pos_tagger = self.tagger_train()
    _tags = pos_tagger.tag(tokens)
    return _tags