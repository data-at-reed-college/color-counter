from shiny import App, reactive, render, ui
import shiny
from matplotlib import pyplot as plt
import random
import os
import io

import numpy as np

# Hardcoded parameters
green_prob_start = 0.8
blue_prob_start = 0.8
green_goal_start = 20
blue_goal_start = 20
max_turns_start = 20

sidebar_state = "desktop" 

green_hex="#34b754"
blue_hex="#337ab7"
black_hex="#000000"

description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam porta, nulla et volutpat porta, mi nulla fermentum urna, bibendum consectetur felis nulla eu nibh. Vivamus dictum lectus egestas, venenatis turpis eu, tincidunt nunc. Nullam facilisis urna sed orci viverra interdum. Etiam blandit semper fringilla."

class Data: # Simple object to store and later write data 
    def __init__(self, cols):
        self.cols = cols
        self.data = []
        self.ncol = len(cols)
    def append(self, row): # add data rows
        assert len(row) == self.ncol
        self.data.append(row)
    def __str__(self): # To get in csv format
        s = ""
        def add_row(row, s, newline = True):
            if newline:
                s += "\n"
            s += str(row[0]) # so we can get commas in an easy way
            i = 1 
            while i < self.ncol:
                s += "," + str(row[i])
                i += 1
            return s
        s = add_row(self.cols, s, newline = False)
        for row in self.data:
            s = add_row(row, s)
        return s
    def clear_data(self): # clear data when called
        self.data = []
    # I probably should have just used pandas but I forgot about that

data_cols = ["green_score", "blue_score", "button_chosen", "number_of_turns","green_goal", "blue_goal", "green_start", "blue_start"] # columns to collect data on. Really the last 4 are largely fixed values, but there's no other way to record them nicely in a csv

app_ui = ui.page_auto(
    ui.sidebar(
        ui.h2("Color Picker Project:"), 
        ui.p(description), 
        ui.download_button("save_data", "Save Data", class_="btn-secondary"), # to save data
        ui.h1("Adjust parameters:"), # these are largely self explanatory
#        ui.input_numeric("green_prob_chooser", "Probability of green button working", 
#                         0.8, min=0, max=1),
#        ui.input_numeric("blue_prob_chooser", "Probability of blue button working", 
#                         0.8, min=0, max=1),
        ui.input_numeric("green_win_condition", "Points for green completion", 
                         20, min=0, max=512),
        ui.input_numeric("blue_win_condition", "Points for blue completion", 
                         20, min=0, max=512),
        ui.input_numeric("green_start", "Points to start green at", 
                         0, min=0, max=512),
        ui.input_numeric("blue_start", "Points to start blue at", 
                         0, min=0, max=512),
        ui.input_numeric("max_turns", "Number of button presses",
                         20, min=0, max=512),
        ui.input_action_button("update_params", "Update Parameters"),
        width = 450,
        open=sidebar_state
    ),
    ui.card(
        ui.layout_columns(
            ui.input_action_button("green_btn", "Pick Green!", class_="btn-lg",
                                   style = f"height: 125px; color: #fff; background-color: {green_hex};"),
            ui.layout_columns(
                ui.input_action_button("reset", "Reset Scores\n(resets data)",
                                       class_="btn-secondary", style = "height: 125px; width = 125px"),
#                ui.input_action_button("reset_data", "Reset Data",
#                                       class_="btn-secondary", style = "height: 125px; width = 125px")
                ui.card(
                    ui.h5("Turns left:"),
                    ui.output_text("turns_left")
                    )
            ),
            ui.input_action_button("blue_btn", "Pick Blue!", class_="btn-lg",
                                   style = f"height: 125px; color: #fff; background-color: {blue_hex};")
            )
    ),
    ui.card(
        #ui.card_header("Current Status:"),
        ui.layout_columns(
            ui.card(
                ui.card(
                    ui.h1("Total Green Points"),
                    ui.output_text("green_prob_text"),
                    ui.card_body(
                        ui.h2(ui.output_text("counter1")),
                    )
                ),
                ui.card(
                    ui.h1("Total Blue Points"),
                    ui.output_text("blue_prob_text"),
                    ui.card_body(
                        ui.h2(ui.output_text("counter2")),
                    )
                )
            ),
             ui.card(
                ui.card_body(
                   ui.output_plot("plot"),
                )
            )
        )
    )
)

