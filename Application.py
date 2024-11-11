import json
import random
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# Clear the frame when switching between pages
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Menu command to add options
def menu_command():
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    Champ_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Programs", menu=Champ_menu)
    Champ_menu.add_command(label="Single Random Champion", command=show_single_randomizer_page)
    Champ_menu.add_command(label="Random Team Champions", command=show_team_randomizer_page)


# Filter champions based on role
def filter_champions_role(champion_data, role):
    if role == 'All':
        return champion_data
    return [champion for champion in champion_data if role in champion['positions']]

def filter_champions_region(champion_data, region):
    if region == 'All':
        return champion_data
    return [champion for champion in champion_data if region in champion['regions']]

def filter_champions_range(champion_data, region):
    if region == 'All':
        return champion_data
    return [champion for champion in champion_data if region in champion['range']]

def filter_champions_damage(champion_data, region):
    if region == 'All':
        return champion_data
    return [champion for champion in champion_data if region in champion['adap_type']]

def filter_champions():
    role = role_var.get()
    region = region_var.get()
    ranged = range_var.get()
    damage = damage_var.get()

    filtered_role_champions = filter_champions_role(champion_data, role)
    filtered_region_champions = filter_champions_region(filtered_role_champions, region)
    filtered_range_champions = filter_champions_range(filtered_region_champions, ranged)
    filtered_champions = filter_champions_damage(filtered_range_champions, damage)

    return filtered_champions


# Display the single champion randomizer
def show_single_randomizer_page():
    clear_frame()
    menu_command()

    title_label = tk.Label(root, text="Random Champion Selector", font=("Helvetica", 22), bd=2, relief="solid", padx=10, pady=5)
    title_label.pack(pady=10)

    filterTitle = tk.Label(root, text="Filtering part", font=("Helvetica", 16), justify="center")
    filterTitle.pack(pady=10)

    # Create a frame to contain the dropdowns horizontally
    dropdown_frame = tk.Frame(root)
    dropdown_frame.pack(pady=10)

    # Role label and dropdown
    role_label = tk.Label(dropdown_frame, text="Role:", font=("Helvetica", 12))
    role_label.grid(row=0, column=0, padx=5, pady=(0, 5))  # Padding between label and dropdown

    global role_var
    role_var = tk.StringVar()
    role_var.set("Top")

    role_dropdown = tk.OptionMenu(dropdown_frame, role_var, "Top", "Jungle", "Middle", "Bottom", "Support", "All")
    role_dropdown.grid(row=1, column=0, padx=5)

    # Region label and dropdown
    region_label = tk.Label(dropdown_frame, text="Region:", font=("Helvetica", 12))
    region_label.grid(row=0, column=1, padx=5, pady=(0, 5))

    global region_var
    region_var = tk.StringVar()
    region_var.set("All")

    region_dropdown = tk.OptionMenu(dropdown_frame, region_var, "All", 'Bandle City', 'Bilgewater', 'Camavor', 'Demacia', 'Freljord', 'Icathia', 'Ixtal', 'Ionia', 'Kathkan', 'Targon', 'Noxus', 'Piltover', 'Runeterra', 'Shadow Isles', 'Shurima', 'The Void', 'Zaun')
    region_dropdown.grid(row=1, column=1, padx=5)

    # Range label and dropdown
    range_label = tk.Label(dropdown_frame, text="Range:", font=("Helvetica", 12))
    range_label.grid(row=0, column=2, padx=5, pady=(0, 5))

    global range_var
    range_var = tk.StringVar()
    range_var.set("All")

    range_dropdown = tk.OptionMenu(dropdown_frame, range_var, "All", "Melee", "Ranged")
    range_dropdown.grid(row=1, column=2, padx=5)

    # Damage label and dropdown
    damage_label = tk.Label(dropdown_frame, text="Damage:", font=("Helvetica", 12))
    damage_label.grid(row=0, column=3, padx=5, pady=(0, 5))

    global damage_var
    damage_var = tk.StringVar()
    damage_var.set("All")

    damage_dropdown = tk.OptionMenu(dropdown_frame, damage_var, "All", "Physical", "Magic")
    damage_dropdown.grid(row=1, column=3, padx=5)

    # Champion info label
    ChampionsTitle = tk.Label(root, text="Champion part", font=("Helvetica", 16), justify="center")
    ChampionsTitle.pack(pady=10)

    global champ_icon_label
    champ_icon_label = tk.Label(root)
    champ_icon_label.pack(pady=10)

    global champ_info_label
    champ_info_label = tk.Label(root, text="Click 'Select Champion' to begin!", wraplength=300, justify="center")
    champ_info_label.pack(pady=20)

    pick_button = tk.Button(root, text="Pick Random Champion", command=pick_random_champion)
    pick_button.pack(pady=10)

