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
contact_names = ["Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", "Ismael Camus"]
contact_roles = ["Product Manager", "Senior Business Planner", "Senior Account Executive", "AI Agent / Past Core PMM", "Sr. Solution Engineer - Data & AI", "Product Manager", "Product Manager", "Solution Specialist - Azure Data & AI", "Product Manager", "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", "Director, Corporate Business Development", "Senior Product Marketing Manager", "Director Business Planning", "Principal Product Manager", "Senior Business Planner", "Director & Team Lead, Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"]

# --- NEW: Added the Team array based on your provided data ---
contact_teams = ["Microsoft FastTrack", "Azure Virtual Desktop", "Public Sector Sales", "Copilot Product Marketing", "Data & AI Customer Success", "Microsoft Teams Core", "Azure Cloud Platform", "Azure Data & AI Specialist Team Unit", "Xbox Cloud Gaming", "Microsoft Marketing Operations", "MCAPS Americas", "Windows Cloud (Windows 365)", "Corporate Business Development", "Surface Commercial Marketing", "Monetization & Strategy", "Azure Virtual Desktop", "Microsoft 365 Business Planning", "Cloud & AI Monetization", "Aspire / University Hires (Marketing)", "Cloud/AI Infra & Investments Strategy"]

contact_strengths = ["2. Medium", "2. Medium", "1. Weak", "2. Medium", "1. Weak", "2. Medium", "2. Medium", "1. Weak", "2. Medium", "3. Strong", "1. Weak", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "3. Strong", "2. Medium", "3. Strong", "1. Weak", "2. Medium"]

# Automatically formats emails: first 2 letters of first name + last name + @microsoft.com
contact_emails = []
for name in contact_names:
    clean_name = name.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ö", "o")
    parts = clean_name.split()
    first_two = parts[0][:2]
    last_name = "".join(parts[1:]) 
    contact_emails.append(f"{first_two}{last_name}@microsoft.com")

# Section 1: Current Account Status
st.header("1. Current Account Overview")
account_name = st.text_input("Account Name", value="Microsoft")

st.markdown("**Existing Relationships:**")

# Make the table reactive to the input
if account_name.strip().lower() == "microsoft":
    
    df = pd.DataFrame({
        "Name": contact_names,
        "Role": contact_roles,
        "Team": contact_teams, # --- NEW: Inserted the Team column here ---
        "Email": contact_emails, 
        "Relationship strength": contact_strengths,
        "LinkedIn Action": ["https://www.linkedin.com"] * len(contact_names) 
    })
    
    st.dataframe(
        df,
        column_config={
            "LinkedIn Action": st.column_config.LinkColumn(
                "Profile Link",
                display_text="🔗 View Profile" 
            )
        },
        hide_index=True,
        use_container_width=True 
    )
else:
    # --- NEW: Updated the empty table layout to include the Team column ---
    st.warning(f"No existing CRM records found for '{account_name}'. Displaying empty matrix.")
    st.dataframe(pd.DataFrame(columns=["Name", "Role", "Team", "Email", "Relationship strength", "Profile Link"]), hide_index=True, use_container_width=True)

# Section 2: LinkedIn Scrape & Org Mapping
st.header("2. AI Organization Mapping")
target_department = st.text_input("Which department do you want to expand into?", value="Enterprise AI Solutions")

if st.button("Scrape LinkedIn & Find Bridges"):
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
                    "bridge_strength": "3. Strong",
                    "linkedin_status": "1st Degree Connection", 
                    "rationale": "As a GTM Strategy Leader, Aparajita likely aligns directly with VP-level leaders rolling out new AI solutions."
                },
                {
                    "name": "Marcus Vance",
                    "role": f"Director of {target_department} Integration",
                    "bridge_name": "Steve Downs",
                    "bridge_role": "Principal Product Manager",
                    "bridge_strength": "3. Strong",
                    "linkedin_status": "2nd Degree Connection (3 Mutuals)", 
                    "rationale": "Principal PMs frequently collaborate with Integration Directors to execute technical rollouts."
                }
            ]

# Section 3: Display Leads and Generate Outreach
if 'leads' in st.session_state and account_name.strip().lower() == "microsoft":
    st.success(f"Found {len(st.session_state['leads'])} high-value prospects!")
    
    for i, lead in enumerate(st.session_state['leads']):
        st.markdown(f"### Prospect {i+1}: {lead['name']}")
        st.markdown(f"**Title:** {lead['role']}")
        st.markdown(f"🔗 **Best Internal Bridge:** {lead['bridge_name']} ({lead['bridge_role']})")
        st.markdown(f"🤝 **LinkedIn Connection Status:** {lead['linkedin_status']}") 
        st.info(f"**AI Mapping Rationale:** {lead['rationale']}")
        
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
                LinkedIn Relationship: {lead['linkedin_status']}
                
                Write a short, professional email that the NewtonX CPM can send to {lead['bridge_name']} asking for an introduction to {lead['name']}.
                
                CRITICAL INSTRUCTION:
                If the LinkedIn Relationship is "1st Degree Connection", explicitly mention in the email that you noticed they are directly connected on LinkedIn. 
                If it is a "2nd Degree Connection", ask if they happen to cross paths or know them internally.
                
                Mention the value NewtonX provides (expert B2B market research and rapid insights) and how it might help the target prospect's department.
                Keep it brief, friendly, and easy for the bridge contact to forward. Do not use placeholders like [Your Name].
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                # Display the draft in a code block with an automatic Copy button
                draft_text = response.choices[0].message.content
                st.markdown("**Outreach Draft:** *(Click the icon in the top right of the box to copy)*")
                st.code(draft_text, language="markdown")
        
        st.divider()
