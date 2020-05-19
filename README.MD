# Bloons TD 6 (Pseudo) Rich Presence

## Installation

First, clone the repository.

```cmd
git clone https://www.github.com/yolodude25/btd6-rich-presence
```

Then, install the required modules

```cmd
cd btd6-rich-presence
```

```cmd
pip install -r requirements.txt
```

## Arguments

### `-m, --map`

Map you are playing.

#### Available Values

List of all maps can be found in [assets.json](assets.json)

#### Notes

This argument uses fuzzy search, and you can type approximate map names and if they are close enough, it will recognize them.

### `-d, --difficulty`

Difficulty you are playing at.

#### Available Values

`easy`, `medium`, `hard`

#### Notes

Cannot be used without `--map` being set.

### `-v, --variation`

Difficulty variation.

#### Available Values

List of all variation can be found in [assets.json](/assets.json).

The variation must be available for the selected difficulty.

#### Notes

Cannot be used without `--difficulty` being set.

This argument uses fuzzy search, and you can type approximate variation names and if they are close enough, it will recognize them.

## Usage

Run `presence.py` with your arguments.

To exit the program just close the python script.
