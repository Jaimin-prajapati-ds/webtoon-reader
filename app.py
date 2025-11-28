import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Webtoon Reader", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0;
    }
    .stTitle {
        color: #FF6B6B;
        text-align: center;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# API Base URL
API_URL = st.secrets.get("api_url", "http://localhost:8000/api")

st.title("🎨 Webtoon Reader - Comic Portal")
st.subheader("Discover amazing comics and manhwas")

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 📚 Navigation")
    page = st.radio(
        "Choose a page:",
        ["🏠 Home", "📖 Browse Comics", "➕ Add Comic", "📊 Statistics"]
    )

# Home Page
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Comics", "50+", "+5 this month")
    with col2:
        st.metric("Total Chapters", "500+", "+50 this month")
    with col3:
        st.metric("Active Readers", "1000+", "+100 this week")
    
    st.markdown("---")
    
    st.subheader("📌 Featured Comics")
    
    # Sample comic data
    comics_data = [
        {
            "title": "My First Comic",
            "author": "Your Name",
            "chapters": 15,
            "status": "Ongoing",
            "rating": 4.5
        },
        {
            "title": "Epic Adventure",
            "author": "Creator Name",
            "chapters": 32,
            "status": "Completed",
            "rating": 4.8
        },
        {
            "title": "Love & Dreams",
            "author": "Romance Writer",
            "chapters": 24,
            "status": "Ongoing",
            "rating": 4.3
        }
    ]
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for idx, comic in enumerate(comics_data):
        with cols[idx % 3]:
            st.write(f"### {comic['title']}")
            st.write(f"👤 Author: **{comic['author']}**")
            st.write(f"📕 Chapters: **{comic['chapters']}**")
            st.write(f"Status: **{comic['status']}**")
            st.write(f"⭐ Rating: **{comic['rating']}/5**")
            st.button(f"Read {comic['title']}", key=f"read_{comic['title']}")

# Browse Comics Page
elif page == "📖 Browse Comics":
    st.subheader("Browse All Comics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search = st.text_input("🔍 Search comics...")
    with col2:
        sort_by = st.selectbox("Sort by:", ["Latest", "Popular", "Rating"])
    
    st.markdown("---")
    
    # Display comics in grid
    cols = st.columns(3)
    
    sample_comics = [
        {"title": "Comic 1", "chapters": 10, "status": "Ongoing"},
        {"title": "Comic 2", "chapters": 25, "status": "Completed"},
        {"title": "Comic 3", "chapters": 15, "status": "Ongoing"},
        {"title": "Comic 4", "chapters": 8, "status": "Ongoing"},
        {"title": "Comic 5", "chapters": 30, "status": "Completed"},
        {"title": "Comic 6", "chapters": 12, "status": "Ongoing"},
    ]
    
    for idx, comic in enumerate(sample_comics):
        with cols[idx % 3]:
            st.write(f"**{comic['title']}**")
            st.write(f"Chapters: {comic['chapters']}")
            st.write(f"Status: {comic['status']}")
            if st.button("Read", key=f"comic_{idx}"):
                st.success(f"Opening {comic['title']}...")

# Add Comic Page
elif page == "➕ Add Comic":
    st.subheader("Add a New Comic")
    
    with st.form("comic_form"):
        title = st.text_input("Comic Title *")
        slug = st.text_input("URL Slug (auto-generated) *")
        description = st.text_area("Description")
        author = st.text_input("Author Name")
        cover_url = st.text_input("Cover Image URL")
        status = st.selectbox("Status", ["Ongoing", "Completed", "Hiatus"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("✅ Create Comic"):
                if title and slug:
                    st.success(f"✨ Comic '{title}' created successfully!")
                    st.json({
                        "title": title,
                        "slug": slug,
                        "description": description,
                        "author": author,
                        "status": status,
                        "created_at": datetime.now().isoformat()
                    })
                else:
                    st.error("Please fill in all required fields")
        with col2:
            st.form_submit_button("❌ Reset")

# Statistics Page
elif page == "📊 Statistics":
    st.subheader("Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Comics", "50", "+5")
    with col2:
        st.metric("Total Chapters", "500", "+50")
    with col3:
        st.metric("Active Users", "1200", "+100")
    with col4:
        st.metric("Daily Reads", "450", "+30")
    
    st.markdown("---")
    
    # Charts
    import random
    chart_data = pd.DataFrame(
        {
            "Day": [f"Day {i}" for i in range(1, 8)],
            "Reads": [random.randint(300, 600) for _ in range(7)],
            "New Comics": [random.randint(1, 5) for _ in range(7)]
        }
    )
    
    st.line_chart(chart_data.set_index("Day"))
    
    st.markdown("---")
    
    st.subheader("📈 Top Comics")
    top_comics = pd.DataFrame({
        "Comic Title": ["Comic A", "Comic B", "Comic C", "Comic D"],
        "Views": [15000, 12000, 9500, 8200],
        "Rating": [4.8, 4.6, 4.4, 4.2],
        "Status": ["Ongoing", "Completed", "Ongoing", "Hiatus"]
    })
    st.dataframe(top_comics, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🚀 Webtoon Reader Platform | Built with Streamlit</p>
    <p>© 2025 | FastAPI Backend + React Frontend + Streamlit Dashboard</p>
</div>
""", unsafe_allow_html=True)
