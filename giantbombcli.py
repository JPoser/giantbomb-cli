#!/usr/bin/python3
import json, requests, datetime
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

class giantbomb_cli:
    def __init__(self):
        #initialises the cli class
        self.headers = {'User-Agent': 'giantbomb-test-cli 0.1', 'From': 'joe.poser@gmail.com'}
        # read config file and set api key class variable 
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.api_key = self.config.get('default' , 'api_key')

    def search(self, search_term):
        # create dictionary for results
        output_games = {}
        # search the api for the term in the arguements
        url = 'http://www.giantbomb.com/api/search/?api_key=%s&format=json&query="%s"&resources=game' % (self.api_key, search_term)
        # call api using requests library with headers
        api_search = requests.get(url, headers=self.headers).json()
        #loop through dict
        result_dict = api_search['results']

        for game in result_dict:
            output_games[game.get('name')] = game.get('api_detail_url')
        
        #return dict with game name as key and api_urls as val 
        return output_games


    def game_details(self, game):
        # get details of specific game
        # call search
        search_results = self.search(game)
        api_url = ""
        # loop through keys to see if there is a specific match
        for return_game, return_url in search_results.items():
            if return_game.lower() == game.lower():
                game_name = return_game
                api_url = return_url
        
        if api_url == "":
            return "error game not found"

        # set api_url to include extra arguments to use api key and return json
        api_url = api_url + "?api_key=" + self.api_key + "&format=json"
        # call api
        game_get = requests.get(api_url, headers=self.headers).json()
        # return game data and name
        output_game_data = game_get['results']
        return [game_name, output_game_data]

    def output_search(self, games):
        print("Search Results:")
        for g in games:
            print(g)

    def output_game(self, game, dlc_flag):
        #print(game)
        game_name = game[0]
        game_data = game[1]
        print("Name: " + game_name)
        print("Description: " + game_data['deck'])
        print("Developed by: ", end='')
        for devs in game_data['developers']:
            print(devs['name'], end=', ')
        print('')
        print("Genre: ", end='')
        for genre in game_data['genres']:
            print(genre['name'], end=', ')
        if dlc_flag == True:
            dlcs = self.get_dlcs(self.game_details(game_name))
            if len(dlcs) > 0:
                try:
                    sorted_dlcs = sorted(dlcs, key=lambda p: datetime.datetime.strptime(p['release_date'], "%Y-%m-%d %H:%M:%S"))
                except TypeError:
                    print("Error: release date not found - printing in ")
                    sorted_dlcs = dlcs
                print("\nDLC list: ")
                for dlc in sorted_dlcs:
                    print("DLC name: " + dlc['name'])
                    if dlc['deck'] != None: 
                        print("DLC description: " + dlc['deck'])
                    print("Platform: " + dlc['platform'].get('name'))
                    if dlc['release_date'] != None: 
                        print("Release Date: " + dlc['release_date'])
                    print("")
            else:
                print("")
                print("No DLC found")

    def get_dlcs(self, game):
        # Func to get list of game dlcs from 
        # Get game data dictionary from get game function 
        game_data = game[1]
        dlc_list = []
        results_list = []
        # get list of dlc api url's from 
        try:
            for dlc in game_data['dlcs']:
                dlc_list.append(dlc['api_detail_url'])
        except KeyError:
            results_list = []  

        for url in dlc_list:
            url = url + "?api_key=" + self.api_key + "&format=json"
            results_list.append(requests.get(url, headers=self.headers).json()['results'])

        return results_list