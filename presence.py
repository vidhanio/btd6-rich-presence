import time, argparse, json, configparser, pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pypresence import Presence

# Functions


def lower_if_exists(lie_argument):
    if lie_argument:
        lie_output = lie_argument.lower()
    else:
        lie_output = lie_argument
    return lie_output


def fuzzy_error(fe_string, fe_list, fe_thresh):
    if fe_string != None:
        if process.extractOne(fe_string, fe_list)[1] < fe_thresh:
            return True
        else:
            return False


def presence_gen():

    # Setup default values

    pg_presencedict = {}
    pg_presencedict["large_image"] = config["Normal"]["large_image"]
    pg_presencedict["large_text"] = config["Normal"]["large_text"]
    pg_presencedict["small_image"] = config["Normal"]["small_image"]
    pg_presencedict["small_text"] = config["Normal"]["small_text"]
    pg_presencedict["details"] = config["Normal"]["details"]
    pg_presencedict["state"] = config["Normal"]["state"]
    pg_presencedict["party_size"] = []
    pg_presencedict["start"] = start_time
    pg_formatdict = {}
    pg_formatdict["map_image"] = ""
    pg_formatdict["map_hf"] = ""
    pg_formatdict["difficulty_hf"] = ""
    pg_formatdict["variation_hf"] = ""
    pg_formatdict["variation_image"] = ""
    pg_formatdict["icon"] = "icon"
    pg_coop = coop
    if map:
        pg_map = process.extractOne(map, list(assets["maps"].keys()))[0]
        pg_formatdict["map_image"] = assets["maps"][pg_map]["image"]
        pg_formatdict["map_hf"] = assets["maps"][pg_map]["name_hf"]
    if difficulty:
        pg_difficulty = difficulty
        pg_formatdict["difficulty_hf"] = assets["difficulties"][pg_difficulty][
            "name_hf"
        ]
        if variation:
            pg_variation = process.extractOne(
                variation, list(assets["difficulties"][difficulty]["variations"].keys())
            )[0]
            pg_formatdict["variation_hf"] = assets["difficulties"][difficulty][
                "variations"
            ][pg_variation]["name_hf"]
            pg_formatdict["variation_image"] = assets["difficulties"][difficulty][
                "variations"
            ][pg_variation]["image"]
        else:
            pg_variation = "standard"
            pg_formatdict["variation_hf"] = assets["difficulties"][difficulty][
                "variations"
            ][pg_variation]["name_hf"]
            pg_formatdict["variation_image"] = assets["difficulties"][difficulty][
                "variations"
            ][pg_variation]["image"]
    if map and difficulty:
        for pg_field in list(config["Normal"].keys()):
            pg_presencedict[pg_field] = config["Normal"][pg_field].format(
                **pg_formatdict
            )
    elif map:
        for pg_field in list(config["No Difficulty"].keys()):
            pg_presencedict[pg_field] = config["No Difficulty"][pg_field].format(
                **pg_formatdict
            )
    if pg_coop:
        for pg_field in list(config["Co-Op"].keys()):
            pg_presencedict[pg_field] = config["Co-Op"][pg_field].format(
                **pg_formatdict
            )
        pg_presencedict["party_size"] = pg_coop
    if not map:
        for pg_field in list(config["No Map"].keys()):
            pg_presencedict[pg_field] = config["No Map"][pg_field].format(
                **pg_formatdict
            )
        pg_presencedict["start"] = None
    for pg_field in list(pg_presencedict.keys()):
        if pg_presencedict[pg_field] == "" or pg_presencedict[pg_field] == []:
            pg_presencedict[pg_field] = None
    return pg_presencedict


# Parsers

# Parse the arguments. Note that -m and -v do not have to be exact.

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--map", help="Map you are playing.")
parser.add_argument("-d", "--difficulty", help="Difficulty you are playing at.")
parser.add_argument("-v", "--variation", help="Difficulty variation.")
parser.add_argument("-c", "--coop", help="Number of players in your co-op game.")
args = parser.parse_args()

# Parse the config file.

config = configparser.ConfigParser()
config.read("config.ini")

# Parse the json file.

assets = json.load(open("assets.json", "r"))


# If the argument exists, then make it lowercase to normalize.

map = lower_if_exists(args.map)
difficulty = lower_if_exists(args.difficulty)
variation = lower_if_exists(args.variation)
if args.coop:
    coop = [int(args.coop), 4]
else:
    coop = args.coop
if args.coop:
    coop = [int(args.coop), 4]
else:
    coop = args.coop

# Load the data for each map and difficulty from the json.

assets = json.load(open("assets.json", "r"))

# Set up some basic errors if there are invalid inputs.

if difficulty and (map == None):  # Cannot have a difficulty without a map
    parser.error("--difficulty requires --map.")
if variation and (difficulty == None):  # Cannot have a variation without a difficulty
    parser.error("--variation requires --difficulty.")
if coop and (map == None):
    parser.error("--coop requires --map.")  # Cannot have Co-Op without a map

# For map and variation, fuzzywuzzy will check if the closest match in the list has a score of lower than 75.
# If it does, it will return an error.

if fuzzy_error(map, list(assets["maps"].keys()), 75):
    parser.error("invalid map.")
if difficulty:
    if difficulty not in list(assets["difficulties"].keys()):
        parser.error("invalid difficulty.")
    if fuzzy_error(
        variation, list(assets["difficulties"][difficulty]["variations"].keys()), 75
    ):
        parser.error("invalid variation.")
if coop:
    if not (1 <= coop[0] <= 4):
        parser.error("invalid co-op player count.")


# Setting up the rich presence.

client_id = config["Rich Presence"]["client_id"]
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="icon", large_text="Bloons TD 6", details="In Menu")
start_time = time.time()

# Check through different cases and run the one that fits.

pvars = presence_gen()
pprint.pprint(pvars)
while True:
    RPC.update(
        large_image=pvars["large_image"],
        large_text=pvars["large_text"],
        small_image=pvars["small_image"],
        small_text=pvars["small_text"],
        details=pvars["details"],
        state=pvars["state"],
        party_size=pvars["party_size"],
        start=pvars["start"],
    )
    time.sleep(5)
