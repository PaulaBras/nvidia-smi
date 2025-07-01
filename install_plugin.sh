#!/bin/bash

# CheckMK Plugin Installation Script
# This script installs the nvidia-smi plugin files to the correct CheckMK locations

SITE_ROOT="/omd/sites/test"
LOCAL_ROOT="$SITE_ROOT/local"

echo "Installing nvidia-smi plugin files..."

# Create necessary directories
mkdir -p "$LOCAL_ROOT/lib/check_mk/base/plugins/agent_based"
mkdir -p "$LOCAL_ROOT/share/check_mk/agents/plugins"
mkdir -p "$LOCAL_ROOT/share/check_mk/checkman"
mkdir -p "$LOCAL_ROOT/share/check_mk/web/plugins/metrics"

# Copy files to correct locations
echo "Copying agent_based plugin..."
cp agent_based/nvidia_smi.py "$LOCAL_ROOT/lib/check_mk/base/plugins/agent_based/"

echo "Copying agent plugin..."
cp agent/nvidia-smi "$LOCAL_ROOT/share/check_mk/agents/plugins/"
chmod +x "$LOCAL_ROOT/share/check_mk/agents/plugins/nvidia-smi"

echo "Copying checkman documentation..."
cp checkman/nvidia-smi "$LOCAL_ROOT/share/check_mk/checkman/"

echo "Copying web metrics..."
cp web/plugins/metrics/nvidia-smi.py "$LOCAL_ROOT/share/check_mk/web/plugins/metrics/"

echo "Installation complete!"
echo ""
echo "Now you can create the MKP package with:"
echo "mkp package nvidia_smi.manifest"