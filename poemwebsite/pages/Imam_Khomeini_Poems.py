import streamlit as st

####### SETTINGS ######
page_title = "Imam Khomeini Poems"
page_icon = ":book:"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

### HIDE MENU AND FOOTER ###
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

### PAGE CONTENT ###

st.markdown("_<h1 style='text-align: center; color: white;'>Imam Khomeini Poems</h1>_", unsafe_allow_html=True)

# Display an image at the top
image_path = 'khomeini2.jpg'  # Replace with the path to your image
st.image(image_path, width=500)

# Function to read and parse poems from a text file
def load_poems(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content into lines
        lines = content.split('\n')
        
        poems = []
        titles = []
        current_title = None
        current_poem = []
        
        for line in lines:
            line = line.strip()
            if not line:
                # Empty line signifies the end of a poem
                if current_title:
                    poems.append((current_title, '\n'.join(current_poem)))
                    titles.append(current_title)
                current_title = None
                current_poem = []
            elif current_title is None:
                # The first non-empty line is the title
                current_title = line
            else:
                # The rest are part of the poem
                current_poem.append(line)
        
        # Add the last poem if there's no trailing newline
        if current_title:
            poems.append((current_title, '\n'.join(current_poem)))
            titles.append(current_title)
        
        return titles, dict(poems)
    except UnicodeDecodeError:
        st.error("There was an error decoding the file. Please ensure it is encoded in UTF-8.")
        return [], {}
    except FileNotFoundError:
        st.error("The file was not found. Please check the file path.")
        return [], {}

# Load poems
file_path = 'imamkhomeinipoems.txt'  # Replace with the path to your poems file
titles, poems_dict = load_poems(file_path)

# Add a placeholder option
placeholder = "CHOOSE A POEM"

# Select box for poem titles
selected_title = st.selectbox(
    label="List of poem:",
    options=[placeholder] + titles,  # Add placeholder to the list of options
    index=0  # Set the default index to 0, which is the placeholder
)

# Display the selected poem
if selected_title != placeholder:
    poem_content = poems_dict.get(selected_title, "")
    st.info(f'**{selected_title}**\n\n{poem_content}')
else:
    st.write("Please select a poem from the dropdown.")

# Navigation link
st.markdown('<br><a href="/Ayatollah_Bahjat_Saying">Go to Ayatollah Bahjat Quotes</a>', unsafe_allow_html=True)

