import math
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
import const

# General

APP_NAME = "MirPredict"

# File Paths
p_LOGO_IMG = "logo.png"
p_OPEN_BTN_IMG = 'open_res_btn.png'
p_COPY_BTN_IMG = 'copy_btn.png'
p_SEARCH_ENTRY = "TextBox_Bg.png"
p_BACK_BTN = "picture6.png"
p_FILTER_BTN = "picture7.png"
#
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
x_STATS = (w_WIDTH/2) - 100
x_FILTER = x_STATS+50
x_SECOND_REC = (w_WIDTH)*0.69
#
# Fonts
f_STATS_NUM = ("Arial-BoldMT", 13)
f_STATS_TITLE = ("Arial-BoldMT", 15, 'bold')
f_RESULTS_TITLE = ("Arial-BoldMT", 15)
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
t_MSG_WRONG_MIR = 'This is not a valid miR sequence.'
t_MSG_MIR_LENGTH = 'Micro RNA string should be at ' \
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
t_MIR_LABLE = "miR sequence: "
t_WELCOME_TXT = "Welcome to "
t_INFO_TXT = "targets prediction and\n" \
                "functional annotations of micro RNA\n" \
                "by comparing results of two databases:\n" \
                "- 'Diana' Databasse\n" \
                "- 'MirDB' Database\n\n" \
                "The search uses two robust algorithms\n" \
                "and will take about 2 minutes to run.\n" \
                "At that time the program is not responsive.\n" \
# Locations
y_HEAD = 60
y_KNOW_MORE = 450
y_SEARCH_BTN = 340
y_BACK_BTN = 420
y_MIR_ENTRY_IMG = 280
y_MIR_ENTRY = y_MIR_ENTRY_IMG - 5
y_MIR_ENTRY_TXT = y_MIR_ENTRY_IMG - 16

ASSETS_PATH = Path(__file__).resolve().parent / "assets"

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1, x1+radius, y1,   x2-radius, y1,  x2-radius,
              y1,x2, y1, x2, y1+radius,   x2, y1+radius,   x2, y2-radius,
              x2, y2-radius,   x2, y2, x2-radius, y2,  x2-radius, y2,
              x1+radius, y2,   x1+radius, y2,  x1, y2, x1, y2-radius,x1,
              y2-radius, x1, y1+radius,x1, y1+radius,x1, y1]
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
        msg_type = msg_type[0] if len(msg_type) == 1 else msg_type
        if msg_type == const.QUIT:
            res = tk.messagebox.askquestion(title='Save search',
                                            message=t_MSG_QUIT)
            return res == 'yes'
        elif msg_type == const.MIRDB_OVERLOAD_ERROR:
            tk.messagebox.showinfo(title='MirDB over load',
                                   message=t_MSG_DB_OVERLOAD)
        elif msg_type == const.LENGTH_ERROR:
            tk.messagebox.showinfo(title='Mir Length Error',
                                   message=t_MSG_MIR_LENGTH)
        elif msg_type == const.WRONG_MIR_ERROR:
            tk.messagebox.showinfo(title='Wrong miR Error',
                                   message=t_MSG_WRONG_MIR)
        else:
            tk.messagebox.showerror(title='Unknown Error', message=msg_type)

