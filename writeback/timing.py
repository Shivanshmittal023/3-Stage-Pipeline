import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_timing_diagram():
    # Setup the figure
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_facecolor('white')

    # ---------------------------------------------------------
    # 1. Define Data
    # ---------------------------------------------------------
    cycles = 12
    y_gap = 2  # Vertical spacing between signals

    # Signal Names and Logic (1 = High, 0 = Low)
    signals = [
        {"name": "clk",               "type": "clk",  "data": []},

        # Stall is HIGH at Cycle 6
        {"name": "stall_read_i",      "type": "bit",
            "data": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]},

        {"name": "wb_branch_i",       "type": "bit",
            "data": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
        {"name": "wb_stall_first_o",  "type": "bit",
            "data": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]},
        {"name": "wb_stall_second_o", "type": "bit",
            "data": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]},
        {"name": "wb_write_byte_o",   "type": "bus",  "data": [
            "0", "0010", "1100", "0", "0", "0", "0", "0", "0", "0", "0", "0"]},
        {"name": "wb_alu_op",         "type": "bus",  "data": [
            "-", "SB", "SH", "-", "-", "-", "-", "-", "LB", "LBU", "LH", "-"]},

        # fetch_pc_i keeps counting up regardless of the stall (Free running counter)
        {"name": "fetch_pc_i",        "type": "bus",  "data": [
            "100", "104", "108", "10C", "110", "114", "118", "11C", "120", "124", "128", "12C"]},

        # inst_fetch_pc_o logic:
        # Cycle 5 (114): Normal
        # Cycle 6 (Stall): Holds 114 (Does NOT go to 118)
        # Cycle 7 (No Stall): Jumps straight to 11C (Skipping 118)
        {"name": "inst_fetch_pc_o",   "type": "bus",  "data": [
            "100", "104", "108", "10C", "110", "114", "114", "11C", "120", "124", "128", "12C"]},

        {"name": "wb_read_data_o",    "type": "bus",  "data": [
            "-", "-", "-", "-", "-", "-", "-", "-", "FF..FF", "00..FF", "F..8000", "-"]},
    ]

    # ---------------------------------------------------------
    # 2. Drawing Functions
    # ---------------------------------------------------------
    y = 0
    for sig in reversed(signals):
        name = sig["name"]
        dtype = sig["type"]
        data = sig["data"]

        # Draw Label
        ax.text(-1.5, y + 0.5, name, fontsize=12,
                ha='right', va='center', weight='bold')

        # Draw Signal
        if dtype == "clk":
            x_pts = []
            y_pts = []
            for i in range(cycles):
                x_pts.extend([i, i+0.5, i+0.5, i+1])
                y_pts.extend([y, y, y+1, y+1])
            ax.plot(x_pts, y_pts, 'k-', linewidth=1.5)

        elif dtype == "bit":
            x_pts = [0]
            y_pts = [y + data[0]]
            for i in range(len(data)):
                x_pts.append(i)
                y_pts.append(y + data[i])
                x_pts.append(i+1)
                y_pts.append(y + data[i])
            ax.plot(x_pts, y_pts, 'b-', linewidth=2)

        elif dtype == "bus":
            for i in range(cycles):
                val = data[i]
                if i < len(data):
                    # Transition lines
                    ax.plot([i, i+0.1], [y+0.5, y], 'k-', linewidth=0.5)
                    ax.plot([i, i+0.1], [y+0.5, y+1], 'k-', linewidth=0.5)
                    # Horizontal lines
                    ax.plot([i+0.1, i+1], [y, y], 'k-', linewidth=1)
                    ax.plot([i+0.1, i+1], [y+1, y+1], 'k-', linewidth=1)
                    # Closing lines
                    ax.plot([i+1, i+1.1], [y, y+0.5], 'k-', linewidth=0.5)
                    ax.plot([i+1, i+1.1], [y+1, y+0.5], 'k-', linewidth=0.5)
                    # Text
                    ax.text(i + 0.55, y + 0.5, val, ha='center',
                            va='center', fontsize=9)

        y += y_gap

    # ---------------------------------------------------------
    # 3. Formatting
    # ---------------------------------------------------------
    for i in range(cycles + 1):
        ax.axvline(i, color='gray', linestyle='--', alpha=0.3)
        ax.text(i + 0.5, y, f"Cycle {i+1}",
                ha='center', fontsize=8, color='gray')

    ax.set_xlim(0, cycles)
    ax.set_ylim(-1, y + 1)
    ax.axis('off')

    plt.title("Write Back (WB) Stage Timing Diagram (Corrected Stall Logic)",
              fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig("wb_timing_matplotlib_v2.png", dpi=300)
    print("Success! Generated 'wb_timing_matplotlib_v2.png'")
    plt.show()


if __name__ == "__main__":
    draw_timing_diagram()
