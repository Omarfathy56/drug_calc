
import streamlit as st

st.title("Antifungal Pharmacokinetics Calculator")

# -------------------------
# Drug Selection
# -------------------------
drug = st.selectbox("Select Drug", [
    "Voriconazole",
    "Posaconazole",
    "Itraconazole",
    "Flucytosine"
])

st.write("Enter patient data:")

# -------------------------
# Inputs
# -------------------------
weight = st.number_input("Weight (kg)", min_value=0.0, value=None, placeholder="Enter weight")
if weight:
    height = st.number_input("Height (cm)", min_value=0.0, value=None, placeholder="Enter height")
    if height:
        age = st.slider("Age", min_value=1, max_value=100)
        if age:
            if drug == "Flucytosine":
                dose = 25
            else:
                old_dose_statues = st.select_slider("Dose Status", ["Loading" , "Maintenance"])
            css = st.number_input("Css (mg/L)", min_value=0.0, value=None, placeholder="Enter Css")
            if css:
                gender = st.selectbox("Vd (L/kg)", ['male', 'female'])
                if gender:
                    scr = st.number_input("Scr", min_value=0.0, value=None, placeholder="Enter Scr")
                    if scr:
                        c_measured = st.number_input("C measured", min_value=0.0, value=None, placeholder="Enter C_measured")
                        if c_measured:  
                            infusion_time = st.number_input("Infusion Time (hr)", min_value=0.0, value=None, placeholder="Enter IT")
                            if infusion_time:
                                if drug == "Voriconazole":
                                    if old_dose_statues == "Loading":
                                        dose = 6
                                    else:
                                        dose = 4
                                    tau = 12
                                    vd_factor = st.selectbox("Vd (L/kg)", [4.0, 4.5, 5.0])
                                    st.info(f"tau is fixed at 12 hour, Dose {dose} mg/kg")

                                elif drug == "Posaconazole":
                                    dose = 300
                                    tau = 24
                                    vd_factor = st.selectbox("Vd (L/kg)", [5.0, 7.5, 10.0])
                                    st.info("tau is fixed at 24 hour, Dose 300 mg")

                                elif drug == "Itraconazole":
                                    dose = 200
                                    tau = st.selectbox("tau", [12.0, 24.0])
                                    vd_factor = 10.0
                                    st.info("Vd is fixed at 10 L/kg, Dose 200 mg")

                                elif drug == "Flucytosine":
                                    tau = 6
                                    vd_factor = st.selectbox("Vd (L/kg)", [0.6, 0.75, 0.9])
                                    st.info("tau is fixed at 6 hour , Dose 25 mg/kg")
                                
                                if st.button("Calculate"):

                                    try:
                                        vd = weight * vd_factor

                                        # -------------------------
                                        # Common Calculations
                                        # -------------------------
                                        cl = dose / (css * tau)
                                        ld = css * vd
                                        md = cl * css * tau
                                        infusion_rate = dose / infusion_time
                                        new_dose = dose * (css / c_measured)
                                        clcr = (140 - age) * weight / (72 * scr)

                                        
                                        if drug == "Voriconazole":
                                            t_half = (0.693 * vd) / cl

                                        elif drug == "Posaconazole":
                                            t_half = "25–35 hr"

                                        elif drug == "Itraconazole":
                                            t_half = "30–40 hr"

                                        elif drug == "Flucytosine":
                                            t_half = "3–6 hr"

                                        # -------------------------
                                        # Interval (τ)
                                        # -------------------------
                                        if drug == "Flucytosine":
                                            interval = (0.693 * vd) / cl
                                        else:
                                            interval = (cl * css) / css

                                        # -------------------------
                                        # Results
                                        # -------------------------
                                        st.subheader("Results:")

                                        st.write(f"Volume of Distribution (Vd): {vd:.2f} L")
                                        st.write(f"Clearance (Cl): {cl:.2f} L/hr")
                                        st.write(f" Old Dose (Ld): {ld:.2f} mg")
                                        st.write(f"Maintenance Dose (Md): {md:.2f} mg")
                                        st.write(f"New Dose (Mg/kg): {new_dose:.2f}Mg")
                                        st.write(f"Clcr (mL/min): {clcr:.2f}mL/min")

                                        st.write(f"Half-life (t½): {t_half}")

                                        st.write(f"Infusion Rate: {infusion_rate:.2f} mg/hr")
                                        st.write(f"Suggested Interval (τ): {interval:.2f} hr")
                                        
                                        
                                        st.markdown("---")

                                        # -------------------------
                                        # Clinical Notes (From Document)
                                        # -------------------------
                                        st.subheader("Clinical Notes & Monitoring")
                                        
                                        if drug == "Voriconazole":
                                            st.info("Repeat a 2nd pre-dose 3-5 days after the first level and 3-5 days after any dose alteration or iv to oral switch.")
                                        
                                        elif drug == "Posaconazole":
                                            st.info("Repeat a pre-dose level 7 days after any dose change.")
                                        
                                        elif drug == "Itraconazole":
                                            st.info("Use oral solution in preference to capsules if possible (superior bioavailability).\n\nRepeat a pre-dose level 7 days after any dose change.")
                                        
                                        elif drug == "Flucytosine":
                                            st.error("⚠️ Levels greater than 100mg/L are toxic.")
                                            st.info("Repeat pre and post-dose levels within 3 days of any dose change.")

                                    except ZeroDivisionError:
                                        st.error("Invalid input: division by zero")