def server(input, output, session):
    # Reactive value to store the counter
    count1 = reactive.value(0) # could be changed to better name
    count2 = reactive.value(0)
    green_prob = reactive.value(green_prob_start) # various internal parameters
    blue_prob = reactive.value(blue_prob_start) # these prob parameters aren't being used, so if we were spending more time, it would be worth removing them and replacing all with hardcoded values, but whatever
    green_goal = reactive.value(green_goal_start)
    blue_goal = reactive.value(blue_goal_start)
    green_start = reactive.value(0)
    blue_start = reactive.value(0)
    green_sign = reactive.value(1) # these are based on start and goals, tell whether or not to decrement or increment scores; take on either 1 or -1
    blue_sign = reactive.value(1)
    num_turns = reactive.value(max_turns_start)

    data = reactive.value(Data(data_cols)) 
    # data stores a pointer to a Data object. If we want to modify data, we modify the pointer in data.get() as a Data object. This makes the data local to each web-session, so the data don't mingle with each other
    
    # Increment counter when button is pressed
    @reactive.effect
    @reactive.event(input.green_btn) 
    def _():
        if num_turns() <= 0:
            return
        data.get().append([count1(), count2(), "'Green'", num_turns(),
                    green_goal(), blue_goal(), green_start(), blue_start()]) # I don't know what data they want
        if random.random() <= green_prob(): # could increment either counters
            count1.set(count1() + green_sign() * 1)
        if random.random() > green_prob(): # probability to increment the other, I'm using green_prob just because we want the two probabilities to be 0.8 and 0.2 and 0.2 happens to be 1 - 0.8
            count2.set(count2() + blue_sign() * 1)
        num_turns.set(num_turns()-1)

    
    @reactive.effect # Now for the blue button
    @reactive.event(input.blue_btn)
    def _():
        if num_turns() <= 0:
            return
        data.get().append([count1(), count2(), "'Blue'", num_turns(),
                    green_goal(), blue_goal(), green_start(), blue_start()]) # I don't know what data they want
        if random.random() <= blue_prob():
            count2.set(count2() + blue_sign() * 1)
        if random.random() > blue_prob(): # same comment as earlier
            count1.set(count1() + green_sign() * 1)
        num_turns.set(num_turns()-1)
    
    # Reset both counters when reset button is pressed; do we want this?
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        count1.set(0)
        count2.set(0)
        num_turns.set(input.max_turns())

#    @reactive.effect
#    @reactive.event(input.reset_data)
#    def _():
#        data.get().clear_data()


    @reactive.effect
    @reactive.event(input.update_params)
    def _():
#        green_prob.set(input.green_prob_chooser())
#        blue_prob.set(input.blue_prob_chooser())
        green_goal.set(input.green_win_condition())
        blue_goal.set(input.blue_win_condition())
        green_start.set(input.green_start())
        blue_start.set(input.blue_start())
        num_turns.set(input.max_turns())
        count1.set(green_start())
        count2.set(blue_start())

        if green_goal() >= green_start():
            green_sign.set(1)
        else:
            green_sign.set(-1)

        if blue_goal() >= blue_start():
            blue_sign.set(1)
        else:
            blue_sign.set(-1)
    
    # Display the current counts
    @render.text
    def counter1():
        return str(count1())
    @render.text
    def counter2():
        return str(count2())
    @render.text
    def green_prob_text():
        string="With a green button press, there's a 80% chance to "
        if green_sign() == 1:
            string += "increase green and another 20% to "
            if blue_sign() == 1:
                string += "increment blue"
                return string
            string += "decrement blue"
            return string
        # else green_sign == -1
        string+= "decrement green and another 20% to "
        if blue_sign() == 1:
            string += "increment blue"
            return string
        string += "decrement blue"
        return string


    @render.text
    def blue_prob_text():
        string="With a blue button press, there's a 80% chance to "
        if blue_sign() == 1:
            string += "increase blue and another 20% to "
            if green_sign() == 1:
                string += "increment green"
                return string
            string += "decrement green"
            return string
        # else blue_sign == -1
        string+= "decrement blue and another 20% to "
        if green_sign() == 1:
            string += "increment green"
            return string
        string += "decrement green"
        return string

    @render.text
    def turns_left():
        return str(num_turns())
    @render.plot
    def plot():
        k = 0 # Make bars aligned well
        max_val = max(green_goal(), blue_goal(), count1(), count2(), green_start(), blue_start())
        while max_val > 2**k-1:
            k += 1 # So the plot isn't as jittery
        plt.bar(x=["Green","Blue"],height=[count1(),count2()],color=[f'{green_hex}',f'{blue_hex}'])
        plt.ylim(0,2**k)
        plt.hlines(green_goal(), xmin=-0.4, xmax=0.4, color = black_hex)
        plt.hlines(blue_goal(), xmin=0.6, xmax = 1.4, color = black_hex)

    @render.download(filename = "color_picker_data.csv")
    def save_data():
        yield str(data.get()) # we are just yielding a string of data (defined the method earlier)

app = App(app_ui, server)

shiny.run_app(app=app,
              host="0.0.0.0",
              port=7860
              ) # actually run the app
