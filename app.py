from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import speech_recognition as sr
import os
import sqlite3

import google.generativeai as genai

## Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


## Fucntion To retrieve query from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    You only have the permission to select the data and you cannot edit, add or delete any information into the database!
    The SQL database has the name Chinook and has the following 
    The Chinook database has 11 tables as follows:
 employees table stores employee data such as id, last name, first name, etc. It also has a field named ReportsTo to specify who reports to whom.
 customers table stores customer data.
 invoices & invoice_items tables: these two tables store invoice data. The invoices table stores invoice header data and the invoice_items table stores the invoice line items data.
 artists table stores artist data. It is a simple table that contains the id and name.
 albums table stores data about a list of tracks. Each album belongs to one artist. However, one artist may have multiple albums.
 media_types table stores media types such as MPEG audio and AAC audio files.
 genres table stores music types such as rock, jazz, metal, etc.
 tracks table stores the data of songs. Each track belongs to one album.
 playlists & playlist_track tables: playlists table stores data about playlists. Each playlist contains a list of tracks. Each track may belong to multiple playlists. The relationship between the playlists and tracks tables is many-to-many. The playlist_track table is used to reflect this relationship.
    also the sql code should not have ``` in beginning or end and sql word in output

    """
    
]


# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")
voice = st.button("Give voice command")
listener = sr.Recognizer()

def speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio input
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        global text
        text = recognizer.recognize_google(audio)

        print("You said:", text)
        response=get_gemini_response(text,prompt)
        print(response)
        st.subheader(response)
        if "UPDATE" not in response:
            response=read_sql_query(response,"chinook.db")
            st.subheader("The Response is")
            for row in response:
                print(row)
                st.header(row)
         
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        
    except sqlite3.OperationalError as e:
        st.header(e)

    except sr.RequestError as e:
        print("Sorry, an error occurred while processing your request:", e) 

if voice:
    speech_to_text()

# if voice:
# print("hello")
# with sr.Microphone() as source:
#             print('listening...')
#             voice = listener.listen(source)
#             command = listener.recognize_google(voice)
#             print(command)
            # question = command
            # response=get_gemini_response(question,prompt)
            # print(response)
            # response=read_sql_query(response,"chinook.db")
            # st.subheader("The Response is")
            # for row in response:
            #   print(row)
            #   st.header(row)

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"chinook.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)