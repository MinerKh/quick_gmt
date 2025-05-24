"""
常量定义模块
定义程序中使用的常量
"""

# 窗口设置
WINDOW_TITLE = "GMT插件"
WINDOW_SIZE = "600x800"
WINDOW_BG_COLOR = "#f0f0f0"

# 字体设置
FONT_FAMILY = "微软雅黑"
TITLE_FONT = (FONT_FAMILY, 16, "bold")
NORMAL_FONT = (FONT_FAMILY, 10)

# 默认值
DEFAULT_IMAGE_NAME = "output"
DEFAULT_IMAGE_FORMAT = "png"
DEFAULT_REGION = {
    "min_lon": 118,
    "max_lon": 135,
    "min_lat": 38,
    "max_lat": 55
}

# 图片格式选项
IMAGE_FORMATS = ["png", "eps", "pdf"]

# 输出目录
OUTPUT_DIR = "output" 

# 多边形绘制默认参数
DEFAULT_POLYGON = {
    "points": [
        {"x": 124.18, "y": 43.05},
        {"x": 124.18, "y": 45.15},
        {"x": 127.05, "y": 45.15},
        {"x": 127.05, "y": 43.05}
    ],
    "pen_width": "2p",
    "pen_color": "red",
    "close": True
}

# 点绘制默认参数
DEFAULT_POINT = {
    "x": 125.289795,
    "y": 43.824175,
    "style": "c0.1c",
    "fill": "red",
    "pen_width": "1p",
    "pen_color": "red",
    "transparency": 30
}

# 颜色选项
COLOR_OPTIONS = [
    "black", "red", "blue", "green", "yellow", "purple", "orange", "brown", "gray",
    "white", "pink", "cyan", "magenta", "darkred", "darkblue", "darkgreen"
]

# 线条粗细选项
PEN_WIDTH_OPTIONS = ["0.5p", "1p", "2p", "3p", "4p", "5p"]

# GMT内置配色表选项
GMTCPTS = (
    'abyss', 'bathy', 'cool', 'copper', 'cubhelix',
    'dem1', 'dem2', 'dem3', 'dem4', 'drywet',
    'earth', 'elevation', 'etopo1', 'gebco', 'geo',
    'globe', 'gray', 'haxby', 'hot', 'ibcso',
    'jet', 'no_green', 'ocean', 'oleron','polar', 'rainbow',
    'red2green', 'relief', 'seafloor', 'sealand', 'seis',
    'split', 'terra', 'topo', 'turbo', 'viridis',
    'world', 'wysiwyg'
)

# 地形分辨率选项
RESOLUTIONS = (
    '01d', '30m', '20m', '15m', '10m', '06m', '05m', '04m', '03m', '02m', '01m',
    '30s', '15s', '03s', '01s'
)