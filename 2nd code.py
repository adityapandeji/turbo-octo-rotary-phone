import math
from scipy.special import factorial

def erlang_b(A, N):
    """Calculate blocking probability using Erlang B formula"""
    numerator = (A ** N) / factorial(N)
    denominator = sum([(A ** k) / factorial(k) for k in range(N + 1)])
    return numerator / denominator

def calculate_ci_ratio(reuse_factor, zone_radius):
    """Calculate accurate C/I ratio in dB for given reuse factor and zone radius"""
    n = 4  # path loss exponent (urban)
    D = zone_radius * math.sqrt(3 * reuse_factor)  # reuse distance
    R = zone_radius  # cell radius
    ci_linear = (D/R)**n / 6
    return 10 * math.log10(ci_linear)

# Hardcoded network parameters
zones = {
    'Zone1': {
        'subscribers': 10000,
        'radius': 25,
        'cells': 4,
        'static_channels': 6,
        'dynamic_channels': 3,
        'reuse_factor': 4,
        'traffic': 50
    },
    'Zone2': {
        'subscribers': 15000,
        'radius': 30,
        'cells': 6,
        'static_channels': 8,
        'dynamic_channels': 6,
        'reuse_factor': 3,
        'traffic': 75
    },
    'Zone3': {
        'subscribers': 5000,
        'radius': 15,
        'cells': 2,
        'static_channels': 4,
        'dynamic_channels': 0,
        'reuse_factor': 7,
        'traffic': 25,
        'half_rate': True
    }
}

# Calculate metrics
for zone, data in zones.items():
    if zone == 'Zone3' and data.get('half_rate', False):
        data['effective_channels'] = (data['static_channels'] + data['dynamic_channels']) * 2
    else:
        data['effective_channels'] = data['static_channels'] + data['dynamic_channels']
        
    data['blocking_prob'] = erlang_b(data['traffic'], data['effective_channels']) * 100
    data['ci_ratio'] = calculate_ci_ratio(data['reuse_factor'], data['radius'])

# Print formatted table with perfect alignment
header = ("{:<6} | {:<10} | {:<6} | {:<5} | {:<9} | {:<10} | {:<7} | {:<7} | {:<9} | {:<6} | {:<12}"
          .format("Zone", "Subscribers", "Radius", "Cells", "Static Ch", "Dynamic Ch", "Total Ch", 
                  "Traffic", "Blocking %", "C/I", "Reuse Factor"))
divider = "-" * len(header)

print(header)
print(divider)
for zone, data in zones.items():
    print("{:<6} | {:>10,} | {:>6}km | {:>5} | {:>9} | {:>10} | {:>7} | {:>7} | {:>8.2f}% | {:>5.1f}dB | K={:<3}"
          .format(zone, 
                  data['subscribers'],
                  data['radius'],
                  data['cells'],
                  data['static_channels'],
                  data['dynamic_channels'],
                  data['effective_channels'],
                  data['traffic'],
                  data['blocking_prob'],
                  data['ci_ratio'],
                  data['reuse_factor']))