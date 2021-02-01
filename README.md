
# Giantbomb API Cli

### Installation
To install create a new virtual environment using python3 and run  `pip3 install --requirement requirements.txt`

You will also need an api key from the Giantbomb api, this can be obtained from [the giantbomb api page](https://www.giantbomb.com/api/).

Once you have obtained the api key add it to config.ini:
```
[default]
api_key = $API_KEY
```

### Testing
To run unit tests I run `python3 -m pytest`

### Usage
usage: `main.py [-h] [-search] [-get-game] [-get-game-dlc] parameters`

```
positional arguments:
  parameters      Search terms or game name

optional arguments:
  -h, --help     show this help message and exit
  -search        Search for a list of games using a search term
  -get-game      Get information about a single game
  -get-game-dlc  Get information about a single game and its dlc
```

### Known issues
The API sometimes doesn't return complete data if it doesn't exist in the giantbomb database, this means that DLC will sometimes not display in date order. I've written some logic to catch the ones that I experienced in manual testing but there may be others where this is the case.

The CLI is also not the best, it will take multiple arguments without complaining and only run the first but it's servicable and I wanted to focus on getting the logic right for the api class and to write it in a way that would be extensible. It could be extended and made nice fairly easily.

Getting DLC's is very slow, this is partly because python is slow and partly because my code isn't very optimised. I'm sure this could be improved with a bit of effort.
