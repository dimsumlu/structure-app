import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from io import BytesIO

st.set_page_config(page_title="结构效应分析工具", layout="centered")

st.title("📊 结构效应与退费率效应分析工具")
st.markdown("上传一份包含 **维度列 + 在班人数 + 退费人数** 的 CSV 文件，字段顺序需为：")
st.markdown("**维度、基期在班人数、当期在班人数、基期退费人数、当期退费人数**")
uploaded_file = st.file_uploader("📂 上传 CSV 文件", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"读取 CSV 文件失败：{e}")
        st.stop()

    cols = df.columns.tolist()
    if len(cols) < 5:
        st.error("CSV 至少应包含 5 列")
        st.stop()

    col_ch, col_in0, col_in1, col_ref0, col_ref1 = cols[:5]

    def strip_suffix(colname):
        return re.sub(r'(人数|数量)', '', colname)

    col_in0_ratio = strip_suffix(col_in0) + "占比"
    col_in1_ratio = strip_suffix(col_in1) + "占比"
    col_in0_rate = strip_suffix(col_ref0) + "率"
    col_in1_rate = strip_suffix(col_ref1) + "率"

    sum_in0 = df[col_in0].sum()
    sum_in1 = df[col_in1].sum()
    sum_ref0 = df[col_ref0].sum()
    sum_ref1 = df[col_ref1].sum()

    df[col_in0_ratio] = df[col_in0] / sum_in0
    df[col_in1_ratio] = df[col_in1] / sum_in1
    df[col_in0_rate] = df[col_ref0] / df[col_in0].replace(0, np.nan)
    df[col_in1_rate] = df[col_ref1] / df[col_in1].replace(0, np.nan)

    R0 = sum_ref0 / sum_in0
    df["结构效应(pp)"] = (df[col_in1_ratio] - df[col_in0_ratio]) * (df[col_in0_rate] - R0) * 100
    df["退费率效应(pp)"] = df[col_in1_ratio] * (df[col_in1_rate] - df[col_in0_rate]) * 100
    df["合计影响(pp)"] = df["结构效应(pp)"] + df["退费率效应(pp)"]

    for c in [col_in0_ratio, col_in1_ratio, col_in0_rate, col_in1_rate,
              "结构效应(pp)", "退费率效应(pp)", "合计影响(pp)"]:
        df[c] = df[c].round(4)

    summary = pd.DataFrame({
        col_ch: ["总计"],
        col_in0: [sum_in0],
        col_in1: [sum_in1],
        col_ref0: [sum_ref0],
        col_ref1: [sum_ref1],
        col_in0_ratio: [1.0000],
        col_in1_ratio: [1.0000],
        col_in0_rate: [round(sum_ref0 / sum_in0, 4)],
        col_in1_rate: [round(sum_ref1 / sum_in1, 4)],
        "结构效应(pp)": [round(df["结构效应(pp)"].sum(), 4)],
        "退费率效应(pp)": [round(df["退费率效应(pp)"].sum(), 4)],
        "合计影响(pp)": [round(df["合计影响(pp)"].sum(), 4)]
    })

    cols_out = cols + [
        col_in0_ratio, col_in1_ratio,
        col_in0_rate, col_in1_rate,
        "结构效应(pp)", "退费率效应(pp)", "合计影响(pp)"
    ]

    df_final = pd.concat([df[cols_out], summary[cols_out]], ignore_index=True)

    st.success("✅ 分析完成！下方可查看和下载结果：")
    st.dataframe(df_final)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_final.to_excel(writer, index=False, sheet_name="结果")

    st.download_button(
        label="📥 下载 Excel 文件",
        data=output.getvalue(),
        file_name="结构分析结果.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
