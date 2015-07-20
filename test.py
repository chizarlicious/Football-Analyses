#!/usr/bin/env python

# charles mceachern

# summer 2015

# json football data sanity check

import json # for accessing the data files
import os # for navigating directories







def main():
  # navigate to the root of the data directory
  os.chdir('../data/reco/')
  
  # scroll through seasons
  seasons = sorted(os.listdir('.'))
  for s in seasons:
  
    # debug: only look at the first season
    if seasons.index(s) > 0:
      break

    os.chdir(s)
    games = sorted(os.listdir('.'))
    print s+' season ('+str(len(games))+' games) '
    # scroll through games
    for g in games:
      print '\tgame '+str(games.index(g))+': '+g[14:24].replace('_',' ')

      # debug: only look at the first game
      if games.index(g) > 20:
        break

      # load game data from json file into a big dictionary object
      with open(g) as gamefile:
        gamedict = json.load(gamefile)
      # establish data structure to store score data
      teams = ['home', 'away']
      types = ['touchdown', 'field goal', 'extra point', 'safety']
      values = {'touchdown':6, 'field goal':3, 'extra point':1, 'safety':2}
      scores = {}
      for tm in teams:
        scores[tm] = {}
        for ty in types:
          scores[tm][ty] = 0
      # scroll through plays to collect scoring data
      for playwrapper in gamedict['plays']:

        # debug: only scroll through the first 10 plays of a game
#        if gamedict['plays'].index(playwrapper) > 50:
#          break

#        if 'scoring' in playwrapper['play']:
#          print '\t\t',playwrapper


        play = playwrapper['play']
        if 'scoring' in play:
          tm = play['scoring']['team']
          ty = play['scoring']['type']
#          print '\t\t'+tm+' '+ty
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
      for tm in teams:
        # add up the total for each team
        total = 0
        for ty in types:
          total = total + scores[tm][ty]*values[ty]
        print '\t\t'+tm+': '+str(total),
        # also present the score breakdown
#        for ty in types:
#          print '\t\t\t'+str(scores[tm][ty])+'x '+ty
        if scores[tm]['touchdown']==scores[tm]['extra point']:
          print '\tsame number of touchdowns and extra points'
        else:
          print '\tNOT THE SAME number of touchdowns and extra points'


    # back out of season directory
    os.chdir('..')

# for importability
if __name__ == '__main__':
  main()


