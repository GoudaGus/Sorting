from tkinter import *
from tkinter import filedialog
from os import environ
from traceback import format_exc
from algorithims import *
from random import shuffle
from time import sleep
"""Sort numbers either using a pregenerated list or import your own."""

class Main_UI:
    def __init__(self):
        self.master = Tk()
        self.master.title("Sorting")
        self.master['bg'] = '#f2f2f2'
        # Init pane for window
        self.paned = PanedWindow(self.master, orient=VERTICAL, width=800, height=600)
        self.paned.grid(column=1,row=0)
        # Init window class for pane
        self.window = Window(self.master)
        self.paned.config(orient=VERTICAL, width=(self.window.bar_width * (self.window.bar_amt + .3)), height=(self.window.bar_amt * self.window.bar_len_mult + 30))
        self.window.refresh_list()
        self.paned.add(self.window)
        # Init search items
        self.entry_search = Entry(self.master)
        self.entry_search.grid(column=1, row=2, padx=775, sticky="w")
        self.label_search = Label(self.master, text="Search for number:")
        self.label_search.grid(column=1, row=1, padx=775, sticky="w")
        self.button_search = Button(self.master, text="Search", command=lambda: self.init_search())
        self.button_search.grid(column=1, row=2, padx=900, sticky="w")
        # Init files button
        self.files = FileIO(self.master)
        self.file_button = Button(self.master, text="Choose File...", command=lambda: self.start_file())
        self.file_button.grid(column=1, row=2, padx=655, sticky="w")
        # Init bar amt label
        self.label_bar_amt = Label(self.master, text="Number of bars:")
        self.label_bar_amt.grid(column=1, row=1, padx=29, sticky="w")
        # Init bar amt entry
        self.entry_bar_amt = Entry(self.master)
        self.entry_bar_amt.insert(END, f"{self.window.bar_amt}")
        self.entry_bar_amt.grid(column=1, row=2, padx=30, sticky="w")
        # Init reverse box and var 
        self.r = BooleanVar()
        self.reverse_check = Checkbutton(self.master, text="Reverse sort", variable=self.r, onvalue=True, offvalue=False)
        self.reverse_check.grid(column=1, row=2, padx=530, sticky="w")
        # Init ins sort button
        self.button_ins_sort = Button(self.master, text="Insertion Sort", command=lambda: self.begin_sort(type=0, r=self.r.get()))
        self.button_ins_sort.grid(column=1,row=2, padx=260, sticky="w")
        #Init sel sort button
        self.button_sel_sort = Button(self.master, text="Selection Sort", command=lambda: self.begin_sort(type=1, r=self.r.get()))
        self.button_sel_sort.grid(column=1,row=2, padx=350, sticky="w")
        #Init bog sort button
        self.button_bog_sort = Button(self.master, text="Bogo Sort", command=lambda: self.begin_sort(type=2, r=self.r.get()))
        self.button_bog_sort.grid(column=1,row=2, padx=440, sticky="w")
        # Init reset button
        self.reset_button = Button(self.master, text="Reset/Shuffle", command=lambda: self.change_amt_update())
        self.reset_button.grid(column=1, row=2, padx=175, sticky="w")
        # Init status label
        self.label_status = Label(self.master, text="")
        self.label_status.grid(column=1, row=3, padx=300)
        # Init inprog 
        self.check_sort_finish()
        # mainloop
        self.master.mainloop()

    def init_search(self):
        self.search_found = False
        if self.entry_search.get() != "":
            try:
                self.search_int = int(self.entry_search.get())
                if self.search_int in self.window.input_list:
                    self.search_found = True
                    self.window.update_search(self.search_int)
                    self.edit_status(f"Success! The number {self.search_int} was found.", False)
                else:
                    self.edit_status(f"The number {self.search_int} cannot be found.", False)
            except ValueError:
                self.edit_status("Search query cannot be iterated.")
            except: 
                self.edit_status(f"Unexpected error: {format_exc()}")
        else:
            self.edit_status("Search must not be empty.")

    def start_file(self):
        self.file_path = self.files.file_explorer()
        if self.file_path[len(self.file_path)-4:len(self.file_path)].lower() == ".txt":
            try:
                with open(self.file_path, "r") as numberfile:
                    try:
                        filecont = [int(i.strip()) for i in numberfile.read().split(",")]
                        self.window.input_list = filecont
                        self.window.update_vars()
                        self.refresh_size()
                        self.window.update_canv()
                        # self.entry_bar_amt.insert(END, f"{len(filecont)}")
                        self.window.update_search(None)
                        self.edit_status("Imported file successfully.", False)
                    except ValueError:
                        self.edit_status("File contents are not iterable.")
                    except: 
                        self.edit_status(f"Unexpected error: {format_exc()}")
                    numberfile.close()
            except FileNotFoundError:
                self.edit_status(f"{self.file_path} not found.")
            except: 
                self.edit_status(f"Unexpected error: {format_exc()}")
        elif self.file_path != "":
            self.edit_status("File not does not end with '.txt'.")

    def change_amt_update(self):
        if not self.window.inprog:
            try:
                if int(self.entry_bar_amt.get()) >= 2:
                    self.new_amt = int(self.entry_bar_amt.get())
                    self.window.refresh_list(self.new_amt)
                    self.window.update_vars()
                    self.refresh_size()
                else:
                    self.edit_status("Input is below 2.")
            except ValueError:
                self.edit_status("Input cannot be interated.")
            except: 
                self.edit_status(f"Unexpected error: {format_exc()}")
        else:
            self.edit_status("Sorting is in progress.")
    
    def edit_status(self, status_message, error=True):
        def delete_status(self):
            self.label_status.config(text="")
        if error:
            self.label_status.config(text=f"Error: {status_message}")
        else:
            self.label_status.config(text=f"{status_message}")
        self.master.after(5000, lambda: delete_status(self))

    def refresh_size(self):
        self.paned.config(orient=VERTICAL, width=(self.window.bar_width * (self.window.bar_amt + .3)), height=(self.window.max * self.window.bar_len_mult + 30))
    
    def button_update_stop(self, type):
        if self.window.test(self.window.input_list):
            if type == 0:
                self.button_ins_sort.config(text="Stop Sort", command=lambda: self.stop_sort(type))
            elif type == 1:
                self.button_sel_sort.config(text="Stop Sort", command=lambda: self.stop_sort(type))
            elif type == 2:
                self.button_bog_sort.config(text="Stop Sort", command=lambda: self.stop_sort(type))

    def check_sort_finish(self):
        if not self.window.inprog:
            self.stop_sort()
            self.window.stop = False
        self.master.after(50, lambda: self.check_sort_finish())

    def stop_sort(self, type=0):
        self.window.stop = True
        # if type == 0:
        self.button_ins_sort.config(text="Insertion Sort", command=lambda: self.begin_sort(type=0, r=self.r.get()))
        # elif type == 1:
        self.button_sel_sort.config(text="Selection Sort", command=lambda: self.begin_sort(type=1, r=self.r.get()))
        # elif type == 2:
        self.button_bog_sort.config(text="Bogo Sort", command=lambda: self.begin_sort(type=2, r=self.r.get()))

    def begin_sort(self, r, type=0):
        if not self.window.stop and not self.window.inprog:
            self.window.inprog = True
            self.window.r = r
            self.window.sort_delay = 5000/self.window.bar_amt
            self.button_update_stop(type)
            if type == 0:
                self.window.ins_sort()
            elif type == 1:
                self.window.iteration = 0
                self.window.sel_sort()
            elif type == 2:
                self.window.bog_sort()
        elif self.window.inprog:
            self.edit_status("Sorting is in progress.")
        else:
            self.edit_status("Program is stuck, try resterting.")


