#!/bin/sh

set -eu

mc alias set local http://minio:9000 minioadmin minioadmin

mc mb --ignore-existing local/retail-source
mc mb --ignore-existing local/retail-destination
mc mb --ignore-existing local/retail-checkpoints

mc cp --recursive /sample_data/orders local/retail-source/
mc cp --recursive /sample_data/inventory local/retail-source/
mc cp --recursive /sample_data/returns local/retail-source/

echo "MinIO setup complete."
echo "Source bucket: retail-source"
echo "Destination bucket: retail-destination"
echo "Checkpoint bucket: retail-checkpoints"
