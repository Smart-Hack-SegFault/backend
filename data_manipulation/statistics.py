import pandas as pd
import matplotlib.pyplot as plt
import json


def compute_stats_work_days(data):
    stats = data.agg({"hours": ["mean", "median", "std"]})
    stats = pd.Series.to_dict(stats['hours'])
    data = pd.DataFrame.to_dict(data)
    return stats, data


def cmpute_stats_org_hours(data):
    stats = data.agg({"org_hours": ["mean", "median", "std"]})
    stats = pd.Series.to_dict(stats['hours'])
    return stats
