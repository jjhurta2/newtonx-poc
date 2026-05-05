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
contact_names = [
    "Luis Sande", "Cosme Ochoa", "Francisca Readi Vargas", "Sammy Shen", 
    "Reisel González Pérez", "Delaney Overton", "Hitesh Jonnalagadda", 
    "Natalia Pérez López", "Andre Bernal", "Tim Harrison", "özlem sezginel", 
    "Aparajita Bhattacharyya", "Elisa Garcia", "Jennie Cady", "Nili Shah", 
    "Steve Downs", "Marcela Colmenares Amaya", "Prachi Jalan", "Yiyi Cui", 
    "Ismael Camus"
]

contact_roles = [
    "Product Manager", "Senior Business Planner", "Senior Account Executive", 
    "AI Agent / Past Core PMM", "Sr. Solution Engineer Data & AI", "Product Manager", 
    "Product Manager", "Solution Specialist Azure Data & AI", "Product Manager", 
    "Director of Business Management", "Finance Manager", "GTM Strategy & Monetization Leader", 
    "Director Corporate Business Development", "Senior Product Marketing Manager", 
    "Director Business Planning", "Principal Product Manager", "Senior Business Planner", 
    "Director & Team Lead Monetization Strategy", "Incoming PMM", "Sr. Finance Manager"
]

contact_teams = [
    "Microsoft FastTrack", "Azure Virtual Desktop", "Public Sector Sales", 
    "Copilot Product Marketing", "Data & AI Customer Success", "Microsoft Teams Core", 
    "Azure Cloud Platform", "Azure Data & AI Specialist Team Unit", "Xbox Cloud Gaming", 
    "Microsoft Marketing Operations", "MCAPS Americas", "Windows Cloud", 
    "Corporate Business Development", "Surface Commercial Marketing", "Monetization & Strategy", 
    "Azure Virtual Desktop", "Microsoft 365 Business Planning", "Cloud & AI Monetization", 
    "Aspire / University Hires", "Cloud/AI Infra & Investments Strategy"
]

contact_strengths = [
    "2. Medium", "2. Medium", "1. Weak", "2. Medium", "1. Weak", 
    "2. Medium", "2. Medium", "1. Weak", "2. Medium", "3. Strong", 
    "1. Weak", "3. Strong", "3. Strong", "2. Medium", "3. Strong", 
    "3. Strong", "2. Medium", "3. Strong", "1. Weak", "2. Medium"
]

contact_emails = [
    "lusande@microsoft.com", 
    "coochoa@microsoft.com", 
    "frreadivargas@microsoft.com",
    "sashen@microsoft.com", 
    "regonzalezperez@microsoft.com", 
    "deoverton@microsoft.com",
    "hijonnalagadda@microsoft.com", 
    "naperezlopez@microsoft.com", 
    "anbernal@microsoft.com",
    "tiharrison@microsoft.com", 
    "ozsezginel@microsoft.com", 
    "apbhattacharyya@microsoft.com",
    "elgarcia@microsoft.com", 
    "jecady@microsoft.com", 
    "nishah@microsoft.com",
    "stdowns@microsoft.com", 
    "macolmenaresamaya@microsoft.com", 
    "prjalan@microsoft.com",
    "yicui@microsoft.com", 
    "iscamus@microsoft.com"
]

contact_linkedin = [
    "https://www.linkedin.com/in/luisfelipesande", 
    "https://www.linkedin.com/in/cosme-ochoa",
    "https://www.linkedin.com/in/francisca-readi", 
    "https://www.linkedin.com/in/sammy-shen",
    "https://www.linkedin.com/in/reisel-gonzalez", 
    "https://www.linkedin.com/in/delaneyoverton",
    "https://www.linkedin.com/in/hitesh-jonnalagadda", 
    "https://www.linkedin.com/in/natalia-pérez-lópez-67195167",
    "https://www.linkedin.com/in/andre-bernal", 
    "https://www.linkedin.com/in/timothykharrison",
    "https://www.linkedin.com/in/ozlem-sezginel", 
    "https://www.linkedin.com/in/opub",
    "https://www.linkedin.com/in/elisa-garcia-b8bb2092", 
    "https://www.linkedin.com/in/jennie-cady",
    "https://www.linkedin.com/in/nili-shah", 
    "https://www.linkedin.com/in/steve-downs",
    "https://www.linkedin.com/in/marcela-colmenares", 
    "https://www.linkedin.com/in/prachi-jalan",
    "https://www.linkedin.com/in/yiyi-cui", 
    "https://www.linkedin.com/in/ismael-camus"
]

# Section 1: Current Account Status
st.header("1. Current Account Overview")
account_name = st.selectbox("Account Name", options=["Microsoft"])

st.markdown("**Existing Relationships:**")

if account_name.strip().lower() == "microsoft":
    df = pd.DataFrame({
        "Name": contact_names,
        "Role": contact_roles,
        "Team": contact_teams,
        "Email": contact_emails, 
        "Relationship strength": contact_strengths,
        "LinkedIn Action": contact_linkedin 
    })
    
    st.dataframe(
        df,
        column_config={
            "LinkedIn Action": st.column_config.LinkColumn("Profile Link", display_text="🔗 View Profile")
        },
        hide_index=True,
        use_container_width=True 
    )
else:
    st.warning(f"No existing CRM records found for '{account_name}'. Displaying empty matrix.")
    st.dataframe(pd.DataFrame(columns=["Name", "Role", "Team", "Email", "Relationship strength", "Profile Link"]), hide_index=True, use_container_width=True)

