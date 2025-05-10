import json
import streamlit as st

with open("capsules.json") as f:
    capsules = json.load(f)

if "log" not in st.session_state:
    st.session_state["log"] = []

capsule_names = [capsule["Name"] for capsule in capsules]
capsule_caffeine = [capsule["Caffeine"] for capsule in capsules]

capsules_types = sorted(set(capsule["Type"] for capsule in capsules))

selected_type = st.selectbox("Choose capsule type", capsules_types)

filtered_capsules = [capsule for capsule in capsules if capsule["Type"] == selected_type]

filtered_names = [capsule["Name"] for capsule in filtered_capsules]

selected_name = st.selectbox("Select capsule", filtered_names)

def caffeine_value():
    for capsule in filtered_capsules:
        if capsule["Name"] == selected_name:
            caffeine = capsule["Caffeine"]
            return(caffeine)
    return None

st.number_input("Caffeine (mg)", value=caffeine_value(), step=1.0, disabled=True)

if st.button("➕ Add to log"):
    st.session_state["log"].append({
        "name": selected_name,
        "caffeine": caffeine_value()
    })
    st.success(f"Added {selected_name} to log!")

if st.button("Clear Log"):
    st.session_state["log"] = []
    st.success("Log Cleared!")
    
st.markdown("### ☕ Today's Log")
for entry in st.session_state["log"]:
    st.write(f"- {entry['name']} ({entry['caffeine']} mg)")

total = sum(entry["caffeine"] for entry in st.session_state["log"])
st.markdown(f"**Total caffeine today: {total} mg**")

if total > 400:
    st.warning("You've exceeded the recommended daily limit (400mg). :(")

