#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    https://shiny.posit.co/
#

library(shiny)

green_prob_start = 0.8
blue_prob_start = 0.8
green_goal_start = 20
blue_goal_start = 20

sidebar_state = "closed" # start sidebar closed by default; a possibly better alternative would be
# sidebar_state = "desktop"

green_hex="#34b754"
blue_hex="#337ab7"
black_hex="#000000"

description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam porta, nulla et volutpat porta, mi nulla fermentum urna, bibendum consectetur felis nulla eu nibh. Vivamus dictum lectus egestas, venenatis turpis eu, tincidunt nunc. Nullam facilisis urna sed orci viverra interdum. Etiam blandit semper fringilla."


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
#    titlePanel("Old Faithful Geyser Data"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
	    h2("Color Picker Project:"),
	    p(description),
	    downloadButton("Download_Data", "Download Data"), # Save data
	    h1("Adjust parameters"), # These are self explanatory
	    numericInput("green_prob_chooser", "Probability of green button working",
			              green_prob_start, min=0, max=1),
	    numericInput("blue_prob_choser", "Probability of blue button working",
		               blue_prob_start, min=0, max=1),
	    numericInput("green_win_condition", "Points for green completion",
			              green_goal_start, min=0, max=512),
	    numericInput("blue_win_condition", "Points for blue completion",
			              blue_goal_start, min=0, max=512),
	    actionButton("update_params", "Update Parameters\n(resets data)"),
	    width = 450
    ),
    card( # there's no card function???
    	layout_columns(
    	  actionButton("green_btn", "Pick Green!", class="btn-lg"), # Have to include style
    		  layout_columns(
    		    actionButton("reset", "Reset Scores"), # Have to get style
    		    actionButton("reset_data", "Reset Data") # Have to get style
    		  ),
    	    actionButton("blue_btn", "Pick Blue!", class="btn-lg") #Style
    	)
    ),
    card(
	card_header("Current Status:"),
	layout_columns(
	    card(
		card(
		    h1("Total Green Points"),
		    textOutput("green_prob_text"),
		    h2(textOutput("counter1"))
		),
		card(
		    h1("Total Blue Points"),
		    textOutput("blue_prob_text"),
		    h2(textOutput("counter2"))
		)
	    ),
	    card(
		plotOutput("plot")
	    )
	)
    )
)


# Define server logic required to draw a histogram
server <- function(input, output) {
    values = reactiveValues()
    values$count1 = 0
    values$count2 = 0
    values$green_prob = green_prob_start
    values$blue_prob = blue_prob_start
    values$green_goal = green_goal_start
    values$blue_goal = blue_goal_start

    values$data = data.frame(green_score = 0, blue_score = 0, button_chosen = NA, 
			     green_prob = values$green_prob, blue_prob = values$blue_prob,
			     green_goal = values$green_goal, blue_goal = values$blue_goal)
    ## Initialize a dataframe. R doesn't really like datarames with no data but columnames so I've initialized this to nothing
    


}

# Run the application 
shinyApp(ui = ui, server = server)
