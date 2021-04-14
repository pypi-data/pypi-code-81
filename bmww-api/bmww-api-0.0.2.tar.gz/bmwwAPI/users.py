import bs4
import requests
import sys
from bs4 import BeautifulSoup as soup

class users():
    def __init__(self, uiD):
        #This gets the user url
        self.uiD = str(uiD)
        self.user_page = requests.get('https://batmanwonderwoman.com/fanfiction/viewuser.php?uid=' + self.uiD + '&sort=update').text
        self.user_page_url = requests.get('https://batmanwonderwoman.com/fanfiction/viewuser.php?uid=' + self.uiD + '&sort=update')
        self.user_soup = soup(self.user_page, "html.parser")
        #If the user doesn't exist
        try:
            self.member_time = self.user_soup.select('#biocontent .label')[0].next_element.next_element.string
            if self.member_time == '12.31.1969':
                print("This id doesn't lead to any username")
                sys.exit()
            #Checks for user characteristics that are always there
            self.penname = self.user_soup.select('#biotitle .label')[0].next_element.next_element[:-3]
        except:
            pass
        else:
            #If the user exists
            print("If these fields are empty in the user's profile, an empty string will be returned")
            #Checks for user characteristics that may or may not be there
            self.penname = self.user_soup.select('#biotitle .label')[0].next_element.next_element[:-3]
            self.real_name = self.user_soup.select('#biotitle .label')[1].next_element.next_element.string
            self.member_status = self.user_soup.select('#biocontent .label')[1].next_element.next_element
            self.bio = [x.text for x in self.user_soup.select('#biocontent p')]
            self.user_url = self.user_page_url.url
            try:
                self.beta_reader = self.user_soup.select('.authorfields .label')[0].next_element.next_element.string
                self.gender = self.user_soup.select('.authorfields .label')[1].next_element.next_element.string
                self.recent_story = self.user_soup.select('.title a')[0].string
                self.stories = self.user_soup.select('#active a')[0].next_element.next_element.string.strip()
                self.series = self.user_soup.select('#tabs span')[1].next_element.next_element.next_element.string.strip()
                self.reviews = self.user_soup.select('#tabs span')[2].next_element.next_element.next_element.string.strip()
                self.challenges = self.user_soup.select('#tabs span')[3].next_element.next_element.next_element.string.strip()
                self.favorite_series = self.user_soup.select('#tabs span')[4].next_element.next_element.next_element.string.strip()
                self.user_favorites = self.user_soup.select('#tabs span')[5].next_element.next_element.next_element.string.strip()
            except:
                print('If an error was raised, the user may not have this information on their profile')
                self.stories = self.user_soup.select('#active a')[0].next_element.next_element.string.strip()
                self.series = self.user_soup.select('#tabs span')[1].next_element.next_element.next_element.string.strip()
                self.reviews = self.user_soup.select('#tabs span')[2].next_element.next_element.next_element.string.strip()
                self.challenges = self.user_soup.select('#tabs span')[3].next_element.next_element.next_element.string.strip()
                self.favorite_series = self.user_soup.select('#tabs span')[4].next_element.next_element.next_element.string.strip()
                self.user_favorites = self.user_soup.select('#tabs span')[5].next_element.next_element.next_element.string.strip()
            else:
                pass
