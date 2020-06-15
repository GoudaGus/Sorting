from tkinter import *
from algorithims import insertion_sort, selection_sort
from random import shuffle
from time import sleep


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
        self.paned.config(orient=VERTICAL, width=(self.window.bar_width * (self.window.bar_amt + .3)), height=(self.window.bar_amt * self.window.bar_len_mult + 25))
        self.window.refresh_list()
        self.paned.add(self.window)
        # Init bar amt entry
        self.entry_bar_amt = Entry(self.master)
        self.entry_bar_amt.insert(END, f"{self.window.bar_amt}")
        self.entry_bar_amt.grid(column=1, row = 1, ipadx=20, sticky="w")

        self.r = BooleanVar()
        self.reverse_check = Checkbutton(self.master, text="Reverse sort", variable=self.r, onvalue=True, offvalue=False)
        self.reverse_check.grid(column=1, row=1, padx=440, sticky="w")
        # Init ins sort button
        self.button_ins_sort = Button(self.master, text="Insertion Sort", command=lambda: self.window.begin_sort(type=0, r=self.r.get()))
        self.button_ins_sort.grid(column=1,row=1, padx=260, sticky="w")
        #Init sel sort button
        self.button_sel_sort = Button(self.master, text="Selection Sort", command=lambda: self.window.begin_sort(type=1, r=self.r.get()))
        self.button_sel_sort.grid(column=1,row=1, padx=350, sticky="w")
        # Init reset button
        self.reset_button = Button(self.master, text="Reset/Shuffle", command=lambda: self.change_amt())
        self.reset_button.grid(column=1, row=1, padx=175, sticky="w")
        # Init error label
        self.label_error = Label(self.master, text="")
        self.label_error.grid(column=1, row=2, padx=300)
        # mainloop
        self.master.mainloop()

    def change_amt(self):
        # 
        try:
            self.new_amt = int(self.entry_bar_amt.get())
            self.window.refresh_list(self.new_amt)
            self.refresh_size()
        except ValueError:
            self.edit_error("Input cannot be interated.")
    
    def edit_error(self, error_message):
        def delete_error(self):
            self.label_error.config(text="")
        self.label_error.config(text=f"Error: {error_message}")
        self.master.after(3000, lambda: delete_error(self))

    def refresh_size(self):
        self.paned.config(orient=VERTICAL, width=(self.window.bar_width * (self.window.bar_amt + .3)), height=(self.window.bar_amt * self.window.bar_len_mult + 25))
    
class Window(PanedWindow):
    def __init__(self, parent, bar_len_mult=5, bar_width=15, bar_amt=50, sort_delay=100, def_color="white", def_sort_color="lightgreen"):
        # Create pane object, assign parent
        PanedWindow.__init__(self, parent, width=bar_width * bar_amt, height=bar_amt * (bar_len_mult * 3/2 + 5), bg="red")
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
        self.r = False
        
    def refresh_list(self, custom_len=0):
        """Call to create new seq list up to self.bar_amt."""
        if not custom_len == self.bar_amt and not custom_len == 0:
            self.bar_amt = int(custom_len)
        # Todo: add random value option for list
        self.input_list = [i for i in range(self.bar_amt)]
        shuffle(self.input_list)
        self.update_canv()

    def update_canv(self):
        """Call to clear canvas and redraw objects, will fill with green if sorting is finished."""
        self.main_canvas.delete("all")
        for i in range(len(self.input_list)):
            self.main_canvas.create_rectangle(i * self.bar_width, 0, i * self.bar_width + self.bar_width, self.input_list[i] * self.bar_len_mult, fill=self.bar_color)
            self.main_canvas.create_text(i * self.bar_width + (self.bar_width / 2), self.input_list[i] * self.bar_len_mult + 15, text=self.input_list[i])
        if not self.bar_color == self.def_color:
            self.bar_color = self.def_color

    def begin_sort(self, r, type=0):
        self.r = r
        self.sort_delay = 5000/self.bar_amt
        if type == 0:
            self.ins_sort()
        elif type == 1:
            self.iteration = 0
            self.sel_sort()

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

    def sel_sort(self):
        # self.r = r
        # def redo(self):
        #     sort(self)
        self.update_canv()
        if self.test(self.input_list):
            self.input_list = selection_sort(self.input_list, self.iteration, self.r)
            self.iteration += 1
            self.parent.after(int(self.sort_delay), lambda: self.sel_sort())
        else:
            self.bar_color = self.def_sort_color
            self.update_canv()

    def ins_sort(self):
        # def redo(self):
        #     sort(self)
        self.update_canv()
        if self.test(self.input_list):
            self.input_list = insertion_sort(self.input_list, self.r)
            self.parent.after(int(self.sort_delay), lambda: self.ins_sort())
        else:
            self.bar_color = self.def_sort_color
            self.update_canv()


def main():
    """Initialize program."""
    _ = Main_UI()


if __name__ == "__main__":
    main()