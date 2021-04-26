import requests
from bs4 import BeautifulSoup
import os
import wget


class helper:
    def SourceCode(self, url, selector1, selector2):
        source_Code = requests.get(url)
        plain_Text = source_Code.text
        soup = BeautifulSoup(plain_Text, "html.parser")
        soup_Select1 = ""
        # print(soup.select(selector1))
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

    def download_file(self, url, filename):
        req = requests.get(url, allow_redirects=True)
        cwd = os.path.dirname(__file__)
        if not os.path.exists(f"{cwd}\\{filename}.pdf"):
            open(f"{cwd}\\{filename}.pdf", "a+").close()
            with open(f"{cwd}\\{filename}.pdf", "wb") as f:
                f.write(req.content)
                print(f"Downloaded: {filename}")
        else:
            print(f"Already Downloaded: {filename}")

    def cleanFolderName(self, filename):
        x = filename
        for i in '\/:*?"<>|':
            x = x.replace(i, "")
        return x


class SingleDownload(helper):
    def __init__(self, url):
        self.url = "https://sci-hub.se/" + url
        self.download()

    def download(self):
        if ".pdf" in self.url or "=pdf" in self.url:
            filename = self.cleanFolderName(self.url.split("/")[-1].replace(".pdf", ""))
            self.download_file(self.url, filename)
        else:
            download_url, filename = self.SourceCode(self.url, "li a", "div#citation")
            filename = self.cleanFolderName(filename)
            if download_url == "":
                filename = self.cleanFolderName(
                    self.url.split("/")[-1].replace(".pdf", "")
                )
                self.download_file(self.url, filename)
            else:
                self.download_file(download_url, filename)


class MultipleDownload:
    def __init__(self):
        cwd = os.path.dirname(__file__)
        self.list2download = []
        try:
            with open(f"{cwd}\\list2download.txt") as fp:
                self.list2download = [line.strip() for line in fp.readlines()]
        except:
            print(
                f"FileN0Tf0unD Err0r: {cwd}\\list2download.txt\nResolve:\n"
                + f"1. Create a file named list2download.txt at {cwd}\n"
                + "2. Insert all the links to download the pdf\n"
                + "3. Re run the application\n"
                + "4. Downloading must start in seconds & ENJOY!"
            )
        # print(self.list2download)
        self.download_all()

    def download_all(self):
        for i in range(len(self.list2download)):
            print(f"# of remaining files to download: {len(self.list2download)}")
            SingleDownload(self.list2download.pop(0))
        print("All Done!")


if __name__ == "__main__":
    x = MultipleDownload()
