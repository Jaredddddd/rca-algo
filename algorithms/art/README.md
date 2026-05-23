# RUN

sudo juicefs mount redis://10.10.10.38:6379/1 /mnt/jfs -d --cache-size=1024

uv run client.py preprocess

uv run client.py train

uv run client.py test


