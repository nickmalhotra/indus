# indus
Toolkit for Indus project

INdus NLP Toolkit.py is just an addendum on top of Indian NLTK so that some work needed for NLP purpose for Indus project cna be done .The repository is free to use to tokenize words in 40+ Hindi dialects , clean english words etc. 
There is a test file also given to tet the code 

Data/Stopwords repository has the stopwords needed .Currently there are stop words for Hindi and its dialects like maithili. More are in the process and will be added soon  

General usage 
> python test_indus_toolkit.py 

In test_indus_toolkit
import os
import string
import numpy as np
from IndusNLPToolkit import Toolkit

ip = Toolkit()
print(ip.pos_tags("हाय मेरे कोल 10000 स्टिकर न"))

print(ip.clean_text("हाय मेरे कोल 10000 स्टिकर न"))

etc...

