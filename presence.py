import time, argparse, json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pypresence import Presence

# Parse the arguments. Note that -m and -v do not have to be exact.

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--map", help="Map you are playing.")
parser.add_argument("-d", "--difficulty", help="Difficulty you are playing at.")
parser.add_argument("-v", "--variation", help="Difficulty variation.")
args = parser.parse_args()

# If the argument exists, then make it lowercase to normalize.

if args.map:
    map = args.map.lower()
else:
    map = args.map
if args.difficulty:
    difficulty = args.difficulty.lower()
else:
    difficulty = args.difficulty
if args.variation:
    variation = args.variation.lower()
else:
    variation = args.variation

# Load the data for each map and difficulty from the json.

assets = json.load(open("assets.json", "r"))

# Set up some basic errors if there are invalid inputs.

if difficulty and (map == None):  # Cannot have a difficulty without a map
    parser.error("--difficulty requires --map.")
if variation and (difficulty == None):  # Cannot have a variation without a difficulty
    parser.error("--variation requires --difficulty.")

# For map and variation, fuzzywuzzy will check if the closest match in the list has a score of lower than 75.
# If it does, it will return an error.

if map:
    if process.extractOne(map, list(assets["maps"].keys()))[1] < 75:
        parser.error("invalid map.")
if difficulty:
    if difficulty not in list(assets["difficulties"].keys()):
        parser.error("invalid difficulty")
if variation:
    if (
        process.extractOne(
            variation, list(assets["difficulties"][difficulty]["variations"].keys())
        )[1]
        < 75
    ):
        parser.error("invalid variation.")

# Setting up the rich presence.

client_id = "712088548278403123"
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="icon", large_text="Bloons TD 6", details="In Menu")
start_time = time.time()

# Check through different cases and run the one that fits.

if map and difficulty and variation:
    map = process.extractOne(map, list(assets["maps"].keys()))[0]
    variation = process.extractOne(
        variation, list(assets["difficulties"][difficulty]["variations"].keys())
    )[0]

    # Map: {Map}
    print(f'Map: {assets["maps"][map]["name_hf"]}')
    # Difficulty: {Difficulty} - {Variation}
    print(
        f'Difficulty: {assets["difficulties"][difficulty]["name_hf"]} - '
        f'{assets["difficulties"][difficulty]["variations"][variation]["name_hf"]}'
    )

    while True:
        RPC.update(
            # {map_image}
            large_image=assets["maps"][map]["image"],
            # {Map}
            large_text=assets["maps"][map]["name_hf"],
            # {variation_image}
            small_image=assets["difficulties"][difficulty]["variations"][variation][
                "image"
            ],
            # {Difficulty} - {Variation}
            small_text=(
                f'{assets["difficulties"][difficulty]["name_hf"]} - '
                f'{assets["difficulties"][difficulty]["variations"][variation]["name_hf"]}'
            ),
            # {Map} ({Difficulty})
            details=(
                f'{assets["maps"][map]["name_hf"]} '
                f'({assets["difficulties"][difficulty]["name_hf"]})'
            ),
            # In Game
            state="In Game",
            start=start_time,
        )
        time.sleep(30)

elif map and difficulty:
    map = process.extractOne(map, list(assets["maps"].keys()))[0]
    variation = "standard"

    # Map: {Map}
    print(f'Map: {assets["maps"][map]["name_hf"]}')
    # Difficulty: {Difficulty} - {Variation}
    print(
        f'Difficulty: {assets["difficulties"][difficulty]["name_hf"]} - '
        f'{assets["difficulties"][difficulty]["variations"][variation]["name_hf"]}'
    )

    while True:
        RPC.update(
            # {map_image}
            large_image=assets["maps"][map]["image"],
            # {Map}
            large_text=assets["maps"][map]["name_hf"],
            # {variation_image}
            small_image=assets["difficulties"][difficulty]["variations"][variation][
                "image"
            ],
            # {Difficulty} - {Variation}
            small_text=(
                f'{assets["difficulties"][difficulty]["name_hf"]} - '
                f'{assets["difficulties"][difficulty]["variations"][variation]["name_hf"]}'
            ),
            # {Map} ({Difficulty})
            details=(
                f'{assets["maps"][map]["name_hf"]} '
                f'({assets["difficulties"][difficulty]["name_hf"]})'
            ),
            # In Game
            state="In Game",
            start=start_time,
        )
        time.sleep(30)

elif map:
    map = process.extractOne(map, list(assets["maps"].keys()))[0]

    # Map: {Map}
    print(f'Map: {assets["maps"][map]["name_hf"]}')

    while True:
        RPC.update(
            # {map_image}
            large_image=assets["maps"][map]["image"],
            # {Map}
            large_text=assets["maps"][map]["name_hf"],
            # {Map}
            details=f'{assets["maps"][map]["name_hf"]}',
            # In Game
            state="In Game",
            start=start_time,
        )
        time.sleep(30)

elif map == None:
    # In Menu
    print("In Menu")

    while True:
        RPC.update(
            # {btd6_icon}
            large_image="icon",
            # Bloons TD 6
            large_text="Bloons TD 6",
            # In Menu
            details="In Menu",
        )
        time.sleep(30)
