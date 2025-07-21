import streamlit as st
import os
import json
import re
from datetime import datetime, timedelta, time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from urllib.parse import urlencode
import dateutil.parser as date_parser

def get_auth_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": st.secrets["CLIENT_ID"],
                "client_secret": st.secrets["CLIENT_SECRET"],
                "redirect_uris": [st.secrets["REDIRECT_URI"]],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/tasks'
        ],
        redirect_uri=st.secrets["REDIRECT_URI"]
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    return auth_url

def exchange_code_for_credentials(code):
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": st.secrets["CLIENT_ID"],
                    "client_secret": st.secrets["CLIENT_SECRET"],
                    "redirect_uris": [st.secrets["REDIRECT_URI"]],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=[
                'https://www.googleapis.com/auth/calendar',
                'https://www.googleapis.com/auth/tasks'
            ],
            redirect_uri=st.secrets["REDIRECT_URI"]
        )
        flow.fetch_token(code=code)
        return flow.credentials
    except Exception as e:
        st.error(f"OAuth token exchange failed: {e}")
        return None

def get_calendar_events(creds, time_min=None, time_max=None):
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z'
    if not time_min:
        time_min = now
    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          maxResults=20, singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])

def create_event(creds, summary, start_time, end_time):
    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event

def get_task_lists(creds):
    service = build('tasks', 'v1', credentials=creds)
    try:
        result = service.tasklists().list().execute()
        return result.get('items', [])
    except Exception as e:
        st.error(f"Error fetching task lists: {e}")
        return []

def get_tasks(creds, tasklist_id):
    service = build('tasks', 'v1', credentials=creds)
    try:
        result = service.tasks().list(tasklist=tasklist_id).execute()
        return result.get('items', [])
    except Exception as e:
        st.error(f"Error fetching tasks: {e}")
        return []

def create_task(creds, tasklist_id, title, notes=None, due=None):
    service = build('tasks', 'v1', credentials=creds)
    task = {'title': title}
    if notes:
        task['notes'] = notes
    if due:
        task['due'] = due
    
    try:
        created_task = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
        return created_task
    except Exception as e:
        st.error(f"Error creating task: {e}")
        return None

# Natural Language Processing Functions
def parse_user_message(message):
    """Parse user message to determine intent and extract information."""
    message = message.lower().strip()
    
    # Intent detection patterns
    task_patterns = [
        r'create task|add task|new task|make task|task:',
        r'remind me to|i need to|todo|to do',
        r'add to my tasks|put on my task list'
    ]
    
    event_patterns = [
        r'create event|add event|new event|schedule|meeting',
        r'book|appointment|calendar|plan for',
        r'set up a meeting|arrange'
    ]
    
    # Check for task creation
    for pattern in task_patterns:
        if re.search(pattern, message):
            return parse_task_request(message)
    
    # Check for event creation
    for pattern in event_patterns:
        if re.search(pattern, message):
            return parse_event_request(message)
    
    # Default response for general queries
    return {
        'type': 'general',
        'response': "I can help you create tasks and events! Try saying something like:\n"
                   "- 'Create a task to buy groceries'\n"
                   "- 'Schedule a meeting tomorrow at 2pm'\n"
                   "- 'Remind me to call John on Friday'\n"
                   "- 'Add event: Team standup at 9am Monday'"
    }

def parse_task_request(message):
    """Extract task information from user message."""
    # Remove common task prefixes
    task_text = re.sub(r'(create task|add task|new task|make task|remind me to|i need to|todo|to do|task:)\s*', '', message, flags=re.IGNORECASE)
    
    # Extract due date patterns
    due_date = None
    date_patterns = [
        r'(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
        r'(on|by|due)\s+(\d{1,2}[/-]\d{1,2}[/-]?\d{0,4})',
        r'(next week|this week|next month)',
        r'(in \d+ days?|in \d+ weeks?)'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, task_text, re.IGNORECASE)
        if match:
            try:
                due_date = parse_date_string(match.group())
                # Remove the date part from task text
                task_text = re.sub(pattern, '', task_text, flags=re.IGNORECASE).strip()
                break
            except:
                continue
    
    # Clean up task text
    task_text = re.sub(r'\s+', ' ', task_text).strip()
    if not task_text:
        task_text = "New task"
    
    return {
        'type': 'task',
        'title': task_text,
        'due_date': due_date,
        'notes': None
    }

