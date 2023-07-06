import random
import time
import csv
import tkinter as tk


class DotTest:
    def __init__(self):
        self.results = []
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600)  # Adjust the dimensions according to your screen
        self.canvas.pack()
        self.dot_size = 10
        self.current_dot = None

    def run(self):
        seed = input("Enter a seed value: ")
        random.seed(seed)
        dots = self.generate_random_dots()
        self.display_instructions()

        for dot in dots:
            self.current_dot = dot
            self.display_dot()
            start_time = time.time()
            self.canvas.bind("<Button-1>", self.get_click_position)
            self.root.mainloop()
            end_time = time.time()
            click_distance = self.calculate_distance(dot, self.current_dot)
            click_time = end_time - start_time
            self.results.append((seed, dot, self.current_dot, click_distance, click_time))
            self.update_progress(len(self.results), len(dots))

        test_name = input("Enter a name for the test: ")
        self.save_results(test_name)
        self.ask_for_retest()

    def generate_random_dots(self):
        dots = []
        for _ in range(25):
            x = random.randint(0, 800)  # Change the values according to your screen resolution
            y = random.randint(0, 600)  # Change the values according to your screen resolution
            dots.append((x, y))
        return dots

    def display_instructions(self):
        print("Click on each dot as it appears. Press Enter to start the test.")
        input()

    def display_dot(self):
        self.canvas.delete("dot")
        x, y = self.current_dot
        self.canvas.create_oval(x - self.dot_size, y - self.dot_size, x + self.dot_size, y + self.dot_size, fill="red",
                                tags="dot")

    def get_click_position(self, event):
        click_position = (event.x, event.y)
        self.root.quit()  # Exit the main loop to proceed to the next dot
        self.current_dot = click_position

    def calculate_distance(self, dot, click_position):
        dot_x, dot_y = dot
        click_x, click_y = click_position
        return ((dot_x - click_x) ** 2 + (dot_y - click_y) ** 2) ** 0.5

    def update_progress(self, completed, total):
        progress = completed / total * 100
        print(f"Progress: {completed}/{total} dots ({progress:.1f}%)\n")

    def save_results(self, test_name):
        with open('results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for result in self.results:
                writer.writerow([test_name] + list(result))
        print("Results saved.")

    def ask_for_retest(self):
        choice = input("Enter 'same' to repeat the test with the same seed, 'new' for a new seed, or 'done' to exit: ")
        if choice.lower() == 'same':
            self.results = []
            self.run()
        elif choice.lower() == 'new':
            self.results = []
            self.run()
        elif choice.lower() == 'done':
            print("Testing complete.")
            self.root.destroy()


test = DotTest()
test.run()