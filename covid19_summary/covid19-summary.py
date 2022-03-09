import requests
import io
import pandas as pd
from datetime import date, datetime, timedelta
from jinja2 import Template
import argparse


def main():

    parser = argparse.ArgumentParser(description='COVID19 patients Summary')
    parser.add_argument('-u', '--url', required=True)
    parser.add_argument('-f', '--htmlfile', required=True)
    parser.add_argument('-t', '--templatefile', required=True)
    args = parser.parse_args()

    print(args.url)
    print(args.htmlfile)

    # 感染者の CSV データを取り込んで pandas で読み込む
    res = requests.get(args.url)
    df = pd.read_csv(io.BytesIO(res.content), encoding='shift-jis', encoding_errors='ignore')
    df['Date'] = pd.to_datetime(df['公表_年月日'])

    # 日付ごとにデータの件数を数える
    number_of_patients = df.groupby('Date').size() \
        .reset_index(name='Count') \
        .set_index('Date')

    # 前週の同一曜日と比較した状態を設定する
    number_of_patients['Status'] = number_of_patients.apply(get_status, args=(number_of_patients,), axis=1)

    html = generate_html(number_of_patients, args.templatefile)
    with open(args.htmlfile, 'wt') as f:
        f.write(html)


# 指定された日付毎のデータ件数 (感染者数) のステータスを返す
#   'yellow' : 前週の同一曜日より少なくなっている
#   'red'    : 前週の同一曜日より多くなっている
def get_status(row, number_of_patients):
    last_week_date = row.name - timedelta(days=7)
    if last_week_date in number_of_patients.index:
        if row['Count'] <= number_of_patients['Count'][last_week_date]:
            return 'yellow'
        return 'red'
    else:
        return 'red'


# 開始 / 終了日から週毎の日付のリストを返すジェネレータ
def dates_of_weeks(start, stop):
    current = start
    if current.isoweekday() != 7:
        current = current - timedelta(days=current.isoweekday())
    end_date = stop
    if end_date.isoweekday() != 7:
        end_date = end_date + timedelta(days=(6-end_date.isoweekday()))
    else:
        end_date = end_date + timedelta(days=6)
    step = timedelta(days=7)
    while current <= end_date:
        dates = []
        for n in range(7):
            dates.append(current + timedelta(days=n))
        yield dates
        current = current + step


# 指定された日毎の感染者数データからレポート用の HTML を生成する
def generate_html(number_of_patients, template_file):
    with open(template_file, 'rt') as f:
        html = f.read()

    template = Template(html)
    data = {
        'dates_of_weeks': dates_of_weeks(number_of_patients.index.min(), pd.to_datetime(date.today())),
        'number_of_cases': number_of_patients,
        'daybox_classes': ['daybox', 'daybox', 'daybox', 'daybox', 'daybox', 'daybox', 'daybox'],
        'generate_date': datetime.now().strftime('%Y/%-m/%-d %-H:%-M'),
    }
    return template.render(data)


if __name__ == "__main__":
    main()