# Section 2: Enterprise Waterfall Discovery
st.header("2. AI Target & Bridge Discovery")
target_department = st.text_input("Which department do you want to expand into?", value="Enterprise AI Solutions")

if st.button("Find Targets & Map Bridges"):
    if account_name.strip().lower() != "microsoft":
        st.error("Please select an account with existing relationships (e.g., Microsoft) to map bridges.")
    else:
        # Visualizing the Waterfall Logic for the presentation
        with st.spinner(f"Querying CRM & Affinity for internal {target_department} contacts..."):
            time.sleep(1.5)
        with st.spinner("1 target found internally. Triggering ZoomInfo for net-new profiles..."):
            time.sleep(1.5)
        with st.spinner("Profiles found. Cross-referencing Affinity metadata to identify internal Bridge contacts..."):
            time.sleep(2.0)
            
            st.session_state['leads'] = [
                {
                    "name": "Sarah Jenkins",
                    "role": f"VP of {target_department}",
                    "bridge_name": "Aparajita Bhattacharyya",
                    "bridge_role": "GTM Strategy & Monetization Leader",
                    "connection_type": "Direct Communication (Affinity)",
                    "connection_score": "88/100 (Strong)", 
                    "rationale": "Affinity captured 14 email exchanges and 2 calendar invites that included both Aparajita and Sarah in the last 6 months."
                },
                {
                    "name": "Marcus Vance",
                    "role": f"Director of {target_department} Integration",
                    "bridge_name": "Steve Downs",
                    "bridge_role": "Principal Product Manager",
                    "connection_type": "Alumni Match (ZoomInfo)",
                    "connection_score": "0/100 (No direct contact)", 
                    "rationale": "No internal email metadata found. Fallback to ZoomInfo match: Both Marcus and Steve worked at Citrix DaaS in 2014."
                },
                {
                    "name": "Chloe Davies",
                    "role": f"Head of {target_department} Operations",
                    "bridge_name": "None (Direct Outreach)",
                    "bridge_role": "N/A",
                    "connection_type": "Cold Outreach (ZoomInfo)",
                    "connection_score": "0/100 (No overlap)", 
                    "rationale": "No internal email metadata found. No heuristic alumni overlap found in ZoomInfo. Recommending direct cold value proposition outreach."
                }
            ]

# Section 3: Display Leads and Generate Outreach
if 'leads' in st.session_state and account_name.strip().lower() == "microsoft":
    st.success(f"Search complete. Found {len(st.session_state['leads'])} high-value prospects.")
    
    for i, lead in enumerate(st.session_state['leads']):
        st.markdown(f"### Prospect {i+1}: {lead['name']}")
        st.markdown(f"**Title:** {lead['role']}")
        st.markdown(f"🔗 **Best Internal Bridge:** {lead['bridge_name']} ({lead['bridge_role']})")
        st.markdown(f"📊 **Connection Type:** {lead['connection_type']}") 
        st.info(f"**Mapping Rationale:** {lead['rationale']}")
        
        generate_email = st.button(f"Generate Outreach Draft", key=f"btn_{i}")

        if generate_email:
            with st.spinner("Synthesizing relationship context into personalized outreach..."):
                prompt = f"""
                You are an elite sales strategist for NewtonX.
                Account: {account_name}
                Target Prospect: {lead['name']} ({lead['role']})
                Bridge Contact (Your existing relationship at the account): {lead['bridge_name']} ({lead['bridge_role']})
                Connection Type: {lead['connection_type']}
                Relationship Details: {lead['rationale']}
                
                INSTRUCTIONS BASED ON CONNECTION TYPE:
                
                Scenario A: "Direct Communication (Affinity)"
                Task: Write an email to the Bridge Contact asking them to introduce you to the Target Prospect.
                Structure: Acknowledge you saw they recently interacted/met with the Target (use the Relationship Details). Explain briefly why you want to connect with the Target (to share NewtonX's rapid insights value). Ask if they'd be willing to pass along a short intro.
                Tone: Direct, friendly, and casual. Strictly avoid overly formal, stiff, or passive-aggressive phrasing. Speak to them as a familiar industry partner.
                
                Scenario B: "Alumni Match (ZoomInfo)"
                Task: Write an email to the Bridge Contact asking for an introduction to the Target Prospect.
                Structure: Mention that you are trying to reach the Target, and noticed they both worked at the specific past company mentioned in the Relationship Details. Ask if they actually knew each other there and if they'd feel comfortable making a warm intro. Give them an easy out if they don't actually know them well.
                Tone: Direct, friendly, and casual. Strictly avoid overly formal, stiff, or passive-aggressive phrasing.
                
                Scenario C: "Cold Outreach (ZoomInfo)"
                Task: Write a cold email DIRECTLY to the Target Prospect. (Do NOT address the Bridge Contact).
                Structure: Hook them with a challenge relevant to their specific department. Introduce NewtonX as the solution for B2B market research and rapid expert insights. Include a soft call to action.
                Tone: Professional, concise, compelling, and organizational-focused rather than overly intimate.
                
                CRITICAL RULES FOR ALL SCENARIOS:
                - Write ONLY the email body. Do not include subject lines.
                - Do not use bracketed placeholders like [Your Name] or [Link].
                - Keep it under 100 words.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                draft_text = response.choices[0].message.content
                st.markdown("**Outreach Draft:** *(Click the icon in the top right of the box to copy)*")
                st.code(draft_text, language="markdown")
        
        st.divider()
