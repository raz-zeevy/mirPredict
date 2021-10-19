import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
import lib.const as const

# General
APP_NAME = "MirPredict"

# File Paths
p_LOGO_IMG = "logo.png"
p_OPEN_BTN_IMG = 'open_res_btn.png'
p_COPY_BTN_IMG = 'copy_btn.png'
p_SEARCH_ENTRY = "TextBox_Bg.png"
p_BACK_BTN = "picture6.png"
p_FILTER_BTN = "picture7.png"
p_CLEAR_BTN = "clear_btn.png"

# General Sizes
BOX_RADUIS = 35
s_SMALL_BTN_H = 40
s_SMALL_BTN_W = 120
#
# Window Sizes
w_WIDTH = 862
w_HEIGHT = 519
#
# Coordinates
x_STATS = (w_WIDTH / 2) - 175
x_FILTER = x_STATS + 50
x_SECOND_REC = (w_WIDTH) * 0.69
#
# Fonts
f_STATS_NUM = ("Arial-BoldMT", 13)
f_STATS_TITLE = ("Arial-BoldMT", 15, 'bold')
f_RESULTS_TITLE = ("Arial-BoldMT", 15)
f_RESULTS_SUB_TITLE = ("Arial-BoldMT", 12)
f_RESULTS_MIR_NAME = ("Arial-BoldMT", 12, 'bold')
f_INFO_TEXT = ("Georgia", int(16.0))
f_ENTRY = ("Calibri 16")
f_ENTRY_lABLE = ("Arial-BoldMT", int(13.0))
f_SEARCH_TITLE = ("Arial-BoldMT", int(20.0))
#
# Colors
c_TEXT_OVER_MAIN = "white"
c_ENTRY_LABLE = "#515486"
bgc_TEXT_BOX = "#F6F7F9"
bgc_OLD_BACKGROUND = "#3A7FF6"
bgc_PRIMARY = "#9797EC"
bgc_SECONDARY = "#FCFCFC"
bgc_BTN_COLOR = '#3a7ff6'
# Text
TITLE_MIR_LENGTH = 30
t_MSG_MIR_NOT_FOUND_ERROR = 'It seems that no miR was found ' \
                            'with this name.'
t_MSG_WRONG_MIR = 'This is not a valid miR sequence.'
t_MSG_MIR_LENGTH = 'Micro RNA sequence should be at ' \
                   'least 17 ' \
                   'characters long, and no longer ' \
                   'than 30.'
t_MSG_DB_OVERLOAD = 'mirDb is overloading. ' \
                    'please wait 2 minutes ' \
                    'before running a new search'
t_MSG_QUIT = 'Would you like to keep ' \
             'the files from the current ' \
             'search?'
t_RESULTS_TITLE = 'Search Results for'
t_SCROLBAR_TITLE = '#|Gene|Avg. Grade\n'
t_AVE_FILTER_LABLE = 'Min. avg grade'
t_GRADE_FILTER_LABLE = 'Min. grade'
t_MIR_LABLE = "miR sequence / miR name / search ID: "
t_WELCOME_TXT = "Welcome to "
t_INFO_TXT = "targets prediction and\n" \
             "functional annotations of micro RNA\n" \
             "by comparing results of two databases:\n" \
             "- 'Diana' Databasse\n" \
             "- 'MirDB' Database\n\n" \
             "The search uses two robust algorithms\n" \
             "and will take about 2 minutes to run.\n" \
             "At that time the program is not responsive.\n"
t_MSG_TEMP_UNK_ERROR = 'Temporary unknown error has occurred, please try ' \
                       'again. This might have happend due to poor internet ' \
                       'connection.'
# Locations
#     Search
y_MIR_ENTRY_IMG = 280
y_MIR_ENTRY = y_MIR_ENTRY_IMG - 5
y_MIR_ENTRY_TXT = y_MIR_ENTRY_IMG - 16
y_OPEN_HISTORY_BTN = 30
x_HISTORY_FOLDER = w_WIDTH - 60
y_INFO_TEXT = 180.0
y_MAIN_TITLE = 100.0
y_KNOW_MORE = 450
y_SEARCH_BTN = 340
#     Results
y_HEAD_DIV = 100
y_BACK_BTN = 420

