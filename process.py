#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util
import streamlit as st
import pandas as pd


# In[ ]:


# streamlit UI display

class AppUserInterface:
    
    uploaded_file = []
    
    @classmethod
    def execute(cls):
        """
        main method
        """
        cls.headings()
        cls.upload_widget()
        while not cls.uploaded_file:
            cls.upload_widget()
    
    @classmethod    
    def headings(cls):    
        st.title("Address Matching with SBERT-LaBSE")
        st.write("Murdoch MSc. IT TSA2025 ICT619 Project Assignment")
        st.write("Group1 Student IDs: 35370919, 35427755, 35059342")
        st.divider()
        st.write("Please upload your excel workbook in this format")
        st.write("Column A = Address Unique ID. This helps you identify the address")
        st.write("Column B = Source Address")
        st.write("Column C = Target Address")
        st.divider()

    @classmethod
    def upload_widget(cls):
        cls.uploaded_file.append(
        st.file_uploader("Upload an Excel Workbook", type=["xlsx", "xls"])
        )
    
    


# In[ ]:

AppUserInterface.execute()


