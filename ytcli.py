import os
import platform
import setup
osname = platform.system()
mpv = ""
pip = ""
clear = ""
if osname == "Linux":
    mpv = "mpv"
    pip = "pip3"
    clear = "clear"
elif osname == "Windows":
    mpv = ".\mpv"
    pip = "pip"
    clear = "cls"

# Importing and installing dependencies
try:
    from youtubesearchpython import VideosSearch
    from pytube import Playlist
    import sqlite3
    hasmpv = len(os.popen(mpv+" --version").read())
    haspip = len(os.popen(pip+" --version").read())
    if hasmpv == 0 or haspip == 0:
        raise Exception
except:
    setup.install(osname)
    from youtubesearchpython import VideosSearch
    from pytube import Playlist
    import sqlite3

# To manipulate data in database
def change(query, data=[]):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    if len(data) == 0:
        cur.execute(query)
    else:
        # for queries having many attribute values to insert
        cur.executemany(query, data)
    con.commit()

# To fetch data from database
def fetch(query):
    con = sqlite3.connect("playlist.db")
    cur = con.cursor()
    res = cur.execute(query)
    li = res.fetchall()
    return li

# To display menu
def menu(title, options):
    os.system(clear)
    for i, val in enumerate(options):
        print(str(i+1) + "\t" + val)
    print("\q\tBack")
    choice = input(title)
    os.system(clear)
    return choice

# To search for a particular song
def search(osname):
    s = ''
    while True:
        s = input("Search: ")
        if s == "\q":
            break
        else:
            videosSearch = VideosSearch(s, limit=50)
            r = videosSearch.result()
            disp_li = []
            li = []
            os.system(clear)

            for i in r["result"]:
                title = i["title"][:40]
                if len(title) < 40:
                    title = title + " "*(40 - len(title))
                duration = i["duration"]
                views = i["viewCount"]["short"]
                disp_li.append("{0}\t\t\t{1}\t\t{2}".format(
                    title, duration, views))
                li.append(i["link"])

            # sending data to display search details
            play(disp_li, li)

# To prompt the user to select a song
def play(disp_li, li):
    music = menu(title="Choose Song: ", options=disp_li)
    if music == "\q":
        return
    else:
        choice = menu(title="Enter your choice: ", options=["Audio only mode", "Regular Mode"])
        print(disp_li[int(music)-1])
        print("\n", li[int(music)-1], "\n")
        if choice == "1":
            command = mpv+" {0} --no-video".format(li[int(music)-1])
        elif choice == "2":
            command = mpv+" {0}".format(li[int(music)-1])
        else:
            return ""
        os.system(command)
           
# To add new playlist
def addPlaylist():
    os.system(clear)
    name = input("Enter playlist name:")
    link = input("Enter url:")
    query = "CREATE TABLE IF NOT EXISTS Playlist(id, name, link)"
    change(query)
    query = "SELECT id FROM Playlist"
    id = 0
    li = fetch(query)

    # Setting playlist id
    if len(li) == 0:
        id = 1
    else:
        # id will be stored as str but converting to int for usage
        id = int(max(li)[0]) + 1

    data = [(str(id), name, link)]
    query = "INSERT INTO Playlist VALUES(?, ?, ?)"
    change(query, data)

# To prompt the user to select a playlist
def getPlaylist():
    query = "SELECT id, name FROM Playlist"
    li = fetch(query)
    res = True
    # Prompt user to add new playlist if there are no existing playlist saved
    if len(li) == 0:
        addPlaylist()
        li = fetch(query)
        res = False

    disp_li = []
    for i in li:
        disp_li.append(" ".join(i))
    # displays playlist menu
    playlist = menu(title="Choose playlist: ", options=disp_li)
    print("Updating playlist......")
    if playlist == "\q":
        return ["", False]
    index = int(playlist)
    query = "SELECT link FROM Playlist WHERE id='"+str(index)+"'"
    li = fetch(query)
    url = li[0][0]
    return url

# To prompt the user to select a playlist for deletion
def delPlaylist(osname):
    link = getPlaylist()
    query = "DELETE FROM Playlist WHERE link='"+link + "'"  # deleting playlist record from database
    change(query)

if __name__ == "__main__":
    while(True):
        choice = menu(title="Enter your choice: ", options=["Start Playlist", "Add Playlist", "Delete Playlist", "Search"])
        if choice == "1":
            link = getPlaylist()
            if len(link) != 0:
                mode = menu(title="Choose mode: ", options=["Audio only mode", "Regular Mode"])
                if mode == "1":
                    command = mpv+" "+link+" --no-video --shuffle"
                elif mode == "2":
                    command = mpv+" "+link+" --shuffle"
                else:
                    continue
                os.system(command)
        elif choice == "2":
            addPlaylist()
        elif choice == "3":
            delPlaylist(osname)
        elif choice == "4":
            search(osname)
        elif choice == "\q":
            exit()
