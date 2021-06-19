#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import pandas as pd
import plotly.express as px

class Figures:
    data_table = None

    def __init__(self, logger, data):
        self.logger = logger
        self.data_path = data

    def load_data(self):
        self.data_table = pd.read_csv(self.data_path, sep=',')

    def annotate_data(self):
        # Make new perctenage alignment columns
        self.data_table['target_alignment_rate'] = self.data_table.loc[:, ('bt2_total_aligned_target')] / self.data_table.loc[:, ('bt2_total_reads_target')] * 100
        self.data_table['spikein_alignment_rate'] = self.data_table.loc[:, ('bt2_total_aligned_spikein')] / self.data_table.loc[:, ('bt2_total_reads_spikein')] * 100
        # self.data_table.describe()
        # print(self.data_table)
        # self.data_table.info()

    def generate_dash_plots(self):
        # Init
        plots = dict()

        # Get Data
        self.load_data()
        self.annotate_data()

        # Plot 1
        plot1, data1 = self.alignment_summary_ex()
        plots["alignment_summary"] = plot1

        return (plots, data)

    def gen_plots_to_folder(self, output_path):
        # Init
        sb.set_theme()
        abs_path = os.path.abspath(output_path)

        # Get plots and supporting data tables
        plots, data = self.generate_dash_plots()

        # Save data to output folder
        for key in data:
            data[key].to_csv(os.path.join(abs_path, key + '.csv'), index=False)
            plots[key].savefig(os.path.join(abs_path, key + '.png'))

    ##### PLOTS #####

    def alignment_summary_ex(self):
        # Subset data 
        df_data = self.data_table.loc[:, ('id', 'group', 'bt2_total_reads_target', 'bt2_total_aligned_target', 'target_alignment_rate', 'spikein_alignment_rate')]

        fig = px.box(df_data, x="group", y="bt2_total_reads_target")

        return fig, df_data