# trendhire_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import time

# API endpoint (change in production)
API_ENDPOINT = "http://localhost:8000"

# Page title and configuration
st.set_page_config(
    page_title="TrendHire: Discover the future of hiring—before it happens",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4a86e8;
        margin-bottom: 0;
    }
    .tagline {
        font-size: 1.2rem;
        color: #767676;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .dashboard-section {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>TrendHire</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Discover the future of hiring—before it happens</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Select a page", [
        "Dashboard", 
        "Trend Velocity", 
        "Skill Mapper", 
        "Gap Analyzer", 
        "Salary Signals",
        "Data Collection"
    ])
    
    st.markdown("---")
    st.markdown("### Filters")
    time_range = st.select_slider(
        "Time Range", 
        options=["Last 7 days", "Last 30 days", "Last 90 days", "Last 6 months"]
    )
    
    if page in ["Trend Velocity", "Skill Mapper", "Gap Analyzer"]:
        job_category = st.multiselect(
            "Job Categories",
            ["AI/ML", "Software Engineering", "Data Science", "DevOps", "Product Management"],
            default=["AI/ML"]
        )

# Dashboard Page
if page == "Dashboard":
    st.header("TrendHire Dashboard")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trending Skills", "27", "+5")
    with col2:
        st.metric("Emerging Roles", "12", "+3")
    with col3:
        st.metric("Salary Trend", "$125K", "+2.5%")
    with col4:
        st.metric("Skill Gap Score", "0.67", "-0.05")
    
    # Charts
    st.subheader("Top Trending Skills")
    
    # Sample data (would come from API)
    skills_data = {
        "Skill": ["RAG Development", "LangChain", "FAISS", "Prompt Engineering", "Vector Databases"],
        "Velocity": [0.92, 0.87, 0.82, 0.78, 0.73],
        "Category": ["AI/ML", "AI/ML", "AI/ML", "AI/ML", "Data Science"]
    }
    df_skills = pd.DataFrame(skills_data)
    
    fig_skills = px.bar(
        df_skills, 
        x="Skill", 
        y="Velocity", 
        color="Category",
        title="Skills by Trend Velocity",
        labels={"Velocity": "Trend Velocity Score"}
    )
    st.plotly_chart(fig_skills, use_container_width=True)
    
    # Two columns for additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emerging Job Roles")
        roles_data = {
            "Role": ["RAG Engineer", "AI Product Manager", "LLM Fine-tuner", "Prompt Engineer", "MLOps Specialist"],
            "Growth": [145, 112, 95, 87, 72]
        }
        df_roles = pd.DataFrame(roles_data)
        
        fig_roles = px.bar(
            df_roles, 
            x="Role", 
            y="Growth",
            title="Job Roles by Growth (%)",
            color="Growth",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_roles, use_container_width=True)
    
    with col2:
        st.subheader("Skill to Education Gap")
        gap_data = {
            "Skill": ["Vector DBs", "LLM Fine-tuning", "RAG", "Multimodal AI", "AI Ethics"],
            "Market Demand": [0.89, 0.82, 0.93, 0.76, 0.68],
            "Education Coverage": [0.45, 0.52, 0.38, 0.41, 0.72]
        }
        df_gap = pd.DataFrame(gap_data)
        
        fig_gap = go.Figure()
        fig_gap.add_trace(go.Bar(
            x=df_gap["Skill"],
            y=df_gap["Market Demand"],
            name="Market Demand",
            marker_color="rgb(55, 83, 109)"
        ))
        fig_gap.add_trace(go.Bar(
            x=df_gap["Skill"],
            y=df_gap["Education Coverage"],
            name="Education Coverage",
            marker_color="rgb(26, 118, 255)"
        ))
        
        fig_gap.update_layout(
            title="Market Demand vs. Education Coverage",
            barmode="group"
        )
        
        st.plotly_chart(fig_gap, use_container_width=True)

