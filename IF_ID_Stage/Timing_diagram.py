import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_timing_diagram():
    # Setup Data for 13 Clock Cycles
    cycles = 13

    # 1. Minimal Signals & Pipeline Stages
    # CLK is generated procedurally
    pc = ["0x00", "0x04", "0x08", "0x0C", "0x0C", "0x28",
          "0x2C", "0x30", "0x34", "0x38", "0x3C", "0x40", "0x44"]
    if_instr = ["ADD", "BEQ", "SUB (Flush)", "NOP (Stall)", "NOP (Stall)",
                "LW", "SW", "AND", "OR", "XOR", "SLL", "SRL", "ADD"]
    ex_instr = ["-", "ADD", "BEQ", "NOP", "NOP", "NOP",
                "LW", "SW", "AND", "OR", "XOR", "SLL", "SRL"]
    wb_instr = ["-", "-", "ADD", "BEQ", "NOP", "NOP",
                "NOP", "LW", "SW", "AND", "OR", "XOR", "SLL"]

    # Control Signals
    stall = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    # Asserted when SW is in WB (based on pipelined mem_write)
    mem_write = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

    # Data Signals
    exec_imm = ["0", "0", "32", "0", "0", "0", "4", "8",
                "0", "0", "0", "0", "0"]  # 32 is branch offset
    exec_res = ["-", "R1+R2", "Br Taken", "-", "-", "-", "PC+4",
                "R2", "R4&R5", "R6|R7", "R8^R9", "R1<<2", "R3>>1"]
    wb_result = ["-", "-", "R1+R2", "-", "-", "-", "-",
                 "Mem[..]", "-", "R4&R5", "R6|R7", "R8^R9", "R1<<2"]

    # Setup Figure
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, cycles)
    ax.set_ylim(-1, 10)
    ax.axis('off')  # Hide default axes

    # Define Y-offsets for each signal track
    tracks = {
        "CLK": 9,
        "PC": 8,
        "IF Stage": 7,
        "EX Stage": 6,
        "WB Stage": 5,
        "Stall": 4,
        "Mem Write": 3,
        "Exec Imm": 2,
        "Exec Res": 1,
        "WB Result": 0
    }

    # Helper function to draw a boolean waveform
    def draw_bool_wave(y_base, data, color='blue'):
        ax.text(-0.5, y_base + 0.2, list(tracks.keys())[list(tracks.values()).index(y_base)],
                fontsize=12, fontweight='bold', ha='right', va='center')

        # Draw clock cycle vertical lines
        for i in range(cycles + 1):
            ax.axvline(x=i, color='gray', linestyle='--', alpha=0.3)

        x_points, y_points = [0], [y_base + data[0]*0.6]
        for i in range(cycles):
            x_points.extend([i+1, i+1])
            if i < cycles - 1:
                y_points.extend([y_base + data[i]*0.6, y_base + data[i+1]*0.6])
            else:
                y_points.extend([y_base + data[i]*0.6, y_base + data[i]*0.6])

        ax.plot(x_points, y_points, color=color, linewidth=2)

    # Helper function to draw bus data (hexagons/boxes)
    def draw_bus(y_base, data, name, color='lightblue'):
        ax.text(-0.5, y_base + 0.3, name, fontsize=12,
                fontweight='bold', ha='right', va='center')
        for i in range(cycles):
            # Draw a box for the data valid period
            val = data[i]
            if val != "-" and val != "0":
                poly = patches.Polygon([
                    (i + 0.05, y_base),
                    (i + 0.15, y_base + 0.6),
                    (i + 0.85, y_base + 0.6),
                    (i + 0.95, y_base),
                    (i + 0.85, y_base - 0.0),  # Flat bottom for simplicity
                    (i + 0.15, y_base - 0.0)
                ], closed=True, edgecolor='black', facecolor=color, alpha=0.7)

                # Highlight flushed/stalled instructions
                if "Flush" in val or "Stall" in val:
                    poly.set_facecolor('lightcoral')

                ax.add_patch(poly)
                # Add text inside
                ax.text(i + 0.5, y_base + 0.3, val, ha='center', va='center', fontsize=9,
                        color='black', fontweight='bold')
            else:
                # Draw a straight line for empty/invalid bus
                ax.plot([i, i+1], [y_base+0.3, y_base+0.3],
                        color='black', linewidth=1)

    # 1. Draw CLK
    clk_data = [i % 2 for i in range(cycles * 2)]  # toggle every half cycle
    x_clk = np.arange(0, cycles, 0.5)
    y_clk = [tracks["CLK"] + (1 if i % 2 == 0 else 0)
             * 0.6 for i in range(len(x_clk))]
    ax.text(-0.5, tracks["CLK"] + 0.2, "CLK", fontsize=12,
            fontweight='bold', ha='right', va='center')
    ax.step(x_clk, y_clk, where='post', color='black', linewidth=2)

    # 2. Draw Data Buses
    draw_bus(tracks["PC"], pc, "PC", color='lightgreen')
    draw_bus(tracks["IF Stage"], if_instr, "IF Stage", color='thistle')
    draw_bus(tracks["EX Stage"], ex_instr, "EX Stage", color='lightskyblue')
    draw_bus(tracks["WB Stage"], wb_instr, "WB Stage", color='khaki')

    # 3. Draw Boolean Control Signals
    draw_bool_wave(tracks["Stall"], stall, color='red')
    draw_bool_wave(tracks["Mem Write"], mem_write, color='purple')

    # 4. Draw Additional Data Buses
    draw_bus(tracks["Exec Imm"], exec_imm, "Exec Imm", color='lightgray')
    draw_bus(tracks["Exec Res"], exec_res, "Exec Res", color='wheat')
    draw_bus(tracks["WB Result"], wb_result, "WB Result", color='palegreen')

    # X-axis labels
    for i in range(cycles):
        ax.text(i + 0.5, -0.8, f"Cycle {i+1}",
                ha='center', fontsize=10, fontweight='bold')

    plt.title("Pipeline Processor Timing Diagram (Branch Flush & Write-back)",
              fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    draw_timing_diagram()
