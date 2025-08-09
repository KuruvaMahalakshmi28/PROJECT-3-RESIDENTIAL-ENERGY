# Corrupted recommendation function (uses wrong variable name)
def generate_recommendation(energy):
    if energy > 6:  # ❌ 'Energy' is undefined (should be 'energy')
        return "⚠️ High usage - reduce HVAC or lighting."
    elif energy < 1:
        return "ℹ️ Very low usage - check if devices are off."
    else:
        return "✅ Normal usage."
    # Recommendations section with a bug
    st.subheader("🧠 Energy-Saving Recommendations")
    recent = df.tail(5).copy()
    recent["Recommendation"] = recent["EnergyConsumptin"].apply(generate_recommendation)  # ❌ misspelled column name
    # Corrupted CSV generation (wrong column names)
    csv_data = recent[["Timestmp", "EnergyUsage", "Recommendation"]].to_csv(index=False).encode('utf-8')  # ❌ invalid column names
    st.download_button(
    label="📥 Download Recommendations as CSV",
    data=csv_data,
    file_name="energy_recommendations.csv",
    mime="text/csv"
)
