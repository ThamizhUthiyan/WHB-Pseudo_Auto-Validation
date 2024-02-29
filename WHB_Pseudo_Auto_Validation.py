# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 23:41:04 2024

@author: uth2001
"""

import pandas as pd
import streamlit as st
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def app():
    st.title('WHB_Pseudo - Auto Validation')
    a = st.file_uploader("Upload IDE File")

    b = st.file_uploader("Upload Pseudo allocation file")

    if a and b is not None:
        df1 = pd.read_csv(a)
        df2 = pd.read_excel(b)

        def compare_rows(row1, row2):
            changes = {}
            for col in df1.columns:
                if col != 'Item Code' and row1[col] != row2[col]:
                    if pd.isna(row1[col]) and pd.isna(row2[col]):
                        changes[col] = ""
                    else:
                        changes[col] = f"{row1[col]} changed to {row2[col]}"
            return changes

        # Function to find changes between GIC and NEW Pseudo GIC and return a dataframe
        def find_changes(row):
            gic = row['GIC']
            new_pseudo_gic = row['NEW PSEUDO GIC']

            gic_row = df1[df1['Item Code'] == gic].iloc[0]
            new_pseudo_gic_row = df1[df1['Item Code']
                                     == new_pseudo_gic].iloc[0]

            changes = compare_rows(gic_row, new_pseudo_gic_row)
            return pd.Series(changes)

        # Apply the function row-wise to df2
        changes_df = df2.apply(find_changes, axis=1)

        # Concatenate the changes dataframe with df2
        output_df = pd.concat([df2, changes_df], axis=1)
        output_df['QC Status'] = output_df['QC Status'].astype(str)
        st.dataframe(output_df)

        def convert_df(df):
            return df.to_csv().encode('utf-8')
        df_f = convert_df(output_df)
        st.download_button(
            label="Download Output file",
            data=df_f,
            file_name='WHB_Pseudo Auto Validation file.csv', mime='text/csv'
        )
