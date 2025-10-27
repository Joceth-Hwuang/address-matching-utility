#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from process import say_hello

st.title("My First Streamlit App")
st.write("This app calls a function from another Python file.")
st.divider()

# Call the function from process.py
say_hello()

