import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_timing_diagram():
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_facecolor('#f0f0f0')

    # Configuration
    cycles = 11
    # Signal names and their Y-positions
    signals = [
        ("Event", 0),
        ("wb_result", 1.5),
        ("next_pc", 3.0),
        ("branch_taken", 4.5),
        ("Internal ALU", 6.0),
        ("alu_operand2", 7.5),
        ("alu_operand1", 9.0),
        ("IN: Op/Ctrl", 10.5),
        ("PC (in)", 12.0),
        ("stall_read", 13.5),
        ("reset_n", 15.0),
        ("clk", 16.5)
    ]

    # Data from the user's ASCII chart
    data_map = {
        # 2x resolution
        "clk":          [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        "reset_n":      [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "stall_read":   [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "PC (in)":      ["0000", "100", "104", "108", "128", "132", "136", "136", "140", "..."],
        "IN: Op/Ctrl":  ["NOP", "ADD", "ADDI", "BEQ", "BNE", "SUB", "OR", "OR", "AND", "..."],
        "alu_operand1": ["xxxx", "10", "20", "5", "5", "100", "A", "A", "F", "..."],
        "alu_operand2": ["xxxx", "10", "5", "5", "3", "50", "B", "B", "0", "..."],
        "Internal ALU": ["xxxx", "20", "25", "0", "2", "50", "A|B", "A|B", "F", "..."],
        "branch_taken": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        "next_pc":      ["x+4", "104", "108", "128", "132", "136", "140", "140", "144", "..."],
        "wb_result":    ["0", "0", "20", "25", "?", "?", "50", "50", "A|B", "..."],
        "Event":        ["[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]", ""]
    }

    # Helper to draw a bus (box with text)
    def draw_bus(y_pos, data_list, color='#ffffff'):
        for i, text in enumerate(data_list):
            if i >= cycles:
                break
            # Draw hexagon/box shape
            rect = patches.Rectangle(
                (i, y_pos - 0.4), 1, 0.8, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            # Add text
            ax.text(i + 0.5, y_pos, text, ha='center',
                    va='center', fontsize=9, fontweight='bold')

    # Helper to draw single bit line
    def draw_bit(y_pos, bit_data, color='blue', is_clk=False):
        x_vals = []
        y_vals = []

        if is_clk:
            # Clock is high frequency
            for i in range(cycles):
                x_vals.extend([i, i+0.5, i+0.5, i+1])
                y_vals.extend([y_pos-0.4, y_pos-0.4, y_pos+0.4, y_pos+0.4])
        else:
            # Standard signals
            for i, val in enumerate(bit_data):
                if i >= cycles:
                    break
                y_level = y_pos + 0.4 if val else y_pos - 0.4
                if i == 0:
                    x_vals.extend([i, i+1])
                    y_vals.extend([y_level, y_level])
                else:
                    prev_y = y_vals[-1]
                    x_vals.extend([i, i, i+1])
                    y_vals.extend([prev_y, y_level, y_level])

        ax.plot(x_vals, y_vals, color=color, linewidth=2)

    # Drawing Loop
    for name, y in signals:
        # Label
        ax.text(-0.2, y, name, ha='right', va='center',
                fontsize=11, fontweight='bold')

        # Draw Data
        if name == "clk":
            draw_bit(y, [], is_clk=True, color='black')
        elif name in ["reset_n", "stall_read", "branch_taken"]:
            # Pad data to prevent index errors
            d = data_map[name] + [d for d in [data_map[name][-1]]
                                  * (cycles - len(data_map[name]))]
            draw_bit(y, d, color='red' if name == "stall_read" else 'green')
        elif name == "Event":
            for i, text in enumerate(data_map[name]):
                ax.text(i + 0.5, y, text, ha='center',
                        va='center', fontsize=10, color='#555')
        else:
            # Bus signals
            color = '#e6f3ff' if "alu" in name.lower() else '#fff2cc'
            if name == "wb_result":
                color = '#e2f0d9'
            draw_bus(y, data_map[name], color=color)

    # Grid and Formatting
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 18)
    ax.set_xticks(range(11))
    ax.set_xticklabels([f"C{i}\n{i*10}ns" for i in range(11)])
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)

    # Remove Y axis ticks/spines
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.title("Pipeline Stage 2 (Execute) Timing Diagram", fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('timing_diagram.png')
    plt.close()


draw_timing_diagram()
