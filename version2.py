from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

def downloadLoop(siteDirectory,yearStart,yearEnd,examNumber,examSeason,season,paperNumber,variants,missingFile):
    for year in range(yearStart,yearEnd+1):
        print(f"Downloading {examNumber} 20{year} {season} paper {paperNumber} ms and qp")
        paperCodes = ['ms','qp']
        for paperCode in paperCodes:
            for variant in range(0,variants+1):
                if variant == 0 or variant == "0":
                    variant = ""
                paper = download(siteDirectory,examNumber,examSeason,year,paperCode,paperNumber,variant)
                filePath = Path(f"./downloads/{examNumber}_{examSeason}{year}_ms_{paperNumber}{variant}.pdf")
                filePath.write_bytes(paper.content)
                try:
                    PdfReader(filePath)
                except PdfReadError:
                    print(f"Invalid PDF file ({filePath})")
                    missingFile.write(f"\nMISSING: {examNumber}_{examSeason}{year}_ms_{paperNumber}{variant}.pdf")
                    remove(filePath)
                else:
                    pass

def main():
    configFile = open("configV2.json", "r").read()
    config = loads(configFile)
    Path("./downloads").mkdir(parents=True, exist_ok=True)
    missingFile = open("./downloads/missing.txt","a")
    if (config['yearStart'] < config['yearEnd'] or config['yearStart'] == config['yearEnd']) and (config['season'] == "w" or config['season'] == "s" or config['season'] == "m"):
        if config['season'] == "w":
            examSeason = "Winter"
        elif config['season'] == "s":
            examSeason = "Summer"
        elif config['season'] == "m":
            examSeason = "March"
        missingFile.write(f"\n\nDOWNLOADING from 20{config['yearStart']} to 20{config['yearEnd']} {config['examNumber']} {examSeason} papers {config['paperNumber']} - Missing Files if any:")
        downloadLoop(config['siteDirectory'],config['yearStart'],config['yearEnd'],config['examNumber'],config['season'],examSeason,config['paperNumber'],config['variants'],missingFile)
        missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    elif (config['yearStart'] < config['yearEnd'] or config['yearStart'] == config['yearEnd']) and (config['season'] == "all"):
        seasons = {"w":"Winter","s":"Summer","m":"March"}
        for season in seasons.keys():
            examSeason = seasons[season]
            missingFile.write(f"\n\nDOWNLOADING from 20{config['yearStart']} to 20{config['yearEnd']} {config['examNumber']} {examSeason} papers {config['paperNumber']} - Missing Files if any:")
            downloadLoop(config['siteDirectory'],config['yearStart'],config['yearEnd'],config['examNumber'],season,examSeason,config['paperNumber'],config['variants'],missingFile)
        missingFile.write(f"\n\n If nothing was written above in MISSING, you are good! Redownloading may be required for other files or some papers might just not exist on the directory you are downloading from or maybe just not exist entirely.\n")
    else:
        print("ERROR")
    missingFile.close()

if __name__ == "__main__":
    main()