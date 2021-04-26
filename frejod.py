import requests
from bs4 import BeautifulSoup
import os
import wget
from termcolor import cprint


class helper:
    def SourceCode(self, url, selector1, selector2):
        source_Code = requests.get(url)
        plain_Text = source_Code.text
        soup = BeautifulSoup(plain_Text, "html.parser")
        soup_Select1 = ""
        for i in soup.select(selector1):
            if i.get("onclick") != None and len(i.get("onclick").split("'")) > 1:
                # print(i, " - ", i.get("onclick").split("'"))
                soup_Select1 = i.get("onclick").split("'")[1]
                if soup_Select1[:2] == "//":
                    soup_Select1 = "http:" + soup_Select1
        soup2 = BeautifulSoup(plain_Text, "html.parser")
        # title = soup.select(selector2 + " i")[0].getText()
        # author = soup.select(selector2)[0].getText().split(title)[0]
        if soup_Select1 == "":
            return "", ""
        else:
            soup_Select2 = soup.select(selector2)[0].getText().split("doi")[0]
            return soup_Select1, soup_Select2

    def makedir(self, given_path: str) -> bool:
        """Creates a directory if it doesnt exist without throwing an error
        If the parent directory doesnt exist, function will throw error

        Args:
            given_path (str): path to the directory

        Returns:
            bool: Status of directory creation
        """
        if not os.path.exists(given_path):
            os.mkdir(given_path)
            return True
        return False

    def download_file(self, url: str, filename: str):
        """Downloads a pdf file from the internet

        Args:
            url (str): URL of the file specified
            filename (str): PDF Filename

        Returns:
            [type]: Status of the file creation
        """

        if (not filename) or (not url):
            cprint(
                "[!] No file to downloaded because either given url is not proper or the file does not exist in the free-database",
                "red",
            )
            return 0
        try:
            req = requests.get(url, allow_redirects=True)
            cwd = f"{os.path.dirname(__file__)}\\downloads"
            self.makedir(cwd)
            if not os.path.exists(f"{cwd}\\{filename}.pdf"):
                open(f"{cwd}\\{filename}.pdf", "a+").close()
                with open(f"{cwd}\\{filename}.pdf", "wb") as f:
                    f.write(req.content)
                    cprint(f"Downloaded: {filename}", "green")
                    return 1
            else:
                cprint(f"Already Downloaded: {filename}", "green")
                return 1
        except:
            return 0

    def cleanPathName(self, filename: str) -> str:
        """Cleans the filename according to Windows file system

        Args:
            filename (str): name of the file to be cleaned

        Returns:
            str: Clean filename
        """
        x = filename
        for i in '\/:*?"<>|':
            x = x.replace(i, "")
        return x


class SingleDownload(helper):
    """Only used when you need to download a single File

    Args:
        helper (class): Helper class / Base class
    """

    def __init__(self, url):
        self.file_exist = False
        self.url = "https://sci-hub.se/" + url

    def download(self):
        """Gets the to be downloaded file URL and downloads the file"""
        if ".pdf" in self.url or "=pdf" in self.url:
            # if you get the direct link
            filename = self.cleanPathName(self.url.split("/")[-1].replace(".pdf", ""))
        else:
            # need to find the download link form the html content
            download_url, filename = self.SourceCode(self.url, "li a", "div#citation")
            filename = self.cleanPathName(filename)
            if download_url == "":
                filename = self.cleanPathName(
                    self.url.split("/")[-1].replace(".pdf", "")
                )
        self.download_file(download_url, filename)


class MultipleDownload:
    def printResolution(self, l: list = None) -> None:
        cwd = os.path.dirname(__file__)
        resolve_steps = [
            f"Create (if not exists) a file named list.txt at {cwd}",
            "Insert all the links to be downloaded in pdf format",
            "Rerun the application",
            "Downloading must start in seconds & ENJOY!",
        ]
        print("Resolve: ")
        for ind, step in enumerate(resolve_steps):
            print(f"{ind+1}. {step}")

    def readListFile(self):
        cwd = os.path.dirname(__file__)
        self.list2download = []
        path__ = f"{cwd}\\list.txt"
        if os.path.exists(path__):
            self.fileExistence = True
            with open(path__) as fp:
                self.list2download = [
                    line.strip() for line in fp.readlines() if line.strip()
                ]
        else:
            cprint("[!] FileNotFound Error: {cwd}\\list.txt", "red")
            self.fileExistence = False
            self.printResolution()

    def __init__(self):
        self.readListFile()

    def download(self) -> int:
        """Download all files

        Returns:
            int: 0 if file doesn't exist,1 if no url in the file, else 2
        """
        if not self.fileExistence:
            return 0
        if self.list2download:
            for i in range(len(self.list2download)):
                cprint(
                    f"# of remaining files to download: {len(self.list2download)}",
                    "cyan",
                )
                SingleDownload(self.list2download.pop(0)).download()
            cprint("All Done!", "magenta")
            return 2
        else:
            cprint("Nothing to download :(", "cyan")
            self.printResolution()
            return 1


if __name__ == "__main__":
    MultipleDownload().download()
