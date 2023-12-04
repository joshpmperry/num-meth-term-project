import tkinter as tk
import numpy as np

import numpy as np

def deBoor(k, x, t, c, p):
    n = len(c) - 1  # The highest index of the control points

    d = [int(coord[0]) for coord in [c[j + k - p] if 0 <= (j + k - p) <= n else (0, 0) for j in range(0, p + 1)]]

    for r in range(1, p + 1):
        for j in range(p, r - 1, -1):
            denominator = (t[j + 1 + k - r] - t[j + k - p])
            alpha = (x - t[j + k - p]) / denominator if denominator != 0 else 0.0
            d[j] = int(np.nan_to_num((1.0 - alpha) * d[j - 1] + alpha * d[j]))

    return d[p]







class BSplineCurve:
    def __init__(self, root):
        self.root = root
        self.root.title("B-Spline Curve")

        self.canvas = tk.Canvas(self.root, width=1200, height=800, bg="black")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.points = [(500, 200), (500, 500), (700, 200), (700, 500)]
        self.control_ids = []

        self.p = 2  # Degree of B-spline
        self.knots = [0, 0, 0, 1, 2, 3, 3, 3]  # Example knot vector

        self.draw_bspline_curve()
        self.draw_control_points()

    def draw_bspline_curve(self):
        curve_points = []
        for t in np.arange(self.p, len(self.points) + self.p, 0.01):
            x = int(t)
            y = int(deBoor(x, t, self.knots, self.points, self.p))
            curve_points.append((x, y))

        flattened_points = [coord for point in curve_points for coord in point]
        self.canvas.create_line(flattened_points, fill="blue", width=2)


    def draw_control_points(self):
        for point in self.points:
            x, y = point
            control_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="white")
            self.control_ids.append(control_id)
            self.canvas.tag_bind(control_id, "<B1-Motion>", lambda event, point_id=control_id: self.update_control_point(event, point_id))

    def update_control_point(self, event, control_id):
        index = self.control_ids.index(control_id)
        x, y = event.x, event.y
        self.canvas.coords(control_id, x - 5, y - 5, x + 5, y + 5)
        self.points[index] = (x, y)

        self.canvas.delete("all")
        self.draw_bspline_curve()
        self.draw_control_points()

def main():
    root = tk.Tk()
    app = BSplineCurve(root)
    root.mainloop()

if __name__ == "__main__":
    main()
