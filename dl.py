import os
import shutil
from zipfile import ZipFile
from urllib.request import urlopen
from arhivi import archives

print("Downloading archives...")
if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists(os.path.join("data", "dl")):
    os.mkdir(os.path.join("data", "dl"))

for archive_name,meta in archives.items():
    if not os.path.exists(os.path.join("data", "dl",archive_name)):
        print("Downloading", archive_name)
        resp = urlopen(meta['url'])

        output = open(os.path.join("data", "dl", archive_name), 'wb')
        output.write(resp.read())
        output.close()
    else:
        print("Archive", archive_name, "exists, skipping download")

    zipfile = ZipFile(os.path.join("data", "dl",archive_name))
    for file in zipfile.namelist():
        for extractable_file in meta['files']:
            if extractable_file in file:
                if os.path.exists(os.path.join("data", extractable_file)):
                    print("File", extractable_file, "exists, skipping extraction")
                    continue
                else:
                    print("Extracting ", extractable_file)
                    source = zipfile.open(file,'r')
                    target = open(os.path.join("data", extractable_file),'wb')
                    shutil.copyfileobj(source, target)
