import asyncio
import numpy as np
import cv2
import pyautogui
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import json
import time
from threading import Timer

from faicons import icon_svg
from chatlas import ChatAnthropic, content_image_file
from dotenv import load_dotenv
from pathlib import Path


# Import data from shared.py
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

# Get the directory where this script is located
here = Path(__file__).parent

# ChatAnthropic() requires an API key from Anthropic.
_ = load_dotenv()



ui.page_opts(title="visualization dashboard", fillable=True)

# Initialize Shiny chat component

with ui.sidebar(position="right", bg="#f8f8f8"):
    # Use initial settings loaded from file
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

with ui.layout_columns():
   
    with ui.card():
        ui.card_header("plotly plot")
        @render_plotly
        def scatterplot():
            color = "species"
            return px.scatter(
                filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color=None if color == "none" else color,
                trendline="lowess",
            )



@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