ASSETS_PATH = Path(__file__).resolve().parent / "assets"


def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius,
              y1, x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius,
              x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2,
              x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1,
              y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)


class GUI:
    """this class is the at the highest level and it is in charge of all
    the UI components"""

    def __init__(self):
        self.root = tk.Tk()
        # w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        # self._width = int(w / 1.5)
        # self._height = int(h / 1.2)
        # self.root.geometry(
        #     f"{self._width}x{self._height}+{int(w / 7)}+{int(h / 12)}")
        self.main_canvas = None
        # self.pop = PopUp(self.root)
        # self.change_tune = True
        logo = tk.PhotoImage(file=ASSETS_PATH / "icon.gif")
        self.root.call('wm', 'iconphoto', self.root._w, logo)
        self.root.title(APP_NAME)
        self.root.geometry(f"{w_WIDTH}x{w_HEIGHT}")
        self.root.configure(bg=bgc_PRIMARY)

    def route_search(self):
        self.main_canvas = SearchWindow(self.root)

    def route_result(self, results_data):
        self.main_canvas = ResultWindow(self.root, results_data)

    def run(self):
        """this function is called to run the program"""
        self.root.resizable(False, False)
        self.root.mainloop()

    def remove(self):
        """this function destroys the classes canvas"""
        self.main_canvas.canvas.destroy()
        self.main_canvas = None

    @staticmethod
    def show_msg(msg_type):
        if isinstance(msg_type, Exception):
            msg = msg_type.args[0] if len(
                list(msg_type.args)) == 1 else msg_type
        else:
            msg = msg_type
        if msg == const.QUIT:
            res = tk.messagebox.askquestion(title='Save search',
                                            message=t_MSG_QUIT)
            return res == 'yes'
        elif msg == const.ALREADY_OPEN_ERROR:
            tk.messagebox.showinfo(title='Results already open',
                                   message='Please close the previous '
                                           'results .Csv file in order to '
                                           'open '
                                           'a new one. The previous file can '
                                           'be saved as a new file in a '
                                           'different location.')
        elif msg == const.MIRDB_OVERLOAD_ERROR:
            tk.messagebox.showinfo(title='MirDB over load',
                                   message=t_MSG_DB_OVERLOAD)
        elif msg == const.LENGTH_ERROR:
            tk.messagebox.showinfo(title='Mir Length Error',
                                   message=t_MSG_MIR_LENGTH)
        elif msg == const.WRONG_MIR_ERROR:
            tk.messagebox.showinfo(title='Wrong miR Error',
                                   message=t_MSG_WRONG_MIR)
        elif msg == const.SEARCH_ID_NOT_FOUND_ERROR:
            tk.messagebox.showinfo(title='Search ID not found',
                                   message='There is no such search ID in '
                                           'the search history')
        elif msg == const.TEMP_UNKNOWN_ERROR:
            tk.messagebox.showinfo(title='Temporary Unknown Error',
                                   message=t_MSG_TEMP_UNK_ERROR)
        elif msg == const.MIR_NAME_NOT_FOUND_ERROR:
            tk.messagebox.showinfo(title='MiR Not Found Error',
                                   message=t_MSG_MIR_NOT_FOUND_ERROR)
        elif msg == const.CONNECTION_ERROR:
            tk.messagebox.showinfo(title='Connection Error',
                                   message='The program couldn\'t reach the '
                                           'Internet. Please check the '
                                           'Internet connection.')
        else:
            if isinstance(msg_type, Exception):
                tk.messagebox.showerror(title='Unknown Error', message=msg)
                raise msg_type
            # TODO: Remove the raise Excpetion and keep the handle the error
            else:
                tk.messagebox.showerror(title='Unknown Error', message=msg)


