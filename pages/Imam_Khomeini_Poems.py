import streamlit as st
import auth  # Import your custom authentication module

####### SETTINGS ######
page_title = "Imam Khomeini"
page_icon = ":book:"

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
        choice = st.sidebar.radio("Choose an action", ["Login", "Signup"], key="auth_choice_radio_unique")

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
st.title("Imam Khomeini Poems")

# Display an image at the top
image_path = 'khomeini2.jpg'  # Replace with the path to your image
st.image(image_path, width=500)



# Initialize session state for favorites if logged in
if st.session_state.username:
    if 'favorites' not in st.session_state:
        st.session_state.favorites = auth.load_favorites(st.session_state.username)
else:
    # Initialize empty favorites if not logged in
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

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
placeholder = "SEARCH POEM"

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
    
    if st.session_state.username:
        # Show Save to Favorites button if user is logged in
        if st.button("Save to Favorites"):
            if selected_title not in st.session_state.favorites:
                st.session_state.favorites.append(selected_title)
                # Save to file
                auth.save_favorites(st.session_state.username, st.session_state.favorites)
                st.success("Added to favorites!")
            else:
                st.warning("Already in favorites!")
    else:
        st.warning("Log in to save to favorites.")
else:
    st.write("Please select a poem from the dropdown.")

# Display user's favorites if logged in
if st.session_state.username:
    st.sidebar.subheader("Your Favorites:")
    if st.session_state.favorites:
        for title in st.session_state.favorites:
            st.sidebar.write(f"- {title}")
    else:
        st.sidebar.write("No favorites saved yet.")
else:
    st.sidebar.write("Log in to see your saved favorites.")

# Horizontal line for visual separation
st.markdown("---")

# New section: Books and their links
st.header("Books by Imam Khomeini")  # Replace with the title of your choice

# Display the image
books_image_path = 'khomeinibook.jpg'  # Replace with the path to your image
st.image(books_image_path, width=500)

