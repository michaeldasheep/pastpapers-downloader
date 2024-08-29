from pathlib import Path
from json import loads
from questionDownload import download
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from os import remove

def main():
    configFileLocation = open("config.deprecatedv1.json", "r")
    configFile = configFileLocation.read()
    config = loads(configFile)
    configFileLocation.close() # Addressed bug opened by bohrium2b
    cond = True
    while cond == True:
        Path("./downloads").mkdir(parents=True, exist_ok=True)
        for i in range(1,4):
            paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"ms",config['paperNumber'],i)
            filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_ms_{config['paperNumber']}{i}.pdf")
            filePath.write_bytes(paper.content)
            try:
                PdfReader(filePath)
            except PdfReadError:
                print(f"invalid PDF file ({filePath})")
                remove(filePath)
            else:
                pass
        for i in range(1,4):
            paper = download(config['siteDirectory'],config['examNumber'],config['season'],config['year'],"qp",config['paperNumber'],i)
            filePath = Path(f"./downloads/{config['examNumber']}_{config['season']}{config['year']}_qp_{config['paperNumber']}{i}.pdf")
            filePath.write_bytes(paper.content)
            try:
                PdfReader(filePath)
            except PdfReadError:
                print(f"invalid PDF file ({filePath})")
                remove(filePath)
            else:
                pass
        cond = False

if __name__ == "__main__":
    main()
