import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# 🔐 Load local environment variables (for your local desktop testing)
load_dotenv()

# 🌐 Streamlit Cloud Configuration (Attempts to read cloud secrets first, drops back to local .env)
api_key = st.secrets.get("AI_NATIVE_API_KEY") or os.getenv("AI_NATIVE_API_KEY")

# 🖥️ Streamlit UI Page Layout Configuration
st.set_page_config(
    page_title="Multi-Agent Marketing Bureau",
    page_icon="🚀",
    layout="wide"
)

# Sidebar Branding & Credentials Setup
st.sidebar.title("🔐 Control Panel")
st.sidebar.markdown("---")
if not api_key:
    st.sidebar.error("⚠️ AI_NATIVE_API_KEY Not Found!")
    st.sidebar.info("If running locally, check your .env file. If deployed to the cloud, configure your Streamlit Secrets panel.")
else:
    st.sidebar.success("🔑 API Authentication Verified.")

st.sidebar.markdown("""
### 🧠 Active Bureau Agents:
1. **Senior Data Analyst**
2. **Creative Copywriter & DR Architect**
3. **Performance Media Buyer**
""")

# Main Dashboard Headings
st.title("🚀 Multi-Agent Performance Marketing Bureau")
st.subheader("Transform raw ad spreadsheets into execution assets and budget reallocations instantly.")
st.markdown("---")

# 📊 1. File Uploader Interface Element
uploaded_file = st.file_uploader(
    "Upload your raw performance spreadsheet (Excel .xlsx format):", 
    type=["xlsx"]
)

