# 结构效应分析工具（Streamlit 版）

本项目是一个可视化网页工具，用于拆解结构占比和退费率变化对整体退费率的影响。

## 使用步骤：

1. 登录 GitHub 创建一个新仓库，例如 `structure-app`
2. 上传本项目中的全部文件（包括 `.streamlit` 文件夹）
3. 打开 [Streamlit Cloud](https://streamlit.io/cloud)，用 GitHub 登录
4. 选择刚刚的仓库，指定主文件为 `analyze_app.py`
5. 点击 Deploy 即可上线网站！

## 访问形式

上线成功后你会获得一个公网网址，如：

```
https://your-app-name.streamlit.app
```

## 使用方法

上传一个包含如下字段顺序的 CSV 文件：

```
维度 | 基期在班人数 | 当期在班人数 | 基期退费人数 | 当期退费人数
```

系统将输出每类的结构效应、退费率效应及总影响，并支持导出为 Excel。

