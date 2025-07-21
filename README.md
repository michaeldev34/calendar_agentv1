# 📅✅ Calendar Agent v1

A comprehensive Streamlit web application that integrates both Google Calendar events and Google Tasks management in a unified interface.

> **Personal productivity assistant** - Manage your calendar events and tasks in one place!

## 🌟 Features

### 📅 Calendar Events
- **View Events**: Display calendar events within customizable date ranges
- **Create Events**: Add new calendar events with start/end times
- **Date Filtering**: Filter events by specific date ranges
- **Event Details**: View event titles, times, and dates

### ✅ Task Management
- **Multiple Task Lists**: Support for multiple Google Tasks lists
- **Task Operations**: Create, view, complete, and delete tasks
- **Task Details**: Add notes and due dates to tasks
- **Smart Filtering**: Show/hide completed tasks, sort by due date
- **Status Indicators**: Visual indicators for overdue and due-today tasks
- **Task List Management**: Create new task lists directly from the app

### 🏠 Unified Dashboard
- **Today's Overview**: Quick view of today's events and pending tasks
- **Quick Stats**: Metrics showing today's events, pending tasks, and weekly events
- **Cross-Platform View**: See both calendar events and tasks in one place

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Google Cloud Project with Calendar and Tasks APIs enabled
- OAuth 2.0 credentials from Google Cloud Console

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/calendar_agentv1.git
   cd calendar_agentv1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Calendar API and Google Tasks API
   - Create OAuth 2.0 credentials (Web application)
   - Configure authorized redirect URIs

4. **Configure Streamlit secrets**
   Copy the template and add your credentials:
   ```bash
   cp .streamlit/secrets.toml.template .streamlit/secrets.toml
   ```
   Then edit `.streamlit/secrets.toml` with your actual Google API credentials.

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📱 Usage

### First Time Setup
1. Click "Click here to login with Google" to authenticate
2. Grant permissions for Calendar and Tasks access
3. You'll be redirected back to the application

### Dashboard Tab
- View today's events and pending tasks at a glance
- See quick statistics about your schedule and tasks
- Get an overview of the week ahead

### Calendar Events Tab
- Set date range to view events
- Create new events with title, start time, and end time
- View all events in the selected date range

### Tasks Tab
- Select from your existing task lists or create new ones
- View tasks with filtering options (completed/pending, sort by due date)
- Create new tasks with optional notes and due dates
- Mark tasks as complete/incomplete with checkboxes
- Delete tasks with the delete button
- Visual indicators for overdue (🔴) and due today (🟡) tasks

## 🔧 Technical Details

### APIs Used
- **Google Calendar API v3**: For calendar events management
- **Google Tasks API v1**: For task and task list management

### OAuth Scopes
- `https://www.googleapis.com/auth/calendar`: Calendar access
- `https://www.googleapis.com/auth/tasks`: Tasks access

### Key Dependencies
- `streamlit`: Web application framework
- `google-auth`: Google authentication
- `google-auth-oauthlib`: OAuth 2.0 flow
- `google-api-python-client`: Google APIs client library

## 🎨 Features Highlights

### Smart Task Management
- **Overdue Detection**: Tasks past due date are highlighted in red
- **Due Today**: Tasks due today are highlighted in yellow
- **Completion Toggle**: Easy checkbox interface to mark tasks complete
- **Filtering**: Show/hide completed tasks, sort by due date

### Enhanced User Experience
- **Tabbed Interface**: Clean separation between Dashboard, Events, and Tasks
- **Responsive Design**: Works well on different screen sizes
- **Real-time Updates**: Interface updates immediately after actions
- **Error Handling**: Graceful error messages for API issues

### Data Integration
- **Unified View**: See both calendar commitments and task deadlines
- **Cross-Reference**: Understand your full schedule at a glance
- **Multiple Lists**: Support for organizing tasks in different lists

## 🔒 Security & Privacy

- Uses OAuth 2.0 for secure authentication
- No storage of user credentials in the application
- Direct communication with Google APIs
- Credentials are handled securely by Google's authentication system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:
1. Check the Google Cloud Console for API quotas and permissions
2. Verify your OAuth credentials are correctly configured
3. Ensure both Calendar and Tasks APIs are enabled
4. Check the Streamlit logs for detailed error messages

## 🔄 Updates & Changelog

### v2.0.0 - Google Tasks Integration
- ✅ Added Google Tasks API integration
- ✅ Implemented task list management
- ✅ Added unified dashboard view
- ✅ Enhanced UI with tabbed interface
- ✅ Added task filtering and sorting
- ✅ Implemented overdue task detection
- ✅ Added task creation with due dates and notes

### v1.0.0 - Initial Release
- 📅 Google Calendar events viewing
- 📅 Calendar event creation
- 📅 Basic date filtering
