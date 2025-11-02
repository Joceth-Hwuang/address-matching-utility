#!/usr/bin/env python
# coding: utf-8

# In[1]:


from rapidfuzz import fuzz
from sentence_transformers import SentenceTransformer, util
import streamlit as st
import pandas as pd
import re
from io import BytesIO
import os


# In[2]:


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
        cls.footer()
    
    @classmethod    
    def headings(cls):    
        st.title("Address Matching with SBERT-LaBSE")
        st.divider()
        st.write("Please upload your excel workbook in this format")
        st.write("Column A = Address Unique ID. This helps you identify the address (i.e. index)")
        st.write("Column B = Name as 'Native'. This is the source address, non-English")
        st.write("Column C = Name as 'English'. This is the target address, English")
        st.divider()

    @classmethod
    def upload_widget(cls):
        cls.uploaded_file.append(
        st.file_uploader("Upload an Excel Workbook", type=["xlsx", "xls"])
        )
    
    @classmethod    
    def footer(cls):    
        st.divider()
        st.write("Murdoch MSc. IT TSA2025 ICT619 Project Assignment")
        st.write("Group1 Student IDs: 35370919, 35427755, 35059342")
        


# In[3]:


class Backend:

    @classmethod
    def execute_app(cls):
        df = cls.read_data()
        df['SBERT_Score(%)'] = cls.sbertProcessing(df)
        df['SBERT_Score(%)'] = df['SBERT_Score(%)']*100
        
        sbertNonMatch_df = df.loc[df['SBERT_Score(%)'] < 80].copy()
        sbertMatch_df = df.loc[df['SBERT_Score(%)'] >= 80].copy()
        
#         df['NormalizedNative'] = df['Native'].map(normalizeNumbers)
        sbertMatch_df['NativeNumbers'] = sbertMatch_df['Native'].map(cls.normalizeNumbers).map(cls.extractNumbers)
        sbertMatch_df['EnglishNumbers'] = sbertMatch_df['English'].map(cls.extractNumbers)
        sbertMatch_df['NumbersFuzzy_Score(%)'] = cls.fuzzyProcessing(sbertMatch_df)
        
        fuzzyNonMatch_df = sbertMatch_df.loc[sbertMatch_df['NumbersFuzzy_Score(%)'] < 80].copy()
        matchedAddresses_df = sbertMatch_df.loc[sbertMatch_df['NumbersFuzzy_Score(%)'] >= 80].copy()
        
        st.download_button(
            label='Click Here to get output',
            data = cls.output(
                NoMatchSBERT=sbertNonMatch_df,
                NoMatchFuzzy=fuzzyNonMatch_df,
                MatchedAddresses=matchedAddresses_df
            ),
            file_name="output.xlsx"
        )
    
    @classmethod
    def execute(cls):
        df = cls.read_data(applicationRun=False)
        df['SBERT_Score(%)'] = cls.sbertProcessing(df)
        df['SBERT_Score(%)'] = df['SBERT_Score(%)']*100
        sbertNonMatch_df = df.loc[df['SBERT_Score(%)'] < 80].copy()
        sbertMatch_df = df.loc[df['SBERT_Score(%)'] >= 80].copy()
        
#         df['NormalizedNative'] = df['Native'].map(normalizeNumbers)
        sbertMatch_df['NativeNumbers'] = sbertMatch_df['Native'].map(cls.normalizeNumbers).map(cls.extractNumbers)
        sbertMatch_df['EnglishNumbers'] = sbertMatch_df['English'].map(cls.extractNumbers)
        sbertMatch_df['NumbersFuzzy_Score(%)'] = cls.fuzzyProcessing(sbertMatch_df)
        
        fuzzyNonMatch_df = sbertMatch_df.loc[sbertMatch_df['NumbersFuzzy_Score(%)'] < 80].copy()
        matchedAddresses_df = sbertMatch_df.loc[sbertMatch_df['NumbersFuzzy_Score(%)'] >= 80].copy()
        cls.output(applicationRun=False,
            NoMatchSBERT=sbertNonMatch_df,
            NoMatchFuzzy=fuzzyNonMatch_df,
            MatchedAddresses=matchedAddresses_df
        )
    
    @classmethod
    def read_data(cls, applicationRun=True):
        if applicationRun:
            if not AppUserInterface.uploaded_file:
                st.warning("No file uploaded yet.")
                return None
            uploaded_file = AppUserInterface.uploaded_file[0]
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file)
        else:
            path = f"{os.getcwd()}\\address_data_test.xlsx"
            df = pd.read_excel(path) # reads default file from github repo
        return df
    
    @classmethod
    def normalizeNumbers(cls, addr_str):   
        
        numbers_table = str.maketrans(
            {
                "０": "0", 
                "１": "1", 
                "２": "2", 
                "３": "3", 
                "４": "4",
                "５": "5", 
                "６": "6", 
                "７": "7", 
                "８": "8", 
                "９": "9"
            }
        )
        
        return re.sub(r"[‐-‒–—―－ー]", "-", addr_str.translate(numbers_table))
        
    @classmethod
    def extractNumbers(cls, addr_str):
        pattern = r"\d+(?:-\d+)*"
        if not addr_str:
            return ""
        return re.findall(pattern, addr_str)
    

    @classmethod
    def sbertProcessing(cls, df):    
        model = SentenceTransformer('sentence-transformers/LaBSE')
        emb_native = model.encode(df['Native'].tolist(), convert_to_tensor=True)
        emb_english = model.encode(df['English'].tolist(), convert_to_tensor=True)
        #diagonal returns pairwise, cpu activates cpu processing as pandas can't process with gpu, numpy returns array
        return util.cos_sim(emb_native, emb_english).diagonal().cpu().numpy()
    
    @classmethod
    def fuzzyProcessing(cls, df):        
        return df.apply(
            lambda row: fuzz.token_sort_ratio(
                " ".join(sorted(row['NativeNumbers'])), 
                " ".join(sorted(row['EnglishNumbers']))
            ),axis=1
        )

    @classmethod
    def output(cls, applicationRun=True, **dataframes):
        if applicationRun:
            tempOutput = BytesIO()
            for name, df in dataframes.items():
                df.to_excel(tempOutput, sheet_name=name[:31], index=False)
            tempOutput.seek(0)
            return tempOutput
        else:
            path = f"{os.getcwd()}\\output.xlsx"
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                for name, df in dataframes.items():
                    df.to_excel(writer, sheet_name=name[:31], index=False)
    
    


# In[ ]:


AppUserInterface.execute()
if AppUserInterface.uploaded_file:
    Backend.execute_app()


# In[5]:


#for executing locally without the UI
# Backend.execute()

