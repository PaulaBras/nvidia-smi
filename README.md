# NVIDIA SMI Monitoring Plugin for CheckMK

## Overview

This plugin provides comprehensive monitoring for NVIDIA GPUs using the `nvidia-smi` command, integrated with CheckMK monitoring system. The plugin creates multiple services per GPU to monitor various performance metrics and health indicators.

## Features

- **Fan Speed Monitoring** - Track GPU fan speeds with configurable thresholds
- **GPU Utilization Tracking** - Monitor GPU compute utilization percentage
- **Memory Usage Monitoring** - Track GPU memory consumption and availability
- **Process Count Tracking** - Monitor number of processes using each GPU
- **Power Consumption Monitoring** - Track power draw vs power limits
- **Temperature Tracking** - Monitor GPU temperatures with alerts
- **ECC Error Monitoring** - Track single-bit and double-bit ECC errors

## Plugin Structure

```
nvidia-smi-plugin/
├── nvidia_smi.manifest          # MKP package manifest
├── agent_based/
│   └── nvidia_smi.py           # Server-side plugin (check logic)
├── agent/
│   └── nvidia-smi              # Agent script (data collection)
├── checkman/
│   └── nvidia-smi              # Plugin documentation
├── web/
│   └── plugins/
│       └── metrics/
│           └── nvidia-smi.py   # Metrics and graph definitions
└── install_plugin.sh           # Installation helper script
```

## Requirements

- NVIDIA GPU with driver support
- CheckMK 2.4.0p5 or later
- Python 3.x on monitored hosts
- `nvidia-smi` command-line tool installed and accessible

## Installation

### Method 1: Using Installation Script (Recommended)

1. Clone or download this repository to your CheckMK site
2. Navigate to the plugin directory
3. Run the installation script:
   ```bash
   chmod +x install_plugin.sh
   ./install_plugin.sh
   ```
4. Create the MKP package:
   ```bash
   mkp package nvidia_smi.manifest
   ```
5. Install the generated MKP file:
   ```bash
   mkp install nvidia_smi-1.0.4.mkp
   ```

### Method 2: Manual Installation

1. Copy files to CheckMK directories:

   ```bash
   # Agent-based plugin
   cp agent_based/nvidia_smi.py /omd/sites/SITENAME/local/lib/check_mk/base/plugins/agent_based/

   # Agent plugin
   cp agent/nvidia-smi /omd/sites/SITENAME/local/share/check_mk/agents/plugins/
   chmod +x /omd/sites/SITENAME/local/share/check_mk/agents/plugins/nvidia-smi

   # Documentation
   cp checkman/nvidia-smi /omd/sites/SITENAME/local/share/check_mk/checkman/

   # Web metrics
   cp web/plugins/metrics/nvidia-smi.py /omd/sites/SITENAME/local/share/check_mk/web/plugins/metrics/
   ```

2. Restart CheckMK:
   ```bash
   omd restart
   ```

## Agent Deployment

After installation, the plugin will be available in the CheckMK Agent Bakery:

1. Go to **Setup → Agents → Windows, Linux, Solaris, AIX**
2. Create or edit an agent configuration
3. The nvidia-smi plugin should appear in available plugins
4. Enable it for hosts with NVIDIA GPUs
5. Bake and deploy agents

## Services Created

The plugin creates the following services per GPU:

- **GPU X Fan Speed** - Fan speed percentage with WARN/CRIT thresholds
- **GPU X Utilization** - GPU compute utilization percentage
- **GPU X Memory Usage** - Memory usage with percentage and absolute values
- **GPU X Temperature** - GPU temperature in Celsius
- **GPU X Power Usage** - Power consumption vs limits
- **GPU X Processes** - Number of active processes on the GPU

## Metrics Collected

- **GPU ID** - Unique identifier for each GPU
- **GPU Name** - Product name (e.g., "GeForce RTX 4090")
- **Fan Speed** - Fan speed percentage (0-100%)
- **GPU Utilization** - Compute utilization percentage (0-100%)
- **Memory Utilization** - Memory usage percentage (0-100%)
- **ECC Errors** - Single-bit and double-bit error counts
- **Temperature** - GPU temperature in Celsius
- **Power Draw** - Current power consumption in Watts
- **Power Limit** - Maximum power limit in Watts
- **Current Memory Usage** - Used memory in MiB
- **Maximum Memory** - Total available memory in MiB
- **Number of Processes** - Count of active GPU processes

## Thresholds and Alerting

Default warning/critical thresholds:

- **Fan Speed**: 90% / 95%
- **GPU Utilization**: 90% / 100%
- **Memory Usage**: 80% / 90%
- **Temperature**: 80°C / 90°C
- **Power Usage**: 80% / 90% of limit
- **Process Count**: 10 / 20 processes

## Troubleshooting

### Plugin Not Appearing in Agent Bakery

- Ensure all files are in correct CheckMK directories
- Restart CheckMK service: `omd restart`
- Check for errors in `~/var/log/web.log`

### No Data from Agents

- Verify `nvidia-smi` command works on target hosts
- Check agent plugin permissions: `chmod +x nvidia-smi`
- Test agent plugin manually: `/usr/lib/check_mk_agent/plugins/nvidia-smi`

### Services Not Discovered

- Run service discovery on affected hosts
- Check for parsing errors in CheckMK logs
- Verify agent output format matches expected structure

## Development

To modify the plugin:

1. Edit source files in respective directories
2. Run `install_plugin.sh` to update CheckMK installation
3. Test changes with `cmk -D HOSTNAME` for discovery
4. Package with `mkp package nvidia_smi.manifest`

## Version History

- **1.0.4** - Fixed agent bakery deployment, proper directory structure
- **1.0.3** - Initial release with basic GPU monitoring

## License

MIT License - See LICENSE file for details

## Author

Paul à Brassard - https://git.pabr.de/paul/nvidia-smi-plugin
