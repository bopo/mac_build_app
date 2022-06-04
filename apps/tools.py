from PyQt5.Qt import *


def set_infolist(name, app):
    info = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDisplayName</key>
	<string>{name}</string>
	<key>CFBundleExecutable</key>
	<string>MacOS/{app}</string>
	<key>CFBundleIconFile</key>
	<string>app.icns</string>
	<key>CFBundleIdentifier</key>
	<string>{name}<</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>{name}<</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>0.0.0</string>
	<key>NSHighResolutionCapable</key>
	<true/>
</dict>
</plist>'''
    return info