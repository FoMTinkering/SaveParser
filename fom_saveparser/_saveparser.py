import argparse
import json
from fiddletools import FiddleParser
from subprocess import Popen, PIPE, DEVNULL
from pathlib import Path


local = Path(__file__).parent

with open(Path(local)/"settings.json") as fp:
    SETTINGS = json.load(fp)

names = [
    "beach",
    "beach_secret",
    "checksums",
    "date_photos",
    "deep_woods",
    "dragonsworn_glade",
    "earth_seal",
    "eastern_road",
    "farm",
    "fire_seal",
    "gamedata",
    "game_stats",
    "haydens_farm",
    "header",
    "info",
    "mines_entry",
    "narrows",
    "narrows_secret",
    "npcs",
    "player",
    "player_home",
    "player_home_east",
    "player_home_north",
    "player_home_upper_central",
    "player_home_upper_east",
    "player_home_upper_west",
    "player_home_west",
    "priestess_quarters",
    "quests",
    "ruins_seal",
    "ruins_seal",
    "summit",
    "town",
    "void_seal",
    "water_seal",
    "western_ruins",
]

def set_vaultc_path():
    parser = argparse.ArgumentParser(
        prog="fom-saveparser-setvaultc",
        usage="fom-saveparser-setvaultc <VAULTC_FILEPATH>"
    )
    parser.add_argument(
        "vaultc"
    )
    args = parser.parse_args()

    with open(Path(local)/"settings.json", "w") as fp:
        json.dump({"vaultc_path": args.vaultc}, fp)

def extract_savedata():
    parser = argparse.ArgumentParser(
        prog="fom-saveparser-extract",
        usage="fom-saveparser-extract <INPUT_FILEPATH>"
    )
    parser.add_argument(
        "savefile"
    )
    args = parser.parse_args()
    
    save = {}

    for name in names:
        with Popen(f'"{SETTINGS["vaultc_path"]}" view "{args.savefile}" {name}', stdout=PIPE, stderr=DEVNULL, universal_newlines=True) as process:
            for line in process.stdout:
                j = line
                break
        try:
            save[name] = dict(FiddleParser(
                filename=name,
                data=json.loads(j),
                filter="none"
            ))
        except:
            ...

    for name in [f"DynamicGrid_{e}" for e in range(16, 100)]:
        with Popen(f'"{SETTINGS["vaultc_path"]}" view "{args.savefile}" {name}', stdout=PIPE, stderr=DEVNULL, universal_newlines=True) as process:
            for line in process.stdout:
                j = line
        try:
            save[name] = dict(FiddleParser(
                filename=name,
                data=json.loads(j),
                filter="none"
            ))
        except:
            ...

    FiddleParser(
        filename="savedata",
        data=save, 
        filter="none"
    ).to_html()
