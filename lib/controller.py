from lib.gui import GUI
from lib.modules import get_results_data, fetch_data, open_results, \
    open_search_folder, open_readme
import lib.const as const
import os
import pyperclip
import shutil
import logging

# TK events
e_BUTTON_CLICK = '<Button-1>'
e_BUTTON_PRESS = '<ButtonPress-1>'
ESCAPE = '<Escape>'
ENTER = '<Return>'

class Controller:
    def __init__(self, debug='False'):
        os.environ['DEBUG'] = debug
        logging.basicConfig(format='%(asctime)s: %(message)s',
                            level=logging.INFO)
        self.is_novel = None
        self._gui = GUI()
        self._search()
        # self._auto_search('GGUAUG_512121')

    def _search(self):
        def main_menu():
            menu = self._gui.main_canvas.search_menu
            menu.add_command(label="Open Search Folder", command=open_search_folder)
            menu.add_separator()
            menu.add_command(label="Exit", command=lambda: quit())
            menu = self._gui.main_canvas.help_menu
            menu.add_command(label="About...", command=open_readme)

        self._gui.route_search()
        self._gui.main_canvas.search_btn.bind(e_BUTTON_PRESS, lambda e:
        self._click_search())
        main_menu()
        # self._gui.main_canvas.about.bind(e_BUTTON_CLICK, lambda e:
        # open_readme())
        self._gui.main_canvas.click_about = lambda a: print('help')
        self._gui.main_canvas.open_search_folder.bind(e_BUTTON_PRESS,
                                                      lambda
                                                          e: open_search_folder())
        self._gui.root.bind(ESCAPE, lambda e: quit())
        self._gui.root.bind(ENTER, lambda e: self._click_search())

    def _results(self, results_data):
        self._gui.route_result(results_data)
        self._gui.main_canvas.back_btn.bind(e_BUTTON_PRESS, lambda e:
        self._click_back())
        self._gui.main_canvas.copy_btn.bind(e_BUTTON_PRESS, lambda e:
        self._click_copy())
        self._gui.main_canvas.open_btn.bind(e_BUTTON_PRESS, lambda e:
        self._click_open())
        self._gui.main_canvas.filter_btn.bind(e_BUTTON_PRESS, lambda e:
        self._click_filter())
        self._gui.root.bind(ENTER, lambda e: None)
        self._gui.root.bind(ESCAPE, lambda e: self._click_back())

    def run(self):
        self._gui.run()

    def _click_search(self):
        mir = self._gui.main_canvas.click_search()
        if mir != '':
            try:
                data = fetch_data(mir)
                self.search_path, self.is_novel = data[const.s_SEARCH_PATH], \
                                                  data[const.s_SEARCH_NOVEL]
            except Exception as e:
                self._gui.show_msg(e)
            else:
                self.results_data = get_results_data(self.search_path)
                self._routing('results')

    def _auto_search(self, sid):
        self.search_path = fetch_data(sid)[const.s_SEARCH_PATH]
        self.results_data = get_results_data(self.search_path)
        self._routing('results')

    def _click_copy(self):
        genes = [gene[0] for gene in self.results_data['genes']]
        genes_text = ','.join(genes)
        pyperclip.copy(genes_text)

    def _click_filter(self):
        filter_params = self._gui.main_canvas.click_filter()
        self.results_data = get_results_data(self.search_path,
                                             *filter_params)
        self._routing('results')

    def _click_back(self):
        if self.is_novel:
            res = self._gui.show_msg(const.QUIT)
            if not res:
                try:
                    print(self.search_path)
                    shutil.rmtree(self.search_path)
                except OSError as e:
                    self._gui.show_msg(list(e.args))
        self._reset_search()
        self._routing('search')

    def _reset_search(self):
        self.is_novel = None
        self.search_path = None
        self.results_data = None

    def _click_open(self):
        try:
            data = self.results_data['data'].drop_duplicates()
            open_results(data, self.search_path)
        except PermissionError:
            self._gui.show_msg(const.ALREADY_OPEN_ERROR)

    def _routing(self, target):
        """this function governs all the routing"""
        self._gui.root.unbind('<Enter>')
        self._gui.root.unbind(ESCAPE)
        if target == 'search':
            self._gui.remove()
            self._search()
        if target == 'results':
            self._gui.remove()
            self._results(self.results_data)
