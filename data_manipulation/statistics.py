import pandas as pd

def compute_stats_work_days(data):
    stats = data.agg({"hours": ["mean", "median", "std"]})
    stats = pd.Series.to_dict(stats['hours'])
    data = pd.DataFrame.to_dict(data)
    return stats, data


def cmpute_stats_org_hours(data):
    stats = pd.DataFrame(data).agg({"org_hours": ["mean", "median", "std"]})
    stats = pd.Series.to_dict(stats['org_hours'])
    return stats
