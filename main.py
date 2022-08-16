'''
Developed By : Sihab Sahariar
Project Name : PySort GUI
Sorting Algorithm : Bubble Sort, Selection Sort, Merge Sort, Insertion Sort
'''
import random
import time
import sys
import pandas as pd
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import * 
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib as mpl 
mpl.rcParams['toolbar'] = 'None'
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'      # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
    '#fff',     #White
]



class MatplotlibWidget(QMainWindow):

    # Declare class var
    xdata = None
    ydata = None
    loop_state = False

    def __init__(self):
        # Constructor
        QMainWindow.__init__(self)

        # Read UI
        loadUi("gui.ui",self)
        
        self.setWindowIcon(QtGui.QIcon("ico.png"))
        self.setFixedSize(800,600)
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)
        self.MplWidget.canvas.axes.get_yaxis().set_visible(False)

        # Connect methods to buttons :
        self.btn_Bubble.clicked.connect(self.bubble_sort)
        self.btn_Insertion.clicked.connect(self.insert_sort)
        self.btn_Merge.clicked.connect(self.merge_sort)
        self.btn_Selection.clicked.connect(self.select_sort)

        # Update Graph when spin-box is changed
        self.spnBars.valueChanged.connect(self.update_new_graph)

        # Call Shuffle method when clicked
        self.btn_Shuffle.clicked.connect(self.Shuffle_bars)
    
    
    def new_frame(self, highlight_bar):
         
        # Sleep to create a more pleasing animation
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        # Create colour list to indicate which bar is highlighted
        bar_color = ["#00A7E1"] * (len(self.ydata)-1)
        bar_color.insert(highlight_bar,"#ffa500")
        self.draw_graph(self.xdata, self.ydata, bar_color)

        # Process pending envents for the MPL graph
        QtCore.QCoreApplication.processEvents()


    def ani_time(self):
        # Determine sort wait time scaled to bars amount
        ani_speed = self.sldAnim_speed.value()

        # Linear formula that determine the sleep time from the slider value
        ani_interval = (-1/295)*ani_speed + 0.336
        return(ani_interval)
    
    
    def Shuffle_bars(self):
        # Shuffle bars in canvas
        self.MplWidget.canvas.axes.clear()

        bar_count = self.spnBars.value()
        
        scram_ys = [i for i in range(1, bar_count +1)]
        xs = scram_ys.copy()
        
        for j in range(0, len(scram_ys)-1):
            target = random.randint(j, len(scram_ys)-1)
            scram_ys[j] , scram_ys[target] = scram_ys[target], scram_ys[j]
        
        # Send Shuffled data to class var
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, scram_ys, None)
        self.status.setText("Ready For Sorting!")


    def update_new_graph(self):
        # Update canvas on change event from the spin edit
        self.MplWidget.canvas.axes.clear()

        # Create new dataset with changed size
        bar_count = self.spnBars.value()
        ys = [i for i in range(1, bar_count +1)]
        xs = ys.copy()

        # Send data to class var
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # Draw new data onto graph
        self.draw_graph(xs, ys, None)
        

    def initial_graph(self):
        # Startup with bars, not empty graph
        self.update_new_graph()


    def draw_graph(self, xs, ys, bar_color):
        # Draw graph from x-list and y-list
        if bar_color is None:
            self.MplWidget.canvas.axes.bar(xs, ys, color = "#00A7E1")
        else:
            # Color parameter will highlight selected bar (Bar that is being moved)
            self.MplWidget.canvas.axes.bar(xs, ys, color = bar_color)

        self.MplWidget.canvas.draw()      


    def buttons(self, tfstate):
        self.btn_Bubble.setEnabled(tfstate)
        self.btn_Insertion.setEnabled(tfstate)
        self.btn_Merge.setEnabled(tfstate)
        self.btn_Selection.setEnabled(tfstate)
        self.btn_Shuffle.setEnabled(tfstate)
    

    def bubble_sort(self):
        # Copy dataset
        yarray = self.ydata.copy()

        # Disable buttons
        self.buttons(False)
        self.status.setText("Bubble Sort Processing!")

        # Loop through all elements
        for i in range(len(yarray)):

            # Determine new endpoint as last i elements will be sorted (efficientcy)
            endp = len(yarray) - i
            
            # Iterate over new resized dataset
            for j in range(0 , endp):
                
                # Prevent loop reaching out of list
                if j+1 == len(yarray):
                    pass
                else:
                    if yarray[j] > yarray[j+1]:

                        # Swap elements if not ascending 
                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]

                        # Update class var
                        self.ydata = yarray

                        # Call to update graph
                        self.new_frame(j+1)

        self.buttons(True)
        self.status.setText("Bubble Sort Done!")


    def insert_sort(self):
        # Get class variable
        yarray = self.ydata.copy()
        self.status.setText("Insertion Sort Processing!")
        # Disable buttons
        self.buttons(False)

        # Loop through list
        for i in range(len(yarray)):

            if (i+1) == len(yarray):
                # Prevent reading out of list
                break 
            else:
                # If pair not in ascending order
                if yarray[i] > yarray[i+1]:
                    # Using Swaping method for better animation / demostration. Delete and insert method is commented

                    # # Delete and Insert method---------------------------------------------
                    # # Read and remove
                    # temp = yarra.pop(i+1) 

                    # for j in range(i+1):
                    #     if yarray[j] > temp:
                    # 
                    #         # Find first elem that is bigger than Temp, insert at that position, shift the rest down
                    #         index = j
                    #         yarray.insert(index, temp)
                    #         self.new_frame(j)
                    #         break               
                    
                    # Swap method -----------------------------------------------------------
                    # Find the right place for the elem, from beginning till current spot in list
                    for k in reversed(range(i+1)):
                        if yarray[k+1] < yarray[k]:
                            yarray[k], yarray[k+1] = yarray[k+1] , yarray[k]

                            # Update class var
                            self.ydata = yarray

                            # Update graph
                            self.new_frame(k)
                        else:
                            break

        self.buttons(True)
        self.status.setText("Insertion Sort Done!")        
         

    def merge_sort(self):
        # Copy dataset
        yarray = self.ydata.copy()
        self.status.setText("Merge Sort Processing!")
        # Disable buttons
        self.buttons(False)

        yarray = self.merge_split(yarray)

        # Update class var
        self.ydata = yarray
        self.new_frame(0)
        
        self.buttons(True)
        self.status.setText("Merge Sort Done!")        


    def merge_split(self, arr):
        length = len(arr)

        # Return, end of recursion
        if length == 1:
            return(arr)
        
        midp = length//2

        # Call self to split until return single element, update class var
        arr_1 = self.merge_split(arr[:midp])
        self.merge_update(arr_1, self.ydata)
        arr_2 = self.merge_split(arr[midp:])
        self.merge_update(arr_2, self.ydata)
        
        self.new_frame(0)

        # Call merge to sort half lists
        return(self.merge(arr_1, arr_2))


    def merge_update(self, sub_list, main_list):
        
        # Get index of the sorted elements in the main list
        pos = []
        for value in sub_list:
            pos.append(main_list.index(value))

        # Remove elem from main list
        for v in sub_list:
            main_list.remove(v)
        
        # Find range
        high = max(pos)
        low = min(pos)

        # Insert same elements back to main list, from sorted list (in order)
        for i in range(low, high+1):
            main_list.insert(i, sub_list[i-low])

        
    def merge(self, arr_1, arr_2):
        sorted_arr = []

        # Use append and pop, given already sorted lists 
        while arr_1 and arr_2:
            
            if arr_1[0] < arr_2[0]:
                # arr1[0] smaller
                sorted_arr.append(arr_1.pop(0))
            else:
                # arr2[0] smaller
                sorted_arr.append(arr_2.pop(0))

        # Append from sorted sublist, as one of the sub-list will be empty
        while arr_1:
            sorted_arr.append(arr_1.pop(0))

        while arr_2:
            sorted_arr.append(arr_2.pop(0))

        return(sorted_arr)
        
    
    def select_sort(self):
        # Get class variable
        yarray = self.ydata.copy()
        self.status.setText("Selection Sort Processing!")
        # Disable buttons
        self.buttons(False)

        # Loop through list
        for i in range(len(yarray)):

            #Place holder for smallest number in sublist
            holder = None

            # Iterate over unsorted sublist
            for j in range(i,len(yarray)):
                
                if (not holder):
                    holder = yarray[j]
                elif yarray[j] < holder:
                    holder = yarray[j]

                # Show iteration
                self.new_frame(j)
            

            # Read and insert lowest bar into sorted part
            shifter_index = yarray.index(holder)
            yarray.pop(shifter_index)
            yarray.insert(i, holder)

            # Update class var & graph
            self.ydata = yarray

            # Update graph
            self.new_frame(shifter_index)

        self.buttons(True)
        self.status.setText("Selection Sort Done!")        
        

app = QApplication([])
window = MatplotlibWidget()
window.Shuffle_bars()
window.show()
app.exec_()
