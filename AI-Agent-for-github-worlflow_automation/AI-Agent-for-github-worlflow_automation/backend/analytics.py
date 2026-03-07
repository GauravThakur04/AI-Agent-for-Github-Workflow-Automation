# analytics.py

def get_bug_stats():
    """
    Returns basic bug statistics for a repository
    """

    bug_data = {
        "critical": 2,
        "major": 4,
        "minor": 6
    }

    total_bugs = bug_data["critical"] + bug_data["major"] + bug_data["minor"]

    return {
        "bug_statistics": bug_data,
        "total_bugs": total_bugs,
        "status": "analysis completed"
    }


def get_workflow_stats():
    """
    Returns workflow execution statistics
    """

    workflow_data = {
        "successful_runs": 15,
        "failed_runs": 3,
        "pending_runs": 1
    }

    total_runs = sum(workflow_data.values())

    return {
        "workflow_stats": workflow_data,
        "total_runs": total_runs
    }