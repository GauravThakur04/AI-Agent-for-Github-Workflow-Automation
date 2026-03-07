# Trend Report Feature Testing Guide

## Overview
The Trend Report Feature provides intelligent analytics and insights about bug patterns, trends, and project health over time.

## Testing Methods

### 1. **Direct API Testing (cURL/Postman)**

#### Test 1: Basic Trend Analysis
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me bug trends for the last month",
    "user_id": "test_user",
    "session_id": "test_session",
    "github_repo": "owner/repo"
  }'
```

#### Test 2: Time-based Analysis
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How many bugs were created in the last 2 weeks?",
    "user_id": "test_user",
    "session_id": "test_session",
    "github_repo": "owner/repo"
  }'
```

#### Test 3: Assignment Analysis
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Who is assigned to the most bugs?",
    "user_id": "test_user",
    "session_id": "test_session",
    "github_repo": "owner/repo"
  }'
```

#### Test 4: Trend Insights
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the bug trends and insights for this month?",
    "user_id": "test_user",
    "session_id": "test_session",
    "github_repo": "owner/repo"
  }'
```

### 2. **Direct Bug Analytics API Endpoints**

#### Get Bug Analytics
```bash
curl -X GET "http://localhost:8000/api/bugs/analytics?time_period=month&analysis_type=trends" \
  -H "Content-Type: application/json"
```

#### Get Assignment Analysis
```bash
curl -X GET "http://localhost:8000/api/bugs/assignment-analysis?time_period=month" \
  -H "Content-Type: application/json"
```

### 3. **Frontend Chat Testing**

Start the frontend and test these natural language queries:

#### Sample Chat Messages to Test:

1. **"Show me bug trends for the last month"**
   - Expected: Time series data, trend metrics, insights

2. **"How many bugs are open in the last two weeks?"**
   - Expected: Count, trend analysis, period comparison

3. **"What are the bug creation patterns this month?"**
   - Expected: Daily/weekly patterns, growth rate, anomalies

4. **"Who is handling the most bugs?"**
   - Expected: Assignment distribution, workload analysis

5. **"Give me a trend report for this quarter"**
   - Expected: Comprehensive quarterly analysis with recommendations

6. **"What are the bug resolution trends?"**
   - Expected: Resolution time analysis, velocity metrics

7. **"Show me bug trends and insights"**
   - Expected: Full trend report with actionable insights

## Expected Response Structure

### Trend Report Response Example:
```json
{
  "response": "Here's your trend report for the last month:",
  "intent": {
    "action": "BUG_ANALYSIS",
    "parameters": {
      "time_period": "month",
      "analysis_type": "trends"
    }
  },
  "action_result": {
    "trend_report": {
      "time_series": {
        "daily_data": [...],
        "weekly_data": [...],
        "monthly_data": [...]
      },
      "trend_metrics": {
        "growth_rate": 15.2,
        "trend_direction": "increasing",
        "velocity": 2.3
      },
      "insights": [
        "Bug creation rate increased by 15% this month",
        "Most bugs are created on Mondays",
        "Critical bugs take 3x longer to resolve"
      ],
      "performance_indicators": {
        "avg_resolution_time": 5.2,
        "bug_density": 0.8,
        "priority_distribution": {...}
      },
      "recommendations": [
        "Focus on reducing Monday bug creation",
        "Improve critical bug resolution process",
        "Consider additional testing for high-density modules"
      ]
    }
  }
}
```

## Testing Scenarios

### Scenario 1: No Data Available
- Query: "Show me bug trends"
- Expected: Graceful handling with "No bug data available" message

### Scenario 2: Short Time Period
- Query: "Bug trends for last week"
- Expected: Weekly analysis with daily breakdown

### Scenario 3: Long Time Period
- Query: "Bug trends for last year"
- Expected: Monthly/quarterly aggregation

### Scenario 4: Specific Analysis
- Query: "Who is assigned to most bugs?"
- Expected: Assignment distribution and workload analysis

### Scenario 5: Trend Insights
- Query: "What are the bug insights?"
- Expected: Pattern recognition and actionable recommendations

## Key Features to Verify

1. **Time Series Generation**: Daily, weekly, monthly data aggregation
2. **Trend Calculation**: Growth rates, direction analysis
3. **Insight Generation**: Pattern recognition and anomaly detection
4. **Performance Metrics**: Resolution time, density calculations
5. **Recommendations**: Actionable suggestions based on data
6. **Natural Language Processing**: Understanding various query formats
7. **Error Handling**: Graceful handling of missing or invalid data

## Testing Checklist

- [ ] Basic trend analysis works
- [ ] Time period extraction works correctly
- [ ] Assignment analysis provides meaningful insights
- [ ] Trend metrics are calculated accurately
- [ ] Insights are relevant and actionable
- [ ] Recommendations are practical
- [ ] Error handling works for edge cases
- [ ] Natural language queries are understood
- [ ] Response format is consistent
- [ ] Performance is acceptable with large datasets

## Sample Data for Testing

To test with realistic data, you can create sample bugs using:

```bash
curl -X POST "http://localhost:8000/api/bugs" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Bug 1",
    "description": "This is a test bug for trend analysis",
    "bug_type": "runtime_error",
    "priority": 3,
    "github_repo": "owner/repo",
    "user_id": "test_user"
  }'
```

Create multiple bugs with different dates, priorities, and assignees to test the full range of analytics features. 