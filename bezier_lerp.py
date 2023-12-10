import sys
import numpy as np
import math
import tkinter as tk
import random

def lerp(p1, p2, t):
    x = ((1-t)*p1[0]) + (t*p2[0])
    y = ((1-t)*p1[1]) + (t*p2[1])
    return (x, y)

class BezierCurve:
    
    # Drawing functions
    def draw_point(self):
        for p in self.points:
            x, y = p
            pid = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red", outline="white")
            self.point_id.append(pid)
            self.canvas.tag_bind(pid, "<B1-Motion>", lambda event, point_id=pid: self.update_curve(event, point_id))  
        
        self.draw_line(self.points) 
    
    def draw_line(self, p):
        for i in range(len(p) - 1):
            lid = self.canvas.create_line(p[i], p[i + 1], fill="white", dash=(2, 2))
            self.line_id.append(lid)
    
    def draw_lerp_point(self):
        for i in self.lerp_point_id:
            self.canvas.delete(i)
        for i in self.lerp_line_id:
            self.canvas.delete(i)
        for i in self.lerp_p2_id:
            self.canvas.delete(i)
        for i in self.lerp_pf_id:
            self.canvas.delete(i)
        
        self.lerp_points.clear()
        self.lerp_point_id.clear()
        self.lerp_line_id.clear()
        self.lerp_p2.clear()
        self.lerp_p2_id.clear()
        self.lerp_pf.clear()
        self.lerp_pf_id.clear()
        
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            pl = lerp(p1, p2, round(self.slider.get(), 3))
            self.lerp_points.append(pl)
            
        for i in range(len(self.lerp_points)-1):
            p1 = self.lerp_points[i]
            p2 = self.lerp_points[i+1]
            pl = lerp(p1, p2, round(self.slider.get(), 3))
            self.lerp_p2.append(pl)
            
        for i in range(len(self.lerp_p2)-1):
            p1 = self.lerp_p2[i]
            p2 = self.lerp_p2[i+1]
            pl = lerp(p1, p2, round(self.slider.get(), 3))
            self.lerp_pf.append(pl)
        
        for p in self.lerp_points:
            x, y = p
            pid = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", outline="white")
            self.lerp_point_id.append(pid)
        
        for p in self.lerp_p2:
            x, y = p
            pid = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="green", outline="white")
            self.lerp_p2_id.append(pid)
        
        for p in self.lerp_pf:
            x, y = p
            pid = self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white", outline="white")
            self.lerp_pf_id.append(pid)
        
        
        self.draw_lerp_line(self.lerp_points)
        self.draw_lerp_line(self.lerp_p2)
    
    def draw_lerp_line(self, p):
        col = ""
        match p:
            case self.lerp_points:
                col = "blue"
            case self.lerp_p2:
                col = "green"
            case self.points:
                col = "red"
            
        for i in range(len(p) - 1):
            lid = self.canvas.create_line(p[i], p[i + 1], fill=col, dash=(2, 2))
            self.lerp_line_id.append(lid)
        
    # Update functions
    def update_line(self):
        for i, lid in enumerate(self.line_id):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            self.canvas.coords(lid, x1, y1, x2, y2)
            
    def update_lerp_line(self, lp, id):
        for i, lid in enumerate(id):
            x1, y1 = lp[i]
            x2, y2 = lp[i + 1]
            self.canvas.coords(lid, x1, y1, x2, y2)
    
    def update_curve(self, event, pid):
        index = self.point_id.index(pid)
        x, y = event.x, event.y
        self.canvas.coords(pid, x - 10, y - 10, x + 10, y + 10)
        self.points[index] = (x, y)
        
        self.update_line()
        self.draw_lerp_point()
        self.update_lerp_line(self.lerp_points, self.lerp_line_id)
        self.update_lerp_line(self.lerp_p2, self.lerp_line_id)
    
    def slider_changed(self, event):
        self.draw_lerp_point()
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bezier Curve Lerp Demonstration")

        # Set up canvas
        self.canvas = tk.Canvas(self.root, width=1200, height=800, bg="black")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        
        # Points
        #self.points = [(500, 200), (500, 500)]
        #self.points = [(500, 200), (500, 500), (700, 200)]
        self.points = [(500, 200), (500, 500), (700, 200), (700, 500)]
        self.point_id = []
        
        self.lerp_points = []
        self.lerp_point_id = []
        
        self.lerp_p2 = []
        self.lerp_p2_id = []
        
        self.lerp_pf = []
        self.lerp_pf_id = []
        
        self.line_id = []
        self.lerp_line_id = []
        
        self.slider = tk.Scale(self.root, 
                               from_=0, 
                               to=1, 
                               resolution=0.001, 
                               orient=tk.HORIZONTAL, 
                               label="Adjust t"
                               )
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)
        self.slider.set(0)
        self.slider.bind("<B1-Motion>", self.slider_changed)
        
        
        # Run functions
        self.draw_point()
        self.draw_lerp_point()

    
def main():
    root = tk.Tk()
    app = BezierCurve(root)
    root.mainloop()

if __name__ == "__main__":
    main()
