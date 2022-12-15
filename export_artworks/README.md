# 「音楽ファイル アートワーク エクスポート」プログラム

- 音楽ファイル (mp3, m4a) のアートワークをエクスポートする
- 主に MPD (Music Player Daemon) 用
<br/><br/>

# DEMO
<br/><br/>

# Features
<br/><br/>

# Requirement

* Python 3.9.7
* mutagen 1.46.0
<br/><br/>

# Installation
<br/><br/>

# Usage

## export_artworks.py

音楽ファイル (mp3, m4a) のアートワークをエクスポート

```
usage: export_artworks.py [-h] --music-dir MUSIC_DIRECTORY [--artwork-filename EXPORT_FILENAME] [--force-export]

Export music file artworks.

optional arguments:
  -h, --help            show this help message and exit
  -d MUSIC_DIR, --music-dir MUSIC_DIR
                        Music file directory
  -f ARTWORK_FILENAME, --artwork-filename ARTWORK_FILENAME
                        Artrwork file name
  -F, --force-export    Overwrite existing artwork files
```

# Note
<br/><br/>

# Author

* Shinji Miyahara
* Blog : https://tiger62shin.hatenablog.com/
<br/><br/>

# License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).
