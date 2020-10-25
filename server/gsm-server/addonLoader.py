import json
import glob
import zipfile as zipf

def addon_loader():
    gameLoads = dict()
    dirName = './games'
    zipList = glob.glob(dirName + '/*.zip')


    for zipname in zipList:
        addonFile = zipf.ZipFile(zipname)
        manifestFileRaw = addonFile.read('manifest.json')
        manifestFile = json.loads(manifestFileRaw)
        gameLoads = gameLoads | manifestFile

    return (gameLoads)
