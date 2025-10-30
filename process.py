#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util
import streamlit as st
import pandas as pd


# In[ ]:


# streamlit

# header
st.title("Address Matching with SBERT-LaBSE")

# header-description
st.write("Murdoch MSc. IT TSA2025 ICT619 Project Assignment")
st.write("Group1 Student IDs: 35370919, 35427755, 35059342")
st.divider()

# file upload
st.write("Please upload your excel workbook in this format")
st.write("Column A = Address Unique ID. This helps you identify the address")
st.write("Column B = Source Address")
st.write("Column C = Target Address")
st.divider()

# file upload widget
file_uploaded = st.file_uploader("Upload an Excel Workbook", type=["xlsx", "xls"])


# In[ ]:


# extract
if file_uploaded:
    read_df = pd.read_excel(file_uploaded)
    st.write("Preview of uploaded data")
    st.dataframe(df.head(5))
else: 
    st.write("File not uploaded")


# open dataframe


# In[ ]:




