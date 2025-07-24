
[app]
title = Terminal
package.name = terminal
package.domain = com.sezer
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json
icon.filename = assets/icon.png
version = 1.0.0
orientation = portrait
fullscreen = 0
requirements = python3,kivy,kivymd,tinydb,requests,plyer
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 35
android.minapi = 21
android.ndk = 25b
android.sdk = 35
android.archs = arm64-v8a, armeabi-v7a
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 0
