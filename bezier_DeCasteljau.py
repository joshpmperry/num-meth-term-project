import tkinter as tk

def de_casteljau(t, coefs):
    beta = [c for c in coefs] 
    n = len(beta)
    for j in range(1, n):
        for k in range(n - j):
            beta[k] = beta[k] * (1 - t) + beta[k + 1] * t
    return beta[0]

class BezierCurveApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Bezier Curve DeCasteljau")

        self.canvas = tk.Canvas(self.master, width=1200, height=800, bg="black")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.control_points = [(500, 200), (500, 500), (700, 200), (700, 500)]
        self.curve_points = []

        self.curve_id = None
        self.control_point_ids = []
        self.control_line_ids = []

        self.create_control_points()
        self.draw_curve()

    def create_control_points(self):
        for point in self.control_points:
            x, y = point
            point_id = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")
            self.control_point_ids.append(point_id)
            self.canvas.tag_bind(point_id, "<B1-Motion>", lambda event, point_id=point_id: self.update_curve(event, point_id))

        for i in range(len(self.control_points) - 1):
            line_id = self.canvas.create_line(self.control_points[i], self.control_points[i + 1], fill="gray", dash=(2, 2))
            self.control_line_ids.append(line_id)

    def draw_curve(self):
        self.curve_points = []
        for t in range(0, 101):
            t /= 100.0
            x = int(de_casteljau(t, [p[0] for p in self.control_points]))
            y = int(de_casteljau(t, [p[1] for p in self.control_points]))
            self.curve_points.append((x, y))

        if self.curve_id:
            self.canvas.delete(self.curve_id)

        self.curve_id = self.canvas.create_line(self.curve_points, fill="white")

    def update_curve(self, event, point_id):
        index = self.control_point_ids.index(point_id)
        x, y = event.x, event.y
        self.canvas.coords(point_id, x - 5, y - 5, x + 5, y + 5)
        self.control_points[index] = (x, y)

        self.update_control_lines()
        self.draw_curve()

    def update_control_lines(self):
        for i, line_id in enumerate(self.control_line_ids):
            
            x1, y1 = self.control_points[i]
            x2, y2 = self.control_points[i + 1]
            self.canvas.coords(line_id, x1, y1, x2, y2)

if __name__ == "__main__":
    root = tk.Tk()
    app = BezierCurveApp(root)

    root.mainloop()