if uploaded_file is not None and api_key:
    st.success("📂 Spreadsheet successfully staged for extraction.")
    
    # 2. Add an Action Trigger Button
    if st.button("🚀 Kickoff Multi-Agent Studio Run", type="primary"):
        
        with st.status("🎬 Crew assembled. Executing analytical pipeline...", expanded=True) as status:
            
            # --- PANDAS EXTRACTION LAYER ---
            status.write("📊 Extracting and processing spreadsheet metrics...")
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
                EXCEL_DATA_CONTEXT = "\n".join(data_lines)
            except Exception as e:
                st.error(f"Data processing error: {str(e)}")
                st.stop()
                
            # --- LLM ENDPOINT LAYER ---
            status.write("🧠 Securing AI Native endpoint pipelines...")
            custom_llm = LLM(
                model="openai/gpt-4o",
                api_key=api_key,
                base_url="https://api.ainative.studio/v1"
            )
            
            # --- AGENT DECLARATIONS ---
            status.write("🤖 Deploying agent neural states...")
            analyst_agent = Agent(
                role="Senior Data Analyst",
                goal="Audit the verified data metrics to isolate performance anomalies and top conversion engines.",
                backstory="""You are an elite, mathematical digital media auditor. You analyze the exact figures 
                provided to you to determine which platforms require tactical budget changes.""",
                verbose=True,
                llm=custom_llm
            )

            creative_agent = Agent(
                role="Expert Creative Copywriter & Direct Response Architect",
                goal="""Translate verified data into native, platform-specific ad copy fields and layout structured, 
                asset-ready storyboards across Meta, Google, and Amazon ecosystems.""",
                backstory="""You are a master of high-converting multi-channel asset creation. You know how to tailor messaging 
                to fit Meta's emotional hook frameworks, Google's search intent/PMax character bounds, and Amazon's high-intent commercial headlines.""",
                verbose=True,
                llm=custom_llm
            )

            media_buyer_agent = Agent(
                role="Expert Performance Media Buyer",
                goal="Design portfolio distribution architectures and budget pacing strategies based strictly on verified performance figures.",
                backstory="""You are a quantitative media buyer. You evaluate performance data to determine where to scale 
                spend aggressively and where to trim waste safely.""",
                verbose=True,
                llm=custom_llm
            )
            
            # --- TASK DEFINITIONS WITH EXACT CONSTRAINTS ---
            status.write("📋 Injecting cross-channel execution directives...")
            analysis_task = Task(
                description=f"""Analyze the following verified metric breakdown extracted directly from the performance spreadsheet:
                
                {EXCEL_DATA_CONTEXT}
                
                Build a strategic data audit detailing performance efficiency and identifying the clear mathematical winners and losers based on ROAS and CPA volume variance.""",
                expected_output="""An exact mathematical audit report profiling each platform's real efficiency ranking.""",
                agent=analyst_agent
            )

            creative_task = Task(
                description="""Review the raw metrics and the Senior Analyst's audit findings. Target the channels with high-impact, data-driven creative variations customized for native platform interfaces:

                You must generate the creative output in four distinct, production-ready configurations:
                
                1. META DIRECT-RESPONSE COPY VARIATIONS: 
                   Produce 2 distinct copy variations formatted using Meta's field architecture:
                   - [Primary Text]: Long/short hook, core body value proposition, and explicit Call to Action.
                   - [Headline]: Punchy, action-oriented, under-40-character headline.
                   - [Description]: Social proof, guarantee, or urgency metric line.

                2. GOOGLE ADS RESPONSIVE SEARCH / PMAX ASSETS:
                   Produce copy variants that strictly adhere to character maximum limits:
                   - [Headlines (Provide 4 variants)]: Maximum 30 characters each. Must highlight pain points, benefits, and call to action.
                   - [Long Headlines (Provide 2 variants)]: Maximum 90 characters each for Display or Performance Max asset placement.
                   - [Descriptions (Provide 2 variants)]: Maximum 90 characters each detailing specific utility, credibility, or key offers.

                3. AMAZON SPONSORED BRANDS HEADLINES & VISUAL FRAMING:
                   Produce copy assets customized for transactional shopper intent:
                   - [Sponsored Brands Headline (Provide 2 variants)]: Maximum 50 characters each. Must be benefit-driven and comply with Amazon advertising policy (no unsubstantiated superlative claims).
                   - [Creative Asset Direction]: Provide specific aesthetic guidance for the custom image or lifestyle background design to maximize Storefront click-through rates.

                4. DESIGN TEAM STORYBOARD TABLE:
                   Build a comprehensive video storyboard organized inside a Markdown Table for a 30-second cross-channel video/reel concept. It must contain exactly these 4 columns:
                   | Scene / Timestamp | Visual Blueprint (What to design, framing, action, or stock requirement) | Audio & Voiceover (Scripted dialogue or sound effect prompts) | On-Screen Text Overlays (Exact typography/captions to render) |""",
                expected_output="""A comprehensive multi-channel copy portfolio organized by platform (Meta, Google, Amazon) 
                containing field-specific text variations, followed by a unified Markdown Storyboard Table for the production queue.""",
                agent=creative_agent,
                context=[analysis_task]
            )

            media_buy_task = Task(
                description=f"""Review the raw metric context below alongside the previous task analysis findings:
                
                {EXCEL_DATA_CONTEXT}
                
                CRITICAL ALLOCATION GUARDRAILS: 
                1. You MUST quote the exact ROAS, Spend, and CPA numbers inside your final strategy document. Do NOT use generic placeholders or hypothetical metrics.
                2. Your channel distribution breakdown must explicitly match the real performance hierarchy shown in the data.
                3. CONDITIONAL REALLOCATION RULE: If any campaign exhibits a ROAS below a break-even threshold of 2.0x, or exhibits a CPA significantly higher than its platform average (such as Sponsored_Products_Core), you are strictly mandated to propose slashing its allocation to a maintenance budget (0-5%) and immediately reallocating those surplus funds directly into the top 2 highest-performing scale campaigns.""",
                expected_output="""A mathematically grounded Media Buying Blueprint detailing: 
                1. Real Channel Allocation Splits applying the conditional guardrail rules, 
                2. Granular Audience Targeting profiles for the winning channels, and 
                3. A data-backed 30-day scaling timeline quoting exact metrics.""",
                agent=media_buyer_agent,
                context=[analysis_task, creative_task]
            )
            
            # --- CREW ASSEMBLE & RUN ---
            status.write("🚀 Media Studio executing core algorithmic cycle...")
            marketing_crew = Crew(
                agents=[analyst_agent, creative_agent, media_buyer_agent],
                tasks=[analysis_task, creative_task, media_buy_task],
                verbose=True
            )
            
            final_strategy_output = marketing_crew.kickoff()
            status.update(label="✅ Run Complete! Deep Growth Report Assembled Below.", state="complete")
        
        # --- DISPLAY FINAL STRATEGIC OUTPUTS NATIVELY ---
        st.markdown("## 🎯 Final Hardened Growth Strategy & Asset Pack")
        st.markdown(str(final_strategy_output))
        
        # Add a file download button for the design/media buying team
        st.download_button(
            label="💾 Download Full Strategic Document (.md)",
            data=str(final_strategy_output),
            file_name="Automated_Growth_Strategy_2026.md",
            mime="text/markdown"
        )
else:
    if not uploaded_file:
        st.info("💡 Ready and waiting. Drop your weekly performance `.xlsx` file above to begin.")
