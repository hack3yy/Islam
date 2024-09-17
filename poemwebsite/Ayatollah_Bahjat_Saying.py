import streamlit as st
import auth  # Import your custom authentication module

####### SETTINGS ######
page_title = "Ayatollah Bahjat"
page_icon = ":books:"

# Ensure this is the first Streamlit command
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

def handle_authentication():
    # Initialize session state if not present
    if 'username' not in st.session_state:
        st.session_state.username = None
        st.session_state.login_status = 'logged_out'
        st.session_state.favorites = []
    
    # Handle login and signup if the user is not logged in
    if st.session_state.username is None:
        st.sidebar.header('Authentication')
        choice = st.sidebar.radio("Choose", ["Login", "Signup"], key="auth_choice_radio_unique")

        username = st.sidebar.text_input("Username", key="username_input")
        password = st.sidebar.text_input("Password", type="password", key="password_input")
        
        if choice == "Login":
            if st.sidebar.button("Login"):
                if not username or not password:
                    st.error("Username and password cannot be empty.")
                elif auth.login(username, password):
                    st.session_state.username = username
                    st.session_state.favorites = auth.load_favorites(username)  # Load favorites
                    st.session_state.login_status = 'logged_in'
                    st.sidebar.write(f"Logged in as: {username}")
                else:
                    st.error("Invalid username or password")
        
        elif choice == "Signup":
            if st.sidebar.button("Signup"):
                if not username or not password:
                    st.error("Username and password cannot be empty.")
                elif auth.signup(username, password):
                    st.success("Signup successful! Please log in.")
                else:
                    st.error("Username already exists")
    else:
        # User is logged in
        st.sidebar.header(f'Welcome, {st.session_state.username}')
        if st.sidebar.button("Logout"):
            # Save favorites before logout
            auth.save_favorites(st.session_state.username, st.session_state.favorites)
            st.session_state.username = None
            st.session_state.favorites = []
            st.session_state.login_status = 'logged_out'
            st.sidebar.write("Logged out.")

# Run the authentication handler
handle_authentication()

# Title for the page
st.title("Ayatollah Bahjat Saying")

# Display an image at the top
image_path = 'images.jpeg'  # Replace with the path to your image
st.image(image_path, width=500)


# Initialize session state for favorites if logged in
if st.session_state.username:
    if 'favorites' not in st.session_state:
        st.session_state.favorites = auth.load_favorites(st.session_state.username)
else:
    # Initialize empty favorites if not logged in
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

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
                if line.isupper() and not (line.startswith('Q:') or line.startswith('A:')):
                    if current_theme:
                        quotes_dict[current_theme] = '\n'.join(current_quote)

                    current_theme = line
                    if current_theme not in themes:
                        themes.append(current_theme)

                    current_quote = []
                else:
                    current_quote.append(line)

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

# Add a placeholder option
placeholder = "SEARCH THEME"

# Select box for quote themes
selected_theme = st.selectbox(
    label="Select a theme: ",
    options=[placeholder] + themes,  # Add placeholder to the list of options
    index=0  # Set the default index to 0, which is the placeholder
)

# Display the selected theme's quotes
if selected_theme != placeholder:
    quotes_content = quotes_dict.get(selected_theme, "")
    st.info(f'**{selected_theme}**\n\n{quotes_content}')
    
    if st.session_state.username:
        # Show Save to Favorites button if user is logged in
        if st.button("Save to Favorites"):
            if selected_theme not in st.session_state.favorites:
                st.session_state.favorites.append(selected_theme)
                # Save to file
                auth.save_favorites(st.session_state.username, st.session_state.favorites)
                st.success("Added to favorites!")
            else:
                st.warning("Already in favorites!")
    else:
        st.warning("Log in to save to favorites.")
else:
    st.write("Please select a theme from the dropdown.")

# Display user's favorites if logged in
if st.session_state.username:
    st.sidebar.subheader("Your Favorites:")
    if st.session_state.favorites:
        for theme in st.session_state.favorites:
            st.sidebar.write(f"- {theme}")
    else:
        st.sidebar.write("No favorites saved yet.")
else:
    st.sidebar.write("Log in to see your saved favorites.")


# Horizontal line for visual separation
st.markdown("---")

# Section: Books by Author
st.header("Books by Ayatollah Bahjat")

books_image_path = 'bahjatbook.jpg'  # Replace with the path to your books image
st.image(books_image_path, width=500)



# Define book options and their links
books = {
    "Uswat Al-Aarifeen": "https://islamicmobility.com/pdf/Uswat%20Al-Aarifeen%20Life%20of%20Ayatullah%20Bahjat.pdf"
}

# Create a selectbox for books
selected_book = st.selectbox("Select a book:", list(books.keys()))

# Display the link for the selected book
if selected_book:
    book_url = books[selected_book]
    st.write(f"You can find more about **{selected_book}** [here]({book_url}).")

st.markdown(
    """
    <style>
    .nav-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        color: #ffffff;
        background-color: #FFFFFF;
        border-radius: 5px;
        text-align: center;
        text-decoration: none;
    }
    .nav-button:hover {
        background-color: rgb(240, 242, 246);
    }
    </style>
    <a class="nav-button" href="/Imam_Khomeini_Poems">Go to Imam Khomeini Poems</a>
    """,
    unsafe_allow_html=True
)
