import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import time
import os

NCAAF   = 1
NFL     = 2
NBA     = 3
NCAAB   = 4
SOCCER  = 5
MLB     = 6

team_of_interest_list = ["Ohio State","Cincinnati","Xavier","Pittsburgh","Cleveland","Baltimore","Indianapolis"]

def connectTor():
  ## Connect to Tor for privacy purposes
     socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9150, True)
     socket.socket = socks.socksocket
     print("connected to Tor!")

def soup_url(type_of_line, sport, tdate = str(date.today()).replace('-','')):
## get html code for odds based on desired line type and date

  if type_of_line == 'Spreads':
      url_addon = ''
  elif type_of_line == 'ML':
      url_addon = 'money-line/'
  elif type_of_line == 'Totals':
      url_addon = 'totals/'
  else:
      print("Wrong url_addon")

  if(sport == NBA):
    url = 'https://classic.sportsbookreview.com/betting-odds/nba-basketball/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_5')[0]
    except:
        soup = None
  
  elif(sport == NFL):
    url = 'https://classic.sportsbookreview.com/betting-odds/nfl-football/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_16')[0]
    except:
        soup = None
    
  elif(sport == NCAAF):
    url = 'https://classic.sportsbookreview.com/betting-odds/college-football/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_6')[0]
    except:
        soup = None
    
  elif(sport == NCAAB):
    url = 'https://classic.sportsbookreview.com/betting-odds/ncaa-basketball/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_14')[0]
    except:
        soup = None
  
  elif(sport == SOCCER):
    url = 'https://classic.sportsbookreview.com/betting-odds/soccer/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    print(soup_big)
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_16')[0]
    except:
        soup = None
  
  elif(sport == MLB):
    url = 'https://classic.sportsbookreview.com/betting-odds/mlb-baseball/' + url_addon + '?date=' + tdate
    now = datetime.datetime.now()
    raw_data = requests.get(url)
    soup_big = BeautifulSoup(raw_data.text, 'html.parser')
    try:
        soup = soup_big.find_all('div', id='OddsGridModule_3')[0]
    except:
        soup = None
    
   
  timestamp = time.strftime("%H:%M:%S")
  return soup, timestamp
    
    


def parse_and_write_data(soup, date, time, not_ML = True):
## Parse HTML to gather line data by book
    def book_line(book_id, line_id, homeaway):
        ## Get Line info from book ID
        line = soup.find_all('div', attrs = {'class':'el-div eventLine-book', 'rel':book_id})[line_id].find_all('div')[homeaway].get_text().strip()
        return line
    '''
    BookID  BookName
    238     Pinnacle
    19      5Dimes
    93      Bookmaker
    1096    BetOnline
    169     Heritage
    123     BetDSI
    999996  Bovada
    139     Youwager
    999991  SIA
    '''              
    odds_list = []
                     
                     
    counter = 0
    try:
      number_of_games = len(soup.find_all('div', attrs = {'class':'el-div eventLine-rotation'}))
    except:
      return odds_list
    for i in range(0, number_of_games):
        A = []
        H = []
        
        ## Gather all useful data from unique books
        # consensus_data = 	soup.find_all('div', 'el-div eventLine-consensus')[i].get_text()
        info_A = 		        soup.find_all('div', attrs = {'class':'el-div eventLine-team'})[i].find_all('div')[0].get_text().strip()
        team_A =                info_A
        ## get line/odds info for unique book. Need error handling to account for blank data
        try:
            heritage_A =        book_line('169', i, 0)
        except IndexError:
            heritage_A = ''

        info_H = 		        soup.find_all('div', attrs = {'class':'el-div eventLine-team'})[i].find_all('div')[1].get_text().strip()
        team_H =                info_H

        try:
            heritage_H = 	    book_line('169', i, 1)
        except IndexError:
            heritage_H = '.'
            
        A.append('away')
        A.append(team_A)
        A.append(team_H)
        if not_ML:
            heritage_A = heritage_A.replace(u'\xa0',' ').replace(u'\xbd','.5')
            heritage_A_line = heritage_A[:heritage_A.find(' ')]
            heritage_A_odds = heritage_A[heritage_A.find(' ') + 1:]
            A.append(heritage_A_line)
            A.append(heritage_A_odds)
        else:
            A.append(heritage_A.replace(u'\xa0',' ').replace(u'\xbd','.5'))
        H.append('home')
        H.append(team_H)
        H.append(team_A)

        if not_ML:
            heritage_H = heritage_H.replace(u'\xa0',' ').replace(u'\xbd','.5')
            heritage_H_line = heritage_H[:heritage_H.find(' ')]
            heritage_H_odds = heritage_H[heritage_H.find(' ') + 1:]
            H.append(heritage_H_line)
            H.append(heritage_H_odds)

        else:
            H.append(heritage_H.replace(u'\xa0',' ').replace(u'\xbd','.5'))

       
        odds_list.append(A)
        odds_list.append(H)
    return odds_list
