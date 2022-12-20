import os
def install(osname):
    if osname == "Linux":
        distro_name = os.popen("sed -n -e '/^ID=/p' /etc/os-release").read()[3:-1]
        debian_based = ['debian', 'ubuntu', 'linuxmint', 'popos', 'zorin', 'elementary']
        arch_based = ["manjaro", 'arch', 'endeavouros']
        if distro_name in debian_based:
            os.system("sudo apt install mpv")
            os.system("sudo apt install python3-pip")
        elif 'fedora' in distro_name:
            os.system("sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
            os.system("sudo dnf install mpv mpv-libs")
            os.system("sudo dnf install python3-pip")
        elif distro_name in arch_based:
            os.system("sudo pacman -S python-pip")
            os.system("sudo pacman -S mpv")
        else:
            print("Please install the following dependencies:")
            print("1. python3-pip")
            print("2. mpv")

        # Installing python packages
        pkgmgr = "pip3"
        os.system(pkgmgr+" install youtube-search-python")
        os.system(pkgmgr+" install pytube")
        os.system(pkgmgr+" install yt-dlp")
        os.system("mv ~/.local/bin/yt-dlp ~/.local/bin/youtube-dl")
    else:
        # Installing python packages
        pkgmgr = "pip"
        os.system(pkgmgr+" install requests")
        os.system(pkgmgr+" install youtube-search-python")
        os.system(pkgmgr+" install pytube")
        os.system(pkgmgr+" install yt-dlp")
        os.system(pkgmgr+" install py7zr")
        
        import requests
        # Downloading and extracting mpv
        print("Downloading mpv....")
        url = "https://sourceforge.net/projects/mpv-player-windows/files/64bit-v3/mpv-x86_64-v3-20221002-git-2207236.7z/download"

        response = requests.get(url)
        open("mpv.7z", "wb").write(response.content)
        print("Extracting downloaded files....")
        os.system("py7zr x mpv.7z")
        os.system("del mpv.7z")