def parse_event_request(message):
    """Extract event information from user message."""
    # Remove common event prefixes
    event_text = re.sub(r'(create event|add event|new event|schedule|meeting|book|appointment|set up a meeting|arrange)\s*', '', message, flags=re.IGNORECASE)
    
    # Extract time patterns
    start_time = None
    end_time = None
    event_date = None
    
    # Time patterns
    time_patterns = [
        r'at (\d{1,2}:\d{2}\s*(?:am|pm)?)',
        r'at (\d{1,2}\s*(?:am|pm))',
        r'(\d{1,2}:\d{2}\s*(?:am|pm)?)',
        r'(\d{1,2}\s*(?:am|pm))'
    ]
    
    # Date patterns
    date_patterns = [
        r'(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
        r'(on|for)\s+(\d{1,2}[/-]\d{1,2}[/-]?\d{0,4})',
        r'(next week|this week|next month)'
    ]
    
    # Extract time
    for pattern in time_patterns:
        match = re.search(pattern, event_text, re.IGNORECASE)
        if match:
            try:
                time_str = match.group(1) if match.group(1) else match.group()
                start_time = parse_time_string(time_str)
                # Remove time from event text
                event_text = re.sub(pattern, '', event_text, flags=re.IGNORECASE).strip()
                break
            except:
                continue
    
    # Extract date
    for pattern in date_patterns:
        match = re.search(pattern, event_text, re.IGNORECASE)
        if match:
            try:
                date_str = match.group()
                event_date = parse_date_string(date_str)
                # Remove date from event text
                event_text = re.sub(pattern, '', event_text, flags=re.IGNORECASE).strip()
                break
            except:
                continue
    
    # Default to today if no date specified
    if not event_date:
        event_date = datetime.now().date()
    
    # Default to current time + 1 hour if no time specified
    if not start_time:
        start_time = (datetime.now() + timedelta(hours=1)).time()
    
    # Default end time to 1 hour after start
    if not end_time:
        start_datetime = datetime.combine(event_date, start_time)
        end_datetime = start_datetime + timedelta(hours=1)
        end_time = end_datetime.time()
    
    # Clean up event text
    event_text = re.sub(r'\s+', ' ', event_text).strip()
    if not event_text:
        event_text = "New event"
    
    return {
        'type': 'event',
        'title': event_text,
        'date': event_date,
        'start_time': start_time,
        'end_time': end_time
    }

def parse_date_string(date_str):
    """Parse various date string formats."""
    date_str = date_str.lower().strip()
    
    # Handle relative dates
    if 'today' in date_str:
        return datetime.now().date()
    elif 'tomorrow' in date_str:
        return (datetime.now() + timedelta(days=1)).date()
    elif 'next week' in date_str:
        return (datetime.now() + timedelta(weeks=1)).date()
    elif 'this week' in date_str:
        return datetime.now().date()
    elif 'next month' in date_str:
        return (datetime.now() + timedelta(days=30)).date()
    
    # Handle day names
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(days):
        if day in date_str:
            today = datetime.now()
            days_ahead = i - today.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).date()
    
    # Try to parse with dateutil
    try:
        return date_parser.parse(date_str).date()
    except:
        return None

def parse_time_string(time_str):
    """Parse time string to time object."""
    time_str = time_str.lower().strip()
    
    try:
        # Handle formats like "2pm", "14:30", "2:30 pm"
        if 'pm' in time_str or 'am' in time_str:
            return datetime.strptime(time_str.replace(' ', ''), '%I%p').time()
        elif ':' in time_str:
            if 'pm' in time_str or 'am' in time_str:
                return datetime.strptime(time_str.replace(' ', ''), '%I:%M%p').time()
            else:
                return datetime.strptime(time_str, '%H:%M').time()
        else:
            # Just hour
            hour = int(time_str)
            return time(hour, 0)
    except:
        return None

