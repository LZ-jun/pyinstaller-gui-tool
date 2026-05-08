
# PyInstaller GUI Tool

一款基于PyInstaller的图形化Python打包工具，简化Python脚本转可执行文件（.exe）的流程，支持自定义图标、图片资源、打包选项等，无需手动编写命令行参数。


## 项目简介

PyInstaller是Python打包的常用工具，但需要通过命令行操作，对于新手不够友好。本项目提供了直观的图形化界面，将PyInstaller的核心功能可视化，支持一键打包，并自动处理Tcl/Tk等常见依赖问题，特别适合需要频繁打包Python脚本的开发者。


## 功能特点

- **图形化操作**：无需记忆复杂命令，通过界面选择文件和配置选项
- **多格式支持**：
  - 支持Python脚本（.py）打包
  - 支持多种图标格式（.ico/.png/.jpg/.svg），自动转换为.ico
  - 支持包含图片文件夹资源
- **灵活配置**：
  - 打包为单个文件或文件夹
  - 窗口模式（无控制台）或控制台模式
  - 清理临时文件选项
  - 高级选项：隐藏导入、排除模块
- **依赖处理**：自动检测并处理Tcl/Tk依赖，解决递归打包时的路径问题
- **实时日志**：显示打包过程日志，便于排查错误


## 安装说明

### 环境要求

- Python 3.7+
- 依赖库：
  ```bash
  pip install pyinstaller pillow tkinter
  ```

### 直接使用源码

1. 克隆仓库：
   ```bash
   git clone https://github.com/LZ-jun/pyinstaller-gui-tool.git
   cd pyinstaller-gui-tool
   ```

2. 运行程序：
   ```bash
   python CN.py
   ```
or
   ```bash
   python EN.py
   ```

### 打包为独立exe

如需将本工具自身打包为exe，可执行：
```bash
pyinstaller --onefile --windowed --add-data "C:\Python313\tcl\tcl8.6;_tk_data\tcl8.6" --add-data "C:\Python313\tcl\tk8.6;_tk_data\tk8.6" main.py
```
（替换`C:\Python313`为你的Python安装路径）


## 使用教程

1. **选择Python脚本**：点击"浏览..."选择需要打包的.py文件
2. **配置图标（可选）**：勾选"图标文件"并选择图片，工具会自动转换为.ico格式
3. **包含图片文件夹（可选）**：勾选后选择图片文件夹，会将图片打包到exe中
4. **设置输出**：自定义输出文件名和路径（默认当前目录）
5. **选择打包选项**：
   - 打包为单个文件（推荐）
   - 窗口模式（适合GUI程序）或控制台模式（适合命令行程序）
6. **高级选项（可选）**：设置隐藏导入的模块或需要排除的模块
7. **点击"开始打包"**：等待日志显示"打包成功"，即可在输出路径找到exe文件


## 截图展示

<img width="802" height="856" alt="Image" src="https://github.com/user-attachments/assets/9f1fa7c3-a81d-4316-a5f4-7cbc83a13e6f" />

*主界面展示_CN*

<img width="802" height="856" alt="Image" src="https://github.com/user-attachments/assets/09776e49-f8bd-48ba-a71b-e181269dc53d" />

*EN*


## 常见问题

### 1. 打包后exe运行提示"Tcl/Tk依赖缺失"

- 确保打包时选择了正确的原始Python解释器（递归打包时需手动选择）
- 检查Python安装目录下是否存在`tcl\tcl8.6`和`tcl\tk8.6`文件夹

### 2. 图标转换失败

- 确保安装了Pillow库：`pip install pillow`
- 复杂SVG文件可能转换失败，建议先手动转换为.png格式

### 3. 打包后exe体积过大

- 尝试使用"排除模块"功能，移除不必要的依赖
- 取消"打包为单个文件"选项，生成文件夹形式的exe

### 根据pyinstaller:
### https://github.com/pyinstaller/pyinstaller
