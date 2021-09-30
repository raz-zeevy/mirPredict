from gui import GUI
from modules import get_results_data, fetch_data, open_results
import os
import pyperclip
import const
import shutil

ESCAPE = '<Escape>'

class Controller:
    def __init__(self, debug='False'):
        os.environ['DEBUG'] = debug
        self._gui = GUI()
        self._search()

    def _search(self):
        self._gui.route_search()
        self._gui.main_canvas.search_btn.bind('<ButtonPress-1>', lambda e:
        self._click_search())
        self._gui.main_canvas.know_more.bind('<Button-1>', lambda e:
        self._know_more())
        self._gui.root.bind(ESCAPE, lambda e: quit())

    def _results(self, results_data):
        self._gui.route_result(results_data)
        self._gui.main_canvas.back_btn.bind('<ButtonPress-1>', lambda e:
        self._click_back())
        self._gui.main_canvas.copy_btn.bind('<ButtonPress-1>', lambda e:
        self._click_copy())
        self._gui.main_canvas.open_btn.bind('<ButtonPress-1>', lambda e:
        self._click_open())
        self._gui.main_canvas.filter_btn.bind('<ButtonPress-1>', lambda e:
        self._click_filter())
        self._gui.root.bind(ESCAPE, lambda e: self._click_back())

    def run(self):
        self._gui.run()

    def _click_search(self):
        mir = self._gui.main_canvas.click_search()
        self.searched_mir = mir
        try:
            self.search_data = fetch_data(mir)
        except Exception as e:
            self._gui.show_msg(list(e.args))
        else:
            self.temp_folder = list(self.search_data).pop(2)
            self.results_data = get_results_data(self.search_data)
            self._routing('results')

    def _click_copy(self):
        genes = [gene[0] for gene in self.results_data['genes']]
        genes_text = ','.join(genes)
        pyperclip.copy(genes_text)

    def _click_filter(self):
        min_avg, min_grade = self._gui.main_canvas.click_filter()
        self.results_data = get_results_data(self.search_data,
                                             min_avg, min_grade)
        self._routing('results')

    def _click_back(self):
        res = self._gui.show_msg(const.QUIT)
        if not res:
            try:
                print(self.temp_folder)
                shutil.rmtree(self.temp_folder)
            except OSError as e:
                self._gui.show_msg(list(e.args))
        self._reset_search()
        self._routing('search')

    def _reset_search(self):
        self.temp_folder = None
        self.search_data = None
        self.results_data = None

    def _click_open(self):
        file_path = open_results(self.results_data['data'], self.temp_folder)
        os.system(f"start EXCEL.EXE {file_path}")

    def _know_more(self):
        os.system(f"start README.txt")

    def _routing(self, target):
        """this function governs all the routing"""
        self._gui.root.unbind('<Enter>')
        self._gui.root.unbind(ESCAPE)
        if target == 'search':
            self._gui.remove()
            self._search()
        if target == 'results':
            self._gui.remove()
            self.results_data['mir'] = self.searched_mir
            self._results(self.results_data)
