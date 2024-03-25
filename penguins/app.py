import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins
import pandas as pd 
import seaborn as sns
from shiny import reactive, render, req

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Data Ryan Krabbe", fillable=True)

    # Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    ui.input_slider("selected_number_of_bins", "Number of Bins", 1, 100, 30) 
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize("selected_attribute",
                        "Select Attribute",
                        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
                       )
    
    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Number of Plotly Histogram Bins", 30)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn bin count", 1, 25, 15)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", 
                             "Select Species", 
                             ["Adelie", "Gentoo", "Chinstrap"], 
                             selected=["Adelie", "Gentoo", "Chinstrap"], 
                             inline=True)
    
    ui.input_checkbox_group("selected_island_list", 
                             "Select Island", 
                             ["Dream", "Biscoe", "Torgersen"], 
                             selected=["Dream", "Biscoe", "Torgersen"], 
                             inline=True)

    # Add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/ryankrabbe/cintel-02-data", target="_blank")

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Add a DataTable and DataGrid
with ui.accordion(id="acc", open="Data Table"):  
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return filtered_data() 
            
    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return filtered_data()

    # Add a Plotly Histogram, Seaborn Histogram, and Plotly Scatterplot
    #Plotly Histogram
with ui.layout_columns():
    with ui.card(full_screen=False):
        ui.h2("Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            data = filtered_data() 
            return px.histogram(
                data,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species"
            )

    #Seaborn Histogram
    with ui.card(full_screen=True):
        ui.h2("Seaborn Histogram")

        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            data = filtered_data()
            seaborn_hist = sns.histplot(
                data=data,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )
            seaborn_hist.set_title("Seaborn Histogram")
            seaborn_hist.set_ylabel("Count")

    #Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.h2("Plotly Scatterplot")

        @render_plotly
        def plotly_scatterplot():
            data = filtered_data()  
            return px.scatter(
                data,
                title="Plotly Scatterplot",
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
                size_max=8,
            )

@reactive.calc
def filtered_data():
    return penguins_df[
        (penguins_df["species"].isin(input.selected_species_list())) &
        (penguins_df["island"].isin(input.selected_island_list()))]
