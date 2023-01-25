from cmath import inf
from logging import exception
from bs4 import BeautifulSoup
import requests
from csv import writer


url = 'https://wowpedia.fandom.com/wiki/Novel_guide'
get_site = requests.get(url)

soup = BeautifulSoup(get_site.content, 'html.parser')

parent_books = soup.find(class_="mw-parser-output")
books = parent_books.findChildren("ol", recursive=False)


with open('WoW-books.csv', 'w', encoding='utf8', newline='') as f:
    
    header = ['Book Title', 'Author', 'Series']
    w = writer(f)
    w.writerow(header)


    for child in books:
        # Array for the right formatting
        info = []
        # Cleaning the retrieved info
        curr_book = child
        curr_book = curr_book.text.replace('\n', ',').split(',')
        # Appending all the elements after formatting them
        info.append(curr_book)
        

        for element in info[0]:
            
            og_series = ['Day of the Dragon','Lord of the Clans','The Last Guardian']

            try:
                # WoA books have no author specified the same way as the rest
                if ' by ' not in element: 
                    
                    book_title = element
                    book_author = 'Richard A. Knaak'
                    book_series = soup.find(id='War_of_the_Ancients').text
                    
                    #writing to .csv
                    to_write = [book_title, book_author,book_series]
                    w.writerow(to_write)
                
                else:
                    book_title = str(element.split(' by ')[0]) 
                    book_author = str(element.split(' by ')[1])
                    
                    # need to split between OG series and WoW series
                    if book_title in og_series: 
                        book_series = soup.find(id='Original_series').text
                    else:
                        book_series = soup.find(id='WoW_imprint').text[:3]
        
                    to_write = [book_title, book_author,book_series]
                    w.writerow(to_write)

            except Exception as exception:
                print('Oops! Something broke.')
            

