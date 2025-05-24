import os
import sys
import tkinter as tk
from tkinter import messagebox

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.gui.config_gui import ConfigGUI
from src.core.map_generator import MapGenerator
from src.utils.constants import OUTPUT_DIR

def main():
    """主程序入口函数"""
    # 创建地图生成器实例
    map_generator = MapGenerator()
    
    def on_submit(config):
        """
        提交配置的回调函数
        
        Args:
            config (dict): 地图生成配置
        """
        try:
            map_generator.generate(config)
            # 显示成功消息
            messagebox.showinfo(
                "成功", 
                f"图像已成功保存到 {OUTPUT_DIR}/{config['image_name']}.{config['image_format']}"
            )
        except Exception as e:
            # 显示错误消息
            messagebox.showerror("错误", f"生成图像时发生错误：{str(e)}")
    
    # 创建并运行GUI
    app = ConfigGUI(on_submit=on_submit)
    app.run()

if __name__ == "__main__":
    main()