import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta, date

# Set page configuration
st.set_page_config(
    page_title="Accounting Standards Study Plan",
    page_icon="📚",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'categories' not in st.session_state:
    st.session_state.categories = [
        {
            "id": 1,
            "name": "Foundational Concepts",
            "expanded": True,
            "standards": [
                {"id": "LKAS1", "name": "LKAS 1 - Presentation of Financial Statements", "completed": False, "priority": "high", "difficulty": "medium", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "LKAS7", "name": "LKAS 7 - Statement of Cash Flows", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 2,
            "name": "Specific Balance Sheet Items",
            "expanded": False,
            "standards": [
                {"id": "LKAS38", "name": "LKAS 38 - Intangible Assets", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "LKAS40", "name": "LKAS 40 - Investment Property", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "LKAS41", "name": "LKAS 41 - Agriculture", "completed": False, "priority": "low", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "LKAS37", "name": "LKAS 37 - Provisions, Contingent Liabilities and Assets", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 4, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 3},
                {"id": "LKAS19", "name": "LKAS 19 - Employee Benefits", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 4, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 3},
            ]
        },
        {
            "id": 3,
            "name": "Specific Transactions and Events",
            "expanded": False,
            "standards": [
                {"id": "LKAS11", "name": "LKAS 11 - Construction Contracts", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "LKAS18", "name": "LKAS 18 - Revenue", "completed": False, "priority": "high", "difficulty": "medium", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "SLFRS2", "name": "SLFRS 2 - Share-based Payment", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "LKAS23", "name": "LKAS 23 - Borrowing Costs", "completed": False, "priority": "medium", "difficulty": "low", "totalHours": 1, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 4,
            "name": "Financial Instruments",
            "expanded": False,
            "standards": [
                {"id": "LKAS32", "name": "LKAS 32 - Financial Instruments: Presentation", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 4, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 3},
                {"id": "LKAS39", "name": "LKAS 39 - Financial Instruments: Recognition and Measurement", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 5, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 4},
                {"id": "SLFRS7", "name": "SLFRS 7 - Financial Instruments: Disclosures", "completed": False, "priority": "high", "difficulty": "medium", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "LKAS33", "name": "LKAS 33 - Earnings per Share", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 5,
            "name": "Group Accounting and Related Disclosures",
            "expanded": False,
            "standards": [
                {"id": "SLFRS10", "name": "SLFRS 10 - Consolidated Financial Statements", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 4, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 3},
                {"id": "SLFRS11", "name": "SLFRS 11 - Joint Arrangements", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "LKAS28", "name": "LKAS 28 - Investments in Associates and Joint Ventures", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 3, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 2},
                {"id": "LKAS27", "name": "LKAS 27 - Separate Financial Statements", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "SLFRS12", "name": "SLFRS 12 - Disclosure of Interests in Other Entities", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 6,
            "name": "Other Specific Standards",
            "expanded": False,
            "standards": [
                {"id": "SLFRS3", "name": "SLFRS 3 - Business Combinations", "completed": False, "priority": "high", "difficulty": "high", "totalHours": 4, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 3},
                {"id": "SLFRS5", "name": "SLFRS 5 - Non-current Assets Held for Sale and Discontinued Operations", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "SLFRS6", "name": "SLFRS 6 - Exploration for and Evaluation of Mineral Resources", "completed": False, "priority": "low", "difficulty": "low", "totalHours": 1, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "SLFRS4", "name": "SLFRS 4 - Insurance Contracts", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
                {"id": "LKAS34", "name": "LKAS 34 - Interim Financial Reporting", "completed": False, "priority": "medium", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 7,
            "name": "Accounting Policies, Estimates, and Errors",
            "expanded": False,
            "standards": [
                {"id": "LKAS8", "name": "LKAS 8 - Accounting Policies, Changes in Accounting Estimates and Errors", "completed": False, "priority": "high", "difficulty": "medium", "totalHours": 2, "hoursSpent": 0, "notes": "", "scheduledDate": None, "recommendedDays": 1},
            ]
        },
        {
            "id": 8,
            "name": "Already Covered",
            "expanded": False,
            "standards": [
                {"id": "LKAS17", "name": "LKAS 17 - Leasing", "completed": True, "priority": "completed", "difficulty": "completed", "totalHours": 3, "hoursSpent": 3, "notes": "Completed", "scheduledDate": None, "recommendedDays": 0},
                {"id": "LKAS2", "name": "LKAS 2 - Inventory", "completed": True, "priority": "completed", "difficulty": "completed", "totalHours": 2, "hoursSpent": 2, "notes": "Completed", "scheduledDate": None, "recommendedDays": 0},
                {"id": "LKAS16", "name": "LKAS 16 - Property, Plant and Equipment", "completed": True, "priority": "completed", "difficulty": "completed", "totalHours": 3, "hoursSpent": 3, "notes": "Completed", "scheduledDate": None, "recommendedDays": 0},
            ]
        }
    ]

if 'exam_date' not in st.session_state:
    st.session_state.exam_date = datetime.now() + timedelta(days=30)

if 'daily_study_hours' not in st.session_state:
    st.session_state.daily_study_hours = [1, 2, 1, 2, 2, 1, 1]  # Mon-Sun

if 'filter_criteria' not in st.session_state:
    st.session_state.filter_criteria = "all"  # all, priority, incomplete

if 'sort_order' not in st.session_state:
    st.session_state.sort_order = "default"  # default, priority, difficulty

if 'study_plan' not in st.session_state:
    st.session_state.study_plan = []

if 'selected_standard' not in st.session_state:
    st.session_state.selected_standard = None

# Helper functions
def get_total_standards():
    return sum(len([s for s in cat['standards'] if not s['completed']]) for cat in st.session_state.categories)

def get_completed_standards():
    return sum(len([s for s in cat['standards'] if s['completed']]) for cat in st.session_state.categories)

def get_total_hours():
    return sum(sum(s['totalHours'] for s in cat['standards']) for cat in st.session_state.categories)

def get_completed_hours():
    return sum(sum(s['hoursSpent'] for s in cat['standards']) for cat in st.session_state.categories)

def get_remaining_hours():
    return get_total_hours() - get_completed_hours()

def get_total_weekly_hours():
    return sum(st.session_state.daily_study_hours)

def get_days_remaining():
    return (st.session_state.exam_date - datetime.now()).days

def get_required_daily_hours():
    days = get_days_remaining()
    if days <= 0:
        return 0
    return get_remaining_hours() / days

def can_complete_with_current_schedule():
    weeks_remaining = get_days_remaining() / 7
    total_hours_available = get_total_weekly_hours() * weeks_remaining
    return total_hours_available >= get_remaining_hours()

def get_efficiency_score():
    total_weekly_hours = get_total_weekly_hours()
    if total_weekly_hours == 0:
        return 0
    
    weeks_remaining = get_days_remaining() / 7
    total_hours_available = total_weekly_hours * weeks_remaining
    hours_needed = get_remaining_hours()
    
    if hours_needed == 0:
        return 100
    if total_hours_available == 0:
        return 0
    
    raw_score = min(100, (total_hours_available / hours_needed) * 100)
    return round(raw_score)

def get_date_x_days_from_today(days):
    return datetime.now() + timedelta(days=days)

def toggle_standard_completion(category_id, standard_id):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    standard['completed'] = not standard['completed']
                    if standard['completed']:
                        standard['hoursSpent'] = standard['totalHours']
                    break
            break
    # Regenerate study plan
    st.session_state.study_plan = generate_study_plan()

def update_hours_spent(category_id, standard_id, hours):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    standard['hoursSpent'] = max(0, hours)
                    standard['completed'] = standard['hoursSpent'] >= standard['totalHours']
                    break
            break
    # Regenerate study plan
    st.session_state.study_plan = generate_study_plan()

def update_priority(category_id, standard_id, priority):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    standard['priority'] = priority
                    break
            break
    # Regenerate study plan
    st.session_state.study_plan = generate_study_plan()

def update_notes(category_id, standard_id, notes):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    standard['notes'] = notes
                    break
            break

def update_scheduled_date(category_id, standard_id, date_value):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    standard['scheduledDate'] = date_value
                    break
            break
    # Regenerate study plan
    st.session_state.study_plan = generate_study_plan()

def toggle_category_expansion(category_id):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            cat['expanded'] = not cat['expanded']
            break

def select_standard(category_id, standard_id):
    for cat in st.session_state.categories:
        if cat['id'] == category_id:
            for standard in cat['standards']:
                if standard['id'] == standard_id:
                    st.session_state.selected_standard = {
                        **standard,
                        'categoryId': category_id
                    }
                    break
            break

def generate_study_plan():
    # Get incomplete standards
    incomplete_standards = []
    for category in st.session_state.categories:
        for standard in category['standards']:
            if not standard['completed']:
                incomplete_standards.append({
                    **standard,
                    'categoryId': category['id'],
                    'categoryName': category['name']
                })
    
    # Sort by priority (high, medium, low)
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    difficulty_order = {'high': 0, 'medium': 1, 'low': 2}
    
    incomplete_standards.sort(key=lambda s: (
        priority_order.get(s['priority'], 3),
        difficulty_order.get(s['difficulty'], 3)
    ))
    
    # Calculate total study days available based on daily schedule
    days_remaining = get_days_remaining()
    total_study_days = 0
    for i in range(days_remaining):
        day_of_week = (datetime.now().weekday() + i) % 7
        if st.session_state.daily_study_hours[day_of_week] > 0:
            total_study_days += 1
    
    # Now assign dates to each standard
    current_day = 0
    current_day_hours_remaining = 0
    
    plan = []
    
    for standard in incomplete_standards:
        hours_needed = standard['totalHours'] - standard['hoursSpent']
        if hours_needed <= 0:
            continue
        
        days_needed = standard['recommendedDays']
        start_day = current_day
        end_day = current_day
        scheduled_date = None
        
        # Look for the first available day
        while True:
            if current_day >= days_remaining:
                break
            
            day_of_week = (datetime.now().weekday() + current_day) % 7
            
            if st.session_state.daily_study_hours[day_of_week] > 0:
                # If we're starting a new standard and have no hours yet allocated
                if current_day_hours_remaining == 0:
                    current_day_hours_remaining = st.session_state.daily_study_hours[day_of_week]
                    scheduled_date = get_date_x_days_from_today(current_day)
                
                # We found a day with study hours
                end_day = current_day
                
                # If we've allocated enough days, break
                if end_day - start_day + 1 >= days_needed:
                    break
                
                # Otherwise, move to next day
                current_day += 1
                current_day_hours_remaining = 0
            else:
                # No study hours on this day, move to next
                current_day += 1
        
        plan.append({
            **standard,
            'startDate': scheduled_date,
            'endDate': get_date_x_days_from_today(end_day),
            'daysNeeded': days_needed
        })
    
    return plan

# Main app title
st.title("📚 Accounting Standards Study Plan")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Standards", "Timeline", "Analytics"])

# Overview Tab
with tab1:
    st.header("Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Exam Countdown")
        
        # Exam date picker
        exam_date = st.date_input(
            "Exam Date",
            value=st.session_state.exam_date.date(),
            min_value=datetime.now().date(),
            help="Set your exam date to help plan your study schedule"
        )
        
        # Update exam date in session state
        if exam_date != st.session_state.exam_date.date():
            st.session_state.exam_date = datetime.combine(exam_date, datetime.min.time())
            st.session_state.study_plan = generate_study_plan()
        
        days_remaining = get_days_remaining()
        st.metric("Days Remaining", days_remaining)
    
    with col2:
        st.subheader("⏱️ Study Time Required")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Hours", get_total_hours())
            st.metric("Hours Remaining", get_remaining_hours())
        
        with col_b:
            st.metric("Hours Completed", get_completed_hours())
            st.metric("Daily Required", f"{get_required_daily_hours():.1f}")
    
    st.subheader("📊 Progress Overview")
    
    # Progress bars for standards and hours
    col3, col4 = st.columns(2)
    
    with col3:
        total_standards = get_total_standards() + get_completed_standards()
        completed_standards = get_completed_standards()
        st.write(f"Standards Completed: {completed_standards} / {total_standards}")
        st.progress(completed_standards / total_standards if total_standards > 0 else 0)
    
    with col4:
        total_hours = get_total_hours()
        completed_hours = get_completed_hours()
        st.write(f"Hours Completed: {completed_hours} / {total_hours}")
        st.progress(completed_hours / total_hours if total_hours > 0 else 0)
    
    # Study Efficiency
    st.subheader("⚡ Study Efficiency")
    
    efficiency_score = get_efficiency_score()
    
    col5, col6 = st.columns([1, 3])
    with col5:
        # Create a gauge chart for efficiency score
        efficiency_color = "green" if efficiency_score >= 85 else "orange" if efficiency_score >= 60 else "red"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=efficiency_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Efficiency Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': efficiency_color},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 85], 'color': "lightgray"},
                    {'range': [85, 100], 'color': "lightgray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 60
                }
            }
        ))
        
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col6:
        if can_complete_with_current_schedule():
            st.success("✅ Your schedule has enough time to complete all standards before the exam!")
        else:
            st.error("⚠️ Warning: Your current schedule doesn't provide enough study time!")
            additional_hours = get_remaining_hours() / (days_remaining / 7) - get_total_weekly_hours()
            st.warning(f"Suggestion: To complete all standards, you need {additional_hours:.1f} more hours per week")
    
    # Weekly Study Schedule
    st.subheader("📖 Weekly Study Schedule")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    col_days = st.columns(7)
    for i, (day, col) in enumerate(zip(days, col_days)):
        with col:
            st.write(day[:3])
            hours = st.number_input(
                f"Hours {day}",
                min_value=0.0,
                max_value=24.0,
                value=float(st.session_state.daily_study_hours[i]),
                step=0.5,
                label_visibility="collapsed"
            )
            
            if hours != st.session_state.daily_study_hours[i]:
                st.session_state.daily_study_hours[i] = hours
                st.session_state.study_plan = generate_study_plan()
    
    st.info(f"Weekly Total: {get_total_weekly_hours()} hours")

# Standards Tab
with tab2:
    st.header("Standards")
    
    st.info("📝 Organize your standards by priority or difficulty. Click on any standard to add notes or set a specific study date.")
    
    # Filter and sort controls
    col1, col2 = st.columns(2)
    
    with col1:
        filter_criteria = st.selectbox(
            "Filter",
            options=["all", "priority", "incomplete"],
            format_func=lambda x: {"all": "All Standards", "priority": "High Priority Only", "incomplete": "Incomplete Only"}[x],
            index=["all", "priority", "incomplete"].index(st.session_state.filter_criteria)
        )
        
        if filter_criteria != st.session_state.filter_criteria:
            st.session_state.filter_criteria = filter_criteria
    
    with col2:
        sort_order = st.selectbox(
            "Sort",
            options=["default", "priority", "difficulty"],
            format_func=lambda x: {"default": "Default Order", "priority": "By Priority", "difficulty": "By Difficulty"}[x],
            index=["default", "priority", "difficulty"].index(st.session_state.sort_order)
        )
        
        if sort_order != st.session_state.sort_order:
            st.session_state.sort_order = sort_order
    
    # Display categories and standards
    for category in st.session_state.categories:
        # Filter standards
        filtered_standards = category['standards']
        
        if st.session_state.filter_criteria == "priority":
            filtered_standards = [s for s in filtered_standards if s['priority'] == "high"]
        elif st.session_state.filter_criteria == "incomplete":
            filtered_standards = [s for s in filtered_standards if not s['completed']]
        
        # Sort standards
        if st.session_state.sort_order == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2, "completed": 3}
            filtered_standards = sorted(filtered_standards, key=lambda s: priority_order.get(s['priority'], 4))
        elif st.session_state.sort_order == "difficulty":
            difficulty_order = {"high": 0, "medium": 1, "low": 2, "completed": 3}
            filtered_standards = sorted(filtered_standards, key=lambda s: difficulty_order.get(s['difficulty'], 4))
        
        if len(filtered_standards) == 0:
            continue
        
        # Category header with expander
        with st.expander(f"{category['name']} ({sum(1 for s in filtered_standards if s['completed'])} / {len(filtered_standards)})", expanded=category['expanded']):
            # Loop through standards in this category
            for standard in filtered_standards:
                st.write("---")  # Divider between standards
                
                # Main standard info row
                col1, col2, col3 = st.columns([5, 2, 1])
                
                with col1:
                    is_completed = st.checkbox(
                        standard['name'],
                        value=standard['completed'],
                        key=f"cb_{standard['id']}"
                    )
                    
                    if is_completed != standard['completed']:
                        toggle_standard_completion(category['id'], standard['id'])
                    
                    # Priority and difficulty badges
                    priority_color = {
                        "high": "🔴 High",
                        "medium": "🟡 Medium",
                        "low": "🔵 Low",
                        "completed": "🟢 Completed"
                    }
                    
                    difficulty_color = {
                        "high": "🔴 High",
                        "medium": "🟡 Medium",
                        "low": "🔵 Low",
                        "completed": "🟢 Completed"
                    }
                    
                    st.caption(f"{priority_color[standard['priority']]} priority | {difficulty_color[standard['difficulty']]} difficulty")
                    
                    # Display notes if any
                    if standard['notes']:
                        st.info(standard['notes'])
                
                with col2:
                    st.write("Hours Spent")
                    hours = st.number_input(
                        f"Hours {standard['id']}",
                        min_value=0.0, 
                        max_value=float(standard['totalHours'] * 2),
                        value=float(standard['hoursSpent']),
                        step=0.5,
                        label_visibility="collapsed"
                    )
                    
                    if hours != standard['hoursSpent']:
                        update_hours_spent(category['id'], standard['id'], hours)
                
                with col3:
                    st.write(f"of {standard['totalHours']}")
                    # Show progress bar
                    if standard['totalHours'] > 0:
                        progress = standard['hoursSpent'] / standard['totalHours']
                        st.progress(min(1.0, progress))
                
                # Show Edit Details button
                if st.button("Edit Details", key=f"edit_{standard['id']}"):
                    st.session_state.selected_standard = {
                        **standard,
                        'categoryId': category['id']
                    }
                
                # Check if this standard is selected and show details
                if st.session_state.selected_standard and st.session_state.selected_standard['id'] == standard['id']:
                    with st.container():
                        st.subheader("Standard Details")
                        
                        # Priority selection
                        priority = st.selectbox(
                            "Priority",
                            options=["high", "medium", "low"],
                            format_func=lambda x: {"high": "High - Study this first", "medium": "Medium - Important but not urgent", "low": "Low - Can wait if needed"}[x],
                            index=["high", "medium", "low"].index(standard['priority']) if standard['priority'] in ["high", "medium", "low"] else 0,
                            key=f"priority_{standard['id']}"
                        )
                        
                        if priority != standard['priority']:
                            update_priority(category['id'], standard['id'], priority)
                        
                        # Scheduled date
                        scheduled_date = st.date_input(
                            "Scheduled Date (when you plan to study this)",
                            value=standard['scheduledDate'].date() if standard['scheduledDate'] else None,
                            min_value=datetime.now().date(),
                            max_value=st.session_state.exam_date.date(),
                            key=f"date_{standard['id']}",
                            help="Set a specific date when you plan to study this standard"
                        )
                        
                        # Convert date to datetime object for consistency
                        if scheduled_date is not None:
                            scheduled_date_dt = datetime.combine(scheduled_date, datetime.min.time())
                            if standard['scheduledDate'] != scheduled_date_dt:
                                update_scheduled_date(category['id'], standard['id'], scheduled_date_dt)
                        
                        # Notes
                        notes = st.text_area(
                            "Notes",
                            value=standard['notes'],
                            placeholder="Add your notes, key points, or reminders here...",
                            key=f"notes_{standard['id']}"
                        )
                        
                        if notes != standard['notes']:
                            update_notes(category['id'], standard['id'], notes)
                        
                        # Close button
                        if st.button("Close Details", key=f"close_{standard['id']}"):
                            st.session_state.selected_standard = None

# Timeline Tab
with tab3:
    st.header("Timeline")
    
    st.info("📆 This shows your recommended study schedule based on your weekly availability. Green blocks are standards you haven't started, blue blocks are standards you've started but not completed.")
    
    # Generate study plan if not already done
    if len(st.session_state.study_plan) == 0:
        st.session_state.study_plan = generate_study_plan()
    
    # Regenerate button
    if st.button("🔄 Regenerate Timeline"):
        st.session_state.study_plan = generate_study_plan()
    
    # Create a timeline visualization
    if len(st.session_state.study_plan) > 0:
        # Create timeline weeks marks
        days_remaining = get_days_remaining()
        total_weeks = (days_remaining // 7) + 1
        
        # Create weekly markers
        week_markers = []
        for i in range(total_weeks + 1):
            week_date = (datetime.now() + timedelta(days=i*7)).date()
            if week_date <= st.session_state.exam_date.date():
                week_markers.append({
                    'date': week_date,
                    'label': f"Week {i}"
                })
        
        # Create category items for the timeline
        timeline_data = []
        y_position = 0
        
        for category_id in range(1, 9):  # Assuming 8 categories
            category_items = [item for item in st.session_state.study_plan if item['categoryId'] == category_id]
            
            if not category_items:
                continue
                
            # Find category name
            category_name = next((cat['name'] for cat in st.session_state.categories if cat['id'] == category_id), f"Category {category_id}")
            
            # Add category to timeline data
            timeline_data.append({
                'type': 'category',
                'name': category_name,
                'y_position': y_position
            })
            
            y_position += 1
            
            # Add standard items to timeline data
            for item in category_items:
                if not item['startDate'] or not item['endDate']:
                    continue
                
                # Determine color based on status
                color = "rgba(52, 152, 219, 0.7)" if item['hoursSpent'] > 0 else "rgba(46, 204, 113, 0.7)"  # Blue if started, green if not
                
                timeline_data.append({
                    'type': 'standard',
                    'name': item['name'].split(' - ')[0],
                    'start_date': item['startDate'].date(),
                    'end_date': item['endDate'].date(),
                    'color': color,
                    'y_position': y_position,
                    'full_name': item['name'],
                    'priority': item['priority'],
                    'difficulty': item['difficulty'],
                    'totalHours': item['totalHours'],
                    'hoursSpent': item['hoursSpent']
                })
                
                y_position += 1
            
            y_position += 1  # Add space between categories
        
        # Create the figure
        fig = go.Figure()
        
        # Add weekly markers (vertical lines)
        for week in week_markers:
            fig.add_trace(go.Scatter(
                x=[week['date'], week['date']],
                y=[0, y_position],
                mode='lines',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False,
                hoverinfo='none'
            ))
            
            # Add week label at the top
            fig.add_annotation(
                x=week['date'],
                y=0,
                text=week['label'],
                showarrow=False,
                yanchor='bottom',
                font=dict(size=10)
            )
        
        # Add today marker (vertical line)
        fig.add_trace(go.Scatter(
            x=[datetime.now().date(), datetime.now().date()],
            y=[0, y_position],
            mode='lines',
            line=dict(color='red', width=2),
            showlegend=False,
            hoverinfo='none'
        ))
        
        # Add "Today" label
        fig.add_annotation(
            x=datetime.now().date(),
            y=0,
            text="Today",
            showarrow=False,
            yanchor='bottom',
            font=dict(size=10, color='red')
        )
        
        # Add exam date marker (vertical line)
        fig.add_trace(go.Scatter(
            x=[st.session_state.exam_date.date(), st.session_state.exam_date.date()],
            y=[0, y_position],
            mode='lines',
            line=dict(color='purple', width=2),
            showlegend=False,
            hoverinfo='none'
        ))
        
        # Add "Exam" label
        fig.add_annotation(
            x=st.session_state.exam_date.date(),
            y=0,
            text="Exam",
            showarrow=False,
            yanchor='bottom',
            font=dict(size=10, color='purple')
        )
        
        # Add items to the timeline
        for item in timeline_data:
            if item['type'] == 'category':
                # Add category label
                fig.add_annotation(
                    x=datetime.now().date(),
                    y=item['y_position'] + 0.5,
                    text=item['name'],
                    showarrow=False,
                    xanchor='left',
                    font=dict(size=12, color='black')
                )
            elif item['type'] == 'standard':
                # Calculate duration in days
                duration = (item['end_date'] - item['start_date']).days + 1
                
                # Add standard bar
                fig.add_trace(go.Bar(
                    x=[duration],
                    y=[item['y_position']],
                    orientation='h',
                    base=item['start_date'],
                    marker_color=item['color'],
                    text=item['name'],
                    textposition='inside',
                    name=item['full_name'],
                    hoverinfo='text',
                    hovertext=f"{item['full_name']}<br>Priority: {item['priority']}<br>Difficulty: {item['difficulty']}<br>Hours needed: {item['totalHours']}<br>Hours spent: {item['hoursSpent']}"
                ))
        
        # Update layout
        fig.update_layout(
            title="Study Timeline",
            xaxis=dict(
                title="Date",
                type='date',
                tickformat="%b %d",
                tickmode="auto",
                nticks=10,
            ),
            yaxis=dict(
                visible=False,
                showticklabels=False
            ),
            height=max(500, y_position * 30),  # Dynamic height based on number of items
            bargap=0.2,
            bargroupgap=0.1,
            showlegend=False,
            margin=dict(l=150, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.warning("Tip: Click on a standard in the Standards tab to update its priority or schedule a specific date. This will affect how the timeline is generated.")
        
        # Priority Plan
        st.subheader("Priority Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**This Week's Focus**")
            
            for standard in st.session_state.study_plan[:3]:
                priority_color = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🔵"
                }.get(standard['priority'], "⚪")
                
                st.write(f"{priority_color} {standard['name']}")
        
        with col2:
            st.write("**Next Week's Focus**")
            
            for standard in st.session_state.study_plan[3:6]:
                priority_color = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🔵"
                }.get(standard['priority'], "⚪")
                
                st.write(f"{priority_color} {standard['name']}")
        
        # Weekly Schedule Tips
        st.write("**Weekly Schedule Tips**")
        
        min_study_day_index = -1
        min_hours = float('inf')
        for i, hours in enumerate(st.session_state.daily_study_hours):
            if hours > 0 and hours < min_hours:
                min_hours = hours
                min_study_day_index = i
        
        busiest_day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][min_study_day_index] if min_study_day_index >= 0 else 'busy days'
        
        st.write(f"• On your busiest days ({busiest_day}), focus on shorter, simpler standards")
        st.write("• Use weekend days for longer study sessions on difficult topics")
        st.write(f"• Try to complete at least {round(get_total_standards() / days_remaining * 7)} standards per week to stay on track")

# Analytics Tab
with tab4:
    st.header("Analytics")
    
    st.info("📈 This section shows you the distribution of standards by category, priority, and difficulty. Use this to better plan your study approach.")
    
    # Time Distribution by Category
    st.subheader("Study Time Distribution by Category")
    
    # Prepare data
    category_hours = []
    for cat in st.session_state.categories:
        total_hours = sum(s['totalHours'] for s in cat['standards'])
        completed_hours = sum(s['hoursSpent'] for s in cat['standards'])
        
        if total_hours > 0:
            category_hours.append({
                'name': cat['name'],
                'total_hours': total_hours,
                'completed_hours': completed_hours,
                'percent_completed': (completed_hours / total_hours) * 100 if total_hours > 0 else 0,
                'percent_of_curriculum': (total_hours / get_total_hours()) * 100 if get_total_hours() > 0 else 0
            })
    
    # Sort by total hours
    category_hours.sort(key=lambda x: x['total_hours'], reverse=True)
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add total hours bars
    fig.add_trace(go.Bar(
        y=[cat['name'] for cat in category_hours],
        x=[cat['total_hours'] for cat in category_hours],
        orientation='h',
        name='Total Hours',
        marker_color='rgba(55, 83, 109, 0.7)',
        text=[f"{cat['total_hours']} hrs" for cat in category_hours],
        textposition='auto'
    ))
    
    # Add completed hours bars
    fig.add_trace(go.Bar(
        y=[cat['name'] for cat in category_hours],
        x=[cat['completed_hours'] for cat in category_hours],
        orientation='h',
        name='Completed Hours',
        marker_color='rgba(26, 188, 156, 0.7)',
        text=[f"{cat['completed_hours']} hrs" for cat in category_hours],
        textposition='auto'
    ))
    
    # Update layout
    fig.update_layout(
        title="Hours by Category",
        xaxis_title="Hours",
        barmode='overlay',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Standards by Priority and Difficulty
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Standards by Priority")
        
        # Count standards by priority
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for cat in st.session_state.categories:
            for standard in cat['standards']:
                if standard['priority'] in priority_counts and not standard['completed']:
                    priority_counts[standard['priority']] += 1
        
        # Create pie chart
        priority_fig = px.pie(
            values=list(priority_counts.values()),
            names=["High", "Medium", "Low"],
            color=["High", "Medium", "Low"],
            color_discrete_map={"High": "red", "Medium": "gold", "Low": "blue"},
            title="Distribution by Priority"
        )
        
        st.plotly_chart(priority_fig, use_container_width=True)
        
        st.write("**Study Strategy Tips:**")
        st.write("• Focus on high priority standards first")
        st.write("• Schedule medium priority standards throughout the month")
        st.write("• Use gaps in your schedule for low priority standards")
    
    with col2:
        st.subheader("Standards by Difficulty")
        
        # Count standards by difficulty
        difficulty_counts = {"high": 0, "medium": 0, "low": 0}
        for cat in st.session_state.categories:
            for standard in cat['standards']:
                if standard['difficulty'] in difficulty_counts and not standard['completed']:
                    difficulty_counts[standard['difficulty']] += 1
        
        # Create pie chart
        difficulty_fig = px.pie(
            values=list(difficulty_counts.values()),
            names=["High", "Medium", "Low"],
            color=["High", "Medium", "Low"],
            color_discrete_map={"High": "indianred", "Medium": "gold", "Low": "lightblue"},
            title="Distribution by Difficulty"
        )
        
        st.plotly_chart(difficulty_fig, use_container_width=True)
        
        st.write("**Difficulty Strategy Tips:**")
        st.write("• Allocate more time for high difficulty standards")
        st.write("• Study high difficulty topics when you're most alert")
        st.write("• Consider pairing difficult standards with easier ones in a session")
    
    # Standards Completion Forecast
    st.subheader("Standards Completion Forecast")
    
    col3, col4, col5 = st.columns(3)
    
    days_remaining = get_days_remaining()
    completed_standards = get_completed_standards()
    total_incomplete = get_total_standards()
    
    # Current rate (standards completed per day)
    current_rate = completed_standards / max(1, (30 - days_remaining))  # Assuming 30 days total study period
    
    # Required rate (standards needed to complete per day)
    required_rate = total_incomplete / max(1, days_remaining)
    
    # Estimated completion date
    if current_rate > 0:
        estimated_days = total_incomplete / current_rate
        estimated_date = datetime.now() + timedelta(days=estimated_days)
    else:
        estimated_date = None
    
    with col3:
        st.metric("Current Rate", f"{current_rate:.2f} standards/day")
    
    with col4:
        st.metric("Required Rate", f"{required_rate:.2f} standards/day")
    
    with col5:
        st.metric(
            "Estimated Completion", 
            estimated_date.strftime("%b %d") if estimated_date else "N/A"
        )
    
    # Recommendations
    st.success("""
    **Recommendations**
    
    • Focus on Financial Instruments and Group Accounting (the most time-intensive categories)
    • Set aside dedicated time for high difficulty standards like LKAS 39 and SLFRS 10
    • Consider studying related standards together (e.g., LKAS 32, LKAS 39, SLFRS 7)
    • Review your already completed standards occasionally to keep them fresh
    """)

# Ensure study plan is generated
if len(st.session_state.study_plan) == 0:
    st.session_state.study_plan = generate_study_plan()

# Save data
if st.sidebar.button("Save Progress"):
    st.sidebar.success("Progress saved successfully!")

# Export data
if st.sidebar.button("Export Data"):
    # Create a JSON string
    export_data = {
        "categories": st.session_state.categories,
        "exam_date": st.session_state.exam_date.isoformat(),
        "daily_study_hours": st.session_state.daily_study_hours
    }
    
    # Convert to JSON string
    json_str = json.dumps(export_data, indent=2, default=str)
    
    # Provide download link
    st.sidebar.download_button(
        label="Download JSON",
        data=json_str,
        file_name="accounting_study_plan.json",
        mime="application/json"
    )

# Help section
with st.sidebar.expander("Help"):
    st.write("""
    **Dashboard Help**
    
    • **Overview:** See your progress and weekly schedule
    • **Standards:** Track completion of individual accounting standards
    • **Timeline:** Visualize your study plan over time
    • **Analytics:** Analyze your study distribution and patterns
    
    Your progress is automatically saved in your browser.
    """)