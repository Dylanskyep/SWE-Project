import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"

params = st.query_params
if "admin" in params:
    st.session_state.page = "adminlogin"
if "user" in params:
    st.session_state.page = "userlogin"

if st.session_state.page == "welcome":
    st.markdown(
        """
        <style>
       [data-testid="stAppViewContainer"] {
            background-image: 
                linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* black overlay at 50% opacity */
            url('https://regenbrampton.com/wp-content/uploads/2023/08/How-Does-Volunteering-Help-the-Community_-Hero-1536x1008.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Centered overlay */
        .centered-overlay {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 9999;
        }

        /* Fade-in animation */
        @keyframes fadeIn {
            0% { opacity: 0; transform: scale(0.8); }
            100% { opacity: 1; transform: scale(1); }
        }

        /* Big title using a div and !important to override Streamlit */
        .big-title {
            font-family: "Cinzel", serif!important;
            font-weight: 900 !important;
            font-size: 11vh !important;  
            color: white!important;
            text-shadow: 0 8px 25px rgba(255,255,255,0.9) !important;
            margin-bottom: 2rem !important;
            animation: fadeIn 2s ease-out forwards !important;
            line-height: 1 !important;
            white-space: nowrap !important; 
        }

        /* Button row */
        .btn-row {
            display: inline-flex;
            gap: 1rem;
            justify-content: center;
            align-items: center;
        }

        .iv-btn {
            display: inline-block;
            font-family: "Cinzel", serif!important;
            padding: 16px 32px;
            min-width: 240px;
            font-size: 1.2rem;
            font-weight: 700;
            text-decoration: none;
            color: rgb(95, 107, 99)!important;
            background: linear-gradient(135deg,rgb(163, 183, 167),rgb(247, 247, 247));
            border-radius: 10px;
            box-shadow: 0 6px 18px rgba(70, 89, 79, 0.25);
            transition: transform .15s ease, box-shadow .15s ease;

        }
        .iv-btn:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 10px 24px rgba(177, 183, 193, 0.32); 
        }
        .iv-btn.secondary { 
            background: linear-gradient(135deg,rgb(163, 183, 167),rgb(239, 234, 234)); 
        }

        header, #MainMenu, footer {visibility: hidden;}
        </style>

        <div class="centered-overlay">
            <div class="big-title">Welcome to iVolunteer</div>
            <div class="btn-row">
                <a class="iv-btn" href="?admin=1">Admin Login</a>
                <a class="iv-btn secondary" href="?user=1">User Login</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
