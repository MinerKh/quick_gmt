"""
GUI配置界面模块
提供用户交互界面
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.constants import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG_COLOR,
    FONT_FAMILY, TITLE_FONT, NORMAL_FONT,
    DEFAULT_IMAGE_NAME, DEFAULT_IMAGE_FORMAT,
    DEFAULT_REGION, IMAGE_FORMATS, GMTCPTS, RESOLUTIONS
)
from src.gui.dialogs import PolygonConfigDialog, PointConfigDialog, ScaleConfigDialog, CompassConfigDialog

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

class ConfigGUI:
    """配置界面类，负责处理用户交互"""
    
    def __init__(self, on_submit=None):
        """
        初始化配置界面
        
        Args:
            on_submit (callable): 提交配置时的回调函数
        """
        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg='#f7f7f7')
        self.window.resizable(False, False)
        self.on_submit = on_submit
        
        # 存储多边形和点的配置
        self.polygon_config = None
        self.point_config = None
        self.scale_config = None
        self.compass_config = None
        self.help_var = tk.StringVar(value="")
        
        # 设置样式
        self._setup_styles()
        self._create_widgets()
    
    def _setup_styles(self):
        """设置界面样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=8, font=('微软雅黑', 11), relief='flat', borderwidth=0)
        self.style.configure('TLabel', font=('微软雅黑', 11), background='#f7f7f7')
        self.style.configure('TCheckbutton', font=('微软雅黑', 11), background='#f7f7f7')
        self.style.configure('TLabelframe', background='#f7f7f7', borderwidth=0)
        self.style.configure('TLabelframe.Label', font=('微软雅黑', 12, 'bold'), background='#f7f7f7')
    
    def _show_help(self, text):
        self.help_var.set(text)
    def _clear_help(self, event=None):
        self.help_var.set("")
    
    def _create_widgets(self):
        """创建界面控件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20", style='TLabelframe')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建标题
        title_label = ttk.Label(main_frame, text=WINDOW_TITLE, font=('微软雅黑', 22, 'bold'), anchor='center', background='#f7f7f7')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky='ew')
        
        # 创建左侧框架（参数设置）
        self._create_left_frame(main_frame)
        
        # 创建右侧框架（输出设置）
        self._create_right_frame(main_frame)
        
        # 创建区域范围设置
        self._create_region_frame(main_frame)
        
        # 创建按钮框架
        self._create_button_frame(main_frame)
        
        # 帮助提示栏
        self.help_label = ttk.Label(self.window, textvariable=self.help_var, foreground="#0077cc", font=("微软雅黑", 10), background='#f7f7f7')
        self.help_label.grid(row=99, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 15))
    
    def _create_left_frame(self, main_frame):
        """创建左侧参数设置框架"""
        left_frame = ttk.LabelFrame(main_frame, text="参数设置", padding="15", style='TLabelframe')
        left_frame.grid(row=1, column=0, padx=(0, 20), pady=0, sticky="nsew")
        self.elevation_var = tk.BooleanVar(value=True)
        self.elevation_cb = ttk.Checkbutton(left_frame, text="添加高程数据", variable=self.elevation_var)
        self.elevation_cb.grid(row=0, column=0, sticky="w", pady=6)
        self.elevation_cb.bind("<Enter>", lambda e: self._show_help("从GMT数据服务器下载高程数据，第一次加载会比较慢"))
        self.elevation_cb.bind("<Leave>", self._clear_help)
        self.topography_var = tk.BooleanVar(value=True)
        self.topography_cb = ttk.Checkbutton(left_frame, text="添加光照增强效果", variable=self.topography_var)
        self.topography_cb.grid(row=1, column=0, sticky="w", pady=6)
        self.topography_cb.bind("<Enter>", lambda e: self._show_help("如果选用，建议在配色模式中选择gray"))
        self.topography_cb.bind("<Leave>", self._clear_help)
        self.coast_line_var = tk.BooleanVar(value=True)
        self.coast_cb = ttk.Checkbutton(left_frame, text="重新绘制海岸线", variable=self.coast_line_var)
        self.coast_cb.grid(row=2, column=0, sticky="w", pady=6)
        polygon_frame = ttk.Frame(left_frame, style='TLabelframe')
        polygon_frame.grid(row=3, column=0, sticky="w", pady=6)
        self.plot_polygons_var = tk.BooleanVar(value=False)
        self.polygon_cb = ttk.Checkbutton(polygon_frame, text="多边形投图", variable=self.plot_polygons_var)
        self.polygon_cb.pack(side=tk.LEFT)
        ttk.Button(polygon_frame, text="配置", command=self._configure_polygon).pack(side=tk.LEFT, padx=8)
        self.polygon_cb.bind("<Enter>", lambda e: self._show_help("多边形投图：可以将研究区的范围投影上去"))
        self.polygon_cb.bind("<Leave>", self._clear_help)
        point_frame = ttk.Frame(left_frame, style='TLabelframe')
        point_frame.grid(row=4, column=0, sticky="w", pady=6)
        self.plot_points_var = tk.BooleanVar(value=False)
        self.point_cb = ttk.Checkbutton(point_frame, text="投点", variable=self.plot_points_var)
        self.point_cb.pack(side=tk.LEFT)
        ttk.Button(point_frame, text="配置", command=self._configure_point).pack(side=tk.LEFT, padx=8)
        self.point_cb.bind("<Enter>", lambda e: self._show_help("可以将样品位置投影上去"))
        self.point_cb.bind("<Leave>", self._clear_help)
    
    def _configure_polygon(self):
        """配置多边形参数"""
        dialog = PolygonConfigDialog(self.window, self.polygon_config)
        self.window.wait_window(dialog.dialog)
        if hasattr(dialog, 'config'):
            self.polygon_config = dialog.get_config()
    
    def _configure_point(self):
        """配置点参数"""
        dialog = PointConfigDialog(self.window, self.point_config)
        self.window.wait_window(dialog.dialog)
        if hasattr(dialog, 'config'):
            self.point_config = dialog.get_config()
    
    def _create_right_frame(self, main_frame):
        """创建右侧输出设置框架"""
        right_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="15", style='TLabelframe')
        right_frame.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")
        help_text = (             
        )
        help_label = ttk.Label(right_frame, text=help_text, foreground="#666", justify="left")
        help_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        # 图片名称输入
        ttk.Label(right_frame, text="图片名称:").grid(row=1, column=0, sticky="w", pady=6)
        self.image_name = ttk.Entry(right_frame, width=20)
        self.image_name.insert(0, "GMT output")
        self.image_name.grid(row=1, column=1, sticky="w", pady=6)
        self.image_name.bind("<FocusIn>", lambda e: self._show_help("图片名称：仅能输入英文、下划线和数字"))
        self.image_name.bind("<FocusOut>", self._clear_help)
        
        # 图片格式选择
        ttk.Label(right_frame, text="图片格式:").grid(row=2, column=0, sticky="w", pady=6)
        self.image_format = ttk.Combobox(right_frame, values=["png", "eps", "pdf"], width=17)
        self.image_format.set("png")
        self.image_format.grid(row=2, column=1, sticky="w", pady=6)
        self.image_format.bind("<FocusIn>", lambda e: self._show_help("图片格式：推荐导出PDF，可以用其他软件进一步美化"))
        self.image_format.bind("<FocusOut>", self._clear_help)

        # 配色选择
        ttk.Label(right_frame, text="配色模式:").grid(row=3, column=0, sticky="w", pady=6)
        self.cmap_var = tk.StringVar(value="gray")
        self.cmap_combo = ttk.Combobox(right_frame, values=GMTCPTS, textvariable=self.cmap_var, width=17)
        self.cmap_combo.set("gray")
        self.cmap_combo.grid(row=3, column=1, sticky="w", pady=6)
        self.cmap_combo.bind("<FocusIn>", lambda e: self._show_help("推荐用geo，更多配色模式可以在官方文档查看https://docs.gmt-china.org/latest/cpt/"))
        self.cmap_combo.bind("<FocusOut>", self._clear_help)

        # 分辨率选择
        ttk.Label(right_frame, text="分辨率:").grid(row=4, column=0, sticky="w", pady=6)
        self.resolution_var = tk.StringVar(value="02m")
        self.resolution_combo = ttk.Combobox(right_frame, values=RESOLUTIONS, textvariable=self.resolution_var, width=17)
        self.resolution_combo.set("02m")
        self.resolution_combo.grid(row=4, column=1, sticky="w", pady=6)
        self.resolution_combo.bind("<FocusIn>", lambda e: self._show_help("全球地形用30m、全国地形起伏用05m、3度X3度用30s、更小的区域用03s"))
        self.resolution_combo.bind("<FocusOut>", self._clear_help)
    
    def _create_region_frame(self, main_frame):
        """创建区域范围设置框架"""
        region_frame = ttk.LabelFrame(main_frame, text="区域范围设置", padding="15", style='TLabelframe')
        region_frame.grid(row=2, column=0, columnspan=2, padx=0, pady=(20, 0), sticky="ew")
        
        # 区域帮助文本
        region_help = (      )
        region_help_label = ttk.Label(region_frame, text=region_help, foreground="#666", justify="left")
        region_help_label.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
        
        ttk.Label(region_frame, text="经度范围 [最小经度, 最大经度]:").grid(row=1, column=0, columnspan=2, sticky="w", pady=6)
        self.lon_entries = [ttk.Entry(region_frame, width=7) for _ in range(2)]
        for i, entry in enumerate(self.lon_entries):
            entry.insert(0, ["118", "135"][i])
            entry.grid(row=1, column=i+2, padx=2)
            entry.bind("<FocusIn>", lambda e: self._show_help("经度范围：东经开始，0-360"))
            entry.bind("<FocusOut>", self._clear_help)
        
        ttk.Label(region_frame, text="纬度范围 [最小纬度度, 最大纬度]:").grid(row=2, column=0, columnspan=2, sticky="w", pady=6)
        self.lat_entries = [ttk.Entry(region_frame, width=7) for _ in range(2)]
        for i, entry in enumerate(self.lat_entries):
            entry.insert(0, ["38", "55"][i])
            entry.grid(row=2, column=i+2, padx=2)
            entry.bind("<FocusIn>", lambda e: self._show_help("纬度范围：南纬为负，北纬为正"))
            entry.bind("<FocusOut>", self._clear_help)
    
    def _create_button_frame(self, main_frame):
        """创建按钮框架"""
        button_frame = ttk.Frame(main_frame, style='TLabelframe')
        button_frame.grid(row=3, column=0, columnspan=2, pady=30)
        
        # 运行按钮
        self.run_button = ttk.Button(button_frame, text="运行", command=self._run, style='TButton')
        self.run_button.grid(row=0, column=0, padx=20, ipadx=20, ipady=5)
        
        # 退出按钮
        self.exit_button = ttk.Button(button_frame, text="退出", command=self.window.destroy, style='TButton')
        self.exit_button.grid(row=0, column=1, padx=20, ipadx=20, ipady=5)
    
    def _run(self):
        """运行按钮回调函数"""
        try:
            config = {
                "elevation": self.elevation_var.get(),
                "topography": self.topography_var.get(),
                "coast_line": self.coast_line_var.get(),
                "plot_polygons": self.plot_polygons_var.get(),
                "plot_points": self.plot_points_var.get(),
                "region": [float(entry.get()) for entry in self.lon_entries + self.lat_entries],
                "image_name": self.image_name.get(),
                "image_format": self.image_format.get(),
                "polygon_config": self.polygon_config,
                "point_config": self.point_config,
                "cmap": self.cmap_var.get(),
                "resolution": self.resolution_var.get()
            }
            
            if self.on_submit:
                self.on_submit(config)
                
        except ValueError as e:
            messagebox.showerror("错误", "请输入有效的数值")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")
    
    def run(self):
        """运行GUI程序"""
        self.window.mainloop()