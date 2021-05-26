import sys
import webbrowser
import configparser

import tkinter as tk
import multiprocessing as mp

from pathlib import Path
from voila.app import Voila


def start_gui(title: str, notebook_url: str) -> None:
    tk_root = tk.Tk()
    tk_root.title(title)

    tk.Button(
        tk_root,
        text='Reopen',
        command=lambda: webbrowser.open(notebook_url),
        width=20
    ).grid(row=0, sticky=tk.W)
    tk.Button(
        tk_root,
        text='Terminate',
        command=tk_root.destroy,
        width=20
    ).grid(row=1, sticky=tk.W)

    tk_root.protocol('WM_DELETE_WINDOW', tk_root.destroy)
    tk_root.mainloop()


def start_server() -> None:
    data_path = Path(__file__).parent.absolute()
    config = configparser.ConfigParser()
    config.read(data_path / 'config.txt')
    config = config['default']

    if 'add_path' in config:
        for i, p in enumerate(config['add_path'].split(':')):
            sys.path.insert(i, p)

    if config['backend'] == 'voila':
        voila = Voila()

        mp.set_start_method('spawn')
        gui_p = mp.Process(target=start_gui, args=(config['name'], voila.display_url))
        gui_p.start()

        voila_args = [str(data_path / config['notebook_path'])] + ([config['backend_args']] or [])
        voila_p = mp.Process(target=voila.launch_instance, args=(voila_args,))
        voila_p.start()

        gui_p.join()
        voila_p.terminate()
        voila_p.join()


if __name__ == '__main__':
    start_server()
