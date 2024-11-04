import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time

class CharityBudgetPlanner:
    def __init__(self, master):
        self.master = master
        self.master.title("Charity Budget Planner")

        # Load the original background image
        self.original_image = Image.open("image1.jpg")
        self.bg_image = ImageTk.PhotoImage(self.original_image)

        # Create a background label
        self.bg_label = tk.Label(self.master, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Bind the window resize event to dynamically adjust the background
        self.last_resize_time = time.time()
        self.resize_delay = 0.1  # 100ms debounce time
        self.threshold = 20
        self.master.bind("<Configure>", self.on_resize)

        # Default items for the planner
        self.items = [
            {"name": "Food Supplies", "weight": 10, "value": 60},
            {"name": "Medical Kits", "weight": 8, "value": 40},
            {"name": "Books", "weight": 4, "value": 20},
            {"name": "Sleeping Bags", "weight": 12, "value": 50},
            {"name": "Water Bottles", "weight": 3, "value": 10},
            {"name": "First Aid Kits", "weight": 6, "value": 35},
            {"name": "Tents", "weight": 15, "value": 80},
            {"name": "Flashlights", "weight": 2, "value": 15},
            {"name": "Blankets", "weight": 9, "value": 45}
        ]

        self.create_widgets()

    def on_resize(self, event):
        """Debounce and resize only if significant change."""
        current_time = time.time()
        if (current_time - self.last_resize_time) > self.resize_delay:
            width_diff = abs(event.width - self.bg_image.width())
            height_diff = abs(event.height - self.bg_image.height())
            if width_diff > self.threshold or height_diff > self.threshold:
                self.resize_background(event.width, event.height)
                self.last_resize_time = current_time

    def resize_background(self, new_width, new_height):
        """Resize the background image to the new dimensions."""
        resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_image)
        self.bg_label.config(image=self.bg_image)

    def create_widgets(self):
        # Label styling
        label_font = ("Arial", 12, "bold")
        label_color = "#ffffff"  # White color

        # Title label for the output section
        title_label = tk.Label(self.master, text="Charity Budget Planner", font=("Arial", 16, "bold"), fg=label_color, bg="#8B4513")
        title_label.pack(pady=10)

        # Listbox to display items
        self.items_listbox = tk.Listbox(self.master, width=50, height=10, font=label_font, fg="black", bg="#87CEEB")
        self.items_listbox.pack(pady=10)

        # Button to view items
        self.view_button = tk.Button(self.master, text="View Items", command=self.view_items, font=label_font, fg="white", bg="#4CAF50")
        self.view_button.pack(pady=5)

        # Input fields for adding an item
        self.name_entry = tk.Entry(self.master, width=20, font=label_font)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Item Name")

        self.weight_entry = tk.Entry(self.master, width=20, font=label_font)
        self.weight_entry.pack(pady=5)
        self.weight_entry.insert(0, "Item Weight (Integer)")

        self.value_entry = tk.Entry(self.master, width=20, font=label_font)
        self.value_entry.pack(pady=5)
        self.value_entry.insert(0, "Item Value (Integer)")

        # Add and Delete buttons with styling
        self.add_button = tk.Button(self.master, text="Add Item", command=self.add_item, font=label_font, fg="white", bg="#4CAF50")
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(self.master, text="Delete Item", command=self.delete_item, font=label_font, fg="white", bg="#F44336")
        self.delete_button.pack(pady=5)

        # Knapsack button
        self.knapsack_button = tk.Button(self.master, text="Perform Knapsack", command=self.choose_knapsack, font=label_font, fg="white", bg="#FF9800")
        self.knapsack_button.pack(pady=5)

        # Output label
        output_label = tk.Label(self.master, text="Output", font=("Arial", 14, "bold"), fg=label_color, bg="#8B4513")
        output_label.pack(pady=10)

        # Text box to display the output with styling
        self.result_text = tk.Text(self.master, height=10, width=50, font=label_font, fg="black", bg="#87CEEB")
        self.result_text.pack(pady=10)

    def view_items(self):
        """Display all available items in the listbox."""
        self.items_listbox.delete(0, tk.END)
        for item in self.items:
            self.items_listbox.insert(tk.END, f"{item['name']}: Weight = {item['weight']}, Value = {item['value']}")

    def add_item(self):
        """Add a new item based on user input."""
        try:
            name = self.name_entry.get()
            weight = int(self.weight_entry.get())
            value = int(self.value_entry.get())
            self.items.append({"name": name, "weight": weight, "value": value})
            self.view_items()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer values for weight and value.")

    def delete_item(self):
        """Delete the selected item from the listbox and items list."""
        try:
            selected_index = self.items_listbox.curselection()[0]
            del self.items[selected_index]
            self.view_items()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item to delete.")

    def knapsack_01(self, capacity):
        """Perform the 0/1 knapsack algorithm."""
        n = len(self.items)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if self.items[i - 1]['weight'] <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - self.items[i - 1]['weight']] + self.items[i - 1]['value'])
                else:
                    dp[i][w] = dp[i - 1][w]

        result = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                result.append(self.items[i - 1])
                w -= self.items[i - 1]['weight']

        return result

    def knapsack_fractional(self, capacity):
        """Perform the fractional knapsack algorithm."""
        sorted_items = sorted(self.items, key=lambda x: x['value'] / x['weight'], reverse=True)
        total_value = 0
        result = []

        for item in sorted_items:
            if item['weight'] <= capacity:
                result.append(item)
                total_value += item['value']
                capacity -= item['weight']
            else:
                fraction = capacity / item['weight']
                result.append({"name": item['name'], "weight": capacity, "value": item['value'] * fraction})
                total_value += item['value'] * fraction
                break

        return result

    def choose_knapsack(self):
        """Ask the user for the type of knapsack and perform the calculation."""
        capacity = simpledialog.askinteger("Knapsack Capacity", "Enter knapsack capacity:")
        if not capacity:
            return

        choice = simpledialog.askstring("Knapsack Type", "Enter '01' for 0/1 Knapsack or 'Fractional' for Fractional Knapsack:")

        if choice == "01":
            result = self.knapsack_01(capacity)
        elif choice.lower() == "fractional":
            result = self.knapsack_fractional(capacity)
        else:
            messagebox.showerror("Invalid Choice", "Please enter '01' or 'Fractional'.")
            return

        self.display_result(result)

    def display_result(self, result):
        """Display the result of the knapsack algorithm."""
        self.result_text.delete(1.0, tk.END)
        total_value = sum(item['value'] for item in result)
        self.result_text.insert(tk.END, f"Total Value: {total_value}\n\n")
        for item in result:
            self.result_text.insert(tk.END, f"{item['name']} - Weight: {item['weight']}, Value: {item['value']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    planner = CharityBudgetPlanner(root)
    root.mainloop()
