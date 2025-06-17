# Quick GMT - 地图快速绘制工具

Quick GMT 是一个基于 PyGMT 的地图工具，提供了简单易用的图形用户界面，帮助用户快速生成专业的图件。
选择添加高程数据的时候需要联网。  
如果有一定的编程基础，可以直接在cases里修改ipynb文件以快速出图。
如果对项目感兴趣了可以去系统学习gmt和pygmt以更好的绘图。  
[gmt官网](https://www.generic-mapping-tools.org/)  
[gmt中文手册](https://docs.gmt-china.org/latest/intro/)  
[pygmt官网](https://www.generic-mapping-tools.org/)  

## 功能特点

- 🎨 直观的图形用户界面
- 🖼️ 可自定义图像格式和分辨率
- 💾 自动保存生成的地图图像

## 系统要求
- GMT 6.5.0 [安装教程](https://docs.gmt-china.org/latest/install/)
- Python 3.8 或更高版本
- PyGMT 包
- [Pygmt其他依赖包](https://www.pygmt.org/latest/install.html)

## 安装说明

1. 克隆或下载本项目到本地
2. 安装依赖包
3. 尝试运行项目cases文件，如果能正确画图，则配置完毕


## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 在图形界面中：
   - 设置地图范围
   - 选择配色模式、分辨率等参数
   - 添加所需的地图元素
   - 点击运行按钮

3. 生成的地图将保存在 `output` 目录下  

4. 不添加光照增强效果时建议使用geo配色，使用光照增强效果时建议使用gray配色。

## 项目结构

```
quick_gmt/
├── main.py              # 主程序入口
├── src/                 # 源代码目录
│   ├── core/           # 核心功能模块
│   ├── gui/            # 图形界面模块
│   └── utils/          # 工具函数模块
├── output/             # 输出文件目录
└── cases/              # 示例案例目录
```

## 开发说明

- 使用 GMT 作为底层制图引擎
- 采用 Tkinter 构建图形界面
- 模块化设计，便于扩展和维护

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。