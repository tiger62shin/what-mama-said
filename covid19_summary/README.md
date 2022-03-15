# 「北九州市 新型コロナウイルス感染症 陽性患者数」日毎集計プログラム

「北九州市 新型コロナウイルス感染症 陽性患者数」のオープンデータからカレンダー形式で日毎の感染者数を表示する HTML ファイルを出力します。

# DEMO

[北九州市　新型コロナウイルス感染症　陽性患者数のサマリー](https://www.calcium.mydns.jp/kitakyushu_covid19_summary.html)

# Features

# Requirement

* Python 3.9.7
* requests 2.27.1
* pandas 1.4.1
* jinja2 3.0.2

# Installation

# Usage

```
usage: covid19-summary.py [-h] -u URL -f HTMLFILE -t TEMPLATEFILE

COVID19 patients Summary

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL
  -f HTMLFILE, --htmlfile HTMLFILE
  -t TEMPLATEFILE, --templatefile TEMPLATEFILE
```

* Example
```
URL=https://ckan.open-governmentdata.org/dataset/aad66771-0e86-4d38-b08e-7b74d31f442e/resource/111b9476-bc80-4700-9551-3ba8a4ffcebc/download/401005_kitakyushu_covid19_patients.csv
HTMLFILE=kitakyushu_covid19_summary.html
TEMPLATEFILE=covid19-summary-template.html
python covid19-summary.py --url=$URL --htmlfile=$HTMLFILE --templatefile=$TEMPLATEFILE
```

# Note

# Author

* Shinji Miyahara
* Blog : https://tiger62shin.hatenablog.com/

# License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).
