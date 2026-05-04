import streamlit as st
from openai import OpenAI
import time # Added to create a fake loading delay for the "scrape"

# Set up the page
st.set_page_config(page_title="NewtonX Org Mapper", page_icon="🎯")
st.title("NewtonX Dynamic Org Mapper")
st.markdown("Automating stakeholder expansion for Client Partnership Managers.")

# Initialize OpenAI Client (Pulls from Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- DATA SETUP ---
# Stored as lists to easily power the table and the AI logic
contact_names = ["Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", "Ismael Camus"]
contact_roles = ["Product Manager", "Senior Business Planner", "Senior Account Executive", "AI Agent / Past Core PMM", "Sr. Solution Engineer - Data & AI", "Product Manager", "Product Manager", "Solution Specialist - Azure Data & AI", "Product Manager", "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", "Director, Corporate Business Development", "Senior Product Marketing Manager", "Director Business Planning", "Principal Product Manager", "Senior Business Planner", "Director & Team Lead, Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"]
contact_strengths = ["Medium", "Medium", "Weak", "Medium", "Weak", "Medium", "Medium", "Weak", "Medium", "Strong", "Weak", "Strong", "Strong", "Medium", "Strong", "Strong", "Medium", "Strong", "Weak", "Medium"]

# Section 1: Current Account Status
st.header("1. Current Account Overview")
account_name = st.text_input("Account Name", value="Microsoft")

st.markdown("**Existing Relationships:**")
# Swapped to st.dataframe so the 20 contacts are easily scrollable
st.dataframe({
    "Name": contact_names,
    "Role": contact_roles,
    "Relationship strength": contact_strengths
})

# Section 2: LinkedIn Scrape & Org Mapping
st.header("2. AI Organization Mapping")
target_department = st.text_input("Which department do you want to expand into?", value="Enterprise AI Solutions")

# We use a button to trigger the "scrape"
if st.button("Scrape LinkedIn & Find Bridges"):
    with st.spinner(f"Scraping LinkedIn for {target_department} leaders at {account_name}..."):
        time.sleep(2.5) # Pauses for 2.5 seconds to make it feel like real scraping
        
        # We store these fake leads in session_state so they don't disappear when we click other buttons later
        st.session_state['leads'] = [
            {
                "name": "Sarah Jenkins",
                "role": f"VP of {target_department}",
                "bridge_name": "Aparajita Bhattacharyya",
                "bridge_role": "GTM Strategy & Monetization Leader",
                "bridge_strength": "Strong",
                "rationale": "As a GTM Strategy Leader, Aparajita likely aligns directly with VP-level leaders rolling out new AI solutions."
            },
            {
                "name": "Marcus Vance",
                "role": f"Director of {target_department} Integration",
                "bridge_name": "Steve Downs",
                "bridge_role": "Principal Product Manager",
                "bridge_strength": "Strong",
                "rationale": "Principal PMs frequently collaborate with Integration Directors to execute technical rollouts."
            }
        ]

# Section 3: Display Leads and Generate Outreach
# This checks if we have already "scraped" the leads
if 'leads' in st.session_state:
    st.success(f"Found {len(st.session_state['leads'])} high-value prospects!")
    
    # Loop through each lead and create their own section
    for i, lead in enumerate(st.session_state['leads']):
        st.markdown(f"### Prospect {i+1}: {lead['name']}")
        st.markdown(f"**Title:** {lead['role']}")
        st.markdown(f"🔗 **Best Internal Bridge:** {lead['bridge_name']} ({lead['bridge_role']}) - **Strength:** {lead['bridge_strength']}")
        st.info(f"**AI Mapping Rationale:** {lead['rationale']}")
        
        # We give the button a unique key based on the loop index (i) so Streamlit doesn't get confused
        if st.button(f"Generate Outreach Draft to {lead['bridge_name']}", key=f"btn_{i}"):
            with st.spinner("Drafting personalized outreach..."):
                
                # The updated prompt focuses entirely on one specific lead and bridge
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
                
                # Display the AI generated email
                st.write(response.choices[0].message.content)
        
        # Add a visual divider between prospects
        st.divider()
