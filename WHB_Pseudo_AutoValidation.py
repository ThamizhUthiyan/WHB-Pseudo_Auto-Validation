# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 00:09:06 2024

@author: uth2001
"""

import WHB_Pseudo_Auto_Validation

import streamlit as st

PAGES = {
    "WHB_Pseudo_Auto_Validation": WHB_Pseudo_Auto_Validation,

}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
