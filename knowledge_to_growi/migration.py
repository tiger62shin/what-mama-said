import psycopg2
from psycopg2.extras import DictCursor
import argparse

from growiclient import GrowiClient

parser = argparse.ArgumentParser(description='Knowledge to GROWI contents migration.')
parser.add_argument('--kbdb_host', required=True, help='Knowledge DataBase hostname.')
parser.add_argument('--kbdb_port', required=False, default=5432, help='Knowledge DataBase port no.')
parser.add_argument('--kbdb_name', required=True, help='Knoeledge DataBase name.')
parser.add_argument('--kbdb_user', required=True, help='Knowledge DataBase user name.')
parser.add_argument('--kbdb_passwd', required=True, help='Knowledge DataBase user password.')
parser.add_argument('--growi_host', required=True, help='GROWI host name.')
parser.add_argument('--growi_port', required=True, help='GROWI API port no.')
parser.add_argument('--growi_usessl', action='store_true', help='GROWI access with SSL.')
parser.add_argument('--growi_apikey', required=True, help='GROWI API key.')
parser.add_argument('--growi_user', required=True, help='GROWI user name.')
args = parser.parse_args()


# DB接続関数
def get_connection():
    return psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'
                            .format(user=args.kbdb_user,
                                    password=args.kbdb_passwd,
                                    host=args.kbdb_host,
                                    port=args.kbdb_port,
                                    dbname=args.kbdb_name))


# 添付ファイルの移行
def migrate_attachments(conn, growi_client, page, id):
    with conn.cursor(name='files_cursor', cursor_factory=DictCursor) as file_cur:
        id_col = 'knowledge_id'
        if growi_client.is_draft():
            id_col = 'draft_id'
        file_cur.execute('select file_no, knowledge_id, comment_no, draft_id, file_name, file_binary '
                         'from knowledge_files '
                         'where {} = %s'.format(id_col), (id, ))
        for file_row in file_cur:
            print(file_row['file_name'])
            file_path = './knowledge_to_growi/attachments/' + file_row['file_name']
            with open(file_path, 'wb') as f:
                f.write(file_row['file_binary'])
            file_url = growi_client.set_attachment(page, file_path)
            page.replace_attachment(file_row['file_name'], file_url)


# Knowledge -> GROWI ページ移行
def migrage_knowledge(conn, growi_client):
    with conn.cursor(name='knowledges_cursor', cursor_factory=DictCursor) as kb_cur:
        if growi_client.is_draft():
            kb_cur.execute('select draft_id, tag_names, title, content from draft_knowledges '
                           'where delete_flag = 0 '
                           '  and (knowledge_id is null or knowledge_id not in (select knowledge_id from knowledges)) '
                           'order by draft_id')
        else:
            kb_cur.execute('select knowledge_id, tag_names, title, content '
                           'from knowledges '
                           'where delete_flag = 0 '
                           'order by knowledge_id')
        titles = {}
        for kb_row in kb_cur:
            if growi_client.is_draft():
                id = kb_row['draft_id']
            else:
                id = kb_row['knowledge_id']
            print(str(id) + ' : ' + kb_row['title'])
            page_tags = []
            if kb_row['tag_names']:
                page_tags = kb_row['tag_names'].replace(chr(0xa0), '').split(',')
                if len(page_tags) == 1:
                    page_tags.append('')
            title = kb_row['title']
            if title in titles:
                titles[title] += 1
                title += '({})'.format(str(titles[title]))
            else:
                titles[title] = 1
            content = kb_row['content']
            if len(content) == 0:
                content = "## {}".format(title)
            page = growi_client.create_page(title, page_tags, content)
            migrate_attachments(conn, growi_client, page, id)
            growi_client.update_page(page)


with get_connection() as conn:
    # 並び順を後ろの方にするためにドラフトページを先に移行
    growi_client = GrowiClient(
        args.growi_host, args.growi_port, args.growi_apikey, args.growi_user, args.growi_usessl, True)
    migrage_knowledge(conn, growi_client)

    # 公開ページの移行
    growi_client = GrowiClient(
        args.growi_host, args.growi_port, args.growi_apikey, args.growi_user, args.growi_usessl)
    migrage_knowledge(conn, growi_client)