def is_ranked(team):
  #Searched for number in front of team name
  return any(ii.isdigit() for ii in team)
  
def team_of_interest(home,away):
  for team in team_of_interest_list:
    if(home.find(team) >= 0 or away.find(team) >= 0):
      return True
  return False

def get_ranked_games(pre_pruned_data):
  #Pick out the ranked games only
    #We'll throw in UC, Ohio State, and Xavier
  ranked_data   = []
  unranked_data = []
  for game in pre_pruned_data:
    if(is_ranked(game[0]) or is_ranked(game[1]) or team_of_interest(game[0],game[1])):
      ranked_data.append(game)
    else:
      unranked_data.append(game)
  return [ranked_data, unranked_data]
  
def order_my_teams(pre_ranked_teams):
  #Put favorite teams first
  my_teams    = []
  other_teams = []
  for game in pre_ranked_teams:
    if(team_of_interest(game[0],game[1])):
      my_teams.append(game)
    else:
      other_teams.append(game)
  return my_teams + other_teams 
    
    
def get_odds(sport, my_date=0):

    ## Get today's lines
    if(my_date == 0):
      todays_date = str(date.today()).replace('-','')
    else:
      todays_date = my_date
      
    ## change todays_date to be whatever date you want to pull in the format 'yyyymmdd'
    ## One could force user input and if results in blank, revert to today's date. 
    # todays_date = '20140611'

    ## store BeautifulSoup info for parsing
    #print("getting ML")
    soup_ml, time_ml = soup_url('ML', sport, todays_date)
    #print("getting spread")
    soup_rl, time_rl = soup_url('Spreads', sport, todays_date)
    #print("getting totals")
    soup_tot, time_tot = soup_url('Totals', sport, todays_date)

    #print("parsing_ML")
    ML_list = parse_and_write_data(soup_ml, todays_date, time_ml, not_ML = False)
    if(ML_list == []):
      return []
    #print("parsing_spread")
    spread_list = parse_and_write_data(soup_rl, todays_date, time_rl)
    #print("parsing_totals")
    totals_list = parse_and_write_data(soup_tot, todays_date, time_tot)

    formatted_data = []
    num_games = int(len(ML_list)/2)
    for game_num in range(num_games):
      this_game =   [ML_list[game_num*2][2], 
                      ML_list[game_num*2][1], 
                      ML_list[game_num*2][3], 
                      ML_list[game_num*2+1][3], 
                      ML_list[game_num*2][2] + " " + spread_list[game_num*2+1][3], 
                      totals_list[game_num*2][3]
                    ]
      formatted_data.append(this_game)
     
    if(sport == NCAAB or sport == NCAAF):
      formatted_data = get_ranked_games(formatted_data)
      
    if(sport == NFL or sport == NBA):
      formatted_data = order_my_teams(formatted_data)

    return formatted_data

if __name__ == '__main__':
    get_NBA_odds()
