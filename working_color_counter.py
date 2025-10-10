from shiny import App, reactive, render, ui
from matplotlib import pyplot as plt
import random
import os

green_prob_start = 0.8
blue_prob_start = 0.8
green_goal_start = 20
blue_goal_start = 20

# Issues/To-Do: 
## Make data saveable. I've gotten this up following guidance here
### https://shiny.posit.co/py/api/core/render.download.html
### but the button isn't working
## Add description 
## the colors in the data aren't as strings, not major but will probably be a problem depending on language to analyze

green_hex="#34b754"
blue_hex="#337ab7"
black_hex="#000000"

class Data: # This is the easiest way I can think to do this, it puts all the code up here and then I can call later
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


data = Data(["green_score", "blue_score", "button_chosen", "green_prob", "blue_prob", "gren_goal", "blue_goal"]) # hardcode column names and a data object to reference

app_ui = ui.page_auto(
    ui.sidebar(
        ui.h2("Color Picker Project:"), 
        ui.p("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam porta, nulla et volutpat porta, mi nulla fermentum urna, bibendum consectetur felis nulla eu nibh. Vivamus dictum lectus egestas, venenatis turpis eu, tincidunt nunc. Nullam facilisis urna sed orci viverra interdum. Etiam blandit semper fringilla."), # add description
        ui.input_action_button("save_data", "Save Data", class_="btn-primary"), # to save data
        ui.h1("Adjust parameters:"), # these are largely self explanatory
        ui.input_numeric("green_prob_chooser", "Probability of green button working", 
                         0.8, min=0, max=1),
        ui.input_numeric("blue_prob_chooser", "Probability of blue button working", 
                         0.8, min=0, max=1),
        ui.input_numeric("green_win_condition", "Points for green completion", 
                         20, min=0, max=512),
        ui.input_numeric("blue_win_condition", "Points for blue completion", 
                         20, min=0, max=512),
        ui.input_action_button("update_params", "Update Parameters")
    ),
    ui.card(
        ui.layout_columns(
            ui.input_action_button("green_btn", "Pick Green!", class_="btn-lg",
                                   style = f"height: 200px; color: #fff; background-color: {green_hex};"),
            ui.input_action_button("reset", "Reset Scores", class_="btn-secondary",
                                   style = "height: 200px"),
            ui.input_action_button("blue_btn", "Pick Blue!", class_="btn-lg",
                                   style = f"height: 200px; color: #fff; background-color: {blue_hex};")
            )
    ),
    ui.card(
        ui.card_header("Current Status:"),
        ui.layout_columns(
            ui.card(
                ui.card(
                    ui.h1("Total Green Points"),
                    ui.card_body(
                        ui.h2(ui.output_text("counter1")),
                    )
                ),
                ui.card(
                    ui.h1("Total Blue Points"),
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
    blue_prob = reactive.value(blue_prob_start)
    green_goal = reactive.value(green_goal_start)
    blue_goal = reactive.value(blue_goal_start)
    
    # Increment counter when button is pressed
    @reactive.effect
    @reactive.event(input.green_btn) 
    def _():
        data.append([count1(), count2(), "Green", green_prob(), blue_prob(), 
                    green_goal(), blue_goal()]) # I don't know what data they want
        if random.random() <= green_prob(): # could increment either counters
            count1.set(count1() + 1)
            return
        count2.set(count2() + 1)

    
    @reactive.effect # Now for the blue button
    @reactive.event(input.blue_btn)
    def _():
        data.append([count1(), count2(), "Blue", green_prob(), blue_prob(), 
                    green_goal(), blue_goal()]) # I don't know what data they want
        if random.random() <= blue_prob():
            count2.set(count2() + 1)
            return
        count1.set(count1() + 1)
    
    # Reset both counters when reset button is pressed; do we want this?
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        count1.set(0)
        count2.set(0)

    @reactive.effect
    @reactive.event(input.update_params)
    def _():
        green_prob.set(input.green_prob_chooser())
        blue_prob.set(input.blue_prob_chooser())
        green_goal.set(input.green_win_condition())
        blue_goal.set(input.blue_win_condition())
        count1.set(0)
        count2.set(0)
    
    # Display the current counts
    @render.text
    def counter1():
        return str(count1())
    @render.text
    def counter2():
        return str(count2())
    @render.plot
    def plot():
        k = 0 # Make bars aligned well
        max_val = max(green_goal(), blue_goal(), count1(), count2())
        while max_val > 2**k-1:
            k += 1 # So the plot isn't as jittery
        plt.bar(x=["Green","Blue"],height=[count1(),count2()],color=[f'{green_hex}',f'{blue_hex}'])
        plt.ylim(0,2**k)
        plt.hlines(green_goal(), xmin=-0.4, xmax=0.4, color = black_hex)
        plt.hlines(blue_goal(), xmin=0.6, xmax = 1.4, color = black_hex)

    @render.download()
    def save_data():
        path = os.path.join(os.path.dirname(__file__), "color_picker_data.csv")
        return path
        with open(path, "w") as f:
            f.print(str(data))
        return os

app = App(app_ui, server)
app.run() # actually run the app
