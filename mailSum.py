from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords




class utilityFunctions(object):

    def __init__(self):
        self.str1 = " "
        self.separator = ', '

    def mailSummary(self,res):

        summ_words = summarize(res, word_count = 100)
        return summ_words

    #----UTILITY START---#

    def listToString(self,s): 

        return (self.str1.join(s))


    def commaSep(self,data): 

        self.separator.join(data)

        return data


    def remove(self,string):
        
        if(type(string)==None.__class__):
            return "Missing Country"
        
        return string.replace(" ", "")

#----UTILITY END---#