class SearchWindow:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(
            master, bg=bgc_PRIMARY, height=w_HEIGHT, width=w_WIDTH,
            bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(431, 0, 431 + 431, 0 + w_HEIGHT, fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill=bgc_SECONDARY, outline="")

        img = Image.open(ASSETS_PATH / p_LOGO_IMG)
        self.logo_img = img.resize((280, 230), Image.ANTIALIAS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img, master=self.canvas)
        self.canvas.create_image(500, 0, image=self.logo_img, anchor=tk.NW)

        title = tk.Label(
            text=t_WELCOME_TXT + APP_NAME, bg=bgc_PRIMARY,
            fg=c_TEXT_OVER_MAIN, font=f_SEARCH_TITLE)
        title.place(x=27.0, y=120.0)

        info_text = tk.Label(
            text=APP_NAME +" " + t_INFO_TXT,
            bg=bgc_PRIMARY, fg=c_TEXT_OVER_MAIN, justify="left",
            font=f_INFO_TEXT)

        info_text.place(x=27.0, y=200.0)

        self.know_more = tk.Label(
            text="Click here for more information",
            bg=bgc_PRIMARY, fg=c_TEXT_OVER_MAIN, cursor="hand2")
        self.know_more.place(x=27, y=y_KNOW_MORE)
        self.draw_entry()
        self.draw_button()

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

    def draw_button(self):
        self.search_img = tk.PhotoImage(file=ASSETS_PATH / "search.png")
        self.search_btn = tk.Button(self.canvas,
                                    image=self.search_img, borderwidth=0, highlightthickness=0,
                                    relief="flat")
        self.search_btn.place(x=557, y=y_SEARCH_BTN, width=180, height=55)

    def click_search(self):
        return self.mir_entry.get()

class ResultWindow:
    def __init__(self, master, results_data):
        self.results_data = results_data
        self.canvas = tk.Canvas(
            master, bg=bgc_PRIMARY, height=w_HEIGHT, width=w_WIDTH,
            bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0, y_HEAD, x_SECOND_REC, 0 + w_HEIGHT,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(30, y_HEAD-10, 30 + 60, y_HEAD-10 + 5,
                                     fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill=bgc_SECONDARY, outline="")
        self.canvas.create_rectangle(0, 450, w_WIDTH, w_HEIGHT, fill=bgc_SECONDARY,
                                     outline="")
        mir = self.results_data["mir"]
        mir_text = mir if len(mir) < 20 else '...'+mir[-20:]
        self.canvas.create_text(
            30, 30, text=t_RESULTS_TITLE + f' "{mir_text}"',
            fill=c_TEXT_OVER_MAIN,
            font=f_RESULTS_TITLE, anchor="w")
        self.draw_btns()
        self.draw_stats()
        self.grade_filter = self.draw_entry(x_FILTER, 75,
                                            t_GRADE_FILTER_LABLE)
        self.avg_grade_filter = self.draw_entry(x_FILTER, 170,
                                                t_AVE_FILTER_LABLE)
        self.draw_genes()

    def draw_entry(self, x, y, text):
        round_rectangle(self.canvas, x-20, y, x+150,
                        y+60, fill=bgc_TEXT_BOX, radius=35)
        entry = tk.Entry(bd=0, bg=bgc_TEXT_BOX, highlightthickness=0,
                         font=f_ENTRY)
        entry.place(x=x, y=y+25, width=60,
                             height=35)
        entry.focus()
        self.canvas.create_text(x_FILTER, y+15, text=text,
                                fill=c_ENTRY_LABLE,
                                font=f_ENTRY_lABLE,
                                anchor="w")
        return entry

    def draw_btns(self):
        self.back_btn_img = tk.PhotoImage(file=ASSETS_PATH / p_BACK_BTN)
        self.back_btn = tk.Button(self.canvas,
                                  image=self.back_btn_img, borderwidth=0, highlightthickness=0,
                                  relief="flat")
        self.back_btn.place(x=95, y=y_BACK_BTN, width=180, height=55)
        # Filter Btn
        img = Image.open(ASSETS_PATH / p_FILTER_BTN)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.filter_btn_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.filter_btn = tk.Button(self.canvas,
                                  image=self.filter_btn_img, borderwidth=0, highlightthickness=0,
                                  relief="flat")
        self.filter_btn.place(x=x_FILTER, y=250, width=s_SMALL_BTN_W,
                              height=s_SMALL_BTN_H)
         # COPY BUTTON
        img = Image.open(ASSETS_PATH / p_COPY_BTN_IMG)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.copy_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.copy_btn = tk.Button(self.canvas,
                                    image=self.copy_img, borderwidth=0, highlightthickness=0,
                                    relief="flat")
        self.copy_btn.place(x=w_WIDTH-262, y=460, width=s_SMALL_BTN_W,
                              height=s_SMALL_BTN_H)
        # open full analysis
        self.canvas.create_rectangle(0, 450, w_WIDTH, w_HEIGHT, fill=bgc_SECONDARY,
                                     outline="")
        img = Image.open(ASSETS_PATH / p_OPEN_BTN_IMG)
        img = img.resize((s_SMALL_BTN_W, s_SMALL_BTN_H), Image.ANTIALIAS)
        self.open_btn_img = ImageTk.PhotoImage(img, master=self.canvas)
        # self.filter_btn_img = tk.PhotoImage(file=ASSETS_PATH / "picture7.png")
        self.open_btn = tk.Button(self.canvas,
                                  image=self.open_btn_img, borderwidth=0, highlightthickness=0,
                                  relief="flat")
        self.open_btn.place(x=w_WIDTH - 180 + 50, y=460, width=s_SMALL_BTN_W,
                            height=s_SMALL_BTN_H)

    def draw_genes(self):
        f = tk.Frame(self.canvas)
        f.place(x=(w_WIDTH)*0.69+40, y=20)
        scrollbar = tk.Scrollbar(f)
        t = tk.Text(f, height=25, width=24,
                    yscrollcommand=scrollbar.set)
        t.insert(tk.END, t_SCROLBAR_TITLE)
        for i, gene in enumerate(self.results_data['genes']):
            space_add = math.floor(math.log10(len(self.results_data[
                                                      'genes']))) - math.floor(
                math.log10(i+1))
            ord = str(i+1)+' '*space_add
            t.insert(tk.END,f"{ord}| {gene[0]} | {gene[1]}\n")
        scrollbar.config(command='')
        t['state'] = "disabled"
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        t.pack(side="left")

    def draw_stats(self):
        round_rectangle(self.canvas, 25, 75, x_STATS, y_BACK_BTN-170,
                        fill=bgc_TEXT_BOX, radius=BOX_RADUIS)
        round_rectangle(self.canvas,25, y_BACK_BTN-145, x_STATS,
                        y_BACK_BTN-60,
                        fill=bgc_TEXT_BOX, radius=BOX_RADUIS)
        # results_data = [('Diana', 242),('mirDB', 3808),('Both',200)]
        for i, vals in enumerate(self.results_data['stats']):
            y_extra = 15 if i == 2 else 0
            y_value = (i+1)*90
            self.canvas.create_text(
                x_STATS/2-20, y_value+15+y_extra, text=vals[
                    0], fill=c_ENTRY_LABLE,
                font=f_STATS_TITLE, anchor="w")
            self.canvas.create_text(
                x_STATS/2-10, y_value+30+15+y_extra,
                text=str(vals[1]),
                fill=c_ENTRY_LABLE,font=f_STATS_NUM, anchor="w")

    def click_filter(self):
        min_avg = float(self.avg_grade_filter.get()) if \
            self.avg_grade_filter.get().isnumeric() else 0
        min_grade = float(self.grade_filter.get()) if \
            self.grade_filter.get().isnumeric() else 0
        return min_avg,min_grade

if __name__ == '__main__':
  pass