#!/usr/bin/python3
import pytest, json, requests
from sys import argv
from giantbombcli import giantbomb_cli

def test_search():
    cli = giantbomb_cli()
    assert cli.search('stardew') == {'Stardew Valley': 'https://www.giantbomb.com/api/game/3030-50899/'}

def test_game_details():
    cli = giantbomb_cli()
    test_output_name = cli.game_details('metroid')[0]
    test_output_data = cli.game_details('metroid')[1]
    test_data_string = "Don the Power Suit of intergalactic bounty hunter Samus Aran as she recaptures the dangerous Metroid species from the evil Space Pirates. Released by Nintendo in 1986, this game introduced the \"Metroidvania\" style of open-world gameplay on consoles."
    test_name_string = "Metroid"
    assert test_data_string in test_output_data.get('deck') and test_name_string == test_output_name

def test_output_search(capsys):
    cli = giantbomb_cli()
    cli.output_search(cli.search('stardew'))
    assert "Stardew Valley" in capsys.readouterr().out

def test_output_game(capsys):
    cli = giantbomb_cli()
    test_output = cli.output_game(cli.game_details('Mass Effect'), True)
    test_deck_string = "Humanity is still a newcomer on the futuristic galactic stage, and it's up to the charismatic Commander Shepard to investigate the actions of a rogue agent while under threat from a dangerous synthetic race known as the Geth."
    test_dlc_name = "Pinnacle Station"
    assert test_deck_string and test_dlc_name in capsys.readouterr().out


def test_get_dlcs():
    cli = giantbomb_cli()
    test_output = cli.get_dlcs(cli.game_details('Mass Effect'))
    test_output = test_output[0]
    test_string = "In this 253mb downloadable content pack, Shepard and his team are inserted onto a new asteroid and tasked with stopping it from colliding with a planet. It provides about 90 minutes of gameplay."
    assert test_string in test_output.get('deck')