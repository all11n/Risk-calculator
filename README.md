library(shiny)
library(ggplot2)
library(dplyr)

df <- read.csv("fires_clean.csv", sep = ";")
df$dt <- as.Date(df$dt)

daily_fires <- df %>%
  group_by(dt) %>%
  summarise(count = n()) %>%
  arrange(dt)

type_counts <- df %>%
  group_by(type_name) %>%
  summarise(count = n())

ui <- fluidPage(
  titlePanel("Интерактивный анализ пожаров"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("plotType", "Выберите тип графика:",
                  choices = c("Динамика по дням", 
                              "Распределение по типам",
                              "Пространственное распределение")),
      
      conditionalPanel(
        condition = "input.plotType == 'Динамика по дням'",
        sliderInput("dateRange", "Диапазон дат:",
                    min = min(daily_fires$dt), max = max(daily_fires$dt),
                    value = c(min(daily_fires$dt), max(daily_fires$dt)))
      ),
      
      conditionalPanel(
        condition = "input.plotType == 'Распределение по типам'",
        checkboxGroupInput("typeFilter", "Типы пожаров:",
                           choices = unique(df$type_name),
                           selected = unique(df$type_name))
      ),
      
      conditionalPanel(
        condition = "input.plotType == 'Пространственное распределение'",
        sliderInput("latRange", "Диапазон широты:",
                    min = min(df$lat), max = max(df$lat),
                    value = c(min(df$lat), max(df$lat)))
      )
    ),
    
    mainPanel(
      plotOutput("mainPlot", height = "600px")
    )
  )
)

server <- function(input, output) {
  
  output$mainPlot <- renderPlot({
    
    if(input$plotType == "Динамика по дням") {
      daily_fires %>%
        filter(dt >= input$dateRange[1], dt <= input$dateRange[2]) %>%
        ggplot(aes(x = dt, y = count)) +
        geom_line(color = "steelblue", linewidth = 1) +
        geom_point(color = "steelblue", size = 2, alpha = 0.5) +
        labs(title = "Динамика пожаров по дням",
             x = "Дата", y = "Количество пожаров") +
        theme_minimal() +
        theme(plot.title = element_text(hjust = 0.5, size = 16))
      
    } else if(input$plotType == "Распределение по типам") {
      df %>%
        filter(type_name %in% input$typeFilter) %>%
        ggplot(aes(x = reorder(type_name, type_name, function(x) -length(x)))) +
        geom_bar(fill = "coral", alpha = 0.8) +
        labs(title = "Распределение типов пожаров",
             x = "Тип пожара", y = "Количество") +
        theme_minimal() +
        theme(plot.title = element_text(hjust = 0.5, size = 16),
              axis.text.x = element_text(angle = 45, hjust = 1))
      
    } else {
      df %>%
        filter(lat >= input$latRange[1], lat <= input$latRange[2]) %>%
        ggplot(aes(x = lon, y = lat, color = type_name)) +
        geom_point(alpha = 0.6, size = 2) +
        labs(title = "Пространственное распределение пожаров",
             x = "Долгота", y = "Широта") +
        theme_minimal() +
        theme(plot.title = element_text(hjust = 0.5, size = 16)) +
        scale_color_brewer(palette = "Set1")
    }
  })
}

shinyApp(ui = ui, server = server)
