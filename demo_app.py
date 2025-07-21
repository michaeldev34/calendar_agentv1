import streamlit as st
from datetime import datetime, timedelta

# Demo version of the Google Calendar & Tasks Assistant
# This version shows the UI without requiring Google API credentials

st.title("📅 Google Calendar & Tasks Assistant (Demo)")

st.info("🔧 **Demo Mode**: This is a demonstration of the UI. To use with real Google data, configure your Google API credentials in `.streamlit/secrets.toml`")

# Create tabs for Dashboard, Events and Tasks
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "📅 Calendar Events", "✅ Tasks"])

with tab1:
    st.subheader("🏠 Dashboard - Today's Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Today's Events")
        st.markdown("🕒 **09:00** - Team Meeting")
        st.markdown("🕒 **14:30** - Project Review")
        st.markdown("📅 **All Day** - Conference Day")
    
    with col2:
        st.markdown("### ✅ Pending Tasks")
        st.markdown("📋 **Finish project report** (📅 12/25) - *Work*")
        st.markdown("📋 **Buy groceries** - *Personal*")
        st.markdown("📋 **Review code** (📅 12/24) - *Work*")
        st.caption("... and 5 more tasks")
    
    # Quick stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Today's Events", 3)
    
    with col2:
        st.metric("Pending Tasks", 8)
    
    with col3:
        st.metric("This Week's Events", 12)

with tab2:
    st.subheader("📅 Calendar Events")
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now().date())
    with col2:
        end_date = st.date_input("End Date", datetime.now().date() + timedelta(days=7))
    
    # Demo events
    st.subheader("📌 Upcoming Events:")
    st.markdown("- 🕒 **2024-12-24T09:00:00** – Team Meeting")
    st.markdown("- 🕒 **2024-12-24T14:30:00** – Project Review")
    st.markdown("- 🕒 **2024-12-25T10:00:00** – Conference Call")
    st.markdown("- 🕒 **2024-12-26T15:00:00** – Client Presentation")

    st.markdown("---")
    st.subheader("➕ Create New Event")
    new_title = st.text_input("Event Title")

    col1, col2 = st.columns(2)
    with col1:
        s_date = st.date_input("Start Date (Event)", datetime.now().date(), key="event_start_date")
        s_time = st.time_input("Start Time", datetime.now().time(), key="event_start_time")
    with col2:
        e_date = st.date_input("End Date (Event)", datetime.now().date(), key="event_end_date")
        e_time = st.time_input("End Time", (datetime.now() + timedelta(hours=1)).time(), key="event_end_time")

    if st.button("Create Event"):
        if new_title:
            st.success(f"Demo: Event '{new_title}' would be created!")
        else:
            st.error("Please enter an event title.")

with tab3:
    st.subheader("✅ Task Management")
    
    # Task list management
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        task_list_names = ["Work Tasks", "Personal Tasks", "Shopping List"]
        selected_list_index = st.selectbox("Select Task List:", range(len(task_list_names)), 
                                         format_func=lambda x: task_list_names[x])
        selected_list_name = task_list_names[selected_list_index]
    
    with col2:
        st.markdown("##### Create New List")
        new_list_name = st.text_input("List Name", key="new_list_name", placeholder="Enter list name")
        if st.button("Create List", key="create_list_btn"):
            if new_list_name:
                st.success(f"Demo: Task list '{new_list_name}' would be created!")
            else:
                st.error("Please enter a list name.")
    
    st.subheader(f"📋 Tasks in '{selected_list_name}'")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("Show completed tasks", value=False)
    with col2:
        sort_by_due = st.checkbox("Sort by due date", value=True)
    
    # Demo tasks
    demo_tasks = [
        {"title": "Finish project report", "completed": False, "due": "2024-12-25", "notes": "Include all sections"},
        {"title": "Review code", "completed": False, "due": "2024-12-24", "notes": "Focus on security"},
        {"title": "Team meeting prep", "completed": True, "due": None, "notes": ""},
        {"title": "Update documentation", "completed": False, "due": None, "notes": "API docs need updating"},
    ]
    
    # Filter demo tasks
    filtered_tasks = []
    for task in demo_tasks:
        if show_completed or not task["completed"]:
            filtered_tasks.append(task)
    
    if filtered_tasks:
        for i, task in enumerate(filtered_tasks):
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            
            with col1:
                # Checkbox for task completion
                is_completed = task["completed"]
                if st.checkbox("Complete", value=is_completed, key=f"demo_task_{i}", label_visibility="collapsed"):
                    if not is_completed:
                        st.success("Demo: Task marked as complete!")
                        st.rerun()
                else:
                    if is_completed:
                        st.success("Demo: Task marked as incomplete!")
                        st.rerun()
            
            with col2:
                # Task title and notes
                title = task["title"]
                notes = task["notes"]
                due_date = task["due"]
                
                if is_completed:
                    st.markdown(f"~~{title}~~")
                else:
                    st.markdown(f"**{title}**")
                
                if notes:
                    st.caption(f"📝 {notes}")
                if due_date:
                    # Check if overdue
                    due_dt = datetime.strptime(due_date, '%Y-%m-%d').date()
                    today = datetime.now().date()
                    if due_dt < today and not is_completed:
                        st.caption(f"🔴 **Overdue**: {due_date}")
                    elif due_dt == today and not is_completed:
                        st.caption(f"🟡 **Due Today**: {due_date}")
                    else:
                        st.caption(f"📅 Due: {due_date}")
            
            with col3:
                # Delete button
                if st.button("🗑️", key=f"demo_delete_{i}", help="Delete task"):
                    st.success("Demo: Task would be deleted!")
                    st.rerun()
    else:
        st.info("No tasks match the current filter.")
    
    # Create new task
    st.markdown("---")
    st.subheader("➕ Create New Task")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        new_task_title = st.text_input("Task Title", key="new_task_title")
        new_task_notes = st.text_area("Task Notes (optional)", key="new_task_notes")
    with col2:
        new_task_due = st.date_input("Due Date (optional)", value=None, key="new_task_due")
    
    if st.button("Create Task"):
        if new_task_title:
            st.success(f"Demo: Task '{new_task_title}' would be created!")
        else:
            st.error("Please enter a task title.")

st.markdown("---")
st.markdown("### 🔧 Setup Instructions")
st.markdown("""
To use this app with real Google Calendar and Tasks data:

1. **Get Google API Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Calendar API and Google Tasks API
   - Create OAuth 2.0 credentials (Web application)
   - Add `http://localhost:8501` to authorized redirect URIs

2. **Configure Secrets:**
   - Edit `.streamlit/secrets.toml` in this directory
   - Replace the placeholder values with your actual credentials

3. **Run the Real App:**
   - Use `python -m streamlit run app.py` instead of this demo

**Current Demo Features:**
- ✅ Dashboard with overview
- ✅ Calendar events display and creation form
- ✅ Task management with filtering
- ✅ Task creation and completion
- ✅ Visual indicators for due dates
""")
