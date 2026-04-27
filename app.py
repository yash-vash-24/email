# ========================================================
# INTELLIGENT EMAIL ASSISTANT - STREAMLIT APP
# ========================================================
# Student: Yash Vashisth
# Roll Number: 2301730149
# ========================================================

import streamlit as st
from email_processor import analyze_email
from email_connector import SimpleEmailConnector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Email Assistant",
    page_icon="📧",
    layout="wide"
)

# Header with student info
st.markdown("""
<style>
    .header {
        background-color: #2c3e50;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .student-info {
        font-size: 18px;
        font-weight: bold;
        color: #3498db;
    }
    .roll-number {
        font-size: 16px;
        color: #ecf0f1;
    }
</style>
""", unsafe_allow_html=True)

# Display header
st.markdown("""
<div class="header">
    <h1>📧 Intelligent Email Assistant</h1>
    <p class="student-info">Created by: Yash Vashisth</p>
    <p class="roll-number">Roll Number: 2301730158</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for information
with st.sidebar:
    st.markdown("## 📋 About")
    st.write("""
    This intelligent assistant helps you:
    - ✉️ Generate professional email replies
    - 📂 Categorize emails automatically
    - ⚡ Save time on email management
    """)
    st.markdown("---")
    st.markdown("### 🔧 Technology Stack")
    st.write("""
    - **Python**: Programming Language
    - **Transformers**: NLP Models
    - **Streamlit**: UI Framework
    - **Hugging Face**: AI Models
    """)

# Main content
st.header("Email Assistant Tool")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📧 Draft Reply", "📂 Categorize", "🔗 Connect Email", "📚 Tutorial"])

with tab1:
    st.subheader("Generate Reply to Email")

    email_input = st.text_area(
        "Enter the email content you want to reply to:",
        placeholder="Paste your email here...",
        height=150
    )

    if st.button("🚀 Generate Reply", use_container_width=True):
        if email_input.strip():
            with st.spinner("Generating reply..."):
                result = analyze_email(email_input)

                # Display results
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Original Email")
                    st.info(result["original_email"])

                with col2:
                    st.subheader("Generated Reply")
                    st.success(result["generated_reply"])

                # Display category and timestamp
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f"**Category:** `{result['category']}`")
                with col4:
                    st.markdown(f"**Generated at:** `{result['timestamp']}`")
        else:
            st.warning("Please enter an email content")

with tab2:
    st.subheader("Email Categorization")

    categorize_input = st.text_area(
        "Enter email to categorize:",
        placeholder="Paste your email here...",
        height=150,
        key="categorize"
    )

    if st.button("📂 Categorize Email", use_container_width=True):
        if categorize_input.strip():
            result = analyze_email(categorize_input)

            st.markdown("### Categorization Result")

            # Display category with emoji
            category = result["category"]
            category_icons = {
                "Meeting": "📅",
                "Finance": "💰",
                "Project": "📊",
                "Resume/Job": "💼",
                "Important": "⚠️",
                "Support": "🆘",
                "General": "📬"
            }

            icon = category_icons.get(category, "📬")
            st.metric(label="Email Category", value=f"{icon} {category}")

            with st.expander("View Generated Reply"):
                st.write(result["generated_reply"])
        else:
            st.warning("Please enter an email content")

with tab3:
    st.subheader("📧 Gmail Inbox")
    
    # Get credentials from .env
    email_address = os.getenv("EMAIL_ADDRESS", "")
    password = os.getenv("EMAIL_PASSWORD", "")
    
    if not email_address or not password:
        st.error("""
        ❌ **Gmail credentials not configured**
        
        **Setup Instructions:**
        1. Copy `.env.example` to `.env`
        2. Add your Gmail address to `EMAIL_ADDRESS`
        3. Add your [App Password](https://myaccount.google.com/apppasswords) to `EMAIL_PASSWORD`
        4. Reload this page
        """)
    else:
        # Auto-connect on first load
        if 'gmail_connected' not in st.session_state:
            try:
                with st.spinner("Connecting to Gmail..."):
                    connector = SimpleEmailConnector(email_address, password, 'gmail')
                    emails = connector.get_emails(10)
                    
                    st.session_state.connector = connector
                    st.session_state.emails = emails
                    st.session_state.gmail_connected = True
            except Exception as e:
                st.error(f"❌ Failed to connect: {str(e)}")
                st.session_state.gmail_connected = False
        
        # Display emails if connected
        if st.session_state.get('gmail_connected') and st.session_state.get('emails'):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"### 📥 Inbox ({len(st.session_state.emails)})")
            
            with col2:
                if st.button("🔄 Refresh", use_container_width=True, key="refresh_btn"):
                    with st.spinner("Refreshing..."):
                        st.session_state.emails = st.session_state.connector.get_emails(10)
                        st.rerun()
            
            st.markdown("---")
            
            for idx, email_item in enumerate(st.session_state.emails):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**From:** {email_item['from']}")
                        st.markdown(f"**Subject:** {email_item['subject']}")
                    
                    with col2:
                        st.caption(f"📅 {email_item['date'][:16]}")
                    
                    # Show email body
                    with st.expander("📖 View Email", expanded=False):
                        st.text(email_item['body'])
                    
                    # Action buttons
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("💬 Generate Reply", key=f"gen_{idx}", use_container_width=True):
                            with st.spinner("Generating..."):
                                reply = analyze_email(email_item['body'])
                                st.info(reply['generated_reply'])
                    
                    with col2:
                        if st.button("📂 Categorize", key=f"cat_{idx}", use_container_width=True):
                            result = analyze_email(email_item['body'])
                            st.info(f"**Category:** {result['category']}")
                    
                    with col3:
                        if st.button("✉️ Send Reply", key=f"send_{idx}", use_container_width=True):
                            with st.spinner("Sending..."):
                                reply = analyze_email(email_item['body'])
                                from_email = email_item['from']
                                if '<' in from_email:
                                    from_email = from_email.split('<')[1].rstrip('>')
                                
                                if st.session_state.connector.send_reply(
                                    from_email,
                                    f"Re: {email_item['subject']}",
                                    reply['generated_reply']
                                ):
                                    st.success("✅ Reply sent!")
                                else:
                                    st.error("❌ Send failed")
        else:
            st.info("📭 No emails or not connected")



with tab4:
    st.subheader("How to Use")

    st.markdown("""
    ### Features

    **1. Draft Reply Tab:**
    - Paste an email you received
    - Click "Generate Reply" to create a professional response
    - AI drafts the reply automatically

    **2. Categorize Tab:**
    - Paste an email to categorize it
    - System identifies email type
    - Categories: Meeting, Finance, Project, etc.
    
    **3. Gmail Inbox Tab:**
    - Automatically loads your Gmail inbox
    - View all emails
    - Generate & send replies
    - Auto-categorize emails

    ### Supported Categories
    | Category | Keywords |
    |----------|----------|
    | Meeting | meeting, schedule, appointment, conference call |
    | Finance | invoice, payment, bill, receipt, expense |
    | Project | project, task, deadline, deliverable |
    | Resume/Job | resume, cv, job, position, hiring |
    | Important | urgent, asap, important, critical |
    | Support | help, issue, problem, error, bug |
    | General | No matching keywords |

    ### Gmail Setup
    
    **Step 1: Create .env file**
    - Copy `.env.example` to `.env`
    
    **Step 2: Get App Password**
    1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
    2. Select: **Mail** → **Windows Computer**
    3. Copy the 16-character password
    
    **Step 3: Add to .env**
    ```
    EMAIL_ADDRESS=your-email@gmail.com
    EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
    ```
    
    **Step 4: Reload**
    - Refresh the app in browser
    - Inbox loads automatically ✅

    ### Tips
    - App automatically shows Gmail inbox when loaded
    - Click Refresh to reload emails
    - Review AI responses before sending
    - Longer emails = better replies
    """)



# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <p>Intelligent Email Assistant | Yash Vashisth (2301730158)</p>
    <p>Powered by Hugging Face & Transformers</p>
</div>
""", unsafe_allow_html=True)
