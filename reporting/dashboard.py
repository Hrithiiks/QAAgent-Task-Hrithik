import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Path to the Playwright JSON report.
# This assumes you run the streamlit app from the project's root directory.
REPORT_PATH = os.path.join("playwright_tests", "playwright-report", "results.json")

def load_test_results():
    """Loads and parses the Playwright JSON report."""
    if not os.path.exists(REPORT_PATH):
        st.error(f"Playwright report not found at `{REPORT_PATH}`")
        st.info("Please run `npx playwright test` inside the `playwright_tests` directory first to generate a report.")
        return None

    with open(REPORT_PATH) as f:
        try:
            # The report is a sequence of JSON objects, one per line. We need to read them all.
            report_data = [json.loads(line) for line in f]
        except json.JSONDecodeError:
            st.error("Could not parse the report file. It might be empty or corrupted.")
            return None

    results = []
    # The new report format is a list of 'suite' events. We need to find the 'testEnd' events.
    for item in report_data:
        if item.get("method") == "onTestEnd":
            test_info = item.get("params", {})
            result_details = test_info.get("result", {})
            
            # Extract the test title from the 'location' object
            location = test_info.get("location", {})
            title_path = location.get("titlePath", [])
            # Join the path parts to get the full test title, skipping the file name
            full_title = " › ".join(title_path[1:]) if len(title_path) > 1 else "Unknown Test"

            results.append({
                "Title": full_title,
                "Status": result_details.get("status"),
                "Duration (ms)": result_details.get("duration", 0),
                "Error": result_details.get("error", {}).get("message", "No error"),
            })

    return pd.DataFrame(results)

# --- Streamlit App ---
st.set_page_config(page_title="QAgenie Test Report", layout="wide")

st.title("🤖 QAgenie - Test Execution Report")
st.markdown(f"**Report Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")

df = load_test_results()

if df is not None and not df.empty:
    st.header("📊 Test Summary")

    total_tests = len(df)
    passed_tests = len(df[df['Status'] == 'passed'])
    failed_tests = len(df[df['Status'] == 'failed'])
    skipped_tests = len(df[df['Status'] == 'skipped'])
    timed_out = len(df[df['Status'] == 'timedOut'])

    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tests", total_tests)
    col2.metric("✅ Passed", passed_tests)
    # Use delta to highlight failures
    col3.metric("❌ Failed", failed_tests, delta=failed_tests if failed_tests > 0 else 0, delta_color="inverse")
    col4.metric("⏭️ Skipped", skipped_tests)

    st.header("📋 Detailed Test Results")

    # Style the dataframe for better readability
    def style_status(val):
        color = "green" if val == "passed" else "red" if val in ["failed", "timedOut"] else "orange"
        return f"color: {color}; font-weight: bold;"

    st.dataframe(df.style.applymap(style_status, subset=['Status']), use_container_width=True)
    
    # Display details for any failed tests
    if failed_tests > 0:
        st.header("🔬 Failure Analysis")
        failed_df = df[df['Status'] == 'failed']
        for index, row in failed_df.iterrows():
            with st.expander(f"Failed: {row['Title']}"):
                st.error(row['Error'])
                st.info("Check the `playwright-report/data` directory for failure screenshots and videos.")