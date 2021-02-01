from giantbombcli import giantbomb_cli
import argparse

def main():
    g = giantbomb_cli()
    parser = argparse.ArgumentParser(description='CLI interface for the Giantbomb.com API')
    # CLI args
    parser.add_argument('-search', action='store_true', default=False, dest='search_switch', help='Search for a list of games using a search term')
    parser.add_argument('-get-game', action='store_true', default=False, dest='game_switch', help= 'Get information about a single game')
    parser.add_argument('-get-game-dlc', action='store_true', default=False, dest='dlc_switch', help= 'Get information about a single game and its dlc')
    parser.add_argument("parameter", action='store', nargs='+', help="Search terms or game name")
    args = parser.parse_args()
    # convert paramaters into list of strings and then into a single string
    params = map(str, args.parameter)
    params = ' '.join(params)

    # cli logic
    if args.search_switch == True:
        g.output_search(g.search(args.parameter))
    elif args.game_switch == True:
        g.output_game(g.game_details(params), False)
    elif args.dlc_switch == True:
        g.output_game(g.game_details(params), True)
    else:
        parser.print_help()

main()
