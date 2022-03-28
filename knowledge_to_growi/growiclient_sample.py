import argparse

from growiclient import GrowiClient

parser = argparse.ArgumentParser(description='Knowledge to GROWI contents migration.')
parser.add_argument('--growi_host', required=True, help='GROWI host name.')
parser.add_argument('--growi_port', required=True, help='GROWI API port no.')
parser.add_argument('--growi_apikey', required=True, help='GROWI API key.')
parser.add_argument('--growi_user', required=True, help='GROWI user name.')
args = parser.parse_args()

growi_client = GrowiClient(args.growi_host, args.growi_port, args.growi_apikey, args.growi_user)

title = 'GlowiClientで作成したページ'
content = """\
このページは Python で作成した GLOWI Client で作成しました。

![tora.png](/tora.png)
"""
page = growi_client.create_page(title, ['GlowiClient', 'TEST'], content)
file_url = growi_client.set_attachment(page, './knowledge_to_growi/attachments/tora.png')
page.replace_attachment('tora.png', file_url)
growi_client.update_page(page)

content = page.content + \
          """ \
\n

ページを更新します。

![ojiisan.png](/ojiisan.png)
"""

page = growi_client.create_page(page.title, page.tags, content)
file_url = growi_client.set_attachment(page, './knowledge_to_growi/attachments/ojiisan.png')
page.replace_attachment('ojiisan.png', file_url)
growi_client.update_page(page)
