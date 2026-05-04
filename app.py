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
    "Name": ["Sarah Jenkins", "David Chen", "Elena Rodriguez"],
    "Role": ["Director of Product Marketing", "VP of Research & Insights", "Sr. Manager, Cloud Strategy"],
    "Relationship Strength": ["Strong", "Medium", "Weak (1 call)"]
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
        Current Contacts: Sarah Jenkins (Dir. Product Marketing), David Chen (VP Research & Insights), Elena Rodriguez (Sr. Manager Cloud Strategy).
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
