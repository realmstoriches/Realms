import os

BRIDGE = r"F:\Realms\agentic_bridge"
GUI = os.path.join(BRIDGE, "swarm_gui.py")

def expand_gui():
    with open(GUI, "r", encoding="utf-8") as f:
        code = f.read()

    new_buttons = []
    for file in os.listdir(BRIDGE):
        if file.endswith(".py") and file not in code:
            label = file.replace(".py", "").replace("_", " ").title()
            new_buttons.append(f'tk.Button(root, text="{label}", width=30, command=lambda s="{file}": launch(s)).pack(pady=4)')

    if new_buttons:
        insertion_point = code.find("root.mainloop()")
        updated = code[:insertion_point] + "\n" + "\n".join(new_buttons) + "\n" + code[insertion_point:]
        with open(GUI, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"✅ GUI expanded with {len(new_buttons)} new modules.")
    else:
        print("✅ GUI already includes all modules.")

if __name__ == "__main__":
    expand_gui()