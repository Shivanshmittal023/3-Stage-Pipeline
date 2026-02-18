import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_timing_diagram():
    # Setup figure and axes
    fig, ax = plt.subplots(figsize=(15, 10))

    # improved aesthetics
    ax.set_facecolor('white')
    ax.grid(which='both', axis='x', linestyle='--', color='gray', alpha=0.5)

    # Configuration
    cycles = 11
    y_start = 0
    y_spacing = 1.5

    # Data Definitions (aligned with your ASCII art)
    # None represents "---" or invalid/stable previous state

    data = {
        # Signal Name: (Type ('bit' or 'bus'), [Value for C1, C2, ... C11])
        'CLK':   ('clk', range(cycles)),

        # Instruction Fetch
        'PC':    ('bus', ['0x00', '0x04', '0x08', '0x0C', '0x10', '0x14', '0x18', '0x1C', '0x20', '0x24', '0x28']),
        'INSTR': ('bus', ['???', 'I_00', 'I_04', 'I_08', 'I_0C', 'I_10', 'I_14', 'I_18', 'I_1C', 'I_20', 'I_24']),

        # Control Signals
        'RE':    ('bit', [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0]),
        'WE':    ('bit', [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]),

        # Addresses
        'RADDR': ('bus', ['---', '0x20', '---', '0x20', '0x40', '---', '---', '---', '---', '---', '---']),
        'WADDR': ('bus', ['---', '---', '0x20', '---', '0x40', '---', '---', '---', '---', '---', '---']),

        # Data
        'WDATA': ('bus', ['---', '---', '0xAA', '---', '0x99', '---', '---', '---', '---', '---', '---']),
        'RDATA': ('bus', ['???', '???', 'Old20', '0xAA', '0x99', '0x99', '0x99', '0x99', '0x99', '0x99', '0x99'])
    }

    # Ordering of signals from top to bottom
    signal_order = ['CLK', 'PC', 'INSTR', 'RE',
                    'WE', 'RADDR', 'WADDR', 'WDATA', 'RDATA']

    # Helper to draw a single bit signal
    def draw_bit(name, values, y_pos):
        # Draw baseline
        ax.text(-0.8, y_pos + 0.25, name, fontsize=12,
                fontweight='bold', ha='right')

        t_vals = []
        y_vals = []

        for i, val in enumerate(values):
            # Create square wave logic
            t_start = i
            t_end = i + 1

            # Rising/Falling edges
            if i > 0:
                t_vals.append(t_start)
                y_vals.append(y_pos + values[i-1] * 0.8)  # Previous level
                t_vals.append(t_start)
                y_vals.append(y_pos + val * 0.8)         # Current level
            else:
                t_vals.append(t_start)
                y_vals.append(y_pos + val * 0.8)

            t_vals.append(t_end)
            y_vals.append(y_pos + val * 0.8)

        ax.plot(t_vals, y_vals, color='black', linewidth=1.5)

    # Helper to draw a clock signal
    def draw_clock(name, count, y_pos):
        ax.text(-0.8, y_pos + 0.25, name, fontsize=12,
                fontweight='bold', ha='right')
        t_vals = []
        y_vals = []
        for i in range(count):
            # Up
            t_vals.extend([i, i, i + 0.5, i + 0.5])
            y_vals.extend([y_pos, y_pos + 0.8, y_pos + 0.8, y_pos])
        # Finish last cycle
        t_vals.append(count)
        y_vals.append(y_pos)

        ax.plot(t_vals, y_vals, color='black', linewidth=1.5)

    # Helper to draw a bus signal
    def draw_bus(name, values, y_pos):
        ax.text(-0.8, y_pos + 0.4, name, fontsize=12,
                fontweight='bold', ha='right')
        h = 0.8  # Height of bus

        for i, val in enumerate(values):
            x = i

            # Decide shape based on value change or "---"
            is_valid = val not in ['---', '???']
            prev_val = values[i-1] if i > 0 else None

            # Draw hexagon/box for valid data
            if is_valid:
                # Crossover lines at start
                ax.plot([x, x + 0.15], [y_pos + h/2, y_pos + h], 'k-', lw=1)
                ax.plot([x, x + 0.15], [y_pos + h/2, y_pos], 'k-', lw=1)

                # Top/Bottom lines
                ax.plot([x + 0.15, x + 0.85],
                        [y_pos + h, y_pos + h], 'k-', lw=1)
                ax.plot([x + 0.15, x + 0.85], [y_pos, y_pos], 'k-', lw=1)

                # Crossover lines at end
                ax.plot([x + 0.85, x + 1.0],
                        [y_pos + h, y_pos + h/2], 'k-', lw=1)
                ax.plot([x + 0.85, x + 1.0], [y_pos, y_pos + h/2], 'k-', lw=1)

                # Text
                ax.text(x + 0.5, y_pos + h/2, val,
                        ha='center', va='center', fontsize=9)

            elif val == '???':
                # Crosshatch block for unknown
                rect = patches.Rectangle(
                    (x, y_pos), 1, h, linewidth=1, edgecolor='black', facecolor='#eeeeee')
                ax.add_patch(rect)
                # Draw X inside
                ax.plot([x, x+1], [y_pos, y_pos+h], 'k-', lw=0.5)
                ax.plot([x, x+1], [y_pos+h, y_pos], 'k-', lw=0.5)

            else:  # '---'
                # simple midline
                ax.plot([x, x+1], [y_pos + h/2, y_pos + h/2], 'k-', lw=1)

    # Main Drawing Loop
    current_y = (len(signal_order) - 1) * y_spacing

    for sig in signal_order:
        sig_type, sig_data = data[sig]

        if sig == 'CLK':
            draw_clock(sig, cycles, current_y)
        elif sig_type == 'bit':
            draw_bit(sig, sig_data, current_y)
        elif sig_type == 'bus':
            draw_bus(sig, sig_data, current_y)

        current_y -= y_spacing

    # Add Cycle Labels at the top
    for i in range(cycles):
        ax.text(i + 0.5, (len(signal_order)) * y_spacing - 1.0, f'C{i+1}',
                ha='center', fontsize=10, fontweight='bold', color='blue')

    # Add Annotations (A), (B), (C)
    # Calculate y position for RDATA (it is the last signal, so y=0)
    rdata_y = 0

    # Coordinates for annotations based on your ASCII Art
    # (A) under Old20 (Cycle 3 -> index 2)
    ax.annotate('(A)', xy=(2.5, rdata_y - 0.3), xycoords='data',
                ha='center', color='red', fontweight='bold')

    # (B) under 0xAA (Cycle 4 -> index 3)
    ax.annotate('(B)', xy=(3.5, rdata_y - 0.3), xycoords='data',
                ha='center', color='red', fontweight='bold')

    # (C) under 0x99 (Cycle 5 -> index 4)
    ax.annotate('(C)', xy=(4.5, rdata_y - 0.3), xycoords='data',
                ha='center', color='red', fontweight='bold')

    # Final plot adjustments
    ax.set_xlim(0, cycles)
    ax.set_ylim(-1, len(signal_order) * y_spacing)
    ax.set_xticks(range(cycles + 1))
    ax.set_yticks([])  # Hide Y axis values
    ax.set_title(
        "Instruction & Data Memory Timing Diagram (with RAW Forwarding)", fontsize=16, pad=20)

    plt.tight_layout()
    plt.savefig('timing_diagram.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    draw_timing_diagram()
