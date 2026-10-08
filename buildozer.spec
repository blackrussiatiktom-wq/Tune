[app]
title = Tune
package.name = tune
package.domain = com.tunemusic

source.dir = .
source.include_exts = py,kv,png,jpg,ttf
source.include_patterns = assets/*,assets/fonts/*,core/*,ui/*
source.exclude_dirs = tests,bin,.buildozer,__pycache__

version = 0.3

requirements = python3,kivy,mutagen

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/icon.png
android.presplash_color = #000000

android.permissions = READ_EXTERNAL_STORAGE,READ_MEDIA_AUDIO
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

android.allow_backup = True

p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
