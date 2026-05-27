import streamlit as st
import requests


# ==========================================
# 1. ENTERPRISE WEATHER ENGINE WITH CLOUD SECRETS
# ==========================================

def get_live_weather(location, api_key=None):
    """
    Fetches real-time data using secure configuration keys.
    Pulls securely from Streamlit Cloud Secrets if no key is explicitly passed.
    Returns metrics normalized to Celsius.
    """
    if not location:
        return None

    if not api_key:
        try:
            api_key = st.secrets["openweathermap"]["api_key"]
        except Exception:
            st.error("⚠️ Configuration Error: Weather API key missing from cloud secrets infrastructure.")
            return None

    try:
        # Requesting imperial first to preserve baseline algorithm numbers cleanly
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&APPID={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            message = data.get("message", "")
            if "Invalid API key" in message:
                return {"error": "activation_delay"}
            return None

        clouds = data.get("clouds", {}).get("all", 0)
        estimated_uv = max(1.0, 10.0 - (clouds / 10.0))

        # Pull Fahrenheit data and convert dynamically for clean processing
        temp_f = float(data["main"]["temp"])
        temp_c = (temp_f - 32) * 5 / 9

        return {
            "temp_c": round(temp_c, 1),
            "temp_f": temp_f,  # Retained internally for base index equation mapping
            "humidity": int(data["main"]["humidity"]),
            "uv_index": float(estimated_uv),
            "wind_speed_mph": float(data["wind"]["speed"]),
            "wind_speed_kph": round(float(data["wind"]["speed"]) * 1.60934, 1),
            "error": None
        }
    except Exception:
        return None


def calculate_comprehensive_safety(weather, horse):
    """
    Advanced Veterinary Risk Matrix
    Calculates exact thermodynamic burden using physiological modifiers.
    All incoming parameters are processed relative to standard equine thermal thresholds.
    """
    # Baseline equation maps strictly over Fahrenheit conversions
    base_index = weather["temp_f"] + weather["humidity"]
    penalty_score = 0
    risk_factors = []

    # ------------------------------------------
    # CRITICAL TRIGGER CHECKPOINTS (ABSOLUTE FAILS)
    # ------------------------------------------
    if horse["anhidrosis"]:
        return {"status": "CRITICAL RISK: DO NOT RIDE", "score": 999, "color": "red",
                "factors": [
                    "⚠️ ANHIDROSIS: Biological inability to sweat. Life-threatening heatstroke risk if worked in heat."]}

    if horse["hydration"] == "Dehydrated (Tacky gums / Slow skin tent)":
        return {"status": "CRITICAL RISK: DO NOT RIDE", "score": 999, "color": "red",
                "factors": [
                    "⚠️ DEHYDRATION: Pre-existing fluid deficit eliminates the horse's ability to cool itself safely."]}

    if horse["pre_temp_check"] and horse["pre_temp_c"] >= 38.9:  # 38.9°C = 102.0°F
        return {"status": "CRITICAL RISK: DO NOT RIDE", "score": 999, "color": "red",
                "factors": [
                    f"⚠️ ELEVATED INITIAL VITALS: Baseline temperature is currently {horse['pre_temp_c']}°C. The horse is already hyperthermic or fighting infection."]}

    # ------------------------------------------
    # PHYSIOLOGICAL & CLINICAL MODIFIERS
    # ------------------------------------------
    if horse["age"] < 4:
        penalty_score += 8
        risk_factors.append("• Juvenile Thermoregulation: Cardiovascular and sweat systems are not fully matured.")
    elif horse["age"] > 18:
        penalty_score += 12
        risk_factors.append("• Senior Metabolic Profile: Decreased baseline efficiency in shedding deep tissue heat.")

    if horse["bcs"] >= 7:
        penalty_score += 15
        risk_factors.append(
            "• High Body Condition (BCS 7+): Excess adipose tissue acts as an insulator, trapping core heat.")
    elif horse["bcs"] <= 3:
        penalty_score += 8
        risk_factors.append("• Low Body Condition (BCS 3-): Reduced muscle reserves compromise systemic resilience.")

    if horse["type"] in ["Heavy Draft (Clydesdale/Shire/etc.)", "Cob / Heavy Native Pony"]:
        penalty_score += 10
        risk_factors.append(
            "• Heavy Muscle-to-Surface Ratio: Low relative surface area limits radiative heat dissipation.")

    if horse["cushings"]:
        penalty_score += 20
        risk_factors.append(
            "• Hypertrichosis (Cushing's/PPID): Heavy, unshed coat completely blocks ambient wind cooling.")
    elif horse["coat"] == "Heavy Winter / Clipped & Growing back":
        penalty_score += 8
        risk_factors.append("• Unseasonable Coat Thickness: Enhances insulation and delays sweat evaporation.")

    if horse["color"] == "Dark (Black / Dark Bay / Dark Brown)" and weather["uv_index"] >= 5:
        penalty_score += 6
        risk_factors.append(
            "• High Melanin Solar Absorption: Dark coat pigmentation accelerates surface heat absorption.")

    if horse["asthma"]:
        penalty_score += 18
        risk_factors.append(
            "• Compromised Respiratory Tract: Asthma/Heaves restricts vital respiratory heat-dumping capacity.")

    if horse["sweat_type"] == "Thick, white soapy lather":
        penalty_score += 10
        risk_factors.append(
            "• Lathering Sweat: Heavy white foam indicates rapid, high-concentration electrolyte depletion.")

    if horse["pre_temp_check"] and 38.3 <= horse["pre_temp_c"] < 38.9:  # 38.3°C = 101.0°F
        penalty_score += 10
        risk_factors.append(
            f"• Borderline Elevated Baseline Vitals ({horse['pre_temp_c']}°C): Commencing work with reduced safety margin.")

    if horse["turnout"] == "Stabled indoors (Warm, poor airflow building)":
        penalty_score += 7
        risk_factors.append(
            "• Stabled Heat Retention: Standing indoors has pre-warmed the core body temperature before tacking up.")

    if horse["acclimatized"] == "No (Recent climate change or sudden heatwave)":
        penalty_score += 12
        risk_factors.append(
            "• Lack of Acclimatization: Plasma volume and sweat-electrolyte balance have not adjusted to local thermal trends.")
    if horse["fitness"] == "Unfit / Returning from injury":
        penalty_score += 8
        risk_factors.append(
            "• Low Cardiovascular Fitness: Higher heart rates required to pump heated blood to the skin.")

    # ------------------------------------------
    # AMBIENT WEATHER MODIFIERS
    # ------------------------------------------
    if weather["uv_index"] >= 6 and horse["shade"] == "Full Sun / No Arena Cover":
        penalty_score += 10
        risk_factors.append(
            "• Radiant Sun Loading: Direct exposure adds a massive external thermal load to the base index.")

    if weather["wind_speed_mph"] <= 3:
        penalty_score += 6
        risk_factors.append(
            "• Stagnant Boundary Layer: Absence of airflow prevents convective heat removal from wet skin.")
    elif weather["wind_speed_mph"] >= 15:
        penalty_score -= 5
        risk_factors.append(
            "• High Wind Convection: Rapid airflow improves evaporative and convective cooling profiles.")

    if horse["workload"] == "Heavy (Cantering, jumping, intense schooling)":
        penalty_score += 20
        risk_factors.append(
            "• Intensely Demanding Workload: Generates severe metabolic heat within major muscle groups rapidly.")
    elif horse["workload"] == "Moderate (Trot work, light canter, hilly trails)":
        penalty_score += 10
        risk_factors.append("• Moderate Workload: Elevates internal body temperatures steadily over time.")

    total_score = base_index + penalty_score

    if total_score < 130:
        return {"status": "🌿 SAFE TO RIDE: OPTIMAL BASELINE", "score": total_score, "color": "green",
                "factors": risk_factors}
    elif 130 <= total_score <= 150:
        return {"status": "🔶 USE CAUTION: ELEVATED THERMAL STRAIN", "score": total_score, "color": "yellow",
                "factors": risk_factors}
    elif 151 <= total_score <= 175:
        return {"status": "🟧 REDUCED WORK ONLY: SEVERE CARDIOVASCULAR BURDEN", "score": total_score, "color": "orange",
                "factors": risk_factors}
    else:
        return {"status": "🛑 DO NOT RIDE: CRITICAL THERMAL CRISIS", "score": total_score, "color": "red",
                "factors": risk_factors}


# ==========================================
# 2. BRANDED GRAPHICS & UK L10N CSS CODES
# ==========================================

st.set_page_config(page_title="Equine Bio-Thermal Analytics Platform", page_icon="🐴", layout="wide")

brand_primary = "#A6512D"  # Burnt Copper
brand_bg = "#EAD9C8"  # Soft Oat Cream
brand_welfare = "#6F8A73"  # Muted Sage
brand_highlight = "#D98C5F"  # Light Terracotta
brand_text = "#2C2C2C"  # Soft Charcoal

st.markdown(f"""
<style>
    .stApp {{ background-color: {brand_bg}; }}
    h3 {{ font-family: 'Inter', sans-serif !important; font-weight: 700 !important; color: {brand_primary} !important; letter-spacing: -0.5px; }}
    p, span, label, .stMarkdown {{ color: {brand_text} !important; font-family: 'Inter', sans-serif; }}
    .stSubheader {{ font-size: 1.15rem !important; font-weight: 700 !important; color: {brand_primary} !important; border-bottom: 2px solid {brand_highlight}; padding-bottom: 6px; margin-bottom: 15px; }}

    .card-green {{ background-color: #f4f6f4; border-left: 6px solid {brand_welfare}; padding: 22px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 20px; }}
    .card-yellow {{ background-color: #faf7f2; border-left: 6px solid {brand_highlight}; padding: 22px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 20px; }}
    .card-orange {{ background-color: #f7ede6; border-left: 6px solid {brand_primary}; padding: 22px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 20px; }}
    .card-red {{ background-color: #fcf3f2; border-left: 6px solid #b91c1c; padding: 22px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); margin-bottom: 20px; }}

    .card-title {{ font-size: 1.35rem !important; font-weight: 700 !important; margin: 0 0 8px 0 !important; font-family: 'Inter', sans-serif !important; }}
    .card-green .card-title {{ color: {brand_welfare} !important; }}
    .card-yellow .card-title {{ color: {brand_highlight} !important; }}
    .card-orange .card-title {{ color: {brand_primary} !important; }}
    .card-red .card-title {{ color: #b91c1c !important; }}

    .protocol-box {{ line-height: 1.6; font-size: 0.95rem; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }}
    .mono-metric {{ font-family: 'SFMono-Regular', Consolas, monospace; font-weight: 700; background-color: #f1f5f9; padding: 3px 7px; border-radius: 4px; color: {brand_primary}; }}
</style>
""", unsafe_allow_html=True)

st.markdown("### 📊 EQUINE BIO-THERMAL ANALYTICS PLATFORM")
st.caption("UK Metric Localization Profile | Real-Time Atmospheric Evaluation & Equine Risk Analysis")

with st.expander("⚖️ LEGAL COMPLIANCE & LIABILITY CLEARANCE STATEMENTS", expanded=False):
    st.markdown(
        f"<div style='font-size: 0.85rem; color: {brand_text}; opacity: 0.85; line-height: 1.5;'>"
        "This system serves purely as an analytical calculation utility based on generalized thermodynamic indices. "
        "It does not constitute diagnostic clinical feedback, vet medical treatment paths, or formal safety criteria. "
        "Individual equine physiological responses vary aggressively based on genetics, hydration, and unmapped systemic conditions. "
        "Users must cross-reference analytical calculations against real-time common-sense observation. "
        "The developer and hosting entities accept zero liability for animal illness or physical performance injuries."
        "</div>", unsafe_allow_html=True
    )

st.markdown("---")

col_env, col_phys = st.columns([1, 1.2])

with col_env:
    st.markdown("<div class='stSubheader'>🌐 Atmospheric Parameters (UK Metric)</div>", unsafe_allow_html=True)

    manual_mode = st.checkbox("Toggle Manual Override (Skip Weather API Sync)")

    if not manual_mode:
        location = st.text_input("Target Location Profile", placeholder="e.g., London, UK")
        shade = st.radio("Solar Radiation Cover",
                         ["Completely Shaded / Indoor Arena", "Partial Shade / Canopy", "Full Sun / No Arena Cover"])
        weather = get_live_weather(location)
    else:
        location = "Manual Override Mode"
        m_temp_c = st.slider("Observed Temperature (°C)", 15.0, 45.0, 28.0, step=0.5)
        m_hum = st.slider("Observed Relative Humidity (%)", 10, 100, 60)
        m_wind_kph = st.slider("Observed Wind Speed (kp/h)", 0.0, 40.0, 10.0, step=0.5)
        m_uv = st.slider("Estimated Solar Exposure / UV (1-10 Scale)", 1, 10, 5)
        shade = st.radio("Solar Radiation Cover",
                         ["Completely Shaded / Indoor Arena", "Partial Shade / Canopy", "Full Sun / No Arena Cover"])

        # Internal map values supporting baseline math matrix conversions
        m_temp_f = (m_temp_c * 9 / 5) + 32
        m_wind_mph = m_wind_kph / 1.60934
        weather = {"temp_c": m_temp_c, "temp_f": m_temp_f, "humidity": m_hum, "uv_index": m_uv,
                   "wind_speed_mph": m_wind_mph, "wind_speed_kph": m_wind_kph, "error": None}

with col_phys:
    st.markdown("<div class='stSubheader'>🧬 Comprehensive Equine Diagnostics</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        age = st.slider("Chronological Age (Years)", min_value=1, max_value=30, value=10)
        horse_type = st.selectbox("Morphology / Breed Type",
                                  ["Light Riding Horse (Thoroughbred/Warmblood)", "Pony / Native Breed",
                                   "Cob / Heavy Native Pony", "Heavy Draft (Clydesdale/Shire/etc.)"])
        color = st.selectbox("Phenotypic Coat Pigmentation",
                             ["Light (White/Grey/Palomino/Light Chestnut)", "Dark (Black / Dark Bay / Dark Brown)"])
        coat_status = st.selectbox("Current Coat Profile",
                                   ["Shed Out / Summer Coat", "Heavy Winter / Clipped & Growing back"])
        bcs = st.slider("Henneke Body Condition Score (BCS 1-9)", 1, 9, 5)
        turnout = st.selectbox("Pre-Ride Management Status",
                               ["Out in pasture (Breezy, open field)", "Stabled indoors (Warm, poor airflow building)"])

    with c2:
        workload = st.selectbox("Planned Training Intensity Profile", ["Light (Walking, stretching, brief trotting)",
                                                                       "Moderate (Trot work, light canter, hilly trails)",
                                                                       "Heavy (Cantering, jumping, intense schooling)"])
        fitness = st.selectbox("Cardiovascular Conditioning Profile",
                               ["Fit / Fully Conditioned", "Unfit / Returning from injury"])
        acclimatized = st.selectbox("Acclimatization Status", ["Yes (Fully adapted over 2+ weeks to current climate)",
                                                               "No (Recent climate change or sudden heatwave)"])
        hydration = st.selectbox("Clinical Hydration Baseline", ["Normal (Pink, wet gums; rapid skin elastic snap)",
                                                                 "Dehydrated (Tacky gums / Slow skin tent)"])
        sweat_type = st.selectbox("Sweat Consistency Observation",
                                  ["Normal (Clear, wet moisture)", "Thick, white soapy lather"])

        st.markdown("**Pathological Risk States:**")
        anhidrosis = st.checkbox("Diagnosed Anhidrosis (Inability to sweat)")
        cushings = st.checkbox("Diagnosed Cushing's Disease / PPID")
        asthma = st.checkbox("Equine Asthma / RAO / Heaves")

    st.markdown("---")
    st.markdown("**Optional Objective Vitals:**")
    pre_temp_check = st.checkbox("I have a manual pre-ride rectal temperature reading")
    pre_temp_c = 38.0  # Healthy default rest core
    if pre_temp_check:
        pre_temp_c = st.number_input("Enter Pre-Ride Rectal Temperature (°C)", min_value=36.0, max_value=41.5,
                                     value=38.0, step=0.1)

# Package variables
horse_data = {
    "age": age, "type": horse_type, "color": color, "coat": coat_status, "bcs": bcs, "turnout": turnout,
    "workload": workload, "fitness": fitness, "acclimatized": acclimatized, "hydration": hydration,
    "sweat_type": sweat_type, "anhidrosis": anhidrosis, "cushings": cushings, "asthma": asthma,
    "pre_temp_check": pre_temp_check, "pre_temp_c": pre_temp_c, "shade": shade
}

# ==========================================
# 3. ADVANCED VERDICT PROCESSING DISPLAY
# ==========================================

if location:
    if weather is None:
        st.error(
            "❌ System Error: The entered location could not be verified by global servers. Please check geographic formatting.")
    elif weather.get("error") == "activation_delay":
        st.warning(
            "⏳ API Activation Pending: OpenWeatherMap is validating your new key profile. In the meantime, check the box under Section 1 to use Manual Weather Entry mode to explore the full logic!")
    else:
        results = calculate_comprehensive_safety(weather, horse_data)

        st.markdown("---")
        st.markdown("<div class='stSubheader'>📊 Composite System Assessment Verdict</div>", unsafe_allow_html=True)

        card_class = f"card-{results['color']}"
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='card-title'>{results['status']}</div>
            <div style='font-size: 0.95rem; line-height:1.5; color: {brand_text};'>
                Atmospheric readings register at <span class='mono-metric'>{weather['temp_c']}°C</span> with <span class='mono-metric'>{weather['humidity']}%</span> humidity. 
                Applying comprehensive bio-physical burden multipliers outputs an adjusted platform safety score of <span class='mono-metric'>{results['score']}</span>.
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Ambient Temperature", f"{weather['temp_c']}°C")
        m2.metric("Relative Humidity", f"{weather['humidity']}%")
        m3.metric("Wind Current Speed", f"{weather['wind_speed_kph']} km/h")
        m4.metric("Solar Cloud Index", f"{weather['uv_index']:.1f}/10")

        if results["factors"]:
            st.write("")
            with st.expander("🔍 VIEW APPLIED BIO-THERMAL RISK MATRIX BREAKDOWN", expanded=True):
                for factor in results["factors"]:
                    st.markdown(
                        f"<div style='font-size:0.9rem; color:{brand_text}; opacity: 0.85; padding:2px 0;'>{factor}</div>",
                        unsafe_allow_html=True)

        st.write("")
        st.markdown("### 🩺 Mandatory Veterinary Operational Protocol")

        if results["color"] == "green":
            st.markdown(
                f"<div class='protocol-box' style='color:{brand_text}; background-color:#f4f6f4; padding:15px; border: 1px solid {brand_welfare};'>"
                "<strong>• CLEARANCE ISSUED:</strong> Baseline thermal regulation capacity is fully intact. Standard work parameters can proceed without restriction.<br>"
                "<strong>• HYDRATION MANAGEMENT:</strong> Provide clean, unchilled drinking water ad libitum immediately following training cycles to support basic systemic metabolic homeostasis."
                "</div>", unsafe_allow_html=True
            )
        elif results["color"] == "yellow":
            st.markdown(
                f"<div class='protocol-box' style='color:{brand_text}; background-color:#faf7f2; padding:15px; border: 1px solid {brand_highlight};'>"
                "<strong>• INTENSITY REDUCTION REQUIRED:</strong> Limit high-exertion training components by 30%. Enforce a mandatory 3-minute structural standing recovery window every 10 active training minutes.<br>"
                "<strong>• PATHWAY SELECTION:</strong> Restrict work exclusively to covered arenas or heavily shaded environments. Avoid continuous exposed solar pathways.<br>"
                "<strong>• HYDROTHERMAL DISPERSION:</strong> Apply continuous, high-volume cold water to key surface vascular nets (neck frame, pectoral chest wall, inner quarters). <em>Do not waste time with a sweat scraper</em>; moving liquid loops conduct internal heat outward dramatically faster than stagnant air."
                "</div>", unsafe_allow_html=True
            )
        elif results["color"] == "orange":
            st.markdown(
                f"<div class='protocol-box' style='color:{brand_text}; background-color:#f7ede6; padding:15px; border-radius:4px; border: 1px solid {brand_primary};'>"
                "<strong>• AGGRESSIVE WORK RESTRAINTS ENFORCED:</strong> Session goals must be downscaled strictly to low-impact walk frames and highly conservative light trot patterns. Completely eliminate canter patterns and jump training pipelines.<br>"
                "<strong>• CHRONOLOGICAL THRESHOLD:</strong> Training window execution must terminate before reaching 25 elapsed runtime minutes.<br>"
                "<strong>• ACTIVE RECOVERY MONITORING:</strong> If core physiological vitals fail to return to baseline patterns within 20 minutes post-session, immediately deploy systemic cold-water application models across all major locomotive muscle systems."
                "</div>", unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='protocol-box' style='color:#991b1b; background-color:#fef2f2; padding:15px; border: 1px solid #dc2626;'>"
                "<strong>• SYSTEMIC EXERCISE INTERDICTION:</strong> Training operations must be abandoned completely. Environmental constraints paired against horse physiological vulnerabilities indicate absolute metabolic saturation limits.<br>"
                "<strong>• DIRECT PATHOLOGY THREATS:</strong> Proceeding with physical exercise creates high correlations with sudden heatstroke, complete anhidrotic collapse, or systemic rhabdomyolysis (tying-up).<br>"
                "<strong>• RECOVERY ACTIONS:</strong> Stable the animal in deep, unexposed shelter utilizing industrial airflow arrays or active cooling configurations. Maintain hydration support profiles and monitor core parameters closely."
                "</div>", unsafe_allow_html=True
            )

# ==========================================
# 4. VETERINARY RESEARCH & LITERATURE PANEL
# ==========================================
st.write("")
st.markdown("---")
with st.expander("🔍 VETERINARY RESEARCH & REFERENCE INDEX", expanded=False):
    st.markdown(f"""
    <div style='font-size: 0.9rem; line-height: 1.6; color: {brand_text};'>
        <strong>Academic & Regulatory References:</strong><br>
        <ul>
            <li>
                <strong>Thermoregulation Zones:</strong> Healthy adult horses maintain a strict core biological temperature range between 37.5°C and 38.5°C when operating within an atmospheric thermoneutral zone of 5°C to 25°C. Beyond this, metabolic heat dissipation becomes exponentially less efficient due to a low relative surface-to-mass ratio compared to humans 
                <em>(Kang et al., 2023; International Journal of Biometeorology)</em>.
            </li>
            <li>
                <strong>Climate Impact Indices:</strong> The Federation Equestre Internationale (FEI) explicitly utilizes comprehensive environmental tracking indexes (including temperature, humidity, wind velocity, and solar loading coefficients) to safely evaluate performance restrictions and mitigate heat illnesses at global championship levels 
                <em>(Marlin, D., FEI Climate Guidelines)</em>.
            </li>
            <li>
                <strong>Humidity Interferences:</strong> Equines see severe evaporative cooling limits when relative humidity cross-evaluates above 50%, accelerating systemic heart rate strain during athletic collection intervals 
                <em>(Poochipakorn et al., 2024; Animals)</em>.
            </li>
        </ul>
        <br>
        <strong>External Educational Resource Portals:</strong><br>
        • <a href="https://inside.fei.org/" target="_blank" style="color: {brand_primary}; font-weight: 600;">FEI Official Horse Welfare Hub</a><br>
        • <a href="https://www.beva.org.uk/" target="_blank" style="color: {brand_primary}; font-weight: 600;">British Equine Veterinary Association (BEVA) Resources</a>
    </div>
    """, unsafe_allow_html=True)

else:
st.info(
    "💡 Complete Section 1 by entering a geographic query to launch the automated bio-thermal risk evaluation sequence.")