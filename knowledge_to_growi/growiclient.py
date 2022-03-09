import os
import requests
import json
import mimetypes
import re


class GrowiClient:
    """
    GROWI クライアント
    """
    def __init__(self, growihost, port, apitoken, username, ssl=False,
                 draft=False):
        """
        Parameters
        ----------
        growihost : str
            GROWI ホスト名
        apitoken : str
            GROWI API Token
        username : str
            GROWI ユーザ名
        ssl : bool
            true : Yes
            false : No
        draft : bool
            true  ドラフト
            false 公開
        """
        self.base_url = 'http{}://{}'.format('s' if ssl else '', growihost)
        if port:
            self.base_url += ':{}'.format(port)
        self.base_url += '/_api'
        self.base_path = '/{}'.format(username)
        self.params = {"access_token": apitoken, "user": username}
        self.draft = draft

        self.cur_pages = {}
        growi_res = self.__get('pages.list', {"limit": -1})
        for page in growi_res['pages']:
            self.cur_pages[page['path']] = GrowiPage(page['_id'], page['path'],
                                                     page['revision'],
                                                     None, None, None)

    def create_page(self, title, tags, content):
        """
        GROWI のベージを作製する

        Parameters
        ----------
        title : str
            ページ・タイトル
        tags : array
            タグ
        content : str
            ページ本文

        Retruns
        -------
        page : GrowiPage
            GROWI のページを表すオブジェクト
        """
        path = self.__to_path(title)
        if path in self.cur_pages:
            page = self.cur_pages[path]
            page.title = title
            page.tags = tags
            page.content = content
            self.__initialize_attachments_info(page)
            self.update_page(page)
            return page

        payload = {"body": content, "path": path}
        res = self.__post('v3/pages', payload)
        self.cur_pages[path] = GrowiPage(res['page']['id'], res['page']['path'],
                                         res['page']['revision'], title, tags, content)
        return self.cur_pages[path]

    def set_attachment(self, page, file_path):
        """
        指定されたファイルを指定された GROWI ページの添付ファイルとして設定する

        Parameters
        ----------
        page : GrowiPage
            移行対象の GROWI ページを表すオブジェクト
        file_path : str
            移行するファイルのパス
        Retruns
        -------
        file_url : 追加した添付ファイルの参照 url
        """
        file_name = os.path.basename(file_path)
        attachment_info = page.get_attachment_info(file_name)
        if attachment_info:
            self.__remove_attachment(page, attachment_info)
        mime_type = mimetypes.guess_type(file_name)[0]
        file = {'file': (file_name, open(file_path, 'rb'), mime_type)}
        payload = {"page_id": page.id, "path": page.path}
        res = self.__post('attachments.add', payload, file)

        page.add_attachment_info(res['attachment']['id'],
                                 res['attachment']['originalName'],
                                 res['attachment']['filePathProxied'])

        return res['attachment']['filePathProxied']

    def update_page(self, page):
        """
        GROWI ページを更新する

        Parameters
        ----------
        page : GrowiPage
            GROWI ページを表すオブジェクト
        """
        payload = {"body": page.content,
                   "pageTags": page.tags,
                   "page_id": page.id,
                   "revision_id": page.revision}
        res = self.__post('pages.update', payload)
        page.revision = res['page']['revision']

    def is_draft(self):
        """
        DRAFT ページに対する処理かどうかを返す

        Retruns
        -------
        draft : bool
            True  Yes
            False No
        """
        return self.draft

    def __initialize_attachments_info(self, page):
        """
        指定された GROWI ページ情報の添付ファイル情報を初期化する

        Parameters
        ----------
        page : GrowiPage
            GROWI ページを表すオブジェクト
        """
        page_no = 1
        while True:
            growi_res = self.__get('v3/attachment/list',
                                   {"pageId": page.id, "page": page_no})
            if len(growi_res['paginateResult']['docs']) == 0:
                break
            page.initialize_attachments_info(growi_res)
            page_no += 1

    def __remove_attachment(self, page, attachment_info):
        """
        添付ファイルを削除する

        Parameters
        ----------
        page : GrowiPage
            GROWI ページを表すオブジェクト
        attachment_info : GrowiAttachment
            削除する添付ファイル情報
        """
        print("Remove attachment : {}".format(attachment_info.original_name))
        payload = {"attachment_id": attachment_info.id}
        self.__post('attachments.remove', payload)

        page.remove_attachment_info(attachment_info.id)

    def __post(self, verb, payload, file=None):
        """
        GROWI サーバーに POST リクエストを行う

        Parameters
        ----------
        verb : str
            GROWI API
        payload : dict
            リクエストボディ
        file : dict
            アップロードファイル情報
            {'name': ('filename', fileobj)}
        Retruns
        -------
        growi_res : json
            リクエストのレスポンス
        """
        url = self.base_url + '/{}'.format(verb)
        res = requests.post(url, data=payload, files=file, params=self.params)
        res.raise_for_status

        growi_res = res.json()
        # print(json.dumps(growi_res, indent=4))
        if 'errors' in growi_res:
            print(json.dumps(growi_res, indent=4))

        return growi_res

    def __get(self, verb, params=None):
        """
        GROWI サーバーに GET リクエストを行う

        Parameters
        ----------
        verb : str
            GROWI API
        params : dict
            GET のパラメタ
        Retruns
        -------
        growi_res : json
            リクエストのレスポンス
        """
        url = self.base_url + '/{}'.format(verb)
        req_params = self.params.copy()
        if params:
            req_params.update(params)
        res = requests.get(url, params=req_params)
        res.raise_for_status

        growi_res = res.json()
        # print(json.dumps(growi_res, indent=4))
        if 'errors' in growi_res:
            print(json.dumps(growi_res, indent=4))

        return growi_res

    def __to_path(self, title):
        """
        GROWI ページのバスを返す

        Parameters
        ----------
        title : str
            ページ・タイトル

        Retruns
        -------
        path : str
            GROWI のページのバス
        """
        path = '{}/'.format(self.base_path)
        if self.draft:
            path += 'draft/'
        path += title.replace('^', '＾') \
                     .replace('$', '＄') \
                     .replace('*', '＊') \
                     .replace('%', '％') \
                     .replace('?', '？') \
                     .replace('/', '／')
        return path


