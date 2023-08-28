import requests
import zipfile

class VsixPackage:
    def __init__(self, publisher, extension, version, target=None):
        self.publisher = publisher
        self.extension = extension
        self.version = version
        self.target = target

    def get_url(self):
        url = (
            f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/"
            f"{self.publisher}/vsextensions/{self.extension}/{self.version}/vspackage"
        )
        if self.target:
            url += f"?targetPlatform={self.target}"
        return url

    def get_vsix_name(self):
        return f"{package.publisher}.{package.extension}-{package.version}.vsix"


python_packages = [
    VsixPackage("ms-python", "python", "2023.14.0"),
    VsixPackage("ms-python", "vscode-pylance", "2023.8.40"),
    VsixPackage("ms-python", "mypy-type-checker", "2023.2.0"),
    VsixPackage("ms-python", "black-formatter", "2023.4.1"),
    VsixPackage("ms-python", "isort", "2023.10.1"),
    VsixPackage("fudgepops", "kaitai-struct-vscode", "0.9.0"),
    VsixPackage("charliermarsh", "ruff", "2023.34.0", "win32-x64"),
    VsixPackage("redhat", "vscode-xml", "0.26.1", "win32-x64"),
    VsixPackage("tamasfe", "even-better-toml", "0.19.2"),
]


with requests.session() as session:
    session.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
        "host": "marketplace.visualstudio.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.5",
        "accept-encoding": "gzip, deflate, br",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "Sec-Fetch-Site" : "none",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1"
    })
    session.get("https://marketplace.visualstudio.com/")
    
    with zipfile.ZipFile("vscode-python-extensions.zip", 'w') as zip_file:
        for package in python_packages:
            data = b''
            with session.get(package.get_url(), stream=True) as stream:
                file_size = int(stream.headers["Content-Length"])
                for content in stream.iter_content(1024*1024, decode_unicode=False):
                    if content:
                        data += content
                        print(f"got {min(len(data)/file_size*100, 100):.2f}%", end='\r')
            zip_file.writestr(package.get_vsix_name(), data)