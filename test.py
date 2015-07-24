#!/usr/bin/env python

# charles mceachern

# summer 2015

# json football data sanity check

import json # for accessing the data files
import os # for navigating directories










# note: team names are not always 3 characters. use split(). 




def main():
  # navigate to the root of the data directory
  os.chdir('../data/reco/')

  ngames = 0
  winnermoretd = 0
  losermoretd = 0
  samenumbertd = 0

  # scroll through seasons
  seasons = sorted(os.listdir('.'))
  for s in seasons:
  
#    # debug: only look at the first season
#    if seasons.index(s) > 0:
#      break

    os.chdir(s)
    games = sorted(os.listdir('.'))
    print s+' season ('+str(len(games))+' games) '
    # scroll through games
    for g in games:
    
#      # debug: only look at the first game
#      if games.index(g) > 10:
#        break

#      print '\tgame '+str(games.index(g))+': '+g[14:24].replace('_',' ')
      # load game data from json file into a big dictionary object
      with open(g) as gamefile:
        gamedict = json.load(gamefile)
      # establish data structure to store score data
      teams = ['home', 'away']
      values = {'touchdown':6, 'field goal':3, 'extra point':1, 'safety':2, 'two point conversion':2}
      types = values.keys()
      scores = {}
      for tm in teams:
        scores[tm] = {}
        for ty in types:
          scores[tm][ty] = 0
      # scroll through plays to collect scoring data
      for playwrapper in gamedict['plays']:
#        # debug: only scroll through the first 10 plays of a game
#        if gamedict['plays'].index(playwrapper) > 50:
#          break
        play = playwrapper['play']
        if 'scoring' in play:
          tm = play['scoring']['team']
          ty = play['scoring']['type']
          # check for potential key errors
          if tm not in teams:
            print 'unrecognized team: '+tm
            continue
          if ty not in types:
            print 'unrecognized type: ',ty
            continue
          # store the score event
          scores[tm][ty] = scores[tm][ty] + 1
      # present the scoring totals for this game
      totalscore = {}
      for tm in teams:
        totalscore[tm] = sum( [scores[tm][ty]*values[ty] for ty in types] )
#      for tm in teams:
#        print '\t\t'+tm+': '+str(scores[tm]['touchdown'])+' touchdowns, '+str(totalscore[tm])+' points total'
        
      # figure out who won
      winner, loser = ('home', 'away') if totalscore['home']>totalscore['away'] else ('away', 'home')
      
#      print '\t\twinner: '+winner
      
      ngames = ngames + 1

      # did the winner score more touchdowns than the loser?
      if scores[winner]['touchdown']>scores[loser]['touchdown']:
#        print '\t\twinner had more touchdowns'
        winnermoretd = winnermoretd + 1
      elif scores[winner]['touchdown']<scores[loser]['touchdown']:
#        print '\t\tloser had more touchdowns'
        losermoretd = losermoretd + 1
      else:
#        print '\t\twinner and loser same number of touchdowns'
        samenumbertd = samenumbertd + 1

    # back out of season directory
    os.chdir('..')

  print 'total games: '+str(ngames)
  print 'games where the winner scored more touchdowns: '+str(winnermoretd)
  print 'games where the loser scored more touchdowns: '+str(losermoretd)
  print 'games where both teams scored equal touchdowns: '+str(samenumbertd)



# for importability
if __name__ == '__main__':
  main()


