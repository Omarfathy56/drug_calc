
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
    dose = st.number_input("Dose (mg)", min_value=0.0, value=None, placeholder="Enter dose")
    if dose:
        css = st.number_input("Css (mg/L)", min_value=0.0, value=None, placeholder="Enter Css")
        if css:
            ctarget = st.number_input("Target Concentration (mg/L)", min_value=0.0, value=None, placeholder="Enter TC")
            if ctarget:
                tau = st.slider("Interval (hr)", 1, 24, 12)
                if tau:
                    infusion_time = st.number_input("Infusion Time (hr)", min_value=0.0, value=None, placeholder="Enter IT")
                    if infusion_time:  
                        if drug == "Voriconazole":
                            vd_factor = st.selectbox("Vd (L/kg)", [4.0, 4.5, 5.0])

                        elif drug == "Posaconazole":
                            vd_factor = st.selectbox("Vd (L/kg)", [5.0, 7.5, 10.0])

                        elif drug == "Itraconazole":
                            vd_factor = 10.0
                            st.info("Vd is fixed at 10 L/kg")

                        elif drug == "Flucytosine":
                            vd_factor = st.selectbox("Vd (L/kg)", [0.6, 0.75, 0.9])
                        
                        if st.button("Calculate"):

                            try:
                                vd = weight * vd_factor

                                # -------------------------
                                # Common Calculations
                                # -------------------------
                                cl = dose / (css * tau)
                                ld = ctarget * vd
                                md = cl * ctarget * tau
                                infusion_rate = dose / infusion_time

                                # -------------------------
                                # Half-life logic
                                # -------------------------
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
                                    interval = (cl * ctarget) / css

                                # -------------------------
                                # Results
                                # -------------------------
                                st.subheader("Results:")

                                st.write(f"Volume of Distribution (Vd): {vd:.2f} L")
                                st.write(f"Clearance (Cl): {cl:.2f} L/hr")
                                st.write(f"Loading Dose (Ld): {ld:.2f} mg")
                                st.write(f"Maintenance Dose (Md): {md:.2f} mg")

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

