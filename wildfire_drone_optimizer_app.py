import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🔥 Wildfire Suppression Drone Optimizer")

st.markdown("### Configure Your Drone Fleet and Fire Scenario")

# Input sliders
empty_weight = st.slider("Drone Empty Weight (kg)", 10, 100, 27)
payload = st.slider("Payload Capacity (liters)", 5, 100, 23)
cruise_speed = st.slider("Cruise Speed (km/h)", 20, 150, 60)
battery_life = st.slider("Battery Duration (hours)", 0.5, 5.0, 2.0)
lake_distance = st.slider("Distance to Lake (km)", 0.5, 30.0, 5.0)
refill_method = st.selectbox("Refill Method", ["Skimming", "Stop-and-Go"])
refill_time = 2 if refill_method == "Skimming" else 5
num_drones = st.slider("Number of Drones", 1, 50, 10)
drone_cost = st.number_input("Cost per Drone (USD)", value=136000)
drone_operating_cost_hr = st.number_input("Operating Cost per Hour (USD)", value=30)
fire_duration = st.slider("Fire Duration (hours)", 1, 12, 5)

# Calculate turnaround and performance
trip_time = (2 * lake_distance / cruise_speed) + (refill_time / 60)  # hours
missions_per_hour = 1 / trip_time if trip_time > 0 else 0
missions_total = min(battery_life, fire_duration) * missions_per_hour
total_drops = missions_total * num_drones
total_water = total_drops * payload

# Cost analysis
total_operating_cost = num_drones * drone_operating_cost_hr * fire_duration
cost_per_liter = total_operating_cost / total_water if total_water > 0 else float('inf')
fleet_acquisition_cost = num_drones * drone_cost

# Display results
st.markdown("### 💧 Results")
st.metric("Estimated Missions per Drone", f"{missions_total:.1f}")
st.metric("Total Water Delivered", f"{total_water:,.0f} liters")
st.metric("Operational Cost per Liter", f"${cost_per_liter:.2f}")
st.metric("Total Operating Cost", f"${total_operating_cost:,.0f}")
st.metric("Fleet Acquisition Cost", f"${fleet_acquisition_cost:,.0f}")

# Optional: Graph of water delivered vs. fleet size
st.markdown("### 📊 Fleet Scaling Performance")
drone_range = np.arange(1, 51)
flow_rates = drone_range * missions_total * payload / fire_duration
plt.figure(figsize=(8, 4))
plt.plot(drone_range, flow_rates)
plt.xlabel("Number of Drones")
plt.ylabel("Liters per Hour")
plt.title("Suppression Efficiency vs Fleet Size")
plt.grid(True)
st.pyplot(plt)
