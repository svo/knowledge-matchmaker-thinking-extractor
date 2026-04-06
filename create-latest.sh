#!/usr/bin/env bash

image=$1

docker manifest rm "svanosselaer/knowledge-matchmaker-thinking-extractor-${image}:latest" 2>/dev/null || true

docker manifest create \
  "svanosselaer/knowledge-matchmaker-thinking-extractor-${image}:latest" \
  --amend "svanosselaer/knowledge-matchmaker-thinking-extractor-${image}:amd64" \
  --amend "svanosselaer/knowledge-matchmaker-thinking-extractor-${image}:arm64" &&
docker manifest push "svanosselaer/knowledge-matchmaker-thinking-extractor-${image}:latest"
