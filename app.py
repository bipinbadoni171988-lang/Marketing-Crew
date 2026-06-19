import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# 🔐 Load local environment variables
load_dotenv()

# 🌐 Streamlit Cloud Configuration
api_key = st.secrets.get("AI_NATIVE_API_KEY") or os.getenv("AI_NATIVE_API_KEY")

st.set_page_config(
    page_title="Interactive Multi-Agent Bureau",
    page_icon="🚀",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION (App Memory) ---
if "final_output" not in st.session_state:
    st.session_state.final_output = None
if "excel_context" not in st.session_state:
    st.session_state.excel_context = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar UI
st.sidebar.title("🔐 Control Panel")
st.sidebar.markdown("---")
if not api_key:
    st.sidebar.error("⚠️ AI_NATIVE_API_KEY Not Found!")
else:
    st.sidebar.success("🔑 API Authentication Verified.")

st.sidebar.markdown("""
### 🧠 Active Bureau Agents:
1. **Senior Data Analyst** (Auditor)
2. **Creative Copywriter** (DR Architect)
3. **Performance Media Buyer** (Strategist)
""")

# Reset button to clear state and upload a new file
if st.sidebar.button("🧹 Clear Workspace & Start Fresh"):
    st.session_state.final_output = None
    st.session_state.excel_context = ""
    st.session_state.chat_history = []
    st.rerun()

st.title("🚀 Multi-Agent Performance Marketing Bureau")
st.subheader("Transform raw spreadsheets into granular assets, then chat with your crew to refine outputs.")
st.markdown("---")

# 📊 1. File Uploader Interface
uploaded_file = st.file_uploader(
    "Upload your raw performance spreadsheet (Excel .xlsx format):", 
    type=["xlsx"]
)

if uploaded_file is not None and api_key:
    # Only parse if we haven't already processed this session
    if not st.session_state.excel_context:
        try:
            df = pd.read_excel(uploaded_file)
            summary = df.groupby(['Platform', 'Campaign']).agg({
                'Impressions': 'sum',
                'Clicks': 'sum',
                'Spend': 'sum',
                'Conversions': 'sum',
                'Revenue': 'sum'
            }).reset_index()
            
            summary['CTR'] = (summary['Clicks'] / summary['Impressions']) * 100
            summary['CPC'] = summary['Spend'] / summary['Clicks']
            summary['CPA'] = summary['Spend'] / summary['Conversions']
            summary['ROAS'] = summary['Revenue'] / summary['Spend']
            
            data_lines = []
            for _, row in summary.iterrows():
                data_lines.append(
                    f"Platform: {row['Platform']} | Campaign: {row['Campaign']}\n"
                    f"  - Spend: ${row['Spend']:,} | Revenue: ${row['Revenue']:,} | ROAS: {row['ROAS']:.2f}x\n"
                    f"  - Clicks: {row['Clicks']:,} | CTR: {row['CTR']:.2f}% | CPC: ${row['CPC']:.2f} | CPA: ${row['CPA']:.2f}"
                )
            st.session_state.excel_context = "\n".join(data_lines)
            st.success("📂 Data successfully processed into memory context.")
        except Exception as e:
            st.error(f"Data processing error: {str(e)}")
            st.stop()

    # 2. Trigger Main Crew Run (If not already run)
    if st.session_state.final_output is None:
        if st.button("🚀 Kickoff Multi-Agent Studio Run", type="primary"):
            with st.status("🎬 Crew assembled. Executing deep analytical pipeline...", expanded=True) as status:
                
                custom_llm = LLM(
                    model="openai/gpt-4o",
                    api_key=api_key,
                    base_url="https://api.ainative.studio/v1"
                )
                
                # Agents
                analyst_agent = Agent(
                    role="Senior Data Analyst",
                    goal="Perform deep operational financial audits on multi-channel marketing campaigns.",
                    backstory="You are an elite, mathematical digital media auditor. You analyze raw performance metrics down to decimal precision to isolate conversion leaks, high margin engines, and capital waste.",
                    verbose=True,
                    llm=custom_llm
                )

                creative_agent = Agent(
                    role="Expert Creative Copywriter & Direct Response Architect",
                    goal="Translate campaign datasets into comprehensive, psychologically-hooked marketing assets across multiple channels.",
                    backstory="You are a veteran master of direct-response asset creation. You structure frameworks targeting specific demographics, strictly adhering to character limits and compliance boundaries while driving maximum CTR.",
                    verbose=True,
                    llm=custom_llm
                )

                media_buyer_agent = Agent(
                    role="Expert Performance Media Buyer",
                    goal="Design advanced portfolio budget distribution architectures and optimization timelines based entirely on performance efficiency.",
                    backstory="You manage millions in ad spend. You use data to make ruthless budget allocation adjustments, scale high-ROAS hooks, and implement structural testing roadmaps.",
                    verbose=True,
                    llm=custom_llm
                )
                
                # Deeper, More Detailed Tasks
                analysis_task = Task(
                    description=f"Analyze this raw performance breakdown:\n\n{st.session_state.excel_context}\n\nIdentify performance anomalies. Calculate platform-wide aggregate performance averages and rank every single campaign from highest efficiency to lowest. Highlight exactly which ad dollars are driving profitable growth and which are generating systemic waste.",
                    expected_output="An extensive mathematical audit report analyzing channel variances, cost inefficiencies, and top-performing data hubs.",
                    agent=analyst_agent
                )

                creative_task = Task(
                    description="""Review the raw dataset and the Analyst's audit. Generate a comprehensive asset pack with exhaustive detail across four distinct segments:
                    
                    1. META DIRECT-RESPONSE ASSETS: Provide 2 highly detailed variations. Each must explicitly break out:
                       - [Psychological Angle/Hook]: Explain the target emotional trigger.
                       - [Primary Text]: Long-form narrative copy with inline hooks and pain points.
                       - [Headline]: Action-oriented, scannable line under 40 characters.
                       - [Description]: Social proof or trust-building metrics.
                    
                    2. GOOGLE ADS RESPONSIVE TEXT: Provide 4 distinct 30-character headlines, 2 distinct 90-character long headlines, and 2 distinct 90-character description fields. Avoid generic phrases; embed real utility.
                    
                    3. AMAZON SPONSORED BRANDS: Provide 2 high-intent product headlines capped at 50 characters, plus granular, step-by-step visual style guides for lifestyle backgrounds to maximize storefront traffic.
                    
                    4. CREATIVE PRODUCTION STORYBOARD: Build a highly detailed 4-column Markdown Table outlining a 30-second high-impact video script. Detail visual directions, frame styles, camera adjustments, audio/SFX cues, and precise typographical on-screen text overlays scene-by-scene.""",
                    expected_output="A high-density copy portfolio across Meta, Google, and Amazon platforms alongside a complete visual design storyboard matrix.",
                    agent=creative_agent,
                    context=[analysis_task]
                )

                media_buy_task = Task(
                    description=f"""Using the raw context:\n\n{st.session_state.excel_context}\n\nBuild an elite 30-day scaling blueprint. 
                    - You must quote the exact ROAS, CPA, and Spend metrics from the data.
                    - Formulate precise budget adjustments using this rule: If any campaign displays a ROAS under 2.0x or a CPA significantly higher than platform average, slash its budget allocation to a 5% maintenance budget and immediately reallocate that capital into the top 2 highest-performing campaigns.
                    - Build exhaustive demographic and psychographic targeting outlines for the winning channels. Provide a granular week-by-week optimization schedule for the next 30 days.""",
                    expected_output="An operational media buying blueprint with exact budget reallocations, advanced target parameters, and a step-by-step scaling timeline.",
                    agent=media_buyer_agent,
                    context=[analysis_task, creative_task]
                )

                # Execute
                marketing_crew = Crew(
                    agents=[analyst_agent, creative_agent, media_buyer_agent],
                    tasks=[analysis_task, creative_task, media_buy_task],
                    verbose=True
                )
                
                output = marketing_crew.kickoff()
                st.session_state.final_output = str(output)
                status.update(label="✅ Strategy Assembled!", state="complete")
            st.rerun()

    # --- DISPLAY COMPREHENSIVE GENERATED REPORT ---
    if st.session_state.final_output is not None:
        st.markdown("## 🎯 Base Deep Growth Strategy & Asset Pack")
        st.markdown(st.session_state.final_output)
        
        st.download_button(
            label="💾 Download Strategic Asset Pack (.md)",
            data=st.session_state.final_output,
            file_name="Deep_Growth_Strategy_2026.md",
            mime="text/markdown"
        )
        
        st.markdown("---")
        st.markdown("## 💬 Interactive Workspace: Task Your Bureau")
        st.markdown("Use this terminal to issue follow-up commands to your crew. You can ask them to iterate on the copy above, build alternative budget models, or generate complementary execution scripts.")

        # Display conversational log
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input Element for Interactive Tasks
        if user_command := st.chat_input("Ex: 'Rewrite Meta Variation 1 to be funny' or 'Build a negative keyword list for Google Ads'"):
            # Render user input
            with st.chat_message("user"):
                st.markdown(user_command)
            st.session_state.chat_history.append({"role": "user", "content": user_command})

            # Process follow-up task using the core LLM engine backed by data context
            with st.spinner("Agents are executing follow-up task..."):
                follow_up_llm = LLM(
                    model="openai/gpt-4o",
                    api_key=api_key,
                    base_url="https://api.ainative.studio/v1"
                )
                
                # Constructing full contextual memory payload
                system_prompt = f"""You are the director of the Multi-Agent Marketing Bureau. 
                You have access to the raw tracking data:
                {st.session_state.excel_context}
                
                And you have access to the primary strategy report generated by your crew:
                {st.session_state.final_output}
                
                Execute the user's follow-up request with absolute detail, analytical rigor, and execution-ready precision."""
                
                response = follow_up_llm.call(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_command}
                    ]
                )
                
                # Render agent response
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
