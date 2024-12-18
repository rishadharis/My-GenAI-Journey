import streamlit as st
import time
from sarkas import get_data

### Main function to run the app ######
def main():
    st.set_page_config(
        page_title="BustoSarkas",
    )
    # Set page title
    st.title(f"Busto Sarkas (LinkedIn) LLM App")
    st.markdown("""
                <code>
                Mohon untuk memberikan nama dengan tambahan informasi untuk memperkuat akurasi pencarian akun (contoh: Robert Downey Microsoft)
                </code>
                <code>
                Jika akun tidak ditemukan atau akun yang ditampilkan salah, silahkan masukan url profile linkedin secara langsung
                >> Created By: Rishad Harisdias Bustomi <<
                </code>
                """, unsafe_allow_html=True)
    
    # Create search input with specific styling
    search_query = st.text_input("Cari Nama Mu", "")
    
    # Create columns for search button alignment with specific ratio
    col1, col2, col3 = st.columns([6, 2, 1])
    with col3:
        search_button = st.button("Cari")
    
    # Initialize session state for result
    if 'search_result' not in st.session_state:
        st.session_state.search_result = None
        
    # Create placeholder for results
    result_placeholder = st.empty()
    
    if search_button:
        with result_placeholder:
            with st.spinner('Sedang mencari...'):
                try:
                    data = get_data(search_query)
                except Exception as e:
                    data = {
                        "full_name": "Data Tidak Ditemukan",
                        "occupation": "---",
                        "profile_picture": "https://via.placeholder.com/150",
                        "sarkas": "Data linkedin tidak ditemukan. Consider menggunakan URL profile linkedin secara langsung."
                    }
                st.session_state.search_result = {
                    "image_url": data["profile_picture"],
                    "name": data["full_name"],
                    "position": data["occupation"],
                    "description": data["sarkas"]
                }
    
    # Display result if exists
    if st.session_state.search_result:
        with result_placeholder:
            st.write("")  # Add some spacing
            st.markdown("""
                <div style="text-align: center; padding: 20px;">
                    <img src="{}"
                         style="width: 150px; height: 150px; border-radius: 50%; 
                                border: 2px solid #0A66C2; background-color: white;">
                    <div style="margin-top: 20px;">
                        <h2>{}</h2>
                        <h3>{}</h3>
                        <p>{}</p>
                    </div>
                </div>
            """.format(
                st.session_state.search_result["image_url"],
                st.session_state.search_result["name"],
                st.session_state.search_result["position"],
                st.session_state.search_result["description"]
            ), unsafe_allow_html=True)

    # Custom styling
    st.markdown("""
        <style>
        /* Page styling */
        .stApp {
            background-color: #f3f2ef;
        }
        
        /* Input field styling */
        .stTextInput input {
            border-radius: 35px;
            border: 1px solid #e0e0e0;
            padding: 10px 20px;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #0A66C2;
            color: white;
            border-radius: 35px;
            padding: 10px 20px;
            border: none;
            width: 100%;
        }
        
        /* Text styling */
        h2 {
            font-size: 24px;
            font-weight: 600;
            margin: 0;
            padding: 0;
        }
        p {
            font-size: 16px;
            color: #666;
            margin: 5px 0 0 0;
        }
        .stButton p {
            color:white;        
        }
        code {
        white-space : pre-wrap !important;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()