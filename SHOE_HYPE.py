import streamlit as st
import os
import pandas as pd
from PIL import Image
import tensorflow
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50,preprocess_input
import numpy as np
from numpy.linalg import norm
import os
import pickle
from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors
import webbrowser
from bokeh.models.widgets import Div
from button_link import *

hide_menu_style ="""
    <style>
    footer{visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html =True)

if "button_clicked" not in st.session_state:
  st.session_state.button_clicked = False
def callback():
  st.session_state.button_clicked = True

st.title('SHOE HYPE〽️')
st.subheader("FOR THE ONE's ADDICTED TO SNEAKERS👟")

col13, col14 = st.columns(2)
with col13:
  st.image("https://i.pinimg.com/originals/1f/f5/94/1ff594ed96063b9db4866efaaa864ef6.gif")
  st.markdown(button_link('https://www.linkedin.com/in/dhruvtyagi15/', 'Get Connected'), unsafe_allow_html=True)
  if st.button('About the Website'):
    st.markdown("It is a **CNN** based Recommendor System which uses **RESNET** for feature extraction. The features of the uploaded image are compared with the help of **Scikit Learn**. Then the images are Recommended and the accompanied data is fetched from the dataset.")

with col14:
      st.image("https://i.pinimg.com/originals/c5/d0/22/c5d0226ce2a6ccb7266f76183712d6f1.gif")  
      st.image('https://upload.wikimedia.org/wikipedia/commons/f/fa/Bally_Ascar_shoe.gif')
      
feature_list = np.array(pickle.load(open('embeddings_shoes.pkl','rb')))
filenames = pickle.load(open('filenames_shoes.pkl','rb'))

model = ResNet50 (weights='imagenet', include_top=False, input_shape=(224, 224,3))
model.trainable = False

model = tensorflow.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

def save_uploaded_file (uploaded_file):
  try:
      with open (os.path.join('uploads', uploaded_file.name),'wb') as f:
        f.write(uploaded_file.getbuffer())
      return 1
  except:
      return 0

def extract_features(img_path, model):
    img = image.load_img(img_path,target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    
    return normalized_result

def recommend(features,feature_list):
  neighbors = NearestNeighbors(n_neighbors=5, algorithm ='brute', metric='euclidean')
  neighbors.fit(feature_list)
  distances, indices = neighbors.kneighbors([features])
  return indices

product = pd.read_csv('dataset_csv.csv')
data = os.listdir("SHOES_IMAGES")

st.subheader("INSTRUCTIONS:")
st.markdown("__FOR BETTER RECOMMENDATIONS UPLOAD THE IMAGES WHICH ONLY HAVE SHOE PRODUCT, ALINGED HORIZONTALLY AND HAVE WHITE BACKGROUND.__")
st.markdown("DOWNLOAD SAMLE IMAGES FROM MY GITHUB")
st.markdown(button_link('https://github.com/Dhruv-0001/Sample-Images.git', 'Download Sample'), unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose an image") 
if uploaded_file is not None:
  if save_uploaded_file(uploaded_file):
    display_image = Image.open(uploaded_file)

    features = extract_features(os.path.join('uploads',uploaded_file.name),model)

    indices=recommend(features,feature_list)
    value = indices.tolist()[0]

    ls=[]
    for i in value:
      ls.append(data[i])
      i=+1
        
    d=[]
    for i in ls:
      try :
        ref=product['REFERENCE'].tolist()
        ind = ref.index(i)
        d.append(product['DESCRIPTION'][ind])
      except :
        d.append('INFORMATION NOT FOUND IN DATABASE')
      i=+1
      
    u=[]
    for i in ls:
      try :
        ref=product['REFERENCE'].tolist()
        ind = ref.index(i)
        u.append(product['PAGE URL'][ind])
      except:
        u.append("INFORMATION NOT FOUND IN DATABASE")
      i=+1
        
    def result_function(ind):
        col1, col2= st.columns(2)
        with col1:
            var=os.path.join('https://m.media-amazon.com/images/I/', list(filenames[indices[0][ind]].split("\\"))[1] )
            st.image(var)
        with col2:
            try :
                desc=(product['DESCRIPTION'][ref.index(ls[ind])]).split(" ")[0:3]
                st.title((' '.join([str(elem) for elem in desc])).upper())
                st.markdown(product['PAGE URL'][ref.index(ls[ind])], unsafe_allow_html=True)
            except :
                st.markdown('ERROR-INFORMATION NOT FOUND IN DATASET')

    col11, col12 = st.columns(2)
    with col11:
      basewidth = 180
      wpercent = (basewidth / float(display_image.size[0]))
      hsize = int((float(display_image.size[1]) * float(wpercent)))
      img1 = display_image.resize((basewidth, hsize), Image.ANTIALIAS)
      st.image(img1)

    with col12:
      st.markdown('**UPLOADED IMAGE**')

    if st.button('SHOW RECOMMENDATIONS'):
  
        tab1, tab2, tab3, tab4, tab5 = st.tabs(['TAB1','TAB2','TAB3','TAB4','TAB5'])

        with tab1:
            result_function(0)
        with tab2:  
            result_function(1)
        with tab3:
            result_function(2)
        with tab4:
            result_function(3)
        with tab5:
            result_function(4)
          