class GrowiPage:
    """
    GROWI ページを表す

    Attributes
    ----------
    id : str
        ページ ID
    path : str
        パス
    revision : str
        リビジョン
    title : str
        タイトル
    tags : array
        タグ
    content : str
        本文
    """
    def __init__(self, id, path, revision, title, tags, content):
        """
        Parameters
        ----------
        id : str
            ページ ID
        path : str
            パス
        revision : str
            リビジョン
        title : str
            タイトル
        tags : array
            タグ
        content : str
            本文
        """
        self.id = id
        self.path = path
        self.revision = revision
        self.title = title
        self.tags = tags
        self.content = content
        self.attachments = {}

    def replace_attachment(self, file_name, file_path_proxied):
        """
        本文の指定されたファイルの参照 (リンク) を指定された参照 (リンク) に置き換える

        Parameters
        ----------
        file_name : str
            置き換えるフアイル名
        file_path_proxied : str
            置き換える参照 (リンク)
        """
        self.content = re.sub(r'(!\[' + file_name + r'\])\(.+\)',
                              r'\1(' + file_path_proxied + r')',
                              self.content)

    def initialize_attachments_info(self, attachments_list_res):
        """
        GROWI ページの添付ファイル情報を設定する

        Parameters
        ----------
        attachments_list_res : json
            _api/v3/attachment/list の返却データ
        """
        for attachment in attachments_list_res['paginateResult']['docs']:
            self.attachments[attachment['id']] \
                        = GrowiAttachment(attachment['id'],
                                          attachment['originalName'],
                                          attachment['filePathProxied'])

    def add_attachment_info(self, attachment_id, original_name,
                            file_path_proxied):
        """
        添付ファイル情報を追加する
        Parameters
        ----------
        id : str
            添付ファイル ID
        original_name : str
            オリジナルのファイル名
        file_path_proxied : str
            添付ファイルの参照パス (リンク)
        """
        self.attachments[attachment_id] = GrowiAttachment(attachment_id,
                                                          original_name,
                                                          file_path_proxied)

    def get_attachment_info(self, file_name):
        """
        この GROWI ページが指定されたファイル名の添付ファイル情報を返す

        Parameters
        ----------
        file_name : str
            ファイル名
        Retruns
        -------
        attachment : GrowiAttachment
            添付ファイル情報
            添付ファイルが存在しない場合は None
        """
        attachment = [self.attachments[id] for id in self.attachments
                      if self.attachments[id].original_name == file_name]
        if attachment:
            return attachment[0]
        return None

    def remove_attachment_info(self, attachment_id):
        """
        この GROWI ページから指定された添付ファイル ID の添付ファイル情報を削除する

        Parameters
        ----------
        attachment_id : str
            添付ファイル ID
        """
        del self.attachments[attachment_id]


class GrowiAttachment:
    """
    GROWI 添付ファイルを表す

    Attributes
    ----------
    id : str
        添付ファイル ID
    original_name : str
        オリジナルのファイル名
    file_path_proxied : str
        添付ファイルの参照パス (リンク)
    """
    def __init__(self, id, original_name, file_path_proxied):
        """
        Parameters
        ----------
        id : str
            添付ファイル ID
        original_name : str
            オリジナルのファイル名
        file_path_proxied : str
            添付ファイルの参照パス (リンク)
        """
        self.id = id
        self.original_name = original_name
        self.file_path_proxied = file_path_proxied
