import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.preprocessing import preprocess_data
from utils.recommendations import generate_recommendation

def show_dashboard():
    st.title("📊 Energy Consumption Dashboard")

    uploaded_file = st.file_uploader("Upload Energy CSV File", type=["csv"])
    if uploaded_file is None:
        st.info("📂 Please upload a CSV file to view the dashboard.")
        return

    # Load and preprocess data
    df = pd.read_csv(uploaded_file, parse_dates=["Timestamp"])
    df = preprocess_data(df)
    df["LightingUsage"] = pd.to_numeric(df["LightingUsage"], errors="coerce")
    df["HVACUsage"] = pd.to_numeric(df["HVACUsage"], errors="coerce")
    df["EnergyConsumption"] = pd.to_numeric(df["EnergyConsumption"], errors="coerce")
    df = df.dropna(subset=["Timestamp", "EnergyConsumption"])

    # Energy trend
    st.subheader("📈 Overall Energy Consumption Trend")
    fig, ax = plt.subplots()
    ax.plot(df["Timestamp"], df["EnergyConsumption"], color='blue')
    ax.set_title("Energy Consumption Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("kWh")
    ax.grid(True)
    st.pyplot(fig)

    # Anomaly detection
    st.subheader("⚠️ High Usage Anomalies")
    threshold = df["EnergyConsumption"].mean() + 2 * df["EnergyConsumption"].std()
    anomalies = df[df["EnergyConsumption"] > threshold]
    if anomalies.empty:
        st.success("✅ No anomalies detected.")
    else:
        st.error(f"Found {len(anomalies)} anomalies (usage > {threshold:.2f} kWh)")
        st.dataframe(anomalies[["Timestamp", "EnergyConsumption"]])

    # Day-wise usage
    st.subheader("📅 Average Usage by Day of Week")
    df["Weekday"] = df["Timestamp"].dt.day_name()
    weekday_usage = df.groupby("Weekday")["EnergyConsumption"].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    st.bar_chart(weekday_usage)

    # Idle usage
    st.subheader("🚨 Idle Time Energy Waste")
    idle_df = df[(df["Occupancy"] == 0) & ((df["LightingUsage"] > 0) | (df["HVACUsage"] > 0))]
    if idle_df.empty:
        st.success("✅ No energy used during unoccupied periods.")
    else:
        waste_kwh = idle_df["EnergyConsumption"].sum()
        st.warning(f"⚠️ {waste_kwh:.2f} kWh used when no one was home.")
        st.dataframe(idle_df[["Timestamp", "EnergyConsumption", "LightingUsage", "HVACUsage"]])

    # Recommendations and download
    st.subheader("🧠 Energy-Saving Recommendations")
    recent = df.tail(5).copy()
    recent["Recommendation"] = recent["EnergyConsumption"].apply(generate_recommendation)
    st.dataframe(recent[["Timestamp", "EnergyConsumption", "Recommendation"]])

    # Download button
    csv_data = recent[["Timestamp", "EnergyConsumption", "Recommendation"]].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Recommendations as CSV",
        data=csv_data,
        file_name="energy_recommendations.csv",
        mime="text/csv"
    )
