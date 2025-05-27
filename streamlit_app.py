import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Configuration
API_BASE_URL = "https://trendhire.onrender.com"  # Replace with your Railway URL

st.set_page_config(
    page_title="TrendHire - AI Career Intelligence",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 TrendHire: Discover the Future of Hiring")
st.markdown("*AI-powered hiring intelligence that detects emerging job roles and skills before they go mainstream*")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose Feature", [
    "Trending Jobs", 
    "Skill Analysis", 
    "Learning Paths", 
    "Salary Trends"
])

def call_api(endpoint, params=None):
    """Call TrendHire API"""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# Page 1: Trending Jobs
if page == "Trending Jobs":
    st.header("📈 Trending Job Roles")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location", ["Remote", "San Francisco", "New York", "London", "Berlin"])
    with col2:
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Marketing", "All"])
    
    if st.button("Analyze Trends", type="primary"):
        with st.spinner("Discovering trending roles..."):
            # Mock data for demo (replace with API call)
            trending_data = {
                "trending_jobs": [
                    {"title": "AI Safety Engineer", "growth": 340, "avg_salary": 185000, "demand": "Very High"},
                    {"title": "Prompt Engineer", "growth": 280, "avg_salary": 145000, "demand": "High"},
                    {"title": "MLOps Engineer", "growth": 220, "avg_salary": 155000, "demand": "High"},
                    {"title": "Climate Data Scientist", "growth": 190, "avg_salary": 135000, "demand": "Medium"},
                    {"title": "Quantum Software Developer", "growth": 150, "avg_salary": 165000, "demand": "Medium"}
                ]
            }
            
            df = pd.DataFrame(trending_data["trending_jobs"])
            
            # Growth chart
            fig = px.bar(df, x="title", y="growth", 
                        title="Job Role Growth Rate (%)",
                        color="growth",
                        color_continuous_scale="viridis")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            st.subheader("Detailed Metrics")
            st.dataframe(df, use_container_width=True)

# Page 2: Skill Analysis
elif page == "Skill Analysis":
    st.header("🧠 In-Demand Skills Analysis")
    
    skill_input = st.text_input("Enter your current skills (comma-separated)", 
                               placeholder="Python, React, SQL, Machine Learning")
    
    if st.button("Analyze Skills Gap", type="primary") and skill_input:
        with st.spinner("Analyzing skill gaps..."):
            # Mock skill gap analysis
            skills = [s.strip() for s in skill_input.split(",")]
            
            gap_data = {
                "current_skills": skills,
                "trending_skills": ["LangChain", "Vector Databases", "MLOps", "Kubernetes", "Rust"],
                "skill_scores": {
                    "Python": 95,
                    "React": 85,
                    "SQL": 80,
                    "Machine Learning": 90,
                    "LangChain": 20,
                    "Vector Databases": 15,
                    "MLOps": 30,
                    "Kubernetes": 45,
                    "Rust": 10
                }
            }
            
            # Radar chart
            categories = list(gap_data["skill_scores"].keys())
            values = list(gap_data["skill_scores"].values())
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='Skill Level'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                title="Your Skill Profile vs Market Demand"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.subheader("🎯 Skill Gap Recommendations")
            for skill in gap_data["trending_skills"]:
                score = gap_data["skill_scores"].get(skill, 0)
                if score < 60:
                    st.warning(f"**{skill}**: Current level {score}% - High priority for learning")

# Page 3: Learning Paths
elif page == "Learning Paths":
    st.header("🎓 Personalized Learning Paths")
    
    target_role = st.selectbox("Target Role", [
        "AI Engineer", "Data Scientist", "Full Stack Developer", 
        "DevOps Engineer", "Product Manager"
    ])
    
    if st.button("Generate Learning Path", type="primary"):
        with st.spinner("Creating personalized learning path..."):
            # Mock learning path
            learning_path = {
                "AI Engineer": [
                    {"course": "Advanced LangChain Development", "provider": "DeepLearning.AI", "duration": "6 weeks", "rating": 4.8, "price": "$49"},
                    {"course": "Vector Database Mastery", "provider": "Pinecone Academy", "duration": "4 weeks", "rating": 4.7, "price": "$39"},
                    {"course": "MLOps with Kubernetes", "provider": "Coursera", "duration": "8 weeks", "rating": 4.6, "price": "$59"},
                    {"course": "AI Safety & Ethics", "provider": "Stanford Online", "duration": "3 weeks", "rating": 4.9, "price": "Free"}
                ]
            }
            
            st.subheader(f"🛤️ Learning Path for {target_role}")
            
            for i, course in enumerate(learning_path[target_role], 1):
                with st.expander(f"Step {i}: {course['course']}"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Provider", course['provider'])
                    with col2:
                        st.metric("Duration", course['duration'])
                    with col3:
                        st.metric("Rating", course['rating'])
                    with col4:
                        st.metric("Price", course['price'])

# Page 4: Salary Trends
elif page == "Salary Trends":
    st.header("💰 Real-Time Salary Intelligence")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job Title", placeholder="AI Engineer")
    with col2:
        location_salary = st.selectbox("Location", ["San Francisco", "New York", "Remote", "London"])
    
    if st.button("Analyze Salary Trends", type="primary") and job_title:
        with st.spinner("Fetching salary data..."):
            # Mock salary data
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
            salaries = [145000, 148000, 152000, 155000, 158000]
            
            fig = px.line(x=months, y=salaries, 
                         title=f"{job_title} Salary Trend - {location_salary}",
                         labels={'x': 'Month', 'y': 'Average Salary ($)'})
            fig.update_traces(line_color='#00cc96', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
            
            # Current metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Average", "$158,000", "+8.9%")
            with col2:
                st.metric("Market Growth", "+12.5%", "vs last year")
            with col3:
                st.metric("Job Postings", "2,847", "+34%")

# Footer
st.markdown("---")
st.markdown("*Powered by Bright Data MCP Server & Real-Time Web Intelligence*")
st.markdown("Built for the Bright Data x DEV.to Hackathon 2024")