from tkinter import *
from SBRscraper import *
from datetime import date
from time import *
from tk_scrollbar import *

import os

second_update   = 1000
hourly_update   = 1000*60*60
daily_update    = 1000*60*60*24

hour            = 60*60

ALL_SPORTS  = 0
NCAAF       = 1
NFL         = 2
NBA         = 3
NCAAB       = 4
SOCCER      = 5
MLB         = 6


class ticker_top_gui:

  #Initialization method...runs when object
  def __init__(self,master):
    self.master = master
    #make fullscreen
    master.attributes('-fullscreen', True)
    #binds escape key to escape function
    master.bind('<Escape>',lambda e: master.destroy())
    master.configure(background="black")
    master.title("Mike's Odds Ticker")
    
    self.font             = "DS-Digital"
    self.label_size       = 28
    self.num_rows         = 50
    self.num_cols         = 7

    
    #Make Frame to hold spotify and time frames
    self.top_frame      = Frame(bg="black")
    self.odds_frame     = tk_scrollbar_frame(master)
    self.buttons_frame  = Frame(bg="black")
    
    #Make Labels
    titles  = ["Bet #","Home",  "Away","ML Home","ML Away", "Spread", "Over/Under"]
    col     = 0
    self.text_grid  = []
    self.label_grid = []
    
    text_row  = []
    label_row = []
    for col in range(self.num_cols):
      text_row.append(StringVar())
      text_row[col].set(titles[col])
      if(col == 0):
        label_row.append(Label(self.top_frame, textvariable=text_row[col], anchor='w', bg="black", fg="red", width=4, font=(self.font, self.label_size)))
      elif(col == 3 or col == 4):
        label_row.append(Label(self.top_frame, textvariable=text_row[col], anchor='w', bg="black", fg="red", width=9, font=(self.font, self.label_size)))
      elif(col == 5):
        label_row.append(Label(self.top_frame, textvariable=text_row[col], anchor='w', bg="black", fg="red", width=19, font=(self.font, self.label_size)))
      else:
        label_row.append(Label(self.top_frame, textvariable=text_row[col], anchor='w', bg="black", fg="red", width=14, font=(self.font, self.label_size)))
      label_row[col].grid(row=0,column=col*2)
      dummy_label = Label(self.top_frame, text=" ", anchor='w', bg="black", fg="white", width=2, font=(self.font, self.label_size))
      dummy_label.grid(row=0,column=col*2+1)

      
    self.text_grid.append(text_row)
    self.label_grid.append(label_row)
    
    for row in range(self.num_rows):
      text_row  = []
      label_row = []
      for col in range(self.num_cols):
        text_row.append(StringVar())
        text_row[col].set("row=" + str(row) + " col=" + str(col))
        
        if(row % 2 == 0):
          fg_color = "green"
        else:
          fg_color = "dark orange"
        
        if(col == 0):
          label_row.append(Label(self.odds_frame.interior, textvariable=text_row[col], anchor='w', bg="black", fg="red", width=5, font=(self.font, self.label_size)))
        elif(col == 3 or col == 4):
          label_row.append(Label(self.odds_frame.interior, textvariable=text_row[col], anchor='w', bg="black", fg=fg_color, width=10, font=(self.font, self.label_size)))
        elif(col == 5):
          label_row.append(Label(self.odds_frame.interior, textvariable=text_row[col], anchor='w', bg="black", fg=fg_color, width=20, font=(self.font, self.label_size)))
        else:
          label_row.append(Label(self.odds_frame.interior, textvariable=text_row[col], anchor='w', bg="black", fg=fg_color, width=15, font=(self.font, self.label_size)))
        label_row[col].grid(row=row+1,column=col*2)
        dummy_label = Label(self.odds_frame.interior, text=" ", anchor='w', bg="black", fg="red", width=1, font=(self.font, self.label_size))
        dummy_label.grid(row=row+1,column=col*2+1)
        
      self.text_grid.append(text_row)
      self.label_grid.append(label_row)
    

    button_texts      = ["All Sports", "College FB", "NFL", "NBA", "NCAA Hoops"]
    button_cmds       = [self.all_sport_cb,self.ncaaf_cb,self.nfl_cb,self.nba_cb,self.ncaab_cb]
    self.button_list  = []
    count = 0
    for text in button_texts:
      self.button_list.append(Button(self.buttons_frame, command=button_cmds[count], text=button_texts[count], bg="black", activebackground="green", fg="white", width = 20, font=(self.font, self.label_size)))
      self.button_list[count].grid(row=0,column=count)
      count += 1
    
      
    self.sport_select = ALL_SPORTS
    self.button_list[0].config(bg="green",fg="black")
    

    #Pack party and everyone's invited
    self.top_frame.pack(fill=BOTH)
    self.odds_frame.pack(fill=BOTH)
    self.buttons_frame.pack(fill=BOTH)
    
    
    
    #Call Update Functions
    try:
      stat = os.stat("NBA.txt")
      update_time = stat.st_mtime
    except:
      update_time = 0
      
    if(time() >= update_time + hour):
      master.after(second_update, lambda: self.update_odds(master))
    else:
      self.nba_data_list    = read_txt("NBA")
      
      self.nfl_data_list    = read_txt("NFL")
      
      ncaab_ranked          = read_txt("NCAAB_RANKED")
      ncaab_unranked        = read_txt("NCAAB_UNRANKED")
      self.ncaab_data_list  = ncaab_ranked + ncaab_unranked
      self.ncaab_num_ranked = len(ncaab_ranked)
      
      ncaaf_ranked          = read_txt("NCAAF_RANKED")
      ncaaf_unranked        = read_txt("NCAAF_UNRANKED")
      self.ncaaf_data_list  = ncaaf_ranked + ncaaf_unranked
      self.ncaaf_num_ranked = len(ncaaf_ranked)
      
      self.fill_in_boxes(ALL_SPORTS)
      master.after(hourly_update, lambda: self.update_odds(master))
      
  
    
    
    
    
  def all_sport_cb(self):
    self.sport_select = ALL_SPORTS
    button_num = 0;
    for button in self.button_list:
      if(button_num == ALL_SPORTS):
        button.config(bg="green",fg="black")
      else:
        button.config(bg="black",fg="white")
      button_num += 1
      
    self.fill_in_boxes(ALL_SPORTS)
        
  
  def ncaaf_cb(self):
    self.sport_select = NCAAF
    button_num = 0;
    for button in self.button_list:
      if(button_num == NCAAF):
        button.config(bg="green",fg="black")
      else:
        button.config(bg="black",fg="white")
      button_num += 1
      
    self.fill_in_boxes(NCAAF)
  
  def nfl_cb(self):
    self.sport_select = NFL
    button_num = 0;
    for button in self.button_list:
      if(button_num == NFL):
        button.config(bg="green",fg="black")
      else:
        button.config(bg="black",fg="white")
      button_num += 1
      
    self.fill_in_boxes(NFL)
    
  def nba_cb(self):
    self.sport_select = NBA
    button_num = 0;
    for button in self.button_list:
      if(button_num == NBA):
        button.config(bg="green",fg="black")
      else:
        button.config(bg="black",fg="white")
      button_num += 1
      
    self.fill_in_boxes(NBA)
    
  def ncaab_cb(self):
    self.sport_select = NCAAB
    button_num = 0;
    for button in self.button_list:
      if(button_num == NCAAB):
        button.config(bg="green",fg="black")
      else:
        button.config(bg="black",fg="white")
      button_num += 1
      
    self.fill_in_boxes(NCAAB)
      
  def fill_in_boxes(self,sport_option):
    self.odds_frame.reset_view()
    data_to_print = []
    
    
    if(sport_option == ALL_SPORTS):
      stops = []
      if(len(self.ncaaf_data_list) > self.num_rows/2):
        data_to_print += self.ncaaf_data_list[:int(self.num_rows/2)]
      else:
        data_to_print += self.ncaaf_data_list
      stops.append(len(data_to_print))
        
      data_to_print += self.nfl_data_list 
      stops.append(len(data_to_print))
      
      data_to_print += self.nba_data_list 
      stops.append(len(data_to_print))
      
      if(len(self.ncaab_data_list) > self.num_rows/2):
        data_to_print += self.ncaab_data_list[:int(self.num_rows/2)]
      else:
        data_to_print += self.ncaab_data_list
      stops.append(len(data_to_print))
      
      #Print out the data we have
      game_num        = 1
      stop_num        = 0
      sport_game_num  = 1
      for game in data_to_print:
        if(game_num > stops[stop_num]):
          stop_num        += 1
          sport_game_num  = 1
        if(game_num <= self.num_rows):
          self.text_grid[game_num][0].set((stop_num+1)*1000+sport_game_num)
          col_num = 1
          for item in game:
            self.text_grid[game_num][col_num].set(item)
            col_num += 1
          game_num        += 1
          sport_game_num  += 1
      
    
      
    else:
      
      #Print College Football
      if(sport_option == NCAAF):
        data_to_print = self.ncaaf_data_list
        
      #Print NFL
      elif(sport_option == NFL):
        data_to_print = self.nfl_data_list

      #Print NBA
      elif(sport_option == NBA):
        data_to_print = self.nba_data_list
        
      #Print College Basketball
      elif(sport_option == NCAAB):
        data_to_print = self.ncaab_data_list
      

      #Print out the data we have
      game_num = 1
      for game in data_to_print:
        if(game_num <= self.num_rows):
          self.text_grid[game_num][0].set(sport_option*1000+game_num)
          col_num = 1
          for item in game:
            self.text_grid[game_num][col_num].set(item)
            col_num += 1
          game_num += 1

    #Fill in the rest with blank spaces
    if(game_num <= self.num_rows):
      while(game_num <= self.num_rows):
        for col in range(self.num_cols):
          self.text_grid[game_num][col].set("")
        game_num += 1
    



    
    
  def update_odds(self,master):
    todays_date = str(date.today()).replace('-','')
    
  #Only Want Today for the NBA
    print("NBA...")
    self.nba_data_list = get_odds(NBA)
    
    write_txt(self.nba_data_list,"NBA")
    
  #Check the next few days for an NFL game
    nfl_data_list = []
    count         = 0
    nfl_date = int(todays_date)
    while(count < 4):
      print("NFL...date=" + str(nfl_date))
      nfl_data_list_day = get_odds(NFL,str(nfl_date))
      nfl_data_list += nfl_data_list_day
      nfl_date += 1
      count    += 1
    self.nfl_data_list = nfl_data_list
    
    write_txt(self.nfl_data_list,"NFL")
    
      
  #Only Want Today for college basketball
    print("NCAAB")
    [ncaab_ranked, ncaab_unranked]  = get_odds(NCAAB)
    self.ncaab_data_list            = ncaab_ranked + ncaab_unranked
    self.ncaab_num_ranked           = len(ncaab_ranked)
    
    if(self.ncaab_num_ranked > 0):    
      write_txt(self.ncaab_data_list[0:self.ncaab_num_ranked],"NCAAB_RANKED")
    if(len(self.ncaab_data_list) != self.ncaab_num_ranked):
      write_txt(self.ncaab_data_list[self.ncaab_num_ranked:],"NCAAB_UNRANKED")
   
    
  #Check the next few days for a college football game
    ncaaf_ranked = []
    count         = 0
    ncaaf_date = int(todays_date)
    
    unranked_lst = []
    while(ncaaf_ranked == [] and count < 4):
      print("NCAAF...date=" + str(ncaaf_date))
      try:
        [ncaaf_ranked,ncaaf_unranked] = get_odds(NCAAF,str(ncaaf_date))
      except:
        [ncaaf_ranked,ncaaf_unranked] = [[],[]]
      unranked_lst += ncaaf_unranked
      ncaaf_date   += 1
      count        += 1
    self.ncaaf_data_list  = ncaaf_ranked + unranked_lst
    self.ncaaf_num_ranked = len(ncaaf_ranked)
    
    if(self.ncaaf_num_ranked > 0):
      write_txt(self.ncaaf_data_list[0:self.ncaaf_num_ranked],"NCAAF_RANKED")
    if(len(self.ncaaf_data_list) != self.ncaaf_num_ranked):
      write_txt(self.ncaaf_data_list[self.ncaaf_num_ranked:],"NCAAF_UNRANKED")
    
    
    self.fill_in_boxes(ALL_SPORTS)

def write_txt(data_list,txt_name):
  file = open(txt_name + ".txt",'w')
  for game in data_list:
    for item in game:
      file.write(item + "\n")
  file.close()
  
def read_txt(txt_name):
  games_list = []
  file = open(txt_name + ".txt",'r')
  eof = 0
  while(eof == 0):
    this_game = []
    for ii in range(6):
      data = file.readline()
      if(ii==0 and data == ""):
        eof = 1
      this_game.append(data[:-1])
    if(eof == 0):
      games_list.append(this_game)
  file.close()
  return games_list

      
if __name__ == "__main__":
  root = Tk()
  my_gui = ticker_top_gui(root)
  root.mainloop()







    