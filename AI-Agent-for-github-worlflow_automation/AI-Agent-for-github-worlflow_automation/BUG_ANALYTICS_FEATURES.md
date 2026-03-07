# Bug Analytics and Assignment Analysis Features

## Overview

The GitHub AI Agent now includes advanced analytics features that provide insights into bug tracking and team assignments. These features can be accessed through natural language queries in the chat interface or directly via API endpoints.

## Features

### 1. Bug Analytics

#### Natural Language Queries
Users can ask questions like:
- "How many bugs are open in the last week?"
- "Show me bug statistics for the last month"
- "What are the bug trends in the last two weeks?"
- "Give me a summary of bugs from the last 3 months"

#### Supported Time Periods
- `last_week` - Last 7 days
- `last_2_weeks` - Last 14 days  
- `last_month` - Last 30 days
- `last_3_months` - Last 90 days
- `last_year` - Last 365 days
- `all_time` - All bugs (default)

#### Analytics Data Provided
- **Summary Statistics**:
  - Total bugs in period
  - Open bugs count
  - Closed bugs count
  - Resolution rate percentage
  - Average resolution time in days

- **Distribution Analysis**:
  - Priority distribution (1-4 scale)
  - Bug type distribution
  - Status distribution

- **Trends**:
  - Daily bug creation trend (last 7 days)
  - Time period analysis

### 2. Assignment Analytics

#### Natural Language Queries
Users can ask questions like:
- "Show me the assignment details of bugs"
- "Who is assigned to the most bugs?"
- "What's the team workload distribution?"
- "Show assignment analysis by priority"

#### Analytics Data Provided
- **Summary Statistics**:
  - Total bugs
  - Assigned bugs count
  - Unassigned bugs count
  - Unique assignees
  - Average bugs per assignee
  - Assignment rate percentage

- **Assignment Distribution**:
  - Bugs per assignee
  - Top assignees (top 5)
  - Assignment by priority level
  - Assignment by bug type

## API Endpoints

### Bug Analytics
```
GET /bugs/analytics?session_id={session_id}&time_period={period}&analysis_type={type}
```

**Parameters**:
- `session_id` (required): User session ID
- `time_period` (optional): Time period for analysis
- `analysis_type` (optional): Type of analysis

**Response Example**:
```json
{
  "time_period": "last_week",
  "analysis_type": "open_bugs",
  "date_range": {
    "start": "2024-01-01T00:00:00",
    "end": "2024-01-08T00:00:00"
  },
  "total_bugs": 15,
  "analysis": {
    "summary": {
      "total_bugs": 15,
      "open_bugs": 8,
      "closed_bugs": 7,
      "resolution_rate": 46.67,
      "avg_resolution_time_days": 3.2
    },
    "priority_distribution": {
      "1": 3,
      "2": 8,
      "3": 3,
      "4": 1
    },
    "type_distribution": {
      "ui_ux": 5,
      "backend": 4,
      "frontend": 3,
      "general_issue": 3
    },
    "status_distribution": {
      "open": 8,
      "closed": 5,
      "resolved": 2
    },
    "daily_trend": {
      "2024-01-01": 2,
      "2024-01-02": 1,
      "2024-01-03": 3,
      "2024-01-04": 0,
      "2024-01-05": 2,
      "2024-01-06": 1,
      "2024-01-07": 1
    }
  }
}
```

### Assignment Analytics
```
GET /bugs/assignment-analytics?session_id={session_id}
```

**Parameters**:
- `session_id` (required): User session ID

**Response Example**:
```json
{
  "total_bugs": 25,
  "analysis": {
    "summary": {
      "total_bugs": 25,
      "assigned_bugs": 20,
      "unassigned_bugs": 5,
      "unique_assignees": 4,
      "avg_bugs_per_assignee": 5.0,
      "assignment_rate": 80.0
    },
    "assignment_distribution": {
      "john_doe": 8,
      "jane_smith": 6,
      "bob_wilson": 4,
      "alice_brown": 2
    },
    "top_assignees": [
      ["john_doe", 8],
      ["jane_smith", 6],
      ["bob_wilson", 4],
      ["alice_brown", 2]
    ],
    "assignment_by_priority": {
      "1": {
        "john_doe": 2,
        "jane_smith": 1
      },
      "2": {
        "john_doe": 4,
        "jane_smith": 3,
        "bob_wilson": 2
      }
    },
    "assignment_by_type": {
      "ui_ux": {
        "jane_smith": 4,
        "alice_brown": 1
      },
      "backend": {
        "john_doe": 3,
        "bob_wilson": 2
      }
    },
    "unassigned_count": 5
  }
}
```