# Chat Interface Functions
def process_user_request(message, creds):
    """Process user request and execute actions."""
    parsed = parse_user_message(message)

    if parsed['type'] == 'task':
        # Create task
        task_lists = get_task_lists(creds)
        if not task_lists:
            return "❌ No task lists found. Please create a task list in Google Tasks first."

        # Use selected task list from sidebar or first available list
        if "default_task_list_selector" in st.session_state:
            selected_index = st.session_state.default_task_list_selector
            default_list = task_lists[selected_index] if selected_index < len(task_lists) else task_lists[0]
        else:
            default_list = task_lists[0]

        # Convert due date to ISO format if present
        due_date_iso = None
        if parsed['due_date']:
            due_date_iso = datetime.combine(parsed['due_date'], datetime.min.time()).isoformat() + 'Z'

        created_task = create_task(creds, default_list['id'], parsed['title'], parsed['notes'], due_date_iso)

        if created_task:
            due_info = f" (due: {parsed['due_date']})" if parsed['due_date'] else ""
            return f"✅ Task created: **{parsed['title']}**{due_info} in list '{default_list['title']}'"
        else:
            return "❌ Failed to create task. Please try again."

    elif parsed['type'] == 'event':
        # Create event
        start_datetime = datetime.combine(parsed['date'], parsed['start_time'])
        end_datetime = datetime.combine(parsed['date'], parsed['end_time'])

        start_iso = start_datetime.isoformat()
        end_iso = end_datetime.isoformat()

        created_event = create_event(creds, parsed['title'], start_iso, end_iso)

        if created_event:
            return f"📅 Event created: **{parsed['title']}** on {parsed['date']} from {parsed['start_time']} to {parsed['end_time']}"
        else:
            return "❌ Failed to create event. Please try again."

    else:
        return parsed['response']

def get_quick_overview(creds):
    """Get a quick overview of today's events and pending tasks."""
    today = datetime.now().date()
    today_min = datetime.combine(today, datetime.min.time()).isoformat() + 'Z'
    today_max = datetime.combine(today, datetime.max.time()).isoformat() + 'Z'

    # Get today's events
    today_events = get_calendar_events(creds, today_min, today_max)

    # Get pending tasks
    task_lists = get_task_lists(creds)
    pending_tasks = []

    for task_list in task_lists:
        tasks = get_tasks(creds, task_list['id'])
        for task in tasks:
            if task.get('status') != 'completed':
                task['list_name'] = task_list['title']
                pending_tasks.append(task)

    # Format overview
    overview = "📊 **Today's Overview:**\n\n"

    # Events
    if today_events:
        overview += "📅 **Today's Events:**\n"
        for event in today_events[:3]:  # Show max 3 events
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', '(No Title)')
            if 'T' in start:
                event_time = datetime.fromisoformat(start.replace('Z', '+00:00')).strftime('%H:%M')
                overview += f"• {event_time} - {summary}\n"
            else:
                overview += f"• All Day - {summary}\n"
        if len(today_events) > 3:
            overview += f"• ... and {len(today_events) - 3} more events\n"
    else:
        overview += "📅 **Today's Events:** None scheduled\n"

    overview += "\n"

    # Tasks
    if pending_tasks:
        overview += "✅ **Pending Tasks:**\n"
        for task in pending_tasks[:5]:  # Show max 5 tasks
            title = task.get('title', 'Untitled Task')
            list_name = task.get('list_name', 'Unknown List')
            due_date = task.get('due', '')

            if due_date:
                due_formatted = datetime.fromisoformat(due_date.replace('Z', '+00:00')).strftime('%m/%d')
                overview += f"• {title} (📅 {due_formatted}) - *{list_name}*\n"
            else:
                overview += f"• {title} - *{list_name}*\n"
        if len(pending_tasks) > 5:
            overview += f"• ... and {len(pending_tasks) - 5} more tasks\n"
    else:
        overview += "✅ **Pending Tasks:** All caught up! 🎉\n"

    return overview

