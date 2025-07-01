# Colors:
#
#                   red
#  magenta                       orange
#            11 12 13 14 15 16
#         46                   21
#         45                   22
#   blue  44                   23  yellow
#         43                   24
#         42                   25
#         41                   26
#            36 35 34 33 32 31
#     cyan                       yellow-green
#                  green
#
# Special colors:
# 51  gray
# 52  brown 1
# 53  brown 2
#
# For a new metric_info you have to choose a color. No more hex-codes are needed!
# Instead you can choose a number of the above color ring and a letter 'a' or 'b
# where 'a' represents the basic color and 'b' is a nuance/shading of the basic color.
# Both number and letter must be declared!
#
# Example:
# "color" : "23/a" (basic color yellow)
# "color" : "23/b" (nuance of color yellow)
#
# As an alternative you can call indexed_color with a color index and the maximum
# number of colors you will need to generate a color. This function tries to return
# high contrast colors for "close" indices, so the colors of idx 1 and idx 2 may
# have stronger contrast than the colors at idx 3 and idx 10.

metric_info["gpu_utilization"] = {
    "title" : _("GPU Utilization"),
    "unit"  : "%",
    "color" : "31/a",
}

metric_info["memory_utilization"] = {
    "title" : _("Memory Utilization"),
    "unit"  : "%",
    "color" : "21/b",
}

metric_info["temperature"] = {
    "title" : _("Temperature"),
    "unit"  : "°C",
    "color" : "41/b",
}

metric_info["fan_speed"] = {
    "title" : _("Fan Speed"),
    "unit"  : "%",
    "color" : "45/a",
}

metric_info["ecc_errors_single_bit"] = {
    "title" : _("ECC Single Bit Errors"),
    "unit"  : "",
    "color" : "23/a",
}

metric_info["ecc_errors_double_bit"] = {
    "title" : _("ECC Double Bit Errors"),
    "unit"  : "",
    "color" : "23/b",
}

metric_info["power_draw"] = {
    "title" : _("Power Draw"),
    "unit"  : "W",
    "color" : "42/a",
}

metric_info["power_limit"] = {
    "title" : _("Power Limit"),
    "unit"  : "W",
    "color" : "42/b",
}

metric_info["memory_used"] = {
    "title" : _("Memory Used"),
    "unit"  : "MB",
    "color" : "21/a",
}

metric_info["memory_total"] = {
    "title" : _("Total Memory"),
    "unit"  : "MB",
    "color" : "21/b",
}

metric_info["num_processes"] = {
    "title" : _("Number of GPU Processes"),
    "unit"  : "",
    "color" : "36/a",
}

graph_info.append({
    "title"   : _("GPU Utilization"),
    "metrics" : [
        ( "gpu_utilization", "area" ),
        ( "memory_utilization", "line" ),
    ],
})

graph_info.append({
    "title"   : _("Temperature and Fan Speed"),
    "metrics" : [
        ( "temperature", "line" ),
        ( "fan_speed", "line" ),
    ],
})

graph_info.append({
    "title"   : _("ECC Errors"),
    "metrics" : [
        ( "ecc_errors_single_bit", "line" ),
        ( "ecc_errors_double_bit", "line" ),
    ],
})

graph_info.append({
    "title"   : _("Power Metrics"),
    "metrics" : [
        ( "power_draw", "line" ),
        ( "power_limit", "line" ),
    ],
})

graph_info.append({
    "title"   : _("Memory Usage"),
    "metrics" : [
        ( "memory_used", "line" ),
        ( "memory_total", "line" ),
    ],
})

graph_info.append({
    "title"   : _("GPU Processes"),
    "metrics" : [
        ( "num_processes", "line" ),
    ],
})