import glob
import os
import shutil
from pathlib import Path
import zipfile
import tempfile
import sys

BUNDLETOOLS_MAC_PATH = '/Users/User/WORKSPACE/TOOLS/buildtools/bundletool-all-1.13.2.jar'
BUNDLETOOLS_WIN_PATH = 'C:\WORKSPACE\TOOLS\buildtools\bundletool-all-1.13.2.jar'

KEYSTORE_MAC_PATH = '/Users/User/WORKSPACE/TOOLS/buildtools/release.jks'
KEYSTORE_WIN_PATH = 'C:\WORKSPACE\TOOLS\buildtools\release.jks'

KEYSTORE_ALIAS = 'ali'
KEYSTORE_PASS = 'Pass'

def removeIfExists(path):
    if Path.exists(path):
        os.remove(path)


def convertappBundle(aabPath, apksPath, bundletoolsPath, keystorePath):
    cmd = f'java -jar "{bundletoolsPath}" build-apks --bundle="{aabPath}" --output="{apksPath}" --ks="{keystorePath}" --ks-key-alias="{KEYSTORE_ALIAS}" --ks-pass=pass:{KEYSTORE_PASS} --mode=universal'
    os.system(f'echo {cmd}')
    os.system(cmd)


buildDirectory = sys.argv[1]
builds = glob.glob(buildDirectory + '/*.aab')
buildPath = builds[-1]
buildName = Path(buildPath).stem

tempDirectory = tempfile.TemporaryDirectory()
tempDirPath = tempDirectory.name
print(f'Temp dir: {tempDirPath}')
apksPath = Path(tempDirPath, buildName + '.apks')

# Extracted artifacts
tocPath = Path(tempDirPath, 'toc.pb')
universalApkPath = Path(tempDirPath, 'universal.apk')

apkPath = Path(buildDirectory, buildName + '.apk')

print('Check your platform')
if sys.platform == 'darwin':
    print('Hello MacOS')
    print('Converting AAB to APKS in MacOS')
    convertappBundle(buildPath, apksPath, BUNDLETOOLS_MAC_PATH, KEYSTORE_MAC_PATH)
elif sys.platform == 'win32':
    print('Hello Windows')
    print('Converting AAB to APKS in Windows')
    convertappBundle(buildPath, apksPath, BUNDLETOOLS_WIN_PATH, KEYSTORE_WIN_PATH)
else:
    print('WTF')

if not Path.exists(apksPath):
    print("Something went wrong! Can't extract apks")
    exit()

print('Extracting APK from APKS')
with zipfile.ZipFile(apksPath, 'r') as archive:
    archive.extractall(tempDirPath)

print('Pushing artifacts')
shutil.move(universalApkPath, apkPath)

print('Cleaning up')
tempDirectory.cleanup()
