import json
import os
import pickle

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_pkl(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data

def save_pkl(filepath, data):
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)

def load_samples(filedir):
    train_samples = load_pkl(os.path.join(filedir, 'train_samples.pkl'))
    test_samples = load_pkl(os.path.join(filedir, 'test_samples.pkl'))
    # indices = np.random.choice(len(normal_samples), size=int(len(abnormal_samples)*0.9), replace=False)
    # normal_samples = [normal_samples[i] for i in indices]
    return train_samples, test_samples

def hash_init(filedir):
    node_hash = load_pkl(os.path.join(filedir, 'node_hash.pkl'))
    node_dict = list(node_hash)
    type_hash = load_pkl(os.path.join(filedir, 'type_hash.pkl'))
    type_dict = load_pkl(os.path.join(filedir, 'type_dict.pkl'))
    channel_dict = load_pkl(os.path.join(filedir, 'channel_dict.pkl'))
    return node_hash, node_dict, type_hash, type_dict, channel_dict