# Display the team randomizer
def show_team_randomizer_page():
    clear_frame()
    menu_command()

    title_label = tk.Label(root, text="Random Team Champions", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Filter type dropdown
    filter_type_label = tk.Label(root, text="Filter by:", font=("Helvetica", 12))
    filter_type_label.pack(pady=5)

    global filter_var
    filter_var = tk.StringVar()
    filter_var.set("Region")

    filter_type_dropdown = tk.OptionMenu(root, filter_var, "Region", "Damage Type", "Range", command=update_filter_options)
    filter_type_dropdown.pack(pady=5)

    # Frame for the filter-specific dropdown (region, damage type, range)
    global filter_options_frame
    filter_options_frame = tk.Frame(root)
    filter_options_frame.pack(pady=10)

    pick_button = tk.Button(root, text="Pick Random Team", command=pick_random_team)
    pick_button.pack(pady=10)

    global roles, champ_labels, champ_icon_labels, reroll_buttons, reroll_flags
    roles = ["Top", "Jungle", "Middle", "Bottom", "Support"]
    champ_labels = {}
    champ_icon_labels = {}
    reroll_buttons = {}
    reroll_flags = {role: False for role in roles}

    # Create horizontal layout for roles
    team_frame = tk.Frame(root)
    team_frame.pack(pady=10)

    for role in roles:
        role_frame = tk.Frame(team_frame)
        role_frame.pack(side="left", padx=20)

        # Role title above the icon
        role_label = tk.Label(role_frame, text=f"{role}:", font=("Helvetica", 14))
        role_label.pack(pady=5)

        # Champion icon label
        champ_icon_labels[role] = tk.Label(role_frame)
        champ_icon_labels[role].pack(pady=5)

        # Champion name label
        champ_labels[role] = tk.Label(role_frame, text=f"Champion: ", font=("Helvetica", 12))
        champ_labels[role].pack(pady=5)

        # Reroll button under the name
        reroll_buttons[role] = tk.Button(role_frame, text="Reroll", command=lambda r=role: reroll_champion(r))
        reroll_buttons[role].pack(pady=5)

def update_filter_options(selected_filter):
    # Clear the filter options frame
    for widget in filter_options_frame.winfo_children():
        widget.destroy()

    global specific_filter_var
    specific_filter_var = tk.StringVar()

    if selected_filter == "Region":
        # Get valid regions with champions in all roles
        valid_regions = find_valid_regions(champion_data, roles)
        specific_filter_var.set("All")
        filter_options = ["All"] + valid_regions  # Add 'All' option to select from all champions
    elif selected_filter == "Damage Type":
        specific_filter_var.set("All")
        filter_options = ["All", "Physical", "Magic"]
    elif selected_filter == "Range":
        specific_filter_var.set("All")
        filter_options = ["All", "Melee", "Ranged"]
    else:
        return

    filter_dropdown = tk.OptionMenu(filter_options_frame, specific_filter_var, *filter_options)
    filter_dropdown.pack()

# Function to find regions with at least one champion in each role
def find_valid_regions(champion_data, roles):
    valid_regions = []

    for region in ['Bandle City', 'Bilgewater', 'Camavor', 'Demacia', 'Freljord', 'Icathia', 'Ixtal', 'Ionia', 'Kathkan', 
                   'Targon', 'Noxus', 'Piltover', 'Runeterra', 'Shadow Isles', 'Shurima', 'The Void', 'Zaun']:
        region_valid = True
        for role in roles:
            champions_in_role = filter_champions_role(champion_data, role)
            if not any(region in champion['regions'] for champion in champions_in_role):
                region_valid = False
                break
        if region_valid:
            valid_regions.append(region)

    return valid_regions

def pick_random_team():
    global picked_champions
    picked_champions = {}

    filter_type = filter_var.get()
    specific_filter = specific_filter_var.get()

    for role in roles:
        champions = filter_champions_role(champion_data, role)

        # Apply the selected filter
        if filter_type == "Region" and specific_filter != "All":
            champions = [champion for champion in champions if specific_filter in champion['regions']]
        elif filter_type == "Damage Type" and specific_filter != "All":
            champions = [champion for champion in champions if champion['adap_type'] == specific_filter]
        elif filter_type == "Range" and specific_filter != "All":
            champions = [champion for champion in champions if champion['range'] == specific_filter]

        random_champion = get_random_champion(champions)
        picked_champions[role] = random_champion

        # Update the champion's name and icon
        champ_labels[role].config(text=f"{random_champion['name']}")
        display_champion_icon(random_champion['icon_url'], champ_icon_labels[role])

        reroll_flags[role] = False


# Reroll the champion for a specific role (only once)
def reroll_champion(role):
    if reroll_flags[role]:
        messagebox.showwarning("Reroll Limit", f"You can only reroll {role} once!")
        return

    champions = filter_champions_role(champion_data, role)
    new_champion = get_random_champion(champions)
    picked_champions[role] = new_champion

    # Update the champion's name
    champ_labels[role].config(text=f"{new_champion['name']}")

    # Display the new champion's icon
    display_champion_icon(new_champion['icon_url'], champ_icon_labels[role])

    reroll_flags[role] = True  # Mark that reroll has been used

    # Display the new champion's icon
    display_champion_icon(new_champion['icon_url'], champ_icon_labels[role])

    reroll_flags[role] = True  # Mark that reroll has been used


# Load champion data from JSON
def load_champions():
    with open('champions_lol.json', 'r') as json_file:
        champion_data = json.load(json_file)
    return champion_data


# Get a random champion from a filtered list
def get_random_champion(champions):
    return random.choice(champions)


# Pick a random champion for the selected role in the single randomizer
def pick_random_champion():
    filtered_champions = filter_champions()
    random_champion = get_random_champion(filtered_champions)
    display_champion_icon(random_champion['icon_url'], champ_icon_label)
    champ_info_label.config(text=f"{random_champion['name']}", font=("Helvetica", 14))
    return random_champion

def display_champion_icon(icon_url, label):
    try:
        if not icon_url:
            raise ValueError("No icon URL provided")
        
        response = requests.get(icon_url)
        response.raise_for_status()
        image_data = response.content
        image = Image.open(io.BytesIO(image_data)).resize((64, 64), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label.config(image=photo)
        label.image = photo  # Prevent garbage collection

    except Exception as e:
        label.config(text="Failed to load icon")


# Main application setup
root = tk.Tk()
root.title('Random Champion Picker')
root.geometry("1920x1080")

champion_data = load_champions()

show_single_randomizer_page()

root.mainloop()
