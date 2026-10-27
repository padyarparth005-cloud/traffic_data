
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Smart City Traffic Analysis",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Smart City Traffic Data Analysis")
st.caption("Big Data Analytics | Streamlit Dashboard")

path = Path("data/traffic_data.csv")

if not path.exists():
    st.warning("Dataset missing. Run: python generate_data.py")
    st.stop()

df = pd.read_csv(path, parse_dates=["timestamp"])

st.sidebar.header("Traffic Filters")

districts = sorted(df["district"].unique())
selected = st.sidebar.multiselect(
    "Districts", districts, default=districts
)

roads = sorted(df["road"].unique())
selected_roads = st.sidebar.multiselect(
    "Roads", roads, default=roads
)

data = df[
    df["district"].isin(selected)
    & df["road"].isin(selected_roads)
].copy()

if data.empty:
    st.warning("No records match the selected filters.")
    st.stop()

a, b, c, d = st.columns(4)
a.metric("Traffic Records", f"{len(data):,}")
b.metric("Total Vehicles", f"{data['vehicle_count'].sum():,}")
c.metric("Average Speed", f"{data['avg_speed_kmh'].mean():.1f} km/h")
d.metric("Incidents", int((data["incident"] != "None").sum()))

st.divider()

data["hour"] = data["timestamp"].dt.hour

hourly = data.groupby("hour", as_index=False)["vehicle_count"].mean()
roads_data = data.groupby("road", as_index=False).agg(
    average_vehicles=("vehicle_count", "mean"),
    average_speed=("avg_speed_kmh", "mean")
)

district_data = data.groupby("district", as_index=False).agg(
    total_vehicles=("vehicle_count", "sum")
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        px.line(
            hourly, x="hour", y="vehicle_count",
            markers=True, title="Average Traffic by Hour"
        ),
        use_container_width=True
    )

with right:
    st.plotly_chart(
        px.bar(
            roads_data, x="road", y="average_vehicles",
            color="average_speed", title="Road Congestion Analysis"
        ),
        use_container_width=True
    )

st.plotly_chart(
    px.bar(
        district_data, x="district", y="total_vehicles",
        title="District-wise Traffic Volume"
    ),
    use_container_width=True
)

incidents = (
    data[data["incident"] != "None"]
    .groupby("incident").size()
    .reset_index(name="count")
)

if not incidents.empty:
    st.plotly_chart(
        px.pie(
            incidents, names="incident", values="count",
            hole=0.4, title="Traffic Incident Distribution"
        ),
        use_container_width=True
    )

st.subheader("Traffic Dataset")
st.dataframe(data, use_container_width=True)

st.download_button(
    "Download CSV",
    data=data.drop(columns=["hour"]).to_csv(index=False),
    file_name="traffic_data.csv",
    mime="text/csv"
)

image_path = Path("outputs/traffic_dashboard.png")
if image_path.exists():
    with st.expander("View static dashboard output"):
        st.image(str(image_path), caption="Traffic Analysis Output")

st.success("Traffic analysis completed!")