# NVIDIA SMI Monitoring Plugin for CheckMK

## Overview
This plugin provides comprehensive monitoring for NVIDIA GPUs using the `nvidia-smi` command, integrated with CheckMK monitoring system.

## Features
- Fan Speed Monitoring
- GPU Utilization Tracking
- Memory Usage Monitoring
- Process Count Tracking
- Power Consumption Monitoring
- Temperature Tracking

## Components
- `agent/nvidia-smi`: Agent-side script to collect GPU metrics
- `server/nvidia-smi`: CheckMK server-side plugin for parsing and monitoring GPU data

## Requirements
- NVIDIA GPU
- CheckMK Monitoring System
- Python 3.x
- `nvidia-smi` command-line tool

### Installation

- Login Check_MK Server
- Download the latest release plugin
- Run `mkp install nvidia-smi-3.0.mkp`
- Run `mkp list nvidia_smi`
- Copy the `agents/plugins/nvidia_smi` to `~/local/lib/check_mk/base/plugins/agent_based/nvidia_smi`
- Run hosts full scan

## Metrics Collected
- GPU ID
- GPU Name
- Fan Speed
- GPU Utilization
- Memory Utilization
- ECC Errors
- Temperature
- Power Draw
- Power Limit
- Current Memory Usage
- Maximum Memory
- Number of Processes

## License
MIT License - See LICENSE file for details