# Define book options and their links
books = {
    "THE ASHURA UPRISING": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/329-TheAshuraUprising(1).pdf",

    "COMPLETE POETICAL WORKS": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2023/Divane_Emam(En).pdf",

    "40 HADITH": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1621-ForthyHadith.pdf",

    "ISLAMIC AWAKENING": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Imam_Khomeini_and_Islamic_Awakening.pdf",
    "THE EMBODIMENT OF ISLAMIC MORALS": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2023/Divane_Emam(En).pdf",

    "REUNION WITH THE BELOVED": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/558-vadehye-didar-English-a4.pdf",

    "HAJJ": "http://en.imam-khomeini.ir/en/c5_3158/Book/English/Hajj-From-The-Viewpoint-Of-Imam-Khomeini-s-",

    "MANIFESTATION OF MONOTHEISM": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2017/2972-tajalli-tohid.pdf",

    "ADAB AS-SALAT: THE DISCIPLINES OF THE PRAYER": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1248-DisciplinesofthePrayer.pdf",

    "THE SECRET OF PRAYER ( SIRR US SALAT)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/EN6-SECRETOFPRAYER.pdf",

    "ISLAM, WEST AND THE HUMAN RIGHTS": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2218-islam-gharb-va-hoghooghe-bahsar-English-a4.pdf",

    "THE NARRATIVE OF AWAKENING": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/536-hadise-bidari-a4.pdf",

    "THE LAST MESSAGE": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/607-LastMessage.pdf",

    "A CALL TO DIVINE UNITY": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/959-avaye-tohid-a4.pdf",

    "THE POSITION OF WOMEN": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1472-POSITIONOFWOMEN.pdf",

    "THE MUSLIM WORLD": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Imam_Khomeini_and_the_Muslim_World.pdf",

    "THE DYNAMIC STAR THAT NEVER SETS": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/49-n.pdf",

    "ISLAMIC SOLIDARITY IN INFRA-NATIONAL": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2276-IslamicSolidarity.pdf",

    "STANDPOINTS": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/487-Standpoints.pdf",

    "THE GREATEST JIHAD ( COMBAT WITH THE SELF)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1587-jahad-akbar-English-a4.pdf",

    "MANIFESTATION OF THE FRIEND": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2521-TnS(AksEmambaKetabYeksanNist).pdf",

    "STUDY OF THE ROOT CAUSES AND PROCESS OF THE ISLAMIC REVOLUTION IN IRAN": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2559-TS.pdf",

    "THE EMIGRANT OF THE FAITH TRIBE": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/EN8-HAJAHMADSBIOGRAPHY.pdf",

    "RELIGION AND POLITICS": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2017/2278-religion-and-politic-a4(0).pdf",

    "RELIGIOUS DEMOCRACY": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Religious-Democracy.pdf",

    "CONCEPT OF FREEDOM": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Concept-of-Freedom.pdf",

    "SHINING TORCH OF THE ISLAMIC REVOLUTION OF IRAN": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Shining_Torch_of_the_Islamic_Revolution_of_Iran.pdf",

    "THE PERSONALITY OF WOMEN": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2392-majmue-maghalate-imam-khomeini-va-shakhsiyyate-zan-a4.pdf",

    "THE ROLE OF WOMEN IN SOCIETY": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/22-n.pdf",

    "THE LAMP OF GUIDANCE INTO VICEGERENCY AND SANCTITY": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2552-Sn-T.pdf",

    "THE WINE OF LOVE": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1588-bade-eshgh-English-a4.pdf",

    "ETHICS AND POLITICS": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1822-imam-akhlagh-siyasat-English-a4.pdf",

    "THE ISLAMIC REVOLUTION": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2384-imam-khomeini-va-enghelabe-islami-English-a4.pdf",

    "TAHRIR-AL-VASILAH(V.1)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/0000-tahrir%20j1-nA4.pdf",

    "TAHRIR-AL-VASILAH(V.2)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/0000-tahrir%20j2-nA4.pdf",

    "TAHRIR-AL-VASILAH(V.3)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/0000-tahrir%20j3-nA4.pdf",

    "TAHRIR-AL-VASILAH(V.4)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/0000-tahrir%20j4-nA4.pdf",

     "ECONOMIC WITH FOCUS ON SOCIAL JUSTICE": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2017/2971-didgahhaye-eghtesadi.pdf",

    "FUNDAMENTALS OF THE ISLAMIC REVOLUTION SELECTIONS FROM THE TOUGHTS AND OPINIONS OF IMAM KHOMEINI": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/277-FundamentalsoftheIslamicRevolution.pdf",

     "ISLAMIC GOVERNMENT: GOVERNANCE OF THE JURIST": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1358-IslamicGovernment.pdf",

    "ON EXPORTATION OF REVOLUTION": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1335-ExportationoftheRevolution.pdf",

     "SPECIAL SUPPLEMENT ON THE OCCATION OF THE 25TH DEPARTURE ANNIVERSARY OF IMAM KHOMEINI": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/web%20vizhe%20rahbari02.pdf",

    "KAUTHAR (VOL.1)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/574-kosare-1-English-a4.pdf",

    "KAUTHAR (VOL.2)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/573-kosar-2-English-a4.pdf",

     "SPIRITUALITY AND POLITICS": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2277-erfan-o-sissat-English-a4.pdf",

    "THE INTERNATIONAL SYSTEM": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/2007-Imam-va-nezame-beinolmelali-gozide-maghalat-k-A4.pdf",

     "BEHAVIOR AND CHARACTER OF THE HOLY PROPHET OF ISLAM": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/EN1-BehaviorCharacteroftheProphet.pdf",

    "LEGITIMACY OF POWER": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1926-LegitimacyofPower.pdf",

     "BIOGRAPHY AND STRUGGLES OF AYATULLAH SAYYID MUSTAFA KHOMEINI": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/EN2-BiogrphyofSayyidMustafaKhomeini.pdf",

    "A SELECTION OF THE WORKS AND CONDUCT OF IMAM KHOMEINI ABOUT THE QURAN": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/EN3-ImamQuran.pdf",

    "THE LIFE OF IMAM KHOMEINI": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1334-TheLifeofImamKhomeini.pdf",

    "SAHIFEH-YE IMAM (VOL.1)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1695-Sahifeh-ye%20Imam-Vol%201.pdf",

    "SAHIFEH-YE IMAM (VOL.2)": "http://staticsml.imam-khomeini.ir/userfiles/en/Files/NewsAttachment/2018/Sahifeh,_Vol.2(0).pdf",

    "SAHIFEH-YE IMAM (VOL.3)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1697-Sahifeh-ye%20Imam-Vol%203(1).pdf",

    "SAHIFEH-YE IMAM (VOL.4)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1698-Sahifeh-ye%20Imam-Vol%204(1).pdf",

    "SAHIFEH-YE IMAM (VOL.5)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1699-Sahifeh-ye%20Imam-Vol%205.pdf",

    "SAHIFEH-YE IMAM (VOL.6)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1700-Sahifeh-ye%20Imam-Vol%206.pdf",

    "SAHIFEH-YE IMAM (VOL.7)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1701-Sahifeh-ye%20Imam-Vol%207.pdf",

    "SAHIFEH-YE IMAM (VOL.8)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1702-Sahifeh-ye%20Imam-Vol%208%20.pdf",

    "SAHIFEH-YE IMAM (VOL.9)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1703-Sahifeh-ye%20Imam-Vol%209(1).pdf",

    "SAHIFEH-YE IMAM (VOL.10)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1704-Sahifeh-ye%20Imam-Vol%2010.pdf",

    "SAHIFEH-YE IMAM (VOL.11)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1705-Sahifeh-ye%20Imam-Vol%2011.pdf",

    "SAHIFEH-YE IMAM (VOL.12)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1706-Sahifeh-ye%20Imam-Vol%2012(1).pdf",

    "SAHIFEH-YE IMAM (VOL.13)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1707-Sahifeh-ye%20Imam-Vol%2013.pdf",

    "SAHIFEH-YE IMAM (VOL.14)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1708-Sahifeh-ye%20Imam-Vol%2014.pdf",

    "SAHIFEH-YE IMAM (VOL.15)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1709-Sahifeh-ye%20Imam-Vol%2015.pdf",

    "SAHIFEH-YE IMAM (VOL.16)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1710-Sahifeh-ye%20Imam-Vol%2016.pdf",

    "SAHIFEH-YE IMAM (VOL.17)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1711-Sahifeh-ye%20Imam-Vol%2017.pdf",

    "SAHIFEH-YE IMAM (VOL.18)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1712-Sahifeh-ye%20Imam-Vol%2018.pdf",

    "SAHIFEH-YE IMAM (VOL.19)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1713-Sahifeh-ye%20Imam-Vol%2019.pdf",

    "SAHIFEH-YE IMAM (VOL.20)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1714-Sahifeh-ye%20Imam-Vol%2020.pdf",

    "SAHIFEH-YE IMAM (VOL.21)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1715-Sahifeh-ye%20Imam-Vol%2021.pdf",

    "SAHIFEH-YE IMAM (VOL.22)": "http://staticsml.imam-khomeini.ir/en/File/NewsAttachment/2014/1716-Sahifeh-ye%20Imam-Vol%2022-a4.pdf"
}

# Create a selectbox for books
selected_book = st.selectbox("Select a book:", list(books.keys()))

# Display the link for the selected book
if selected_book:
    book_url = books[selected_book]
    st.write(f"You can read the book **{selected_book}** [here]({book_url}).")

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
    <a class="nav-button" href="/Ayatollah_Bahjat_Saying">Go to Ayatollah Bahjat Saying</a>
    """,
    unsafe_allow_html=True
)
