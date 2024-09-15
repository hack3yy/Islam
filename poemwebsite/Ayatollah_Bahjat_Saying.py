import streamlit as st

####### SETTINGS ######
page_title = "Ayatollah Bahjat Quotes"
page_icon = ":books:"

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
st.markdown("_<h1 style='text-align: center; color: white;'>Ayatollah Bahjat Quotes</h1>_", unsafe_allow_html=True)

# Display an image at the top
image_path = 'images.jpeg'  # Replace with the path to your image
st.image(image_path, width=500)

# Function to read and parse quotes from a text file
def load_quotes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        lines = content.split('\n')

        themes = []
        quotes_dict = {}
        current_theme = None
        current_quote = []

        for line in lines:
            line = line.strip()
            if line:
                # Check if line is a theme
                if line.isupper() and not (line.startswith('Q:') or line.startswith('A:')):
                    # Save the previous theme's quotes if there is one
                    if current_theme:
                        quotes_dict[current_theme] = '\n'.join(current_quote)
                    
                    # Start a new theme
                    current_theme = line
                    if current_theme not in themes:
                        themes.append(current_theme)
                    
                    # Prepare for new quotes
                    current_quote = []
                else:
                    # Collect quotes for the current theme
                    current_quote.append(line)

        # Add the last theme's quotes if there's no trailing newline
        if current_theme:
            quotes_dict[current_theme] = '\n'.join(current_quote)

        return themes, quotes_dict
    except UnicodeDecodeError:
        st.error("There was an error decoding the file. Please ensure it is encoded in UTF-8.")
        return [], {}
    except FileNotFoundError:
        st.error("The file was not found. Please check the file path.")
        return [], {}

# Load quotes
file_path = 'Ayatbahjatquotes.txt'  # Replace with the path to your quotes file
themes, quotes_dict = load_quotes(file_path)

# Select box for quote themes
selected_theme = st.selectbox('Select a theme:', options=[' CHOOSE THEME '] + themes)

# Display the selected theme's quotes
if selected_theme and selected_theme != ' CHOOSE THEME ':
    quotes_content = quotes_dict.get(selected_theme, "")
    st.info(f'**{selected_theme}**\n\n{quotes_content}')

# Navigation link
st.markdown('<br><a href="/Imam_Khomeini_Poems">Go to Imam Khomeini Poems</a>', unsafe_allow_html=True)
