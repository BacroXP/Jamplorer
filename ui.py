import tkinter as tk
import math

class TopSinusoidalBar(tk.Canvas):
    def __init__(self, master, width, height, amplitude, frequency, phase_shift, bg_color, curve_color):
        super().__init__(master, width=width, height=height, bg=bg_color)

        self.amplitude = amplitude
        self.frequency = frequency
        self.phase_shift = phase_shift
        self.curve_color = curve_color

        self.draw_bar_and_curve()

    def draw_bar_and_curve(self):
        # Clear canvas
        self.delete("all")

        # Draw the background bar
        self.create_rectangle(0, 0, self.winfo_width(), self.winfo_height(), fill=self["bg"], outline="")

        # Draw the sinusoidal curve at the bottom
        num_points = self.winfo_width()  # Number of points to draw the curve
        curve_points = []

        for x in range(num_points):
            y = self.amplitude * math.sin(2 * math.pi * self.frequency * x / num_points + self.phase_shift)
            curve_points.extend([x, self.winfo_height() - y])

        self.create_line(curve_points, fill=self.curve_color, width=2)

# Create a tkinter window
root = tk.Tk()
root.title("Sinusoidal Bar Example")

# Parameters for the sinusoidal bar
width = 600
height = 200
amplitude = 50
frequency = 2 * math.pi / width  # Adjust frequency based on width to complete one cycle
phase_shift = 0
bg_color = "white"
curve_color = "blue"

# Create the TopSinusoidalBar instance
sinusoidal_bar = TopSinusoidalBar(root, width=width, height=height, amplitude=amplitude,
                                   frequency=frequency, phase_shift=phase_shift,
                                   bg_color=bg_color, curve_color=curve_color)
sinusoidal_bar.pack()

root.mainloop()