class Window(PanedWindow):
    def __init__(self, parent, bar_len_mult=5, bar_width=15, bar_amt=50, sort_delay=100, def_color="white", def_sort_color="lightgreen", def_search_color="lavender"):
        # Create pane object, assign parent
        PanedWindow.__init__(self, parent, width=bar_width * bar_amt, height=bar_amt * (bar_len_mult * 3/2 + 10), bg="red")
        self.parent = parent
        # Create canvas object
        self.main_canvas = Canvas()
        self.add(self.main_canvas)
        # Assign self vars
        self.bar_len_mult = bar_len_mult
        self.bar_width = bar_width
        self.bar_amt = bar_amt
        self.sort_delay = sort_delay
        self.def_color = def_color
        self.bar_color = self.def_color
        self.def_sort_color = def_sort_color
        self.search_found_color = def_search_color
        self.r = False  # Controls if sorting is in reverse
        self.stop = False  # Controls pausing of sorting
        self.inprog = False  # Controls inprogress
        self.search_term = None

    def refresh_list(self, custom_len=0):
        """Call to create new seq list up to self.bar_amt."""
        self.search_term = None
        if not custom_len == self.bar_amt and not custom_len == 0:
            self.bar_amt = int(custom_len)
        # Todo: add random value option for list
        self.input_list = [i + 1 for i in range(self.bar_amt)]
        shuffle(self.input_list)
        self.update_canv()

    def update_search(self, term):
        self.search_term = term
        self.update_canv()

    def update_canv(self):
        """Call to clear canvas and redraw objects, will fill with green if sorting is finished."""
        if not self.test(self.input_list):
            self.bar_color = self.def_sort_color
        self.main_canvas.delete("all")
        for i in range(len(self.input_list)):
            if self.input_list[i] == self.search_term:
                self.main_canvas.create_rectangle(i * self.bar_width, 0, i * self.bar_width + self.bar_width, self.input_list[i] * self.bar_len_mult, fill=self.search_found_color)
            else:
                self.main_canvas.create_rectangle(i * self.bar_width, 0, i * self.bar_width + self.bar_width, self.input_list[i] * self.bar_len_mult, fill=self.bar_color)
            self.main_canvas.create_text(i * self.bar_width + (self.bar_width / 2), self.input_list[i] * self.bar_len_mult + 15, text=self.input_list[i])
        if not self.bar_color == self.def_color:
            self.bar_color = self.def_color

    def update_vars(self):
        self.max = max(self.input_list)
        self.bar_amt = len(self.input_list)

    def test(self, input_list):
        if self.r:
            for i in range(len(input_list) - 1):
                if input_list[i] < input_list[i + 1]:
                    return True
            return False
        else:
            for i in range(len(input_list) - 1):
                if input_list[i] > input_list[i + 1]:
                    return True
            return False

    def finished(self, type):
        self.inprog = False
        self.update_canv()

    def bog_sort(self):
        self.update_canv()
        if self.test(self.input_list):
            self.input_list = bogo_sort(self.input_list)
            if not self.stop:
                self.parent.after(int(self.sort_delay), lambda: self.bog_sort())
            else:
                self.inprog = False
                self.stop = False
        else:
            self.finished(2)

    def sel_sort(self):
        self.update_canv()
        if self.test(self.input_list):
            self.input_list = selection_sort(self.input_list, self.iteration, self.r)
            self.iteration += 1
            if not self.stop:
                self.parent.after(int(self.sort_delay), lambda: self.sel_sort())
            else:
                self.inprog = False
                self.stop = False
        else:
            self.finished(1)

    def ins_sort(self):
        self.update_canv()
        if self.test(self.input_list):
            self.input_list = insertion_sort(self.input_list, self.r)
            if not self.stop:
                self.parent.after(int(self.sort_delay), lambda: self.ins_sort())
            else:
                self.inprog = False
                self.stop = False
        else:
            self.finished(0)

class FileIO():
    def __init__(self, parent):
        self.parent = parent
    def file_explorer(self):
        # Open file explorer
        filename = filedialog.askopenfilename(
                initialdir=f"{environ['USERPROFILE']}/Documents",
                title="Select File",
                filetypes=(("Text files",
                            "*.txt*"),
                            ("all files",
                            "*.*")))
        return filename


def main():
    """Initialize program."""
    mainUI = Main_UI()
    

if __name__ == "__main__":
    main()