import json
import os
from colorama import Fore, Back , Style

white = Fore.WHITE + Style.BRIGHT
accent = Fore.MAGENTA + Style.BRIGHT
green = Fore.LIGHTGREEN_EX + Style.BRIGHT
red = Fore.LIGHTRED_EX + Style.BRIGHT
grey = Fore.LIGHTBLACK_EX
prefix = f"{accent}listmanager@{os.getlogin().lower()}{white}:~$ "

completed = Back.GREEN + " " + Back.RESET + " "
failed = Back.LIGHTRED_EX + " " + Back.RESET + " "

helpText = """
help, ?              $ show this help menu
quit, q, exit        $ exit the application
clear, cls           $ clear the terminal
addlevel, add        $ add level to list file
dellevel, del        $ delete level from list file
editlevel, edit      $ edit/replace level in list file
viewlist, view, list $ display list file
submit               $ submit a list record
calculate, calc      $ calculate records and list points
"""

def submitRecord(level, player):
    # Read current file data
    with open(file) as f:
        try: fileData = json.load(f)
        except: fileData = []

    # Append level data
    for x in fileData:
        if (str(x['name']).lower() == level.lower()):
            victors = x['victors']
            victors.append(player)

    with open(file, mode='w') as f:
        f.write(json.dumps(fileData, indent=2))

def getPlace(x):
    return x['place']

def addLevel(file, name, place, creators, verifier, video, id):
    # Combine level data
    levelData = {"name": name, "place": place, "id": id, "creators": creators, "verifier": verifier, "video": video, "victors" : []}

    # Read current file data
    with open(file) as f:
        try: fileData = json.load(f)
        except: fileData = []

    # Append level data
    for x in fileData:
        if int(x['place']) >= int(place):
            x['place'] = str(int(x['place']) + 1)
    fileData.append(levelData)

    with open(file, mode='w') as f:
        f.write(json.dumps(fileData, indent=2))

def delLevel(file, level):
    # Read current file data
    with open(file) as f:
        try: fileData = json.load(f)
        except: fileData = []

    # Append level data
    for x in fileData:
        if (str(x['name']).lower() == level.lower() or str(x['place']).lower() == level.lower()): fileData.remove(x)

    with open(file, mode='w') as f:
        f.write(json.dumps(fileData, indent=2))

def viewList():
    # I love nested if statements
    i = 1
    try:
        with open(file, "r") as f:
            fileData = json.load(f)
            while i <= len(fileData):
                for x in fileData:
                    if x['place'] == str(i): print(f"#{x['place']} {x['name']} | ID: {x['id']} | By {x['creators']} | Verified by {x['verifier']} | Video: {x['video']}")
                i+=1
    except:
        print(f"{failed}File is missing or incorrectly formatted")

def commandCalculate():
    # This might be the worst code ever written
    completions = []
    with open(file, "r") as f:
        fileData = json.load(f)
        for x in fileData:
            levelName = x['name']
            levelPlace = x['place']
            for x in x['victors']:
                points = round(250 / ((int(levelPlace) + 4) * 0.2))
                completions.append({"player" : x, "level" : levelName, "place" : levelPlace, "points" : points})
        for x in completions:
            print(f"{x['player']} beat {x['level']} at place {x['place']} for {x['points']} list points")
        with open('./data/records.json', mode='w') as f:
            f.write(json.dumps(completions, indent=2))
        leaderboard = []
        for x in completions:
            if not {"player": x['player'], "points": 0} in leaderboard: leaderboard.append({"player": x['player'], "points": 0})
        for l in leaderboard:
            for x in completions:
                l['points'] = sum(int(x['points']) for x in completions if x['player'] == l['player'])
        sorted_leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)
        with open('./data/leaderboard.json', mode='w') as f:
            f.write(json.dumps(sorted_leaderboard, indent=2))
        i = 0
        for x in sorted_leaderboard:
            i = i + 1
            print(f"#{i} {x['player']} | List Points: {x['points']}")
        print(completed + "Calculated list points.")

def commandSubmit():
    level = input(f"{grey}(1/2) {white}Enter level name $ ")
    player = input(f"{grey}(2/2) {white}Enter player name $ ")
    print()
    final = input(f'{grey}Submit {player}s record to list? (Y/N) ')
    if final.lower() == "y": submitRecord(level, player)
    else: pass

def commandDelLevel():
    level = input(f"{grey}{white}Enter level name or position $ ")
    print()
    final = input(f'{grey}Remove "{level}" to list? (Y/N) ')
    if final.lower() == "y": delLevel(file, level)
    else: pass

def commandEditLevel():
    print("Welcome to the Edit Level Wizard!")
    print(f"{grey}Follow the steps to edit a level in the list file.")
    print()
    oldlevel = input(f"{grey}(1/7) {white}Enter old level name or position $ ")
    name = input(f"{grey}(2/7) {white}Enter level name $ ")
    place = input(f"{grey}(3/7) {white}Enter level position $ ")
    id = input(f"{grey}(4/7) {white}Enter level ID $ ")
    creators = input(f"{grey}(5/7) {white}Enter creator(s) $ ")
    verifier = input(f"{grey}(6/7) {white}Enter verifier $ ")
    video = input(f"{grey}(7/7) {white}Enter verification video url $ ")
    print()
    final = input(f'{grey}Overwrite "{oldlevel}" with "{name}"? (Y/N) ')
    if final.lower() == "y":
        delLevel(file, oldlevel)
        addLevel(file, name, place, creators, verifier, video, id)
    else: pass

def commandAddLevel():
    print("Welcome to the Add Level Wizard!")
    print(f"{grey}Follow the steps to add a level to the list file.")
    print()
    name = input(f"{grey}(1/6) {white}Enter level name $ ")
    place = input(f"{grey}(2/6) {white}Enter level position $ ")
    id = input(f"{grey}(3/6) {white}Enter level ID $ ")
    creators = input(f"{grey}(4/6) {white}Enter creator(s) $ ")
    verifier = input(f"{grey}(5/6) {white}Enter verifier $ ")
    video = input(f"{grey}(6/6) {white}Enter verification video url $ ")
    print()
    final = input(f"{grey}Add level to list? (Y/N) ")
    if final.lower() == "y":
        addLevel(file, name, place, creators, verifier, video, id)
        print(completed + white + f'Added "{name}" to the list, use the "calc" command to recalculate list points.')
    else: pass

def commandManager(command):
    if command.lower() == "help" or command == "?": print(helpText)
    elif command.lower() == "q" or command.lower() == "quit" or command.lower() == "exit": quit(0)
    elif command.lower() == "cls" or command.lower() == "clear": os.system("cls")
    elif command.lower() == "add" or command.lower() == "addlevel": commandAddLevel()
    elif command.lower() == "del" or command.lower() == "dellevel": commandDelLevel()
    elif command.lower() == "edit" or command.lower() == "editlevel": commandEditLevel()
    elif command.lower() == "view" or command.lower() == "viewlist" or command.lower() == "list": viewList()
    elif command.lower() == "submit": commandSubmit()
    elif command.lower() == "calc" or command.lower() == "calculate": commandCalculate()
    else: print(f"{failed}Command not found")

version = 2.0
if not os.path.isdir("./data/"): os.system("mkdir .\\data\\")
file = '.\\data\\list.json'
os.system(f"title List Manager {version}")
os.system(f"echo. >> {file}")

print(helpText)
while True:
    inp = input(prefix)
    commandManager(inp)
