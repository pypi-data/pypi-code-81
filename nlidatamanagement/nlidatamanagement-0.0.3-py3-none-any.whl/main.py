import tkinter as tk

from nlidatamanagement.utils.girder_connector import GirderConnector
from nlidatamanagement.utils.zotero_connector import ZoteroConnector
from nlidatamanagement.views.girder.girder_main import GirderUploader
from nlidatamanagement.views.girder.girder_setting import GirderSetting
from nlidatamanagement.views.zotero.zotero_main import ZoteroUploader
from nlidatamanagement.views.zotero.zotero_setting import ZoteroSetting


def generate_girder_win(root, girder_connector):
    # girder_win = tk.Toplevel(root)
    # GirderUploader(girder_win, girder_connector)
    GirderSetting(
            parent_win=root,
            girder_connector=girder_connector,
            on_connect=on_girder_connect
            )


def on_girder_connect(parent_win, girder_connector):
    # girder_win = tk.Toplevel(parent_win)
    GirderUploader(parent_win, girder_connector)


def on_zotero_connect(parent_win, girder_connector, zotero_connector):
    ZoteroUploader(parent_win, girder_connector, zotero_connector)


def generate_zotero_win(root, girder_connector, zotero_connector):
    # zotero_win = tk.Toplevel(root)
    # ZoteroUploader(zotero_win, girder_client)
    ZoteroSetting(
            parent_win=root,
            girder_connector=girder_connector,
            zotero_connector=zotero_connector,
            on_connect=on_zotero_connect
            )


def main():
    root = tk.Tk()
    root.title('Data Management Sys')
    # with open('./config.json', 'r') as f:
    #     config = json.load(f)

    # url = config['GirderServerURL']
    # api_path = config['GirderAPIPath']
    # girder_connector = GirderConnector(url=url, api_path=api_path)
    # girder_connector = GirderConnector()

    girder_btn = tk.Button(
            root,
            height=10,
            width=40,
            padx=10,
            pady=10,
            text='Upload to Girder',
            command=lambda: generate_girder_win(root, GirderConnector())
            )
    girder_btn.pack()

    zotero_btn = tk.Button(
            root,
            height=10,
            width=40,
            padx=10,
            pady=10,
            text='Upload to Zotero',
            command=lambda: generate_zotero_win(root, GirderConnector(), ZoteroConnector())
            )
    zotero_btn.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
