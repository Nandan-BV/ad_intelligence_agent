import pandas as pd

def generate_market_report(analysis_results: list):
    if not analysis_results:
        return pd.DataFrame()
    df = pd.DataFrame(analysis_results)
    return df

def summarize_metrics(df: pd.DataFrame):
    if df.empty:
        return {}
    avg_score = df['estimated_effectiveness_score'].mean()
    common_hooks = df['hook_type'].value_counts().to_dict()
    return {
        'total_ads_analyzed': len(df),
        'average_effectiveness_score': round(avg_score, 1),
        'dominant_hook_types': common_hooks
    }
