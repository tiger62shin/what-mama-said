# Excel ファイルの行をテキストファイル出力

Excel ファイルの 1 行を 1 つの書式化されたテキストファイルに出力します。

# DEMO

# Features

# Requirement

* Python 3.9.7
* openpyxl 3.0.9
* jinja2 3.0.2

# Installation

# Usage

```
usage: excel_to_formatted_text.py [-h] -x EXCELFILE -s SHEETNAME -o OUTPUTFILE [-oe OUTPUTFILE_ENCODING] [-lt {cr,lf,crlf}] -t TEMPLATEFILE [-te TEMPLATEFILE_ENCODING]
                                  [-r STARTROW] [-c STARTCOL]

Excel to formated text

optional arguments:
  -h, --help            show this help message and exit
  -x EXCELFILE, --excelfile EXCELFILE
                        Excel filename
  -s SHEETNAME, --sheetname SHEETNAME
                        Sheet name
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Output filename format
  -oe OUTPUTFILE_ENCODING, --outputfile-encoding OUTPUTFILE_ENCODING
                        Output text file encoding
  -lt {cr,lf,crlf}, --outputfile-lineterminator {cr,lf,crlf}
                        Output text file line terminator
  -t TEMPLATEFILE, --templatefile TEMPLATEFILE
                        Template text filename
  -te TEMPLATEFILE_ENCODING, --templatefile-encoding TEMPLATEFILE_ENCODING
                        Template text file encoding
  -r STARTROW, --startrow STARTROW
                        Excel sheet start row no
  -c STARTCOL, --startcol STARTCOL
                        Excel sheet start column no
  -b BLANK_SKIP_COLUMNS, --blank-skip-columns BLANK_SKIP_COLUMNS
                        Skip if this column is blank```
- --excelfile

  入力する Excel ファイルを指定します。省略不可<br/>
  openpyxl で読み込めるものであれば Excel ファイルの形式に特に制限はありません
- --sheetname

  テキストファイルに出力する内容が記載されている Excel シートの名前を指定します。省略不可<br/>
  注意点
    - 出力対象となる範囲の最初の行は見出し行として使われ、見出し行のセルの値を項目名として使用します (重複していたはなりません)。
    - 出力対象となる範囲の開始行列位置は startrow, startcol で指定することができますが、終了行列位置はデータがある最大の行列位置となります。
- --outputfile

  出力ファイル名を指定します。出力ファイル名には {} で括って出力行データの項目名を指定することができます。例えば<br/>
  ```
  {名前}.txt
  ```
  とすると出力対象行の「名前」列の値のファイル名となります。<br/>
  出力ファイル名にはディレクトリを含めることができます。
  ```
  data/{県}/{名前}.txt
  ```
  ディレクトリが存在しない場合には作成されます。
- --outputfile-encoding

  出力ファイルのエンコーディングを指定します。指定を省略した場合には 'utf8' となります。
- --outputfile-lineterminator
  出力ファイルの改行コードを cr, lf, crlf のいずれかで指定します。指定を省略した場合には 'lf' となります。
- --templatefile

  出力ファイルの書式が記載されたテキストファイルを指定します。省略不可<br/>
  テンプレートファイルは jinja2 のテンプレート構文で記載します。'{{ 項目名 }}' のように記載された部分に Excel ファイルの行の該当する項目名の列位置のデータが出力されます。
- --templatefile-encoding

  テンプレートファイルのエンコーディングを指定します。指定を省略した場合には 'utf8' となります。
- --startrow

  読み込むデータの開始行位置を指定します。省略した場合には 1 となります。<br/>
  startrow で指定された行が見出し行となります。
- --startcol
  読み込むデータの開始列位置を指定します。省略した場合には 1 となります。
- --blank-skip-columns
  指定された列の値がブランクの時、その行をスキップします。省略可<br/>
  複数の列を指定する場合は
  ```
  --blank-skip-columns xxxxx --blank-skip-columns yyyyy
  ```
  のように指定します。

- Example
  - Excel ファイル
    <img width="1046" alt="image" src="https://user-images.githubusercontent.com/101082280/166106815-8ba8dafd-88a2-4353-970a-3afc3ac624c0.png">
  - テンプレートファイル
    ```
    氏名 : {{ 氏名 }}
    電話番号 : {{ 電話番号 }}
    郵便番号 : {{ 郵便番号 }}
    住所 : {{ 住所1 }}{{ 住所2 }}
    ```
  - 実行
    ```
    excel_to_formatted_text.py --excelfile=personal_infomation.xlsx --sheetname=personal_infomation --outputfile={住所1}/{氏名}.txt --templatefile=sample_template.txt
    ```
  - 出力結果
    ```
    福岡県% ls -l
    total 80
    -rw-r--r--   1 tiger  staff  123  4 30 21:58 三輪順一.txt
    -rw-r--r--@  1 tiger  staff  137  4 30 21:58 中岡治雄.txt
    -rw-r--r--   1 tiger  staff  119  4 30 21:58 内村佳祐.txt
    -rw-r--r--   1 tiger  staff  136  4 30 21:58 川島知里.txt
    -rw-r--r--   1 tiger  staff  121  4 30 21:58 松元夏音.txt
    -rw-r--r--@  1 tiger  staff  136  4 30 21:58 横川昌信.txt
    -rw-r--r--   1 tiger  staff  124  4 30 21:58 正木重樹.txt
    -rw-r--r--   1 tiger  staff  117  4 30 21:58 神保和奏.txt
    -rw-r--r--   1 tiger  staff  110  4 30 21:58 野中忠広.txt
    -rw-r--r--   1 tiger  staff  142  4 30 21:58 近藤正次郎.txt
    ```
    ```
    福岡県% cat 三輪順一.txt
    氏名 : 三輪順一
    電話番号 : 0949030476
    郵便番号 : 807-0004
    住所 : 福岡県遠賀郡水巻町樋口東3-18
    ```

# Note

# Author

* Shinji Miyahara
* Blog : https://tiger62shin.hatenablog.com/

# License

[MIT license](https://en.wikipedia.org/wiki/MIT_License).
