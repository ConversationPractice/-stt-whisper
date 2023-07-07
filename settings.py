import os
import json
import traceback
import streamlit as st


# 获取配置文件路径
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
config_path = os.path.join(current_folder_path, "config.json") 

# 默认配置
default_config = {
    "model_name": "small",
}

# 模型列表 K: model_name, V: [parameters, required_vram, relative_speed]
models_dict = {
    "tiny": [39, 1, 32],
    "base": [74, 1, 16],
    "small": [244, 2, 6],
    "medium": [769, 5, 2],
    "large": [1550, 10, 1],
}

def settings_page():
    # 标题
    st.title(body="-STT-WHISPER Settings")
    
    # 检查配置文件是否存在
    if os.path.isfile(config_path) is not True:
        # 不存在则创建默认配置文件
        create_default_configs_file()
    
    # 读取配置文件
    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            config_dict = json.load(fp=fp)
    except json.JSONDecodeError:
        st.error(body="读取配置文件出现问题，将使用默认配置！")
        create_default_configs_file()
        config_dict = default_config
    
    # 展示配置界面
    # 选择模型
    models_name_list = list(models_dict.keys())
    model_name = st.selectbox(label="选择模型", 
                              options=models_name_list, 
                              index=models_name_list.index(config_dict["model_name"]))
    config_dict["model_name"] = model_name
    
    # 模型参数列表
    body = "|模型|参数量|需要的显存|相对速度|\n" \
           "|:------:|:----------:|:-------------:|:--------------:|\n"
    for key in models_dict.keys():
        value = models_dict[key]
        body += f"|  {key}  |    {value[0]} M    |     ~{value[1]} GB     |      ~{value[2]}x      |"
    st.markdown()

    # 确认按钮
    if st.button("保存更改"):
        try:    
            dump_config(config_dict)
        except Exception as e:
            st.error(f"保存失败, 请重试或寻求他人帮助\n" \
                     f"{repr(e)}\n" \
                     f"{traceback.format_exc()}")
        else:
            st.success("保存成功！")

def dump_config(config):
    with open(config_path, "w", encoding="utf-8") as fp:
        json.dump(obj=config, fp=fp)
        
def create_default_configs_file(): 
    dump_config(default_config)