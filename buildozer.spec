[app]
title = LED Controller
package.name = ledcontroller
package.domain = org.led
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,bleak,android,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT, ACCESS_FINE_LOCATION
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
