import streamlit as st
from openai import OpenAI
import os

# Set up the page
st.set_page_config(page_title="NewtonX Org Mapper", page_icon="🎯")
st.title("🎯 NewtonX Dynamic Org Mapper POC")
st.markdown("Automating stakeholder expansion for Client Partnership Managers.")

# Initialize OpenAI Client (Pulls from Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Section 1: Current Account Status (Dummy Data)
st.header("1. Current Account Overview")
account_name = st.text_input("Account Name", value="Microsoft")

st.markdown("**Existing Relationships:**")
# Using a table to cleanly display our dummy existing contacts
st.table({
    "Name": ["Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", "Ismael Camus"],
    "Role": ["Product Manager", "Senior Business Planner", "Senior Account Executive", "AI Agent / Past Core PMM", "Sr. Solution Engineer - Data & AI", "Product Manager", "Product Manager", "Solution Specialist - Azure Data & AI", "Product Manager", "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", "Director, Corporate Business Development", "Senior Product Marketing Manager", "Director Business Planning", "Principal Product Manager", "Senior Business Planner", "Director & Team Lead, Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"],
    "Relationship strength": ["Medium", "Medium", "Weak", "Medium", "Weak", "Medium", "Medium", "Weak", "Medium", "Strength", "Weak", "Strength", "Strength", "Medium", "Strength", "Strength", "Medium", "Strength", "Weak", "Medium"]
})

# Section 2: Expansion Target
st.header("2. Identify Expansion Target")
target_department = st.text_input("Which department do you want to expand into?", value="Enterprise AI Solutions")

# Section 3: AI Generation
if st.button("Generate Expansion Strategy"):
    with st.spinner("Mapping the organization..."):
        
        prompt = f"""
        You are an expert sales strategist for NewtonX.
        Account: {account_name}
        Current Contacts: Luis Sande (Product Manager), Cosme Ochoa (Senior Business Planner), Francisca Readi Vargas (Senior Account Executive), Sammy Shen (AI Agent / Past Core PMM), Reisel González Pérez (Sr. Solution Engineer - Data & AI), Delaney Overton (Product Manager), Hitesh Jonnalagadda (Product Manager), Natalia Pérez López (Solution Specialist - Azure Data & AI), Andre Bernal (Product Manager), Tim Harrison (Director of Business Management), özlem sezginel (Finance Manager), Aparajita Bhattacharyya (GTM Strategy & Monetization Leader), Elisa Garcia (Director, Corporate Business Development), Jennie Cady (Senior Product Marketing Manager), Nili Shah (Director Business Planning), Steve Downs (Principal Product Manager), Marcela Colmenares Amaya (Senior Business Planner), Prachi Jalan (Director & Team Lead, Monetization Strategy), Yiyi Cui (Incoming PMM), Ismael Camus (Sr. Finance Manager).
        Target Expansion Area: {target_department}
        
        Provide the following:
        1. Key Roles to Target: List 3 specific job titles we should search for in the {target_department} department.
        2. The Bridge: Which of our current contacts is best positioned to introduce us to this new department, and why?
        3. Outreach Draft: A short, professional email the CPM can send to that 'Bridge' contact asking for the introduction, mentioning the value NewtonX provides.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        st.success("Analysis Complete!")
        st.write(response.choices[0].message.content)