# Chat UI
st.title("💬 Calendar & Tasks Chat Assistant")
st.markdown("*Talk to me to manage your calendar and tasks!*")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "creds" not in st.session_state:
    st.session_state.creds = None

# Handle OAuth flow
query_params = st.query_params
if "code" in query_params:
    code = query_params["code"]
    st.query_params.clear()
    creds = exchange_code_for_credentials(code)
    if creds:
        st.session_state.creds = creds
        # Add welcome message
        welcome_msg = "🎉 **Welcome to your Calendar & Tasks Chat Assistant!**\n\nI'm connected to your Google account and ready to help! Try asking me:\n\n• 'Show me today's overview'\n• 'Create a task to buy groceries'\n• 'Schedule a meeting tomorrow at 2pm'\n• 'Add task: Call dentist on Friday'"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

if st.session_state.creds:
    creds = st.session_state.creds

    # Chat Interface
    st.markdown("---")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me to create tasks, schedule events, or get an overview..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the request
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                # Handle special commands
                if "overview" in prompt.lower() or "today" in prompt.lower():
                    response = get_quick_overview(creds)
                else:
                    response = process_user_request(prompt, creds)

                st.markdown(response)

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar with quick actions and help
    with st.sidebar:
        st.markdown("### 🚀 Quick Actions")

        if st.button("📊 Today's Overview"):
            overview = get_quick_overview(creds)
            st.session_state.messages.append({"role": "user", "content": "Show me today's overview"})
            st.session_state.messages.append({"role": "assistant", "content": overview})
            st.rerun()

        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("### 💡 Example Commands")
        st.markdown("""
        **Create Tasks:**
        - "Create a task to buy groceries"
        - "Remind me to call John tomorrow"
        - "Add task: Review project proposal by Friday"

        **Schedule Events:**
        - "Schedule a meeting tomorrow at 2pm"
        - "Create event: Team standup Monday 9am"
        - "Book appointment with dentist next week"

        **Get Information:**
        - "Show me today's overview"
        - "What's on my calendar today?"
        """)

        st.markdown("---")
        st.markdown("### ⚙️ Settings")

        # Task list selection for new tasks
        task_lists = get_task_lists(creds)
        if task_lists:
            st.markdown("**Default Task List:**")
            task_list_names = [tl.get('title', 'Unnamed List') for tl in task_lists]
            selected_list_index = st.selectbox(
                "Select default list for new tasks:",
                range(len(task_list_names)),
                format_func=lambda x: task_list_names[x],
                key="default_task_list_selector"
            )
            # Display selected list info
            selected_list = task_lists[selected_list_index]
            st.caption(f"New tasks will be added to: **{selected_list['title']}**")
else:
    # Authentication required
    st.markdown("### 🔐 Authentication Required")
    st.markdown("Please authenticate with your Google account to start using the chat assistant.")
    auth_url = get_auth_url()
    st.markdown(f"[🔗 Click here to login with Google]({auth_url})")

    st.markdown("---")
    st.markdown("### 🎯 What You Can Do")
    st.markdown("""
    Once authenticated, you can chat with me to:

    **📋 Manage Tasks:**
    - "Create a task to buy groceries"
    - "Remind me to call the dentist tomorrow"
    - "Add task: Finish project report by Friday"

    **📅 Schedule Events:**
    - "Schedule a meeting tomorrow at 2pm"
    - "Create event: Team standup Monday at 9am"
    - "Book lunch with Sarah next Tuesday"

    **📊 Get Overviews:**
    - "Show me today's schedule"
    - "What's on my calendar?"
    - "Give me an overview"

    Just type naturally - I'll understand what you want to do! 🤖
    """)
