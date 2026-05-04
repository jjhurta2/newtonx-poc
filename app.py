import streamlit as st
import pandas as pd # Needed to create an empty table
from openai import OpenAI
import time

# Set up the page
st.set_page_config(page_title="NewtonX Org Mapper", page_icon="🎯")
st.title("NewtonX CPM Org Mapper")
st.markdown("The stakeholder expansion assistant for Client Partnership Managers.")

# Initialize OpenAI Client (Pulls from Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- DATA SETUP ---
contact_names = ["Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", "Ismael Camus"]
contact_roles = ["Product Manager", "Senior Business Planner", "Senior Account Executive", "AI Agent / Past Core PMM", "Sr. Solution Engineer - Data & AI", "Product Manager", "Product Manager", "Solution Specialist - Azure Data & AI", "Product Manager", "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", "Director, Corporate Business Development", "Senior Product Marketing Manager", "Director Business Planning", "Principal Product Manager", "Senior Business Planner", "Director & Team Lead, Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"]

# UPDATED: Replaced all text values with the numbered formatting
contact_strengths = ["2. Medium", "2. Medium", "1. Weak", "2. Medium", "1. Weak", "2. Medium", "2. Medium", "1. Weak", "2. Medium", "3. Strong", "1. Weak", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "1. Weak", "2. Medium"]

# Section 1: Current Account Status
st.header("1. Current Account Overview")
account_name = st.text_input("Account Name", value="Microsoft")

st.markdown("**Existing Relationships:**")

# Make the table reactive to the input
if account_name.strip().lower() == "microsoft":
    st.dataframe({
        "Name": contact_names,
        "Role": contact_roles,
        "Relationship strength": contact_strengths
    })
else:
    # Show an empty table and a warning if it's not Microsoft
    st.warning(f"No existing CRM records found for '{account_name}'. Displaying empty matrix.")
    st.dataframe(pd.DataFrame(columns=["Name", "Role", "Relationship strength"]))

# Section 2: LinkedIn Scrape & Org Mapping
st.header("2. AI Organization Mapping")
target_department = st.text_input("Which department do you want to expand into?", value="Enterprise AI Solutions")

if st.button("Scrape LinkedIn & Find Bridges"):
    # Prevent running the scrape if they test a blank/different account
    if account_name.strip().lower() != "microsoft":
        st.error("Please select an account with existing relationships (e.g., Microsoft) to map bridges.")
    else:
        with st.spinner(f"Scraping LinkedIn for {target_department} leaders at {account_name}..."):
            time.sleep(2.5)
            
            st.session_state['leads'] = [
                {
                    "name": "Sarah Jenkins",
                    "role": f"VP of {target_department}",
                    "bridge_name": "Aparajita Bhattacharyya",
                    "bridge_role": "GTM Strategy & Monetization Leader",
                    "bridge_strength": "3. Strong", # UPDATED to match new format
                    "rationale": "As a GTM Strategy Leader, Aparajita likely aligns directly with VP-level leaders rolling out new AI solutions."
                },
                {
                    "name": "Marcus Vance",
                    "role": f"Director of {target_department} Integration",
                    "bridge_name": "Steve Downs",
                    "bridge_role": "Principal Product Manager",
                    "bridge_strength": "3. Strong", # UPDATED to match new format
                    "rationale": "Principal PMs frequently collaborate with Integration Directors to execute technical rollouts."
                }
            ]

# Section 3: Display Leads and Generate Outreach
if 'leads' in st.session_state and account_name.strip().lower() == "microsoft":
    st.success(f"Found {len(st.session_state['leads'])} high-value prospects!")
    
    for i, lead in enumerate(st.session_state['leads']):
        st.markdown(f"### Prospect {i+1}: {lead['name']}")
        st.markdown(f"**Title:** {lead['role']}")
        st.markdown(f"🔗 **Best Internal Bridge:** {lead['bridge_name']} ({lead['bridge_role']}) - **Strength:** {lead['bridge_strength']}")
        st.info(f"**AI Mapping Rationale:** {lead['rationale']}")
        
        # --- NEW: Fake LinkedIn Button ---
        # We put the buttons in columns so they sit nicely side-by-side
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.link_button("🌐 View LinkedIn Profile", "https://www.linkedin.com")
            
        with col2:
            generate_email = st.button(f"Generate Outreach Draft", key=f"btn_{i}")

        if generate_email:
            with st.spinner("Drafting personalized outreach..."):
                prompt = f"""
                You are an expert sales strategist for NewtonX.
                Account: {account_name}
                Target Prospect: {lead['name']} ({lead['role']})
                Internal Bridge Contact: {lead['bridge_name']} ({lead['bridge_role']})
                
                Write a short, professional email that the NewtonX CPM can send to {lead['bridge_name']} asking for a warm introduction to {lead['name']}.
                Mention the value NewtonX provides (expert B2B market research and rapid insights) and how it might help the target prospect's department.
                Keep it brief, friendly, and easy for the bridge contact to forward. Do not use placeholders like [Your Name].
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                st.write(response.choices[0].message.content)
        
        st.divider()
