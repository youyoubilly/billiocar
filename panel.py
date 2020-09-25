import ipywidgets.widgets as widgets
from ipywidgets import Button, HBox, VBox

class NineButton():
    def __init__(self, button_list=None):
        self.button_layout = widgets.Layout(width='100px', height='80px', align_self='center')
        self.button_list = ['Forward', '▲', 'Slide_L', '◄', 'Stop', '►', 'Backward', '▼', 'Slide_R'] if button_list==None else button_list
        self.buttons = [Button(description=i, layout=self.button_layout) for i in self.button_list]
        
    def display(self):
        row1 = HBox([self.buttons[0], self.buttons[1], self.buttons[2]])
        row2 = HBox([self.buttons[3], self.buttons[4], self.buttons[5]])
        row3 = HBox([self.buttons[6], self.buttons[7], self.buttons[8]])
        return VBox([row1, row2, row3])