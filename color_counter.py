from shiny import App, reactive, render, ui
# Code Josie provided

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_action_button("click_me", "Click Me!", class_="btn-primary"),
        ui.input_action_button("reset", "Reset Counter", class_="btn-secondary")
    ),
    ui.card(
        ui.card_header("Button Press Counter"),
        ui.card_body(
            ui.h2(ui.output_text("counter")),
            ui.p("Times button has been pressed")
        )
    )
)

def server(input, output, session):
    # Reactive value to store the counter
    count = reactive.value(0)
    
    # Increment counter when button is pressed
    @reactive.effect
    @reactive.event(input.click_me)
    def _():
        count.set(count() + 1)
    
    # Reset counter when reset button is pressed
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        count.set(0)
    
    # Display the current count
    @render.text
    def counter():
        return str(count())

app = App(app_ui, server)
