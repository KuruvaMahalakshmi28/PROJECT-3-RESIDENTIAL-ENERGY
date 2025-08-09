import streamlit as st
import pandas as pd


def show_assistant():
    st.title("AI Energy Assistant")
    st.write("Ask a question related to your energy usage.")

    df = pd.read_csv("data/sample_energy.csv")

    # Convert 'On'/'Off' to numeric 1/0 for HVAC and Lighting
    df["HVACUsage_numeric"] = df["HVACUsage"].map({"On": 1, "Off": 0})
    df["LightingUsage_numeric"] = df["LightingUsage"].map({"On": 1, "Off": 0})

    question = st.text_input("Enter your question:")

    if question:
        response = answer_question(question, df)
        st.write("### Assistant's Response:")
        st.write(response)


def answer_question(question, df):
    question = question.lower()

    if "hvac" in question:
        avg_hvac = df["HVACUsage_numeric"].mean()
        if avg_hvac > 0.5:
            return (
                f"The HVAC system is frequently used (average usage: {avg_hvac:.2f}). "
                "Consider turning it off when rooms are unoccupied to save energy."
            )
        else:
            return (
                f"The HVAC system is moderately used (average usage: {avg_hvac:.2f}). "
                "Ensure temperature settings are optimal and avoid unnecessary usage."
            )

    elif "lighting" in question or "light" in question:
        avg_light = df["LightingUsage_numeric"].mean()
        if avg_light > 0.5:
            return (
                f"Lighting usage is high (average usage: {avg_light:.2f}). "
                "Consider using motion sensors or switching off lights in unoccupied areas."
            )
        else:
            return (
                f"Lighting usage seems efficient (average usage: {avg_light:.2f}). "
                "Keep up the good habits and use natural light whenever possible."
            )

    elif "occupancy" in question:
        if "lighting" in question:
            unused_lights = df[(df["Occupancy"] == 0) & (df["LightingUsage_numeric"] == 1)]
            count = len(unused_lights)
            return (
                f"There are {count} instances where lights were on but no one was present. "
                "You should consider turning off lights in unoccupied spaces to reduce waste."
            )
        elif "hvac" in question:
            unused_hvac = df[(df["Occupancy"] == 0) & (df["HVACUsage_numeric"] == 1)]
            count = len(unused_hvac)
            return (
                f"There are {count} cases where HVAC was running without any occupancy. "
                "Turn off HVAC systems when no one is present to improve efficiency."
            )
        else:
            return (
                "Occupancy data can help identify idle usage. "
                "Ask about lighting or HVAC usage during unoccupied times for better insights."
            )

    elif "suggest" in question or "improve" in question:
        suggestions = [
            "- Turn off appliances when rooms are unoccupied.",
            "- Use smart plugs or timers for high-usage devices.",
            "- Consider motion sensors for lights.",
            "- Schedule HVAC systems based on occupancy patterns.",
            "- Monitor and analyze daily energy trends regularly.",
        ]
        return "Here are some suggestions to improve energy efficiency:\n\n" + "\n".join(suggestions)

    elif "renewable" in question:
        renewable_avg = df["RenewableEnergy"].mean()
        return (
            f"Your average renewable energy contribution is {renewable_avg:.2f} kWh. "
            "Consider increasing solar or other renewable sources to reduce grid dependence."
        )

    elif "consumption" in question or "energy" in question:
        total = df["EnergyConsumption"].sum()
        avg = df["EnergyConsumption"].mean()
        return (
            f"Your total energy consumption is {total:.2f} kWh with an average of {avg:.2f} kWh per entry. "
            "Analyze which devices contribute most and optimize their usage."
        )

    else:
        return (
            "Sorry, I couldn't understand your question. "
            "Try asking about HVAC, lighting, occupancy, renewable energy, or energy consumption."
        )