## Usage Examples

### 1. Chat Interface
```
User: "How many bugs are open in the last week?"
AI: "Based on the analysis for the last week, you have 8 open bugs out of 15 total bugs. 
     The resolution rate is 46.67% with an average resolution time of 3.2 days. 
     Here's the breakdown by priority: 3 high priority, 8 medium priority, 3 low priority, and 1 critical."

User: "Show me the assignment details of bugs"
AI: "Here's the assignment analysis: You have 25 total bugs with 20 assigned and 5 unassigned. 
     The top assignee is john_doe with 8 bugs, followed by jane_smith with 6 bugs. 
     The assignment rate is 80% with an average of 5 bugs per assignee."
```

### 2. API Usage
```bash
# Get bug analytics for last week
curl "http://localhost:8000/bugs/analytics?session_id=your-session-id&time_period=last_week"

# Get assignment analytics
curl "http://localhost:8000/bugs/assignment-analytics?session_id=your-session-id"

# Get bug analytics with custom parameters
curl "http://localhost:8000/bugs/analytics?session_id=your-session-id&time_period=last_month&analysis_type=priority_distribution"
```

## Implementation Details

### Intent Detection
The system uses advanced LLM-based intent detection to understand user queries:

1. **LLM Analysis**: Uses OpenAI GPT or Hugging Face models to analyze intent
2. **Keyword Fallback**: Falls back to keyword matching if LLM is unavailable
3. **Parameter Extraction**: Automatically extracts time periods and analysis types

### Database Queries
- Uses MongoDB aggregation for efficient data retrieval
- Supports filtering by user, repository, and time periods
- Provides real-time analytics without caching

### Performance
- Optimized queries with proper indexing
- Efficient date range calculations
- Minimal memory usage for large datasets

## Configuration

### Environment Variables
```bash
# Required for LLM intent analysis
OPENAI_API_KEY=your-openai-key
HUGGINGFACE_API_KEY=your-huggingface-key

# MongoDB connection
MONGODB_URI=mongodb://localhost:27017/github_ai_agent
```

### Database Indexes
```javascript
// Recommended indexes for performance
db.bugs.createIndex({"user_id": 1, "created_at": -1})
db.bugs.createIndex({"github_repo": 1, "created_at": -1})
db.bugs.createIndex({"status": 1, "created_at": -1})
db.bugs.createIndex({"assignees": 1})
```

## Error Handling

The system includes comprehensive error handling:

- **Invalid Session**: Returns 401 Unauthorized
- **Missing Repository**: Returns 400 Bad Request
- **Database Errors**: Returns 500 Internal Server Error
- **Invalid Parameters**: Returns 400 Bad Request with details

## Future Enhancements

Planned features for future releases:

1. **Visual Analytics**: Charts and graphs for better data visualization
2. **Export Functionality**: PDF/Excel reports generation
3. **Custom Dashboards**: User-configurable analytics views
4. **Predictive Analytics**: Bug trend predictions and forecasting
5. **Team Performance Metrics**: Individual and team productivity analysis
6. **Integration with External Tools**: Jira, Trello, Asana integration

## Testing

### Manual Testing
1. Create test bugs with different priorities and assignees
2. Test various time periods and analysis types
3. Verify natural language query understanding
4. Test API endpoints with Postman collection

### Automated Testing
```python
# Example test cases
def test_bug_analytics_last_week():
    response = client.get("/bugs/analytics?session_id=test&time_period=last_week")
    assert response.status_code == 200
    data = response.json()
    assert "total_bugs" in data
    assert "analysis" in data

def test_assignment_analytics():
    response = client.get("/bugs/assignment-analytics?session_id=test")
    assert response.status_code == 200
    data = response.json()
    assert "total_bugs" in data
    assert "analysis" in data
```

## Support

For questions or issues with the analytics features:

1. Check the API documentation
2. Review error logs in the backend
3. Test with the provided Postman collection
4. Contact the development team

---

*This documentation covers the comprehensive analytics features added to the GitHub AI Agent. The system provides both natural language querying and direct API access for bug and assignment analytics.* 