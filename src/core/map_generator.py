"""
地图生成器核心模块
提供地图生成的主要功能
"""
import os
import pygmt
import numpy as np
from src.utils.constants import DEFAULT_POLYGON, DEFAULT_POINT

class MapGenerator:
    """地图生成器类，负责处理地图的生成和保存"""
    
    def __init__(self):
        """初始化地图生成器"""
        self.fig = pygmt.Figure()
        self.polygon_config = DEFAULT_POLYGON.copy()
        self.point_config = DEFAULT_POINT.copy()
        
    def generate(self, config):
        """
        根据配置生成地图
        
        Args:
            config (dict): 包含地图生成所需的所有配置参数
                - elevation (bool): 是否添加高程数据
                - topography (bool): 是否添加光照增强效果
                - coast_line (bool): 是否重新绘制海岸线
                - plot_polygons (bool): 是否进行多边形投图
                - plot_points (bool): 是否进行投点
                - compass (bool): 是否显示指南针
                - region (list): 区域范围 [min_lon, max_lon, min_lat, max_lat]
                - image_name (str): 图片名称
                - image_format (str): 图片格式
        """
        self.fig = pygmt.Figure()  # 每次都新建
        self._process_elevation(config)
        self._process_coastline(config)
        self._process_polygons(config)
        self._process_points(config)
        self._process_compass(config)
        
        # 显示图像
        self.fig.show()
        
        # 保存图像
        self._save_image(config)
    
    def _process_elevation(self, config):
        """处理高程数据"""
        cmap = config.get("cmap", "gray")
        resolution = config.get("resolution", "05m")
        if config["elevation"]:
            grid = pygmt.datasets.load_earth_relief(
                resolution=resolution,
                region=config["region"]
            )
            
            if config["topography"]:
                grid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
                pygmt.makecpt(cmap=cmap)
                self.fig.grdimage(
                    grid=grid,
                    projection="M12c",
                    frame=["xa", "ya", f"+t{config['image_name']}"],
                    cmap=cmap,
                )
            else:
                self.fig.grdview(
                    grid=grid,
                    perspective=[180, 90],
                    cmap=cmap,

                    projection="J15c",
                    zsize="1.5c",
                    surftype="s",
                    plane="1000+ggrey",
                    frame=["xaf", "yaf",f"+t{config['image_name']}"]
                )
        else:
            self.fig.basemap(
                region=config["region"],
                projection="M15c",
                frame=["xa1", "ya1","a", f"+t{config['image_name']}"]
            )
    
    def _process_coastline(self, config):
        """处理海岸线"""
        if config["coast_line"]:
            self.fig.coast(
                water="lightblue@80",

                frame=["xa1", "ya1", f"+t{config['image_name']}"]
            )
    
    def _process_polygons(self, config):
        """处理多边形投图"""
        if config["plot_polygons"]:
            polygon_config = config.get("polygon_config") or {}
            points = polygon_config.get("points", [])
            if points:
                x = np.array([p["x"] for p in points])
                y = np.array([p["y"] for p in points])
                pen = f"{polygon_config.get('pen_width', '2p')},{polygon_config.get('pen_color', 'black')}"
                self.fig.plot(
                    x=x,
                    y=y,
                    pen=pen,
                    close=polygon_config.get("close", True)
                )
    
    def _process_points(self, config):
        """处理投点"""
        if config["plot_points"]:
            point_config = config.get("point_config") or {}
            if point_config:
                self.fig.plot(
                    x=point_config.get("x", 120.4033),
                    y=point_config.get("y", -21.3068),
                    style=point_config.get("style", "c0.1c"),
                    fill=point_config.get("fill", "red"),
                    pen=f"{point_config.get('pen_width', '1p')},{point_config.get('pen_color', 'black')}",
                    transparency=point_config.get("transparency", 30)
                )
    
    def _process_compass(self, config):
        """处理比例尺和指南针"""
        compass_config = config.get("compass_config", {})
        scale_config = config.get("scale_config", {})

        # 处理比例尺
        if config.get("scale", False) and scale_config and scale_config.get("map_scale"):
            self.fig.basemap(
                map_scale=scale_config.get("map_scale")
            )

        # 处理指南针
        if config.get("compass", False) and compass_config and compass_config.get("compass"):
            self.fig.basemap(
                compass=compass_config.get("compass")
            )
    
    def _save_image(self, config):
        """保存图像"""
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        output_path = os.path.join(output_dir, f"{config['image_name']}.{config['image_format']}")
        self.fig.savefig(output_path, dpi=600) 

    def _configure_scale(self):
        dialog = ScaleConfigDialog(self.window, self.scale_config)
        self.window.wait_window(dialog.dialog)
        if dialog.result:
            self.scale_config = dialog.result

    def _configure_compass(self):
        dialog = CompassConfigDialog(self.window, self.compass_config)
        self.window.wait_window(dialog.dialog)
        if dialog.result:
            self.compass_config = dialog.result 