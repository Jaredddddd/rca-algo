'''
root cause localization
'''
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from ..unified_representation.representation import SLD, ILD, aggregate_failure_representations, aggregate_instance_representations
from .evaluation import eval_RCL

def RCL(model, test_samples, cases, node_dict, split_ratio=0.3, method='num', t_value=3, before=60, after=300, verbose=False):
    spilit_index = int(len(cases)*split_ratio)
    instance_representations = aggregate_instance_representations(cases[spilit_index:], ILD(model, test_samples), before, after)
    failure_representations, type_labels = aggregate_failure_representations(cases[spilit_index:], SLD(model, test_samples, method, t_value), None, before, after)
    rank_df = cases[spilit_index:].reset_index(drop=True).copy(deep=True)
    for case_id in range(len(rank_df)):
        sld = failure_representations[case_id]
        ilds = instance_representations[case_id]
        similarity_scores = []
        for (node_id, node_vector) in ilds:
            similarity = float(cosine_similarity([node_vector], [sld]))
            similarity_scores.append((node_id, similarity))
        sorted_indices = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        grouped_data = defaultdict(list)
        for key, value in sorted_indices:
            grouped_data[key].append(value)
        grouped_data = {key: sum(values) / len(values) for key, values in grouped_data.items()}
        ranks = sorted(grouped_data.items(), key=lambda x: x[1], reverse=True)
        # ranks = [f'{node_dict[i]}:{value}' for (i, value) in ranks]
        import numpy as np
        ranks = [f'{node_dict[i]}:{0 if np.isnan(value) else value}' for (i, value) in ranks]
        for i in range(len(ranks)):
            rank_df.loc[case_id, f'Top{i+1}'] = f'{str(ranks[i])}'
    for i in range(1, 6):  # 假设k=5
        col = f'Top{i}'
        if col in rank_df.columns:
            rank_df[col] = rank_df[col].astype(str)
    topK, avgK = eval_RCL(rank_df, k=5, verbose=verbose)
    return rank_df, topK, avgK
