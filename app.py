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
    page_title="Multi-Agent Growth & Brand Studio",
    page_icon="🚀",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if "performance_output" not in st.session_state:
    st.session_state.performance_output = None
if "brand_output" not in st.session_state:
    st.session_state.brand_output = None
if "coo_output" not in st.session_state:
    st.session_state.coo_output = None
if "excel_context" not in st.session_state:
    st.session_state.excel_context = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- SIDEBAR CONTROL PANEL & ENGINE SWITCHER ---
st.sidebar.title("🔐 Control Panel")
st.sidebar.markdown("---")

if not api_key:
    st.sidebar.error("⚠️ AI_NATIVE_API_KEY Not Found!")
else:
    st.sidebar.success("🔑 API Authentication Verified.")

st.sidebar.markdown("### 🛠️ Select Workspace Engine")
studio_mode = st.sidebar.radio(
    "Choose your operational workflow:",
    [
        "📊 Performance Optimizer", 
        "✨ Brand Creation Studio",
        "🏔️ Live Operations Tower (Virtual COO)"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Active Workspace"):
    st.session_state.performance_output = None
    st.session_state.brand_output = None
    st.session_state.coo_output = None
    st.session_state.excel_context = ""
    st.session_state.chat_history = []
    st.rerun()

# Shared core LLM setup
if api_key:
    custom_llm = LLM(
        model="openai/gpt-4o",
        api_key=api_key,
        base_url="https://api.ainative.studio/v1"
    )

# ==============================================================================
# ENGINE 1: PERFORMANCE OPTIMIZER
# ==============================================================================
if studio_mode == "📊 Performance Optimizer":
    st.title("🚀 Performance Marketing Optimization Bureau")
    st.subheader("Turn spreadsheet tracking data into direct-response copy and scaling blueprints.")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload raw weekly spreadsheet (Excel .xlsx format):", 
        type=["xlsx"]
    )

    if uploaded_file is not None and api_key:
        if not st.session_state.excel_context:
            try:
                df = pd.read_excel(uploaded_file)
                summary = df.groupby(['Platform', 'Campaign']).agg({
                    'Impressions': 'sum', 'Clicks': 'sum', 'Spend': 'sum', 'Conversions': 'sum', 'Revenue': 'sum'
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
                        f"  - CPA: ${row['CPA']:.2f} | CTR: {row['CTR']:.2f}%"
                    )
                st.session_state.excel_context = "\n".join(data_lines)
                st.success("📂 Data successfully compiled into context memory.")
            except Exception as e:
                st.error(f"Data processing error: {str(e)}")
                st.stop()

        if st.session_state.performance_output is None:
            if st.button("🚀 Kickoff Optimization Run", type="primary"):
                with st.status("🎬 Assembling performance crew...", expanded=True) as status:
                    
                    analyst = Agent(
                        role="Senior Data Analyst",
                        goal="Audit quantitative marketing figures to maximize capital yield.",
                        backstory="An elite media auditor who identifies performance anomalies, scaling hubs, and capital waste.",
                        verbose=True, llm=custom_llm
                    )
                    copywriter = Agent(
                        role="Expert Creative Copywriter & Direct Response Architect",
                        goal="Structure direct-response asset variations mapped to user demographic behavior.",
                        backstory="A veteran copy chief specializing in high-CTR angles, character-capped networks, and step-by-step video storyboards.",
                        verbose=True, llm=custom_llm
                    )
                    media_buyer = Agent(
                        role="Expert Performance Media Buyer",
                        goal="Deploy mathematical scaling parameters and budget reallocations based on performance.",
                        backstory="A systematic growth buyer handling programmatic channel mapping and rigorous optimization cycles.",
                        verbose=True, llm=custom_llm
                    )

                    t1 = Task(
                        description=f"Perform a comprehensive financial audit on this data:\n\n{st.session_state.excel_context}\n\nRank efficiency by ROAS and flag underperforming units.",
                        expected_output="A quantitative performance report mapping platform efficiency metrics.",
                        agent=analyst
                    )
                    t2 = Task(
                        description="Generate an execution asset pack containing 2 multi-field Meta variants, 4 responsive Google text headlines, and a detailed 4-column video storyboard table.",
                        expected_output="A production-ready direct response copy portfolio and layout matrix.",
                        agent=copywriter, context=[t1]
                    )
                    t3 = Task(
                        description=f"Using data context:\n\n{st.session_state.excel_context}\n\nPropose explicit channel reallocations. Enforce maintenance spend limits on high-CPA targets and map out a 30-day scaling calendar.",
                        expected_output="An operational media buying roadmap with exact tracking parameters.",
                        agent=media_buyer, context=[t1, t2]
                    )

                    crew = Crew(agents=[analyst, copywriter, media_buyer], tasks=[t1, t2, t3], verbose=True)
                    st.session_state.performance_output = str(crew.kickoff())
                    status.update(label="✅ Optimization Blueprint Complete!", state="complete")
                st.rerun()

        if st.session_state.performance_output:
            st.markdown("## 🎯 Base Optimization Strategy & Asset Pack")
            st.markdown(st.session_state.performance_output)
            st.download_button("💾 Download Asset Pack (.md)", st.session_state.performance_output, "Optimization_Strategy.md", "text/markdown")

# ==============================================================================
# ENGINE 2: BRAND CREATION STUDIO
# ==============================================================================
elif studio_mode == "✨ Brand Creation Studio":
    st.title("✨ Brand Innovation & Incubation Workspace")
    st.subheader("Build a market-disrupting brand identity, core messaging architecture, and visual direction from scratch.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        input_brand_idea = st.text_input("Brand Working Name / Functional Idea:", placeholder="e.g., 'AuraSleep' or 'An eco-friendly custom running shoe network'")
        input_industry = st.text_input("Industry / Vertical Market Niche:", placeholder="e.g., 'B2C Direct-to-Consumer Wellness technology'")
    with col2:
        input_audience = st.text_input("Primary Target Audience / Demographic Anchor:", placeholder="e.g., 'Overworked corporate professionals ages 30-45 dealing with mild insomnia'")
        input_value_prop = st.text_area("Core Product Superpower / Foundational Problem Solved:", placeholder="e.g., 'Uses biometric lightweight tech woven into sheets to regulate temperature and trigger deep sleep cycles without supplements.'")

    input_competitors = st.text_input("Known Competitors or Market Paradigms to Disrupt:", placeholder="e.g., 'Eight Sleep, Casper, traditional sleep tracking wearables'")

    if st.session_state.brand_output is None:
        if st.button("✨ Incubate Brand Identity", type="primary"):
            if not (input_industry and input_audience and input_value_prop):
                st.error("⚠️ Please fill out at least Industry, Target Audience, and Core Superpower to guide the creation process.")
            elif api_key:
                with st.status("🧪 Incubating brand architecture components...", expanded=True) as status:
                    
                    brand_strategist = Agent(
                        role="Principal Brand Strategist & Market Architect",
                        goal="Formulate high-leverage brand positioning, market whitespace definition, and strategic positioning models.",
                        backstory="A world-class consumer strategist who identifies market gaps and designs long-term product positioning architectures.",
                        verbose=True, llm=custom_llm
                    )
                    verbal_architect = Agent(
                        role="Verbal Identity Architect & Master Copywriter",
                        goal="Create unforgettable brand terminology, foundational tone guidelines, taglines, and messaging matrices.",
                        backstory="An expert wordsmith who builds core identity narratives, values framing, and platform brand guides.",
                        verbose=True, llm=custom_llm
                    )
                    visual_director = Agent(
                        role="Visual Identity & Design Director",
                        goal="Translate brand narratives into explicit visual frameworks, color strategy logic, and creative production prompts.",
                        backstory="An avant-garde creative director who designs color systems, typographical hierarchies, and descriptive generative prompts for physical/digital products.",
                        verbose=True, llm=custom_llm
                    )

                    b_task1 = Task(
                        description=f"""Analyze these conceptual foundation vectors:
                        - Working Concept Name: {input_brand_idea}
                        - Industry/Niche: {input_industry}
                        - Target Audience Group: {input_audience}
                        - Product Superpower: {input_value_prop}
                        - Competitor Context: {input_competitors}
                        
                        Define the precise 'Market Whitespace' this brand owns. Develop 3 distinct, high-impact naming directions with strategic rationale for each, and establish the Brand's Core Strategic Positioning statement.""",
                        expected_output="An extensive competitive positioning matrix, whitespace identification document, and validated naming blueprints.",
                        agent=brand_strategist
                    )

                    b_task2 = Task(
                        description="""Review the positioning whitespace analysis. Build out the complete Brand Verbal Identity Framework:
                        1. THE MISSION NARRATIVE: A high-impact, emotional brand manifesto block.
                        2. TONE OF VOICE ARCHITECTURE: Define 3 distinct tonal attributes with concrete 'Say This / Do Not Say That' execution rules.
                        3. BRAND TAGLINES: Draft 3 distinct hooks (1 Short/Punchy, 1 Benefit-Driven, 1 Emotional/Aspirational).
                        4. THE 60-SECOND ELEVATOR PITCH: A compelling product narrative built for investor or early customer validation.""",
                        expected_output="A complete, client-ready Verbal Identity Playbook outlining brand messaging frameworks.",
                        agent=verbal_architect, context=[b_task1]
                    )

                    b_task3 = Task(
                        description="""Translate the strategy and verbal architectures into a Visual Identity Directive Guide:
                        1. MOOD & AESTHETIC DIRECTION: Define the core emotional environment (e.g., Minimalist High-Tech, Organic Earthy, Kinetic Neo-Punk).
                        2. SYSTEMIC COLOR PALETTE LOGIC: Provide 3 exact Hex code recommendations (Primary, Secondary, Accent) with deep psychological justifications for each selection.
                        3. TYPOGRAPHY GUIDANCE: Detail explicit font pairing profiles (Header style pairing with Body copy typography rules).
                        4. GENERATIVE DESIGN PROMPTS: Provide 3 precise, high-density descriptive prompts designed for Midjourney or DALL-E 3 to generate:
                           - Brand Logo Concept Mark
                           - Primary Product Packaging or App UI Hero Interface Frame
                           - Main Lifestyle Landing Page Digital Asset""",
                        expected_output="A structured visual aesthetic playbook complete with design tokens, palette frameworks, and creative text prompts.",
                        agent=visual_director, context=[b_task1, b_task2]
                    )

                    brand_crew = Crew(agents=[brand_strategist, verbal_architect, visual_director], tasks=[b_task1, b_task2, b_task3], verbose=True)
                    st.session_state.brand_output = str(brand_crew.kickoff())
                    status.update(label="✅ Brand Platform Fully Engineered!", state="complete")
                st.rerun()

    if st.session_state.brand_output:
        st.markdown("## ✨ Engineered Brand Strategy & Launch Architecture")
        st.markdown(st.session_state.brand_output)
        st.download_button("💾 Download Brand Identity Playbook (.md)", st.session_state.brand_output, "Brand_Identity_Playbook.md", "text/markdown")

# ==============================================================================
# ENGINE 3: LIVE OPERATIONS TOWER (VIRTUAL COO)
# ==============================================================================
elif studio_mode == "🏔️ Live Operations Tower (Virtual COO)":
    st.title("🏔️ Virtual COO & Global Scaling Control Tower")
    st.subheader("Manage everyday operations, processing pipelines, and international export channels.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        current_bottleneck = st.selectbox(
            "Identify Current Operational Bottleneck:",
            [
                "Q-Commerce Out-of-Stock Issues",
                "Decentralized SHG Processing Variances",
                "Packaging Degradation & Shelf-Life Limits",
                "Export Regulatory Compliance (US FDA / GCC Ports)",
                "Dynamic Margin Inefficiencies"
            ]
        )
        active_skus = st.text_input("Active SKUs Under Focus:", "Badri A2 Ghee, Wild Forest Honey, Rhododendron Infusion")
    with col2:
        target_export_zone = st.selectbox(
            "Target Global Expansion Zone:", 
            [
                "Middle East (GCC - Dubai/Riyadh/Kuwait)", 
                "Southeast Asia (ASEAN - Singapore/Malaysia/Thailand)",
                "East Asia (Japan/South Korea)",
                "Indian Subcontinent Cross-Border (Nepal/Bangladesh/Sri Lanka)",
                "North America (USA/Canada)", 
                "European Union (EU)"
            ]
        )
        daily_notes = st.text_area("Live Field Notes / Production Updates:", placeholder="e.g., Munsiyari cluster reports a 12% moisture spike in the current Rajma harvest.")

    if st.session_state.coo_output is None:
        if st.button("🚀 Boot Virtual COO Engine", type="primary"):
            if api_key:
                with st.status("⚙️ Activating Virtual COO Control Tower...", expanded=True) as status:
                    
                    virtual_coo = Agent(
                        role="Virtual Chief Operating Officer & Global Scaling Director",
                        goal="Manage daily execution metrics, eliminate supply chain bottlenecks, and scale processing architectures for global export markets.",
                        backstory="An elite consumer goods operations chief with deep expertise scaling FMCG supply chains. Expert at connecting rural manufacturing clusters with quick-commerce platforms and international customs infrastructure.",
                        verbose=True,
                        llm=custom_llm
                    )

                    horizon1_task = Task(
                        description=f"""Analyze the current operational bottleneck: {current_bottleneck}.
                        Using the active SKUs ({active_skus}) and field updates ({daily_notes}), design an immediate mitigation protocol for the next 24-48 hours. 
                        Focus on maintaining quick-commerce dark store fill rates and stabilizing SHG procurement quality metrics.""",
                        expected_output="An immediate 48-hour tactical action plan resolving active supply chain and inventory friction.",
                        agent=virtual_coo
                    )

                    horizon2_task = Task(
                        description=f"""Develop a 90-day systemic optimization plan focused on:
                        1. Processing standardization across procurement clusters.
                        2. Transitioning to high-barrier nitrogen-flush packaging systems to extend product shelf life to 12+ months.
                        3. Pricing and margin protection to ensure a 60%+ gross margin across all premium digital channels.""",
                        expected_output="A structured 90-day operational optimization playbook covering processing, packaging, and unit economics.",
                        agent=virtual_coo,
                        context=[horizon1_task]
                    )

                    horizon3_task = Task(
                        description=f"""Build a 3-year international scaling roadmap targeting {target_export_zone}. 
                        Detail the exact regulatory requirements (e.g., Saudi Food & Drug Authority (SFDA) portal registrations, Singapore Food Agency (SFA) clearings, Halal compliance certifications like JAKIM/MUI, SAFTA tariff exemptions, or APEDA phytosanitary certificates), export logistics networks, and product modifications needed for high-end international and regional wellness channels.""",
                        expected_output="A step-by-step global export expansion blueprint detailing regulatory compliance, trade treaties, and logistics strategy.",
                        agent=virtual_coo,
                        context=[horizon2_task]
                    )

                    coo_crew = Crew(
                        agents=[virtual_coo],
                        tasks=[horizon1_task, horizon2_task, horizon3_task],
                        verbose=True
                    )
                    
                    st.session_state.coo_output = str(coo_crew.kickoff())
                    status.update(label="✅ Operational Playbook Synthesized!", state="complete")
                st.rerun()

    if st.session_state.coo_output:
        st.markdown("## 📊 Strategic Operations & Scaling Playbook")
        st.markdown(st.session_state.coo_output)
        st.download_button(
            label="💾 Download Operational Playbook (.md)",
            data=st.session_state.coo_output,
            file_name="Himalayas_Operations_Playbook.md",
            mime="text/markdown"
        )


# ==============================================================================
# UNIFIED INTERACTIVE WORKSPACE TERMINAL (Maintains Context of Active Engine)
# ==============================================================================
if st.session_state.performance_output or st.session_state.brand_output or st.session_state.coo_output:
    st.markdown("---")
    st.markdown("## 💬 Interactive Workspace: Task Your Bureau")
    st.markdown("Issue follow-up commands to refine, spin off alternative configurations, or generate complementary campaign documents based on the active report context above.")

    # Render previous logs
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_command := st.chat_input("Ex: 'Create an Instagram launch content calendar' or 'Write a custom shipping SOP based on Horizon 1'"):
        with st.chat_message("user"):
            st.markdown(user_command)
        st.session_state.chat_history.append({"role": "user", "content": user_command})

        with st.spinner("Bureau elements analyzing requests..."):
            follow_up_llm = LLM(model="openai/gpt-4o", api_key=api_key, base_url="https://api.ainative.studio/v1")
            
            # Select proper context reference points for memory continuity
            if studio_mode == "📊 Performance Optimizer":
                active_context = st.session_state.performance_output
                data_source_context = st.session_state.excel_context
            elif studio_mode == "✨ Brand Creation Studio":
                active_context = st.session_state.brand_output
                data_source_context = "Brand Incubation Form Entries"
            else:
                active_context = st.session_state.coo_output
                data_source_context = f"Bottleneck: {current_bottleneck} | Target Export: {target_export_zone}"
            
            system_prompt = f"""You are the managing partner of an elite Multi-Agent Growth & Brand Bureau.
            You have access to the initial system context inputs:
            {data_source_context}
            
            And you have access to the complete primary strategic blueprint generated by your team elements:
            {active_context}
            
            Execute the user's iterative command with exceptional precision, real strategic depth, and instantly functional assets."""
            
            response = follow_up_llm.call(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_command}
                ]
            )
            
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
