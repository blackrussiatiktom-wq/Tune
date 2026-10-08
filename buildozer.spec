[app]
title = Tune
package.name = tune
package.domain = com.tunemusic

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,core/*
source.exclude_dirs = tests,bin,.buildozer,__pycache__

version = 0.1

requirements = python3,kivy,mutagen,pyjnius,android

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/icon.png

android.permissions = READ_EXTERNAL_STORAGE,READ_MEDIA_AUDIO
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

android.allow_backup = True

p4a.branch = master
p4a.extra_args = --jobs=1

[buildozer]
log_level = 2
warn_on_root = 0
