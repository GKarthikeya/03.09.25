import streamlit as st
from attendance_scraper import login_and_get_attendance
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Attendance Tracker", layout="wide")

st.title("📊 Attendance Tracker")

# User Login Input
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Fetch Attendance"):
    if not username or not password:
        st.error("⚠️ Please enter both username and password")
    else:
        with st.spinner("Logging in and fetching data..."):
            result = login_and_get_attendance(username, password)

        if not result["overall"]["success"]:
            st.error(result["overall"].get("message", "Login failed"))
        else:
            st.success(f"✅ Attendance fetched successfully!")

            # ------------------------------
            # Overall Stats
            # ------------------------------
            overall = result["overall"]
            st.subheader("📌 Overall Attendance")
            col1, col2, col3 = st.columns(3)
            col1.metric("Present", overall["present"])
            col2.metric("Absent", overall["absent"])
            col3.metric("Percentage", f"{overall['percentage']}%")

            # Pie Chart: Present vs Absent
            fig1, ax1 = plt.subplots()
            ax1.pie(
                [overall["present"], overall["absent"]],
                labels=["Present", "Absent"],
                autopct="%1.1f%%",
                startangle=90,
                explode=(0.05, 0),
            )
            ax1.axis("equal")
            st.pyplot(fig1)

            # ------------------------------
            # Subject-wise Stats
            # ------------------------------
            st.subheader("📚 Subject-wise Attendance")

            df = pd.DataFrame([
                {
                    "Course Code": code,
                    "Course Name": sub["name"],
                    "Present": sub["present"],
                    "Absent": sub["absent"],
                    "Percentage": sub["percentage"],
                    "Status": sub["status"]
                }
                for code, sub in result["subjects"].items()
            ])

            st.dataframe(df, use_container_width=True)

            # Bar Chart: Subject-wise Percentages
            st.subheader("📈 Attendance by Subject")
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            ax2.bar(df["Course Code"], df["Percentage"], color="skyblue")
            ax2.axhline(75, color="green", linestyle="--", label="Safe (75%)")
            ax2.axhline(65, color="red", linestyle="--", label="Condonation (65%)")
            ax2.set_ylabel("Percentage %")
            ax2.set_xlabel("Course Code")
            ax2.set_title("Subject-wise Attendance %")
            ax2.legend()
            st.pyplot(fig2)
