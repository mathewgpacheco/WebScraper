import requests
import random
import time
from bs4 import BeautifulSoup


class Control:

    def __init__(self):
        #stores all the quotes in an array
        self.collection = QuoteCollection()

        #stores tags of quotes in a dictionary
        self.tagCollection = TagMasterCollection()

    def load(self,int):
        #loads specified page
        URL = 'http://quotes.toscrape.com/page/'+ str(int) +'/'
        page = requests.get(URL).text
        soup = BeautifulSoup(page,'lxml')
        quotes = soup.find_all('div',attrs= {'class': 'quote'})

        #extract quotes
        for q in quotes:
            quote = Quote(q.span.text,q.small.text)
            tags = q.div.find_all('a',attrs= {'class':'tag'})
            
            #extract tags and add to tag collection
            for t in tags:
                quote.addTag(t.text)
                self.tagCollection.add(t.text)

            #add quote
            self.collection.add(quote)


    def showMenu(self):
        s = ''
        options = {}
        while True:

            #gets random tags from the tag collection to be displayed to the screen as an option
            for i in range(1,6):
                options[i] = self.tagCollection.get(random.randrange(self.tagCollection.getSize()))

            #display options to screen
            for i in range(1,6):
                s = s + '('+str(i)+')' +'  ' + options[i]+'\n'
            choice = int(input('Enter selection to recieve quote.\n' + s + '(0)  Exit\n\n'))
            if (choice == 0):
                return 0   
            for key in options:
                if(choice == key):
                    #returns the selected tag
                    return (options[choice])
            else:
                s= ''

    


    def launch(self):
    
        num_pages = int(input('Select number of pages to load(integer): '))
        if (num_pages == 0):
            return
        print('Loading pages..')
        for i in range(1,num_pages+1):
            self.load(i)
            #sleep to practice ethical scraping
            time.sleep(random.randrange(1,4))
            print('Loaded page '+ str(i))
        print('\n')

        while(1):
            choice = self.showMenu()
            if (choice == 0):
               return
            self.collection.find(choice)
    

    
class Quote:
    
    #Each quote will have their corresponding tags, and author
    def __init__(self,quote,name):
        self.quote = quote
        self.name = name
        self.tags = []

    #adds tag to the array
    def addTag(self,t):
        self.tags.append(t)
    
    #prints quote with tags
    def printQuote(self):
        print('\n'+self.quote)
        print(self.name)
        print('tags: ',end='')
        for i in range(len(self.tags)):
           print(self.tags[i]+', ', end="")
        print('\n')

class QuoteCollection:   
    
    def __init__(self):

        #main array to hold all quotes
        self.array = []

        #all quotes with a common tag is temporarily stored here
        self.Subset = []
    

    
    def add(self, quote):
        self.array.append(quote)
    
    #references the master quote collection to create a sub array of 
    #quotes that share the common specified tag
    def makeSubset(self,choice):
        for i in range(len(self.array)):
            for k in range(len(self.array[i].tags)):
                if (choice == self.array[i].tags[k]):
                    self.Subset.append(self.array[i])


    def find(self,key):
        self.makeSubset(key)
        #once the sub set is created, it will randomly select
        #a quote from the array and print it.
        choice = random.randrange(0,len(self.Subset))
        self.Subset[choice].printQuote()
        #resets the sub array
        self.Subset.clear()

class TagMasterCollection:
    
    #stores tags in a dictionary
    def __init__(self):
        self.dict = {}
        self.size =0

    def add(self,tag): 
        for i in range(self.size):
            #if tag already exists in the dictionary, don't add it
            if (self.dict.get(i) == tag):
                return
        #else add it to the back
        self.dict[self.size] = tag
        self.size= self.size + 1
    
    def get(self,i):
        return (self.dict.get(i))

    def getSize(self):
        return (self.size)

def main():
    control = Control()
    control.launch()


if __name__ ==  "__main__":
    main()