class SearchWindow:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(
            master, bg=bgc_PRIMARY, height=w_HEIGHT, width=w_WIDTH,
            bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(431, 0, 431 + 431, 0 + w_HEIGHT,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(40, 160, 40 + 60, 160 + 5,
                                     fill=bgc_SECONDARY, outline="")

        img = Image.open(ASSETS_PATH / p_LOGO_IMG)
        self.logo_img = img.resize((280, 230), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img, master=self.canvas)
        self.canvas.create_image(500, 0, image=self.logo_img, anchor=tk.NW)

        title = tk.Label(
            text=t_WELCOME_TXT + APP_NAME, bg=bgc_PRIMARY,
            fg=c_TEXT_OVER_MAIN, font=f_SEARCH_TITLE)
        title.place(x=27.0, y=y_MAIN_TITLE)

        info_text = tk.Label(
            text=APP_NAME + " " + t_INFO_TXT,
            bg=bgc_PRIMARY, fg=c_TEXT_OVER_MAIN, justify="left",
            font=f_INFO_TEXT)

        info_text.place(x=27.0, y=y_INFO_TEXT)

        self.know_more = tk.Label(
            text="Click here for more information",
            bg=bgc_PRIMARY, fg=c_TEXT_OVER_MAIN, cursor="hand2")
        self.know_more.place(x=27, y=y_KNOW_MORE)
        self.draw_entry()
        self.draw_buttons()
        self.top_menu()

    def draw_entry(self):
        self.text_box_bg = tk.PhotoImage(file=ASSETS_PATH / p_SEARCH_ENTRY)
        token_entry_img = self.canvas.create_image(650.5, y_MIR_ENTRY_IMG,
                                                   image=self.text_box_bg)
        self.mir_entry = tk.Entry(bd=0, bg=bgc_TEXT_BOX, highlightthickness=0,
                                  font=f_ENTRY)
        self.mir_entry.place(x=490.0, y=y_MIR_ENTRY, width=321.0, height=35)
        self.mir_entry.focus()
        self.canvas.create_text(
            490.0, y_MIR_ENTRY_TXT, text=t_MIR_LABLE, fill=c_ENTRY_LABLE,
            font=f_ENTRY_lABLE, anchor="w")

    def draw_buttons(self):
        self.search_img = tk.PhotoImage(file=ASSETS_PATH / "search.png")
        self.search_btn = tk.Button(self.canvas,
                                    image=self.search_img, borderwidth=0,
                                    highlightthickness=0,
                                    relief="flat")
        self.search_btn.place(x=557, y=y_SEARCH_BTN, width=180, height=55)
        self.open_search_folder_img = tk.PhotoImage(file=ASSETS_PATH /
                                                         "path_picker.png")
        self.open_search_folder = tk.Button(
            image=self.open_search_folder_img,
            text='',
            compound='center',
            fg='white',
            borderwidth=0,
            highlightthickness=0,
            relief='flat')

        self.open_search_folder.place(
            x=x_HISTORY_FOLDER, y=y_OPEN_HISTORY_BTN,
            width=24,
            height=22)

    def top_menu(self):
        main_menu = tk.Menu(self.master)
        self.search_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Search", menu=self.search_menu)
        self.help_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=main_menu)

    def click_search(self):
        return self.mir_entry.get()


class ResultWindow:
    def __init__(self, master, results_data):
        self.master = master
        self.results_data = results_data
        self.canvas = tk.Canvas(
            master, bg=bgc_PRIMARY, height=w_HEIGHT, width=w_WIDTH,
            bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, y_HEAD_DIV, x_SECOND_REC, 0 + w_HEIGHT,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(30, y_HEAD_DIV - 10, 30 + 60,
                                     y_HEAD_DIV - 10 + 5,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(40, 160, 40 + 60, 160 + 5,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(0, 450, w_WIDTH, w_HEIGHT,
                                     fill=bgc_SECONDARY,
                                     outline="")
        self.draw_title()
        self.draw_btns()
        self.draw_stats()
        self.grade_filter = self.draw_entry(x_FILTER, y_HEAD_DIV + 15,
                                            t_GRADE_FILTER_LABLE, value=self.results_data[
                const.r_FILTER][
                const.r_MIN_GRADE])
        self.avg_grade_filter = self.draw_entry(x_FILTER+150, y_HEAD_DIV + 15,
                                                t_AVE_FILTER_LABLE,
                    value=self.results_data[const.r_FILTER][const.r_MIN_AVG])
        self.tissue_select = self.draw_choice(x=x_FILTER, y=y_HEAD_DIV + 100,
                                              width=120, height=60,
                                              label_text='Tissue:',
                                              values=self.results_data[const.r_SELECTIONS][
                                                  const.r_TISSUE],
                                              value=self.results_data[
                                                  const.r_FILTER][
                                                  const.r_TISSUE])
        self.level_tissue_select = self.draw_choice(x=x_FILTER + 150,
                                                    y=y_HEAD_DIV + 100,
                                                    width=120, height=60,
                                                    label_text='Minimum '
                                                               'Level:',
                                                    values=self.results_data[const.r_SELECTIONS][const.r_LEVEL],
                                                    value=self.results_data[
                                                        const.r_FILTER][
                                                        const.r_TISSUE_LEVEL])
        self.cell_type = self.draw_choice(x=x_FILTER, y=y_HEAD_DIV + 185,
                                          width=120, height=60,
                                          label_text='Cell Type:',
                                          values=self.results_data[const.r_SELECTIONS][
                  const.r_CELL_TYPE],
                                          value=self.results_data[
                                              const.r_FILTER][
                                              const.r_CELL_TYPE])
        self.level_cell_type = self.draw_choice(x=x_FILTER + 150,
                                                y=y_HEAD_DIV + 185,
                                                width=120, height=60,
                                                label_text='Minimum '
                                                               'Level:',
                                                values=self.results_data[const.r_SELECTIONS][const.r_LEVEL],
                                                value=self.results_data[
                                                    const.r_FILTER][
                                                    const.r_CELL_TYPE_LEVEL])
        self.draw_genes()
        self.top_menu()

    def draw_title(self):
        mir = self.results_data[const.r_MIR_SEQ]
        mir_text = mir if len(mir) < TITLE_MIR_LENGTH else '...' + mir[
                                                                   -TITLE_MIR_LENGTH:]
        self.canvas.create_text(
            30, 30, text=t_RESULTS_TITLE + f' "{mir_text}"',
            fill=c_TEXT_OVER_MAIN,
            font=f_RESULTS_TITLE, anchor="w")
        self.canvas.create_text(
            30, 65, text='Mir Name: ',
            fill=c_TEXT_OVER_MAIN,
            font=f_RESULTS_SUB_TITLE, anchor="w")
        self.canvas.create_text(
            105, 65, text=self.results_data[const.r_MIR_NAME],
            fill=c_TEXT_OVER_MAIN,
            font=f_RESULTS_MIR_NAME, anchor="w")

    def draw_entry(self, x, y, text, value=None, width=120, height=60,\
                                                                 y_offset=25,
                   x_offset=15):
        round_rectangle(self.canvas, x-20, y, x + width,
                        y + height, fill=bgc_TEXT_BOX, radius=35)
        entry = tk.Entry(bd=0, bg=bgc_TEXT_BOX, highlightthickness=0,
                         font=f_ENTRY)
        entry.place(x=x, y=y + y_offset, width=width-x_offset,
                    height=height-y_offset)
        entry.focus()
        self.canvas.create_text(x, y + 15, text=text,
                                fill=c_ENTRY_LABLE,
                                font=f_ENTRY_lABLE,
                                anchor="w")
        if value: entry.insert(0,str(value))
        return entry

    def draw_btns(self):
        # Back Btn
        self.back_btn_img = tk.PhotoImage(file=ASSETS_PATH / p_BACK_BTN)
        self.back_btn = tk.Button(self.canvas,
                                  image=self.back_btn_img, borderwidth=0,
                                  highlightthickness=0,
                                  relief="flat")
        self.back_btn.place(x=50, y=y_BACK_BTN, width=180,
                            height=55)
        # Filter Btn
        img = Image.open(ASSETS_PATH / p_FILTER_BTN)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.filter_btn_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.filter_btn = tk.Button(self.canvas,
                                    image=self.filter_btn_img, borderwidth=0,
                                    highlightthickness=0,
                                    relief="flat")
        self.filter_btn.place(x=x_FILTER, y=375, width=s_SMALL_BTN_W,
                              height=s_SMALL_BTN_H)
        # COPY BUTTON
        img = Image.open(ASSETS_PATH / p_COPY_BTN_IMG)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.copy_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.copy_btn = tk.Button(self.canvas,
                                  image=self.copy_img, borderwidth=0,
                                  highlightthickness=0,
                                  relief="flat")
        self.copy_btn.place(x=w_WIDTH - 262, y=460, width=s_SMALL_BTN_W,
                            height=s_SMALL_BTN_H)
        # open full analysis
        self.canvas.create_rectangle(0, 450, w_WIDTH, w_HEIGHT,
                                     fill=bgc_SECONDARY,
                                     outline="")
        img = Image.open(ASSETS_PATH / p_OPEN_BTN_IMG)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.open_btn_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.open_btn = tk.Button(self.canvas,
                                  image=self.open_btn_img, borderwidth=0,
                                  highlightthickness=0,
                                  relief="flat")
        self.open_btn.place(x=w_WIDTH - 180 + 50, y=460, width=s_SMALL_BTN_W,
                            height=s_SMALL_BTN_H)
        # Clear Button
        img = Image.open(ASSETS_PATH / p_CLEAR_BTN)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.clear_btn_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.clear_btn = tk.Button(self.canvas,
                                    image=self.clear_btn_img, borderwidth=0,
                                    highlightthickness=0,
                                    relief="flat", command=self.click_clear_button)
        self.clear_btn.place(x=x_FILTER+142, y=375, width=s_SMALL_BTN_W,
                              height=s_SMALL_BTN_H)


    def draw_genes(self):
        f = tk.Frame(self.canvas)
        f.place(x=(w_WIDTH) * 0.69 + 40, y=20)
        scrollbar = tk.Scrollbar(f)
        t = tk.Text(f, height=25, width=24,
                    yscrollcommand=scrollbar.set)
        t.insert(tk.END, t_SCROLBAR_TITLE)
        for i, gene in enumerate(self.results_data[const.r_GENES]):
            space_add = math.floor(math.log10(len(self.results_data[
                                                      const.r_GENES]))) - math.floor(
                math.log10(i + 1))
            ord = str(i + 1) + ' ' * space_add
            t.insert(tk.END, f"{ord}| {gene[0]} | {gene[1]}\n")
        scrollbar.config(command='')
        t['state'] = "disabled"
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        t.pack(side="left")

    def draw_stats(self):
        round_rectangle(self.canvas, 25, y_HEAD_DIV + 15, x_STATS,
                        y_BACK_BTN - 150,
                        fill=bgc_TEXT_BOX, radius=BOX_RADUIS)
        round_rectangle(self.canvas, 25, y_BACK_BTN - 120, x_STATS,
                        y_BACK_BTN - 30,
                        fill=bgc_TEXT_BOX, radius=BOX_RADUIS)
        # results_data = [('Diana', 242),('mirDB', 3808),('Both',200)]
        for i, vals in enumerate(self.results_data[const.r_STATS]):
            y_extra = 20 if i == 2 else 0
            y_value = i * 90
            y_base = y_HEAD_DIV + 30
            self.canvas.create_text(
                x_STATS / 2 - 20, y_base + y_value + y_extra, text=vals[
                    0], fill=c_ENTRY_LABLE,
                font=f_STATS_TITLE, anchor="w")
            self.canvas.create_text(
                x_STATS / 2 - 10, y_base + y_value + 30 + y_extra,
                text=str(vals[1]),
                fill=c_ENTRY_LABLE, font=f_STATS_NUM, anchor="w")

    def top_menu(self):
        def donothing():
            filewin = tk.Toplevel(self.master)
            button = tk.Button(filewin, text="Do nothing button")
            button.pack()

        results_menu = tk.Menu(self.master)
        # filemenu = tk.Menu(results_menu, tearoff=0)
        # filemenu.add_command(label="New", command=donothing)
        # filemenu.add_command(label="Open", command=donothing)
        # filemenu.add_command(label="Save", command=donothing)
        # filemenu.add_command(label="Save as...", command=donothing)
        # # From some reason got clicked instantly
        # filemenu.add_command(label="Close", command=lambda x: print('quit'))
        #
        # filemenu.add_separator()
        #
        # # From some reason got clicked instantly
        # filemenu.add_command(label="Exit", command=lambda x: print('quit'))
        # results_menu.add_cascade(label="File", menu=filemenu)
        # editmenu = tk.Menu(results_menu, tearoff=0)
        # editmenu.add_command(label="Undo", command=donothing)
        #
        # editmenu.add_separator()
        #
        # editmenu.add_command(label="Cut", command=donothing)
        # editmenu.add_command(label="Copy", command=donothing)
        # editmenu.add_command(label="Paste", command=donothing)
        # editmenu.add_command(label="Delete", command=donothing)
        # editmenu.add_command(label="Select All", command=donothing)
        #
        # results_menu.add_cascade(label="Edit", menu=editmenu)
        # helpmenu = tk.Menu(results_menu, tearoff=0)
        # helpmenu.add_command(label="Help Index", command=donothing)
        # helpmenu.add_command(label="About...", command=donothing)
        # results_menu.add_cascade(label="Help", menu=helpmenu)
        self.master.config(menu=results_menu)

    def click_filter(self):
        min_avg = float(self.avg_grade_filter.get()) if \
            self.avg_grade_filter.get().isnumeric() else 0
        min_grade = float(self.grade_filter.get()) if \
            self.grade_filter.get().isnumeric() else 0
        tissue = self.tissue_select.get()
        tissue_level = self.level_tissue_select.get()
        cell_type = self.cell_type.get()
        cell_type_level = self.level_cell_type.get()
        return min_avg, min_grade, tissue, tissue_level, cell_type,\
               cell_type_level

    def click_clear_button(self):
        self.tissue_select.delete(0,tk.END)
        self.cell_type.delete(0,tk.END)
        self.level_tissue_select.delete(0,tk.END)
        self.level_cell_type.delete(0,tk.END)
        self.avg_grade_filter.delete(0,tk.END)
        self.grade_filter.delete(0,tk.END)

    def draw_choice(self, x, y, label_text, values, value=None, width=120, \
                                                                 height=60,
                    y_offset=30,
                    x_offset=15):
        def_value = (
            'January', 'February', 'March', 'April', 'May', 'June',
            'July',
            'August', 'September', 'October', 'November', 'December')
        values = def_value if not values else values
        # Define the style for combobox widget
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=bgc_TEXT_BOX,
                        background=bgc_TEXT_BOX, borderwidth=3,
                        highlightthickness=0,
                        bordercolor=bgc_TEXT_BOX, font=f_ENTRY_lABLE,
                        arrowsize=12)
        self.master.option_add("*TCombobox*Listbox*Font", f_ENTRY_lABLE)
        self.master.option_add("*TCombobox*Listbox*Width", width - x_offset)
        # Draw Rectangle
        round_rectangle(self.canvas, x - 20, y, x + width,
                        y + height, fill=bgc_TEXT_BOX, radius=35)
        combobox = ttk.Combobox(self.master, width=width, font=f_ENTRY_lABLE)
        combobox['values'] = values
        self.canvas.create_text(x, y + 15, text=label_text,
                                fill=c_ENTRY_LABLE,
                                font=f_ENTRY_lABLE,
                                anchor="w")
        combobox.place(x=x, y=y + y_offset, width=width - x_offset,
                       height=height - y_offset)
        if value:
            val_ind = values.index(value)
            combobox.current(val_ind)
        return combobox

    def draw_menu_options(self):
        x = x_FILTER
        y = y_HEAD_DIV + 250
        # Define the style for combobox widget
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=bgc_TEXT_BOX,
                        background="white", borderwidth=3,
                        highlightthickness=0,
                        bordercolor=bgc_TEXT_BOX)
        round_rectangle(self.canvas, x - 20, y, x + 150,
                        y + 60, fill=bgc_TEXT_BOX, radius=35)
        n = tk.StringVar()
        months = [' January',
                  ' February',
                  ' March',
                  ' April',
                  ' May',
                  ' June',
                  ' July',
                  ' August',
                  ' September',
                  ' October',
                  ' November',
                  ' December']
        value_inside = tk.StringVar(self.master)
        value_inside.set("Select an Option")
        monthchoosen = tk.OptionMenu(self.master, value_inside, *months)
        monthchoosen['borderwidth'] = 0
        monthchoosen['background'] = bgc_TEXT_BOX
        monthchoosen['highlightthickness'] = 0
        monthchoosen.place(x=x, y=y, width=60,
                           height=35)

if __name__ == '__main__':
    pass