# Trend Velocity Page
elif page == "Trend Velocity":
    st.header("Trend Velocity Index")
    st.markdown("Track how fast skills and job titles are rising in demand")
    
    search_term = st.text_input("Search for a skill or job title")
    
    if search_term:
        # Sample API call to get trend velocity (mocked for now)
        # response = requests.get(f"{API_ENDPOINT}/trends/velocity?skill={search_term}")
        # trend_data = response.json()
        
        # Mock data
        trend_data = {
            "trend_velocity": 0.85,
            "change_30d": "+15%",
            "source_breakdown": {
                "job_boards": 0.78,
                "reddit": 0.92,
                "tech_forums": 0.88,
                "learning_platforms": 0.81
            },
            "historical": [
                {"date": "2025-04-15", "value": 0.72},
                {"date": "2025-04-22", "value": 0.75},
                {"date": "2025-04-29", "value": 0.78},
                {"date": "2025-05-06", "value": 0.81},
                {"date": "2025-05-13", "value": 0.85}
            ]
        }
        
        # Display main metric
        st.metric(
            f"Trend Velocity for '{search_term}'", 
            f"{trend_data['trend_velocity']:.2f}", 
            trend_data["change_30d"]
        )
        
        # Display source breakdown
        st.subheader("Source Breakdown")
        source_df = pd.DataFrame({
            "Source": list(trend_data["source_breakdown"].keys()),
            "Score": list(trend_data["source_breakdown"].values())
        })
        
        fig = px.bar(
            source_df,
            x="Source",
            y="Score",
            color="Score",
            color_continuous_scale="Viridis",
            title="Trend Velocity by Source Type"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Historical trend chart
        st.subheader("Historical Trend")
        hist_df = pd.DataFrame(trend_data["historical"])
        hist_df["date"] = pd.to_datetime(hist_df["date"])
        
        fig_hist = px.line(
            hist_df,
            x="date",
            y="value",
            title=f"Trend Velocity for '{search_term}' Over Time",
            labels={"value": "Velocity Score", "date": "Date"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Related trends
        st.subheader("Related Skills & Roles")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Related Skills")
            related_skills = ["Vector Embeddings", "Semantic Search", "Langchain", "Chroma DB", "HuggingFace"]
            for skill in related_skills:
                st.markdown(f"- {skill} (0.{int(70 + 5*related_skills.index(skill))})")
        
        with col2:
            st.markdown("### Related Job Roles")
            related_roles = ["RAG Engineer", "ML Engineer", "Data Scientist", "AI Developer", "LLM Specialist"]
            for role in related_roles:
                st.markdown(f"- {role} (0.{int(80 - 3*related_roles.index(role))})")
    
    else:
        # Sample trending skills table
        st.subheader("Top Trending Skills Right Now")
        trending_data = {
            "Skill": ["RAG", "LangChain", "Vector Databases", "LLM Fine-tuning", "Multimodal AI"],
            "Trend Velocity": [0.92, 0.87, 0.85, 0.82, 0.78],
            "30-Day Change": ["+22%", "+15%", "+18%", "+9%", "+12%"]
        }
        
        st.dataframe(pd.DataFrame(trending_data), hide_index=True)

# Skill Mapper Page
elif page == "Skill Mapper":
    st.header("Skill-to-Opportunity Map")
    st.markdown("Map your existing skills to trending job opportunities")
    
    # Input for user's current skills
    user_skills = st.text_area(
        "Enter your current skills (comma-separated)",
        "Python, Machine Learning, Pandas, PyTorch, SQL"
    )
    
    if st.button("Analyze My Skills"):
        with st.spinner("Analyzing skills..."):
            # Simulate API call
            time.sleep(2)
            
            # Sample data (would come from API)
            skill_map_data = {
                "matching_roles": [
                    {"title": "RAG Engineer", "match_score": 0.75, "missing_skills": ["LangChain", "Vector DBs"]},
                    {"title": "ML Engineer", "match_score": 0.82, "missing_skills": ["MLOps", "Kubernetes"]},
                    {"title": "Data Scientist", "match_score": 0.88, "missing_skills": ["Tableau", "A/B Testing"]},
                    {"title": "AI Developer", "match_score": 0.70, "missing_skills": ["React", "FastAPI", "OAuth"]}
                ],
                "skill_recommendations": [
                    {"skill": "LangChain", "demand_score": 0.91, "learning_difficulty": "Medium"},
                    {"skill": "Vector Databases", "demand_score": 0.89, "learning_difficulty": "Medium"},
                    {"skill": "MLOps", "demand_score": 0.87, "learning_difficulty": "Hard"},
                    {"skill": "Kubernetes", "demand_score": 0.85, "learning_difficulty": "Hard"},
                    {"skill": "React", "demand_score": 0.82, "learning_difficulty": "Medium"}
                ]
            }
            
            # Display matching roles
            st.subheader("Your Matching Job Opportunities")
            
            for i, role in enumerate(skill_map_data["matching_roles"]):
                with st.expander(f"{role['title']} - {int(role['match_score']*100)}% Match"):
                    st.markdown(f"**Missing Skills:** {', '.join(role['missing_skills'])}")
                    
                    # Show estimated salary range (mock data)
                    salary_range = f"${120 - (i*10)}K - ${150 - (i*5)}K"
                    st.markdown(f"**Estimated Salary Range:** {salary_range}")
                    
                    # Show job market trend
                    trend = "↗️ Rising" if i < 2 else ("→ Stable" if i < 3 else "↘️ Declining")
                    st.markdown(f"**Market Trend:** {trend}")
            
            # Display skill recommendations
            st.subheader("Recommended Skills to Learn")
            
            rec_data = pd.DataFrame([
                {
                    "Skill": rec["skill"],
                    "Demand Score": rec["demand_score"],
                    "Learning Difficulty": rec["learning_difficulty"]
                }
                for rec in skill_map_data["skill_recommendations"]
            ])
            
            fig = px.bar(
                rec_data,
                x="Skill",
                y="Demand Score",
                color="Learning Difficulty",
                title="Recommended Skills by Demand",
                color_discrete_map={"Easy": "green", "Medium": "orange", "Hard": "red"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Course recommendations
            st.subheader("Recommended Learning Resources")
            courses = [
                {"title": "Vector Databases for RAG Applications", "platform": "Udemy", "price": "$89.99"},
                {"title": "LangChain for Production LLM Apps", "platform": "Coursera", "price": "$49/month"},
                {"title": "Modern MLOps with Kubernetes", "platform": "Pluralsight", "price": "$29/month"},
                {"title": "Practical RAG Development", "platform": "LinkedIn Learning", "price": "$39.99"}
            ]
            
            for course in courses:
                st.markdown(f"- **{course['title']}** ({course['platform']}, {course['price']})")

# Gap Analyzer Page
elif page == "Gap Analyzer":
    st.header("Skill Gap Analyzer")
    st.markdown("Analyze gaps between job market needs and education content")
    
    analyze_button = st.button("Run Gap Analysis")
    
    if analyze_button:
        with st.spinner("Running analysis..."):
            # Simulate API call
            time.sleep(2)
            
            # Sample data
            gap_data = {
                "market_needs_score": 0.92,
                "education_coverage_score": 0.67,
                "gap_score": 0.25,
                "skill_gaps": [
                    {"skill": "RAG Implementation", "market_demand": 0.95, "education_coverage": 0.45, "gap_score": 0.50},
                    {"skill": "Vector Database Management", "market_demand": 0.88, "education_coverage": 0.40, "gap_score": 0.48},
                    {"skill": "LLM Fine-tuning", "market_demand": 0.85, "education_coverage": 0.55, "gap_score": 0.30},
                    {"skill": "Multimodal LLMs", "market_demand": 0.82, "education_coverage": 0.35, "gap_score": 0.47},
                    {"skill": "Efficient Prompt Engineering", "market_demand": 0.80, "education_coverage": 0.60, "gap_score": 0.20}
                ],
                "recommendations": [
                    "More courses needed on RAG implementation",
                    "Additional content on multimodal LLMs required",
                    "Practical projects in vector database management underrepresented",
                    "Hands-on exercises for LLM fine-tuning needed",
                    "Better integration of prompt engineering with real business cases"
                ]
            }
            
            # Display overall metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Market Demand", f"{gap_data['market_needs_score']:.2f}")
            with col2:
                st.metric("Education Coverage", f"{gap_data['education_coverage_score']:.2f}")
            with col3:
                st.metric("Overall Gap", f"{gap_data['gap_score']:.2f}")
            
            # Display gap chart
            st.subheader("Skill-Specific Gaps")
            
            gap_df = pd.DataFrame([
                {
                    "Skill": item["skill"],
                    "Market Demand": item["market_demand"],
                    "Education Coverage": item["education_coverage"],
                    "Gap Score": item["gap_score"]
                }
                for item in gap_data["skill_gaps"]
            ])
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=gap_df["Skill"],
                y=gap_df["Market Demand"],
                name="Market Demand",
                marker_color="rgb(55, 83, 109)"
            ))
            fig.add_trace(go.Bar(
                x=gap_df["Skill"],
                y=gap_df["Education Coverage"],
                name="Education Coverage",
                marker_color="rgb(26, 118, 255)"
            ))
            
            fig.update_layout(
                title="Market Demand vs. Education Coverage by Skill",
                barmode="group"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display recommendations
            st.subheader("Recommendations for Course Creators")
            for rec in gap_data["recommendations"]:
                st.markdown(f"- {rec}")
            
            # Sample opportunity table
            st.subheader("Education Market Opportunities")
            opportunity_data = {
                "Topic": ["RAG Development Course", "Vector DB Workshop", "Multimodal LLM Bootcamp", "Fine-tuning Masterclass"],
                "Estimated Demand": ["Very High", "High", "High", "Medium-High"],
                "Competitor Count": [3, 2, 1, 5],
                "Opportunity Score": [0.92, 0.88, 0.85, 0.78]
            }
            
            st.dataframe(pd.DataFrame(opportunity_data), hide_index=True)

# Salary Signals Page
elif page == "Salary Signals":
    st.header("Salary Signal Detector")
    st.markdown("Detect hidden shifts in compensation by location, role, and time")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        role_filter = st.multiselect(
            "Job Roles",
            ["AI Engineer", "ML Engineer", "RAG Engineer", "Data Scientist", "AI Product Manager"],
            default=["AI Engineer", "ML Engineer"]
        )
    with col2:
        location_filter = st.multiselect(
            "Locations",
            ["San Francisco", "New York", "Remote", "Seattle", "Austin"],
            default=["San Francisco", "Remote"]
        )
    
    if st.button("Analyze Salary Trends"):
        with st.spinner("Analyzing salary data..."):
            # Simulate API call
            time.sleep(2)
            
            # Sample data
            salary_data = {
                "by_location": {
                    "San Francisco": {"mean": 152000, "median": 145000, "growth": "+5.2%"},
                    "New York": {"mean": 145000, "median": 140000, "growth": "+4.8%"},
                    "Remote": {"mean": 135000, "median": 130000, "growth": "+8.5%"},
                    "Seattle": {"mean": 148000, "median": 142000, "growth": "+3.9%"},
                    "Austin": {"mean": 138000, "median": 132000, "growth": "+7.2%"}
                },
                "by_title": {
                    "AI Engineer": {"mean": 145000, "median": 140000, "growth": "+6.3%"},
                    "ML Engineer": {"mean": 152000, "median": 148000, "growth": "+5.5%"},
                    "RAG Engineer": {"mean": 160000, "median": 155000, "growth": "+12.8%"},
                    "Data Scientist": {"mean": 138000, "median": 132000, "growth": "+4.2%"},
                    "AI Product Manager": {"mean": 155000, "median": 148000, "growth": "+7.5%"}
                },
                "time_trends": [
                    {"month": "2024-11", "mean_salary": 135000, "percent_change": 0},
                    {"month": "2024-12", "mean_salary": 138500, "percent_change": 2.6},
                    {"month": "2025-01", "mean_salary": 142000, "percent_change": 2.5},
                    {"month": "2025-02", "mean_salary": 146500, "percent_change": 3.2},
                    {"month": "2025-03", "mean_salary": 150000, "percent_change": 2.4},
                    {"month": "2025-04", "mean_salary": 155000, "percent_change": 3.3}
                ]
            }
            
            # Display location chart
            st.subheader("Salary by Location")
            location_df = pd.DataFrame([
                {
                    "Location": loc,
                    "Mean Salary": data["mean"],
                    "Growth": data["growth"]
                }
                for loc, data in salary_data["by_location"].items()
                if loc in location_filter
            ])
            
            fig_loc = px.bar(
                location_df,
                x="Location",
                y="Mean Salary",
                color="Growth",
                title="Mean Salary by Location",
                text="Growth"
            )
            st.plotly_chart(fig_loc, use_container_width=True)
            
            # Display role chart
            st.subheader("Salary by Role")
            role_df = pd.DataFrame([
                {
                    "Role": role,
                    "Mean Salary": data["mean"],
                    "Growth": data["growth"]
                }
                for role, data in salary_data["by_title"].items()
                if role in role_filter
            ])
            
            fig_role = px.bar(
                role_df,
                x="Role",
                y="Mean Salary",
                color="Growth",
                title="Mean Salary by Role",
                text="Growth"
            )
            st.plotly_chart(fig_role, use_container_width=True)
            
            # Display time trend
            st.subheader("Salary Trends Over Time")
            time_df = pd.DataFrame(salary_data["time_trends"])
            time_df["month"] = pd.to_datetime(time_df["month"])
            
            fig_time = px.line(
                time_df,
                x="month",
                y="mean_salary",
                title="Salary Trends Over Time",
                labels={"mean_salary": "Mean Salary", "month": "Month"}
            )
            
            # Add percent change as annotations
            for i, row in time_df.iterrows():
                if i > 0:  # Skip first month (no change)
                    fig_time.add_annotation(
                        x=row["month"],
                        y=row["mean_salary"],
                        text=f"+{row['percent_change']}%",
                        showarrow=True,
                        arrowhead=7,
                        ax=0,
                        ay=-40
                    )
            
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Key insights
            st.subheader("Key Insights")
            st.markdown("""
            - **RAG Engineers** show the highest salary growth at **+12.8%**
            - **Remote roles** are seeing faster growth than on-site positions
            - Salaries for AI roles have increased **+14.8%** over the past 6 months
            - Emerging specialty roles command a **$15-25K premium** over general roles
            """)

# Data Collection Page
elif page == "Data Collection":
    st.header("Data Collection")
    st.markdown("Configure and run data collection tasks from various sources")
    
    # Source selection
    st.subheader("Select Data Sources")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Job Boards", "Learning Platforms", "Reddit", "Tech Forums"])
    
    with tab1:
        job_sources = st.multiselect(
            "Select Job Boards",
            ["Indeed", "LinkedIn Jobs", "Wellfound", "BuiltIn", "RemoteOK"],
            default=["Indeed", "LinkedIn Jobs"]
        )
        
        job_keywords = st.text_input("Search Keywords", "AI Engineer, ML Engineer, RAG Engineer")
    
    with tab2:
        learning_sources = st.multiselect(
            "Select Learning Platforms",
            ["Udemy", "Coursera", "LinkedIn Learning", "Pluralsight", "edX"],
            default=["Udemy", "Coursera"]
        )
        
        learning_keywords = st.text_input("Course Topics", "RAG, LangChain, Vector Databases, LLM Fine-tuning")
    
    with tab3:
        reddit_sources = st.multiselect(
            "Select Subreddits",
            ["r/cscareerquestions", "r/MachineLearning", "r/datascience", "r/artificial", "r/jobs"],
            default=["r/cscareerquestions", "r/MachineLearning"]
        )
    
    with tab4:
        forum_sources = st.multiselect(
            "Select Tech Forums",
            ["Hacker News", "Dev.to", "Stack Overflow", "LessWrong", "Hugging Face Forums"],
            default=["Hacker News", "Dev.to"]
        )
    
    # Configure crawling parameters
    st.subheader("Crawling Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Browser Country", ["US", "UK", "Canada", "Germany", "Australia"], index=0)
        user_agent = st.selectbox("User Agent Type", ["desktop", "mobile"], index=0)
    
    with col2:
        stealth_mode = st.checkbox("Enable Stealth Mode", value=True)
        bypass_login = st.checkbox("Attempt Login Wall Bypass", value=True)
    
    # Start crawling button
    if st.button("Start Data Collection"):
        # Construct the source configurations
        sources = []
        
        for job_source in job_sources:
            if job_source == "Indeed":
                sources.append({
                    "url": f"https://www.indeed.com/jobs?q={job_keywords.replace(', ', '+')}",
                    "source_type": "job_board",
                    "selectors": {
                        "main_content": "#mosaic-provider-jobcards",
                        "job_listings": ".job_seen_beacon",
                        "job_title": ".jobTitle",
                        "salary": ".salary-snippet",
                        "location": ".companyLocation"
                    }
                })
        
        for learning_source in learning_sources:
            if learning_source == "Udemy":
                sources.append({
                    "url": f"https://www.udemy.com/courses/search/?q={learning_keywords.replace(', ', '+')}",
                    "source_type": "learning_platform",
                    "selectors": {
                        "main_content": ".course-list--container",
                        "course_listings": ".course-card",
                        "course_title": ".course-card--course-title",
                        "price": ".price-text--price-part",
                        "rating": ".star-rating--rating-number"
                    }
                })
        
        # Display progress bar
        with st.spinner("Starting data collection..."):
            time.sleep(2)
            
            # Create new task
            task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Show task info
            st.success(f"Data collection task started with ID: {task_id}")
            
            # Progress tracking
            progress_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            # Simulate progress updates
            for i in range(101):
                progress_bar.progress(i)
                
                status = "Initializing..."
                if i > 10:
                    status = "Connecting to job boards..."
                if i > 30:
                    status = "Extracting job listings..."
                if i > 50:
                    status = "Processing course data..."
                if i > 70:
                    status = "Analyzing forum discussions..."
                if i > 90:
                    status = "Finalizing data collection..."
                
                progress_placeholder.text(f"Status: {status} ({i}%)")
                time.sleep(0.1)
            
            # Final status
            st.success("Data collection completed successfully!")
            
            # Summary of collected data
            st.subheader("Collection Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Job Listings", "187")
            with col2:
                st.metric("Courses", "92")
            with col3:
                st.metric("Forum Posts", "143")
            
            # Sample of collected data
            st.subheader("Sample Data Preview")
            
            sample_data = {
                "Title": ["AI Engineer", "ML Engineer", "RAG Specialist", "Data Scientist"],
                "Source": ["Indeed", "LinkedIn", "Wellfound", "Indeed"],
                "Salary Range": ["$120K-$150K", "$135K-$165K", "$150K-$185K", "$110K-$140K"],
                "Skills": ["Python, TensorFlow, PyTorch", "ML, SQL, Cloud", "RAG, Embeddings, LangChain", "Python, SQL, Tableau"]
            }
            
            st.dataframe(pd.DataFrame(sample_data), hide_index=True)