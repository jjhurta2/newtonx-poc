import streamlit as st
import pandas as pd 
from openai import OpenAI
import time

# Set up the page
st.set_page_config(page_title="NewtonX Org Mapper", page_icon="🎯", layout="wide")

st.title("NewtonX CPM Org Mapper")
st.markdown("The stakeholder expansion assistant for Client Partnership Managers.")

# Initialize OpenAI Client (Pulls from Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- DATA SETUP ---
# All fields are now explicitly defined to simulate a complete CRM database export
contact_names = ["Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", "Ismael Camus"]
contact_roles = ["Product Manager", "Senior Business Planner", "Senior Account Executive", "AI Agent / Past Core PMM", "Sr. Solution Engineer - Data & AI", "Product Manager", "Product Manager", "Solution Specialist - Azure Data & AI", "Product Manager", "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", "Director, Corporate Business Development", "Senior Product Marketing Manager", "Director Business Planning", "Principal Product Manager", "Senior Business Planner", "Director & Team Lead, Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"]
contact_teams = ["Microsoft FastTrack", "Azure Virtual Desktop", "Public Sector Sales", "Copilot Product Marketing", "Data & AI Customer Success", "Microsoft Teams Core", "Azure Cloud Platform", "Azure Data & AI Specialist Team Unit", "Xbox Cloud Gaming", "Microsoft Marketing Operations", "MCAPS Americas", "Windows Cloud (Windows 365)", "Corporate Business Development", "Surface Commercial Marketing", "Monetization & Strategy", "Azure Virtual Desktop", "Microsoft 365 Business Planning", "Cloud & AI Monetization", "Aspire / University Hires (Marketing)", "Cloud/AI Infra & Investments Strategy"]
contact_strengths = ["2. Medium", "2. Medium", "1. Weak", "2. Medium", "1. Weak", "2. Medium", "2. Medium", "1. Weak", "2. Medium", "3. Strong", "1. Weak", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "1. Weak", "2. Medium"]
contact_emails = ["lusande@microsoft.com", "coochoa@microsoft.com", "frreadivargas@microsoft.com", "sashen@microsoft.com", "regonzalezperez@microsoft.com", "deoverton@microsoft.com", "hijonnalagadda@microsoft.com", "naperezlopez@microsoft.com", "anbernal@microsoft.com", "tiharrison@microsoft.com", "ozsezginel@microsoft.com", "apbhattacharyya@microsoft.com", "elgarcia@microsoft.com", "jecady@microsoft.com", "nishah@microsoft.com", "stdowns@microsoft.com", "macolmenaresamaya@microsoft.com", "prjalan@microsoft.com", "yicui@microsoft.com", "iscamus@microsoft.com"]
contact_linkedin = ["https://www.linkedin.com/in/luis-sande", "https://www.linkedin.com/in/cosme-ochoa", "https://www.linkedin.com/in/francisca-readi", "https://www.linkedin.com/in/sammy-shen", "https://www.linkedin.com/in/reisel-gonzalez", "https://www.linkedin.com/in/delaney-overton", "https://www.linkedin.com/in/hitesh-jonnalagadda", "https://www.linkedin.com/in/natalia-perez", "https://www.linkedin.com/in/andre-bernal", "https://www.linkedin.com/in/tim-harrison", "https://www.linkedin.com/in/ozlem-sezginel", "https://www.linkedin.com/in/aparajita-bhattacharyya", "https://www.linkedin.com/in/elisa-garcia", "https://www.linkedin.com/in/jennie-cady", "https://www.linkedin.com/in/nili-shah", "https://www.linkedin.com/in/steve-downs", "https://www.linkedin.com/in/marcela-colmenares", "https://www.linkedin.com/in/prachi-jalan", "https://www.linkedin.com/in/yiyi-cui", "https://www.linkedin.com/in/ismael-camus"]

# Section 1: Current Account Status
st.header("1. Current Account Overview")
account_name = st.selectbox("Account Name", options=["Microsoft"])

st.markdown("**Existing Relationships:**")

# Make the table reactive to the input
if account_name.strip().lower() == "microsoft":
    
    df = pd.DataFrame({
        "Name": contact_names,
        "Role": contact_roles,
        "Team": contact_teams,
        "Email": contact_emails, 
        "Relationship strength": contact_strengths,
        "LinkedIn Action": contact_linkedin # NEW: Pulls directly from the data array
    })
    
    st.dataframe(
        df,
        column_config={
            "LinkedIn Action": st.column_config.LinkColumn(
                "Profile Link",
                display_text="🔗 View Profile" 
            )
