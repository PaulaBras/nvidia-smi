from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    register,
    render,
    Result,
    Metric,
    State,
    Service,
)

def parse_nvidia_smi(string_table):
    parsed = {}
    for line in string_table:
        if len(line) >= 13:  # Ensure we have all expected fields
            gpu_id = line[0]
            parsed[gpu_id] = {
                'name': line[1],
                'fan_speed': line[2],
                'gpu_util': line[3],
                'mem_util': line[4],
                'ecc_single_bit': line[5],
                'ecc_double_bit': line[6],
                'temperature': line[7],
                'power_draw': line[8],
                'power_limit': line[9],
                'current_memory_usage': line[10],
                'max_memory': line[11],
                'num_processes': line[12]
            }
    return parsed

register.agent_section(
    name="nvidia_smi",
    parse_function=parse_nvidia_smi,
)

def discover_nvidia_smi_fan(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['fan_speed'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_fan(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        fan_speed = int(data['fan_speed'])
        yield Metric('fan', fan_speed, levels=(90, 95))

        if fan_speed > 95:
            yield Result(state=State.CRIT, summary=f"{data['name']} fan speed is {fan_speed}%")
        elif fan_speed > 90:
            yield Result(state=State.WARN, summary=f"{data['name']} fan speed is {fan_speed}%")
        else:
            yield Result(state=State.OK, summary=f"{data['name']} fan speed is {fan_speed}%")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse fan speed")

def discover_nvidia_smi_gpuutil(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['gpu_util'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_gpuutil(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        gpu_util = int(data['gpu_util'])
        yield Metric('gpuutil', gpu_util, levels=(90, 100))
        yield Result(state=State.OK, summary=f"{data['name']} utilization is {gpu_util}%")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse GPU utilization")

def discover_nvidia_smi_memory(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['current_memory_usage'] != 'N/A' and data['max_memory'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_memory(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        current_memory = int(data['current_memory_usage'])
        max_memory = int(data['max_memory'])
        memory_percent = current_memory / max_memory * 100

        yield Metric('memory_usage', current_memory, levels=(max_memory * 0.8, max_memory * 0.9))

        if memory_percent > 90:
            yield Result(state=State.CRIT, summary=f"{data['name']} memory usage is {current_memory}MiB out of {max_memory}MiB ({memory_percent:.1f}%)")
        elif memory_percent > 80:
            yield Result(state=State.WARN, summary=f"{data['name']} memory usage is {current_memory}MiB out of {max_memory}MiB ({memory_percent:.1f}%)")
        else:
            yield Result(state=State.OK, summary=f"{data['name']} memory usage is {current_memory}MiB out of {max_memory}MiB ({memory_percent:.1f}%)")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse memory usage")

def discover_nvidia_smi_processes(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['num_processes'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_processes(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        num_processes = int(data['num_processes'])
        yield Metric('num_processes', num_processes, levels=(10, 20))

        if num_processes > 20:
            yield Result(state=State.CRIT, summary=f"{data['name']} has {num_processes} running processes")
        elif num_processes > 10:
            yield Result(state=State.WARN, summary=f"{data['name']} has {num_processes} running processes")
        else:
            yield Result(state=State.OK, summary=f"{data['name']} has {num_processes} running processes")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse number of processes")

def discover_nvidia_smi_power(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['power_draw'] != 'N/A' and data['power_limit'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_power(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        power_draw = float(data['power_draw'])
        power_limit = float(data['power_limit'])
        
        if power_limit == 0:
            yield Result(state=State.OK, summary=f"{data['name']} power usage is {power_draw:.1f}W (no power limit set)")
            yield Metric('power_draw', power_draw)
            return

        power_percent = power_draw / power_limit * 100
        yield Metric('power_draw', power_draw, levels=(power_limit * 0.8, power_limit * 0.9))

        if power_percent > 90:
            yield Result(state=State.CRIT, summary=f"{data['name']} power usage is {power_draw:.1f}W out of {power_limit:.1f}W ({power_percent:.1f}%)")
        elif power_percent > 80:
            yield Result(state=State.WARN, summary=f"{data['name']} power usage is {power_draw:.1f}W out of {power_limit:.1f}W ({power_percent:.1f}%)")
        else:
            yield Result(state=State.OK, summary=f"{data['name']} power usage is {power_draw:.1f}W out of {power_limit:.1f}W ({power_percent:.1f}%)")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse power usage")

def discover_nvidia_smi_temperature(section) -> DiscoveryResult:
    for gpu_id, data in section.items():
        if data['temperature'] != 'N/A':
            yield Service(item=f'GPU{gpu_id}')

def check_nvidia_smi_temperature(item: str, section) -> CheckResult:
    gpu_id = item.replace('GPU', '')
    if gpu_id not in section:
        return

    data = section[gpu_id]
    try:
        temperature = int(data['temperature'])
        yield Metric('temperature', temperature, levels=(80, 90))

        if temperature > 90:
            yield Result(state=State.CRIT, summary=f"{data['name']} temperature is {temperature}°C")
        elif temperature > 80:
            yield Result(state=State.WARN, summary=f"{data['name']} temperature is {temperature}°C")
        else:
            yield Result(state=State.OK, summary=f"{data['name']} temperature is {temperature}°C")
    except ValueError:
        yield Result(state=State.UNKNOWN, summary="Unable to parse temperature")

register.check_plugin(
    name="nvidia_smi_fan",
    service_name="GPU %s Fan Speed",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_fan,
    check_function=check_nvidia_smi_fan,
)

register.check_plugin(
    name="nvidia_smi_gpuutil",
    service_name="GPU %s Utilization",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_gpuutil,
    check_function=check_nvidia_smi_gpuutil,
)

register.check_plugin(
    name="nvidia_smi_memory",
    service_name="GPU %s Memory Usage",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_memory,
    check_function=check_nvidia_smi_memory,
)

register.check_plugin(
    name="nvidia_smi_processes",
    service_name="GPU %s Processes",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_processes,
    check_function=check_nvidia_smi_processes,
)

register.check_plugin(
    name="nvidia_smi_power",
    service_name="GPU %s Power Usage",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_power,
    check_function=check_nvidia_smi_power,
)

register.check_plugin(
    name="nvidia_smi_temperature",
    service_name="GPU %s Temperature",
    sections=["nvidia_smi"],
    discovery_function=discover_nvidia_smi_temperature,
    check_function=check_nvidia_smi_temperature,
)