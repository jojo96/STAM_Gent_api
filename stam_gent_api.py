import streamlit as st
import json

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('stam_n.png') 

st.title('STAM Gent API')

st.subheader('Click to search by object id')

with open('data.json', 'r', encoding="utf8") as j:
     contents = json.loads(j.read())
     
query_object = st.text_input('Enter the object id:')

#query = '00759'
if st.button('Search by Object ID'):
    for i in range(len(contents)):
        if contents[i]['Objectnummer'] == query_object:
            st.write(contents[i])


# Function to search objects by keyword
def search_by_keyword(query):
    results = []
    for i in range(len(contents)):
        for key, value in contents[i].items():
            if query.lower() in str(value).lower():
                results.append(contents[i])
                break
    return results

# Function to search objects by century
def search_by_century(query):
    results = []
    for i in range(len(contents)):
        if 'Datering' in contents[i].keys() and query in contents[i]['Datering']:
            results.append(contents[i])
    return results

def search_by_artist(query):
    results = []
    for i in range(len(contents)):
        if ('Vervaardiger' in contents[i].keys() and query in contents[i]['Vervaardiger']):
            results.append(contents[i]['Objectnummer'])
    return results


st.subheader('Search objects by materials or techniques:')    

materials = list(set([obj['Materiaal'] for obj in contents if 'Materiaal' in obj.keys()]))
techniques = list(set([obj['Techniek'] for obj in contents if 'Techniek' in obj.keys()]))

query_material = st.selectbox('Select material:', ['', *materials])
query_technique = st.selectbox('Select technique:', ['', *techniques])

if st.button('Get Objects by Material or Technique'):
    obj_ids = []
    
    for i in range(len(contents)):
        if ('Materiaal' in contents[i].keys() and query_material in contents[i]['Materiaal']) or ('Techniek' in contents[i].keys() and query_technique in contents[i]['Techniek']):
            obj_ids.append(contents[i]['Objectnummer'])
                    
    st.write(obj_ids)

# Sidebar for searching by keyword or century
sidebar_option = st.sidebar.radio('Search objects by', ('Keyword', 'Century', 'Artist'))

if sidebar_option == 'Keyword':
    query = st.sidebar.text_input('Enter keyword to search')
    if st.sidebar.button('Search'):
        results = search_by_keyword(query)
        if len(results) > 0:
            st.header(f"Showing {len(results)} results for '{query}':")
            for result in results:
                st.write(result)
        else:
            st.write(f"No results found for '{query}'")
elif sidebar_option == 'Century':
    query = st.sidebar.text_input('Enter century to search')
    if st.sidebar.button('Search'):
        results = search_by_century(query)
        if len(results) > 0:
            st.header(f"Showing {len(results)} results for objects from {query} century:")
            for result in results:
                st.write(result)
        else:
            st.write(f"No results found for objects from {query} century")
elif sidebar_option == 'Artist':
    query = st.sidebar.text_input('Enter artist to search')
    if st.sidebar.button('Search'):
        results = search_by_artist(query)
        if len(results) > 0:
            st.header(f"Showing {len(results)} results for objects by {query}:")
            for result in results:
                st.write(result)
        else:
            st.write(f"No results found for objects by {query}")
