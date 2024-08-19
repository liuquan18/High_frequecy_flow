#!/bin/bash

# Check memory usage of node l20021
node_info=$(scontrol show node l20021)
real_memory=$(echo "$node_info" | grep -oP 'RealMemory=\K\d+')
alloc_memory=$(echo "$node_info" | grep -oP 'AllocMem=\K\d+')
free_memory=$(echo "$node_info" | grep -oP 'FreeMem=\K\d+')

# Convert MB to GB
real_memory_gb=$(echo "scale=2; $real_memory / 1024" | bc)
alloc_memory_gb=$(echo "scale=2; $alloc_memory / 1024" | bc)
free_memory_gb=$(echo "scale=2; $free_memory / 1024" | bc)

echo "Node: l20021"
echo "Real Memory: ${real_memory_gb}GB"
echo "Allocated Memory: ${alloc_memory_gb}GB"
echo "Free Memory: ${free_memory_gb}GB"