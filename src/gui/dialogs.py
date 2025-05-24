"""
对话框模块
提供各种配置对话框
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.constants import (
    COLOR_OPTIONS, PEN_WIDTH_OPTIONS, DEFAULT_POLYGON, DEFAULT_POINT,
    FONT_FAMILY, NORMAL_FONT
)

class PolygonConfigDialog:
    """多边形配置对话框"""
    
    def __init__(self, parent, initial_config=None):
        """
        初始化多边形配置对话框
        
        Args:
            parent: 父窗口
            initial_config: 初始配置
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("多边形配置")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.config = initial_config or DEFAULT_POLYGON.copy()
        self.points = self.config["points"].copy()
        
        self._create_widgets()
        self._update_points_list()
    
    def _create_widgets(self):
        """创建控件"""
        # 点列表
        points_frame = ttk.LabelFrame(self.dialog, text="点列表", padding="5")
        points_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.points_list = tk.Listbox(points_frame, height=10)
        self.points_list.pack(fill=tk.BOTH, expand=True)
        
        # 点操作按钮
        points_btn_frame = ttk.Frame(points_frame)
        points_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(points_btn_frame, text="添加点", command=self._add_point).pack(side=tk.LEFT, padx=2)
        ttk.Button(points_btn_frame, text="删除点", command=self._delete_point).pack(side=tk.LEFT, padx=2)
        ttk.Button(points_btn_frame, text="编辑点", command=self._edit_point).pack(side=tk.LEFT, padx=2)
        
        # 样式设置
        style_frame = ttk.LabelFrame(self.dialog, text="样式设置", padding="5")
        style_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 线条粗细
        ttk.Label(style_frame, text="线条粗细:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.pen_width = ttk.Combobox(style_frame, values=PEN_WIDTH_OPTIONS, width=10)
        self.pen_width.set(self.config["pen_width"])
        self.pen_width.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        # 线条颜色
        ttk.Label(style_frame, text="线条颜色:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.pen_color = ttk.Combobox(style_frame, values=COLOR_OPTIONS, width=10)
        self.pen_color.set(self.config["pen_color"])
        self.pen_color.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # 是否封闭
        self.close_var = tk.BooleanVar(value=self.config["close"])
        ttk.Checkbutton(style_frame, text="封闭曲线", variable=self.close_var).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2
        )
        
        # 确定取消按钮
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _update_points_list(self):
        """更新点列表显示"""
        self.points_list.delete(0, tk.END)
        for i, point in enumerate(self.points):
            self.points_list.insert(tk.END, f"点 {i+1}: ({point['x']}, {point['y']})")
    
    def _add_point(self):
        """添加点"""
        dialog = PointInputDialog(self.dialog)
        self.dialog.wait_window(dialog.dialog)
        if dialog.result:
            self.points.append(dialog.result)
            self._update_points_list()
    
    def _delete_point(self):
        """删除选中的点"""
        selection = self.points_list.curselection()
        if selection:
            del self.points[selection[0]]
            self._update_points_list()
    
    def _edit_point(self):
        """编辑选中的点"""
        selection = self.points_list.curselection()
        if selection:
            index = selection[0]
            dialog = PointInputDialog(self.dialog, self.points[index])
            self.dialog.wait_window(dialog.dialog)
            if dialog.result:
                self.points[index] = dialog.result
                self._update_points_list()
    
    def _on_ok(self):
        """确定按钮回调"""
        if not self.points:
            messagebox.showerror("错误", "请至少添加一个点")
            return
        
        self.config = {
            "points": self.points,
            "pen_width": self.pen_width.get(),
            "pen_color": self.pen_color.get(),
            "close": self.close_var.get()
        }
        self.dialog.destroy()
    
    def get_config(self):
        """获取配置"""
        return self.config

class PointConfigDialog:
    """点配置对话框"""
    
    def __init__(self, parent, initial_config=None):
        """
        初始化点配置对话框
        
        Args:
            parent: 父窗口
            initial_config: 初始配置
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("点配置")
        self.dialog.geometry("300x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.config = initial_config or DEFAULT_POINT.copy()
        self._create_widgets()
    
    def _create_widgets(self):
        """创建控件"""
        # 位置设置
        pos_frame = ttk.LabelFrame(self.dialog, text="位置设置", padding="5")
        pos_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(pos_frame, text="经度:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.x_entry = ttk.Entry(pos_frame, width=15)
        self.x_entry.insert(0, str(self.config["x"]))
        self.x_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(pos_frame, text="纬度:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.y_entry = ttk.Entry(pos_frame, width=15)
        self.y_entry.insert(0, str(self.config["y"]))
        self.y_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # 样式设置
        style_frame = ttk.LabelFrame(self.dialog, text="样式设置", padding="5")
        style_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(style_frame, text="样式:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.style_entry = ttk.Entry(style_frame, width=15)
        self.style_entry.insert(0, self.config["style"])
        self.style_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(style_frame, text="填充颜色:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.fill_color = ttk.Combobox(style_frame, values=COLOR_OPTIONS, width=12)
        self.fill_color.set(self.config["fill"])
        self.fill_color.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(style_frame, text="线条粗细:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.pen_width = ttk.Combobox(style_frame, values=PEN_WIDTH_OPTIONS, width=12)
        self.pen_width.set(self.config["pen_width"])
        self.pen_width.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(style_frame, text="线条颜色:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.pen_color = ttk.Combobox(style_frame, values=COLOR_OPTIONS, width=12)
        self.pen_color.set(self.config["pen_color"])
        self.pen_color.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(style_frame, text="透明度:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.transparency = ttk.Scale(style_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.transparency.set(self.config["transparency"])
        self.transparency.grid(row=4, column=1, sticky="ew", padx=5, pady=2)
        
        # 确定取消按钮
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _on_ok(self):
        """确定按钮回调"""
        try:
            self.config = {
                "x": float(self.x_entry.get()),
                "y": float(self.y_entry.get()),
                "style": self.style_entry.get(),
                "fill": self.fill_color.get(),
                "pen_width": self.pen_width.get(),
                "pen_color": self.pen_color.get(),
                "transparency": int(self.transparency.get())
            }
            self.dialog.destroy()
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数值")
    
    def get_config(self):
        """获取配置"""
        return self.config

class PointInputDialog:
    """点输入对话框"""
    
    def __init__(self, parent, initial_point=None):
        """
        初始化点输入对话框
        
        Args:
            parent: 父窗口
            initial_point: 初始点坐标
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("输入点坐标")
        self.dialog.geometry("250x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.result = None
        self._create_widgets(initial_point)
    
    def _create_widgets(self, initial_point):
        """创建控件"""
        frame = ttk.Frame(self.dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="经度:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.x_entry = ttk.Entry(frame, width=15)
        self.x_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        if initial_point:
            self.x_entry.insert(0, str(initial_point["x"]))
        
        ttk.Label(frame, text="纬度:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.y_entry = ttk.Entry(frame, width=15)
        self.y_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        if initial_point:
            self.y_entry.insert(0, str(initial_point["y"]))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def _on_ok(self):
        """确定按钮回调"""
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.result = {"x": x, "y": y}
            self.dialog.destroy()
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数值")

class ScaleConfigDialog:
    def __init__(self, parent, initial_config=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("比例尺配置")
        self.dialog.geometry("350x120")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.result = None

        ttk.Label(self.dialog, text="GMT表达式（如 jBL+w1000k+o0.5c/0.5c）:").pack(pady=5)
        self.entry = ttk.Entry(self.dialog, width=35)
        self.entry.pack(pady=5)
        if initial_config:
            self.entry.insert(0, initial_config.get("map_scale", "jBL+w1000k+o0.5c/0.5c"))

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _on_ok(self):
        self.result = {"map_scale": self.entry.get()}
        self.dialog.destroy()

class CompassConfigDialog:
    def __init__(self, parent, initial_config=None):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("指南针配置")
        self.dialog.geometry("350x120")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.result = None

        ttk.Label(self.dialog, text="GMT表达式（如 jTL+o1c/1c）:").pack(pady=5)
        self.entry = ttk.Entry(self.dialog, width=35)
        self.entry.pack(pady=5)
        if initial_config:
            self.entry.insert(0, initial_config.get("compass", "jTL+o1c/1c"))

        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="确定", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)

    def _on_ok(self):
        self.result = {"compass": self.entry.get()}
        self.dialog.destroy() 