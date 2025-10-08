from shiny import App, reactive, render, ui
import random
green_prob = 0.8 # hardcoded probabilities, discussions below
blue_prob = 0.8

# Issues/To-Do: 
## Add plots
## Nicer UI?
## Can't get color to display on buttons. 
## Need to make text better
### The cards showing the points could be colored for example, that might be a bit much though
## Could query green and blue probabilities in a UI element
## Display probabilities of truly incrementing each color on button press

app_ui = ui.page_auto(
    ui.card(
        ui.layout_columns(
            ui.input_action_button("green_btn", "Pick Green!", class_="btn-lg",
                                   style = "height: 200px; background-color = #008000"), # color isn't working here
            ui.input_action_button("reset", "Reset Scores", class_="btn-secondary",
                                   style = "height: 200px"),
            ui.input_action_button("blue_btn", "Pick Blue!", class_="btn-lg",
                                   style = "height: 200px")
            )
    ),
    ui.card(
        ui.card_header("Button Press Counter"),
        ui.layout_columns(
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
        )
    )
)

def server(input, output, session):
    # Reactive value to store the counter
    count1 = reactive.value(0) # could be changed to better name
    count2 = reactive.value(0)
    
    # Increment counter when button is pressed
    @reactive.effect
    @reactive.event(input.green_btn) 
    def _():
        if random.random() <= green_prob: # could increment either counters
            count1.set(count1() + 1)
            return
        count2.set(count2() + 1)
    
    @reactive.effect # Now for the blue button
    @reactive.event(input.blue_btn)
    def _():
        if random.random() <= blue_prob:
            count2.set(count2() + 1)
            return
        count1.set(count1() + 1)
    
    # Reset both counters when reset button is pressed; do we want this?
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        count1.set(0)
        count2.set(0)
    
    # Display the current counts
    @render.text
    def counter1():
        return str(count1())
    @render.text
    def counter2():
        return str(count2())

app = App(app_ui, server)
app.run() # actually run the app
