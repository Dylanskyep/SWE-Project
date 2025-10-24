import streamlit as st
from utils import auth as auth_utils

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state.page = "welcome"

params = st.query_params
if "admin" in params:
    st.session_state.page = "adminlogin"
if "user" in params:
    st.session_state.page = "userlogin"
if "page" in params:
    page = params["page"]
    if page == "user_dashboard":
        st.switch_page("pages/User_Dashboard.py")
    elif page == "admin_dashboard":
        st.switch_page("pages/Admin_Dashboard.py")

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
    
if st.session_state.page == "userlogin":
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
                color: rgb(138, 156, 140);
                background-color: rgb(244, 247, 246);
                }
        .title {
            font-size: 50px;
            color: rgb(95, 105, 96)!important;
            white-space: nowrap;
            overflow: hidden;
            border-right: 4px solid rgb(75, 82, 76);
            width: 0;
            animation: 
                typing 3s steps(23, end) forwards, 
                blink-fade 0.7s 3s 3 forwards;  
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 17.5ch; }
        }

        @keyframes blink {
            50% { border-color: transparent }
        } 
                
         @keyframes blink-fade {
            0%, 50%, 100% { border-color: rgb(75, 82, 76); } 
            75%, 100% { border-color: transparent; }
        }
                
        </style>
    
        <div class="title">User Login / Sign-Up</div>
    """, unsafe_allow_html=True)
    
    st.set_page_config(layout="wide")
    left, right = st.columns(2)
    with left:
        st.header("Login")
        email = st.text_input("Email", key="user_login_email")
        password = st.text_input("Password", type="password", key="user_login_password")
        if st.button("Login"):
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                user = auth_utils.login_user(email, password, role="volunteer")
                if user:
                    st.success("Login successful!")
                    st.session_state.user_email = email
                    st.session_state.user_password = password
                    st.session_state.userid = "user_id"
                    st.session_state.role = user.get("role", "volunteer")
                if st.session_state.get("role") == "volunteer":
                    st.success("Login successful! Redirecting to Volunteer Dashboard...")
                    st.query_params.update({"page": "user_dashboard"})
                    st.rerun()
                    
    with right:
        st.header("Sign Up")
        name = st.text_input("Name", key="name")
        email = st.text_input("Email", key="user_signup_email")
        password = st.text_input("Password", type="password", key="user_signup_password")
        if st.button("Sign Up"):
            if not email or not password or not name:
                st.error("Please fill in all fields")
            else:
                user, msg = auth_utils.create_volunteer(name, email, password)
                if not user:
                    st.error(msg)
                else:
                    st.success(msg)
            
if st.session_state.page == "adminlogin":
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
                color: rgb(138, 156, 140);
                background-color: rgb(244, 247, 246);
                }
        .title {
            font-size: 50px;
            color: rgb(95, 105, 96)!important;
            white-space: nowrap;
            overflow: hidden;
            border-right: 4px solid rgb(75, 82, 76);
            width: 0;
            animation: 
                typing 3s steps(23, end) forwards, 
                blink-fade 0.7s 3s 3 forwards;  
        }

        @keyframes typing {
            from { width: 0 }
            to { width: 19.5ch; }
        }

        @keyframes blink {
            50% { border-color: transparent }
        } 
                
         @keyframes blink-fade {
            0%, 50%, 100% { border-color: rgb(75, 82, 76); } 
            75%, 100% { border-color: transparent; }
        }
                
        </style>
    
        <div class="title">Admin Login / Sign-Up</div>
    """, unsafe_allow_html=True)
    
    st.set_page_config(layout="wide")
    left, right = st.columns(2)
    with left:
        st.header("Login")
        email = st.text_input("Email", key="admin_login_email")
        password = st.text_input("Password", type="password", key="admin_login_password")
        if st.button("Login"):
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                admin = auth_utils.login_user(email, password, role="admin")
                if admin:
                    st.success("Login successful!")
                    st.session_state.user_email = email
                    st.session_state.user_password = password
                    st.session_state.userid = "user_id"
                    st.session_state.role = admin.get("role", "admin")
                if st.session_state.get("role") == "admin":
                    st.query_params.update({"page": "admin_dashboard"})
                    st.rerun()

    with right:
        st.header("Sign Up")
        name = st.text_input("Name", key="name")
        email = st.text_input("Email", key="admin_signup_email")
        password = st.text_input("Password", type="password", key="admin_signup_password")
        adminkey = st.text_input("Admin Key", type="password", key="adminkey")
        st.caption("Don't have an admin key? Contact the development team to request one.")
        if st.button("Sign Up"):
            if not email or not password or not name or not adminkey:
                st.error("Please fill in all fields")
            else:
                admin, msg = auth_utils.create_admin(name, email, password, adminkey)
                if not admin:
                    st.error(msg)
                else:
                    st.success(msg)

