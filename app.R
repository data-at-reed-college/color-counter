library(shiny)
library(htmltools)

# Problems: 
## The sidebar is sad. I've commented out a bunch of stuff now to try to get a very basic thing working, but I have no idea why the sidebar isn't working
## R shiny doesn't have card???? It says it does (https://rstudio.github.io/bslib/reference/card.html) or that htmltools does, but it's not in either of the librarys. Whatttt
## Just keep plowing through the code, we have to make sure it all works and in my infinite wisdom I didn't test it at all while porting it over from python


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
	    #downloadButton("Download_Data", "Download Data"), # Save data
	    #h1("Adjust parameters"), # These are self explanatory
	    #numericInput("green_prob_chooser", "Probability of green button working",
			#              green_prob_start, min=0, max=1),
	    #numericInput("blue_prob_choser", "Probability of blue button working",
		  #             blue_prob_start, min=0, max=1),
	    #numericInput("green_win_condition", "Points for green completion",
			#              green_goal_start, min=0, max=512),
	    #numericInput("blue_win_condition", "Points for blue completion",
			#              blue_goal_start, min=0, max=512),
	    #actionButton("update_params", "Update Parameters\n(resets data)"),
	    #width = 450
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

    button_press = function(color, reactive_value) {
      values$data[nrow(values$data)+1,] = c(values$count1, values$count, color, 
                                            values$green_prob, values$blue_prob,
                                            values$green_goal, values4blue_goal)
      if(color == "green") {
        if(runif(1) <= values$green_button) {
          values$count1 = values$count1 + 1
        } else {
          values$count2 = values$count2 + 1
        }
      } else { # color is blue
        if (runif(1) <= values$blue_button) {
          values$count2 = values$count2 + 1
        } else {
          values$count1 = values$count1 + 1
        }
      }
    }
    
        
    observeEvent(input$green_btn, {
      button_press("green", values) # see above function
    })
    
    observeEvent(input$blue_btn, {
      button_press("blue", values)
    })
    
    observeEvent(input$reset, {
      values$count1 = 0
      values$count2 = 0
    })
    
    observeEvent(input$reset_data, {
      values$data = values$data[1,] #trimoff the rest of the data
    })
    
    observeEvent(input$update_params, {
      values$green_prob = input$green_prob_chooser
      values$blue_prob = input$blue_prob_chooser
      values$green_goal = input$green_win_condition
      values$blue_goal = input$blue_win_condition
      values$count1 = 0
      values$count2 = 0
    })
    
    output$counter1 = renderText({values$count1})
    output$counter2 = renderText({values$count2})
    output$green_prob_text = renderText({
      cat("The probability of incrementing green with a green button press is", values$green_prob)
      })
    output$blue_prob_text = renderText({
      cat("The probability of incrementing blue with a blue button press is", values$blue_prob)
    })
    output$plot = renderPlot({
      max_val = max(values$green_goal, values$blue_goal, 
                    values$count1, values$count2)
      k = ceiling(log(max_val, 2)) # to keep the plot from getting jittery with updates
      data.frame(y = c(values$count1, values$count2),
                 label = factor(c("Green", "Blue"), 
                                levels = c("Green", "Blue"))) %>%
        ggplot(aes(label, y, fill = label)) +
        geom_col() +
        geom_segment(
          data = data.frame(x = c(0.55, 1.55),
                            xend = c(1.45, 2.45),
                            y = c(values$green_goal, values$blue_goal),
                            yend = c(values$green_goal, values$blue_goal),
                            label = factor(c("Green", "Blue"), 
                                           levels = c("Green", "Blue"))),
          aes(x =x, xend = xend, y = y, yend = yend, color = label)) +
        theme_bw() +
        scale_fill_manual(
          values = c(green_hex, blue_hex)
        ) + # manually recoding color
        scale_color_manual(values = c(green_hex, blue_hex)) +
        theme(legend.position = "none") +
        labs(x = "", y = "") +
        ylim(0,2^k)
        scale_y_discrete() 
    })
    output$save_data = downloadHandler(
      filename = function(){"color_picker_data.csv"},
      content = function(fname){
        values$data %>%
          slice(-c(1)) %>% # the first row is useless, see me defining data
          write.csv(., fname)
      }
    )
    
    


}

# Run the application 
shinyApp(ui = ui, server = server)
