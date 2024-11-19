import re
import json
from typing import List, Dict
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyperclip  # 用于复制到剪贴板

class NodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("节点生成器 v1.0.2 - By YouTubexiaoer886")
        self.root.geometry("800x800")
        self.generator = NodeGenerator()
        
        # 创建版本信息标签
        version_frame = ttk.Frame(self.root, padding="5")
        version_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Label(version_frame, 
                 text="节点生成器 v1.0.2\n作者：YouTubexiaoer886", 
                 justify=tk.CENTER).grid(row=0, column=0, pady=5)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建所有输入区域
        self.create_input_areas()
        
        # 创建按钮区域
        self.create_buttons()
        
        # 创建结果显示区域
        self.create_result_area()
        
        # 加载现有配置
        self.load_existing_config()
    
    def create_input_areas(self):
        """创建所有输入区域"""
        # 模板节点输入
        ttk.Label(self.main_frame, text="请输入模板节点：").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.template_input = scrolledtext.ScrolledText(self.main_frame, height=4, width=80, wrap=tk.WORD)
        self.template_input.grid(row=1, column=0, columnspan=2, pady=5)
        
        # IP输入
        ttk.Label(self.main_frame, text="IP地址（每行一个）：").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ip_input = scrolledtext.ScrolledText(self.main_frame, height=3, width=80, wrap=tk.WORD)
        self.ip_input.grid(row=3, column=0, columnspan=2, pady=5)
        
        # 端口输入
        ttk.Label(self.main_frame, text="端口（每行一个）：").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.port_input = scrolledtext.ScrolledText(self.main_frame, height=3, width=80, wrap=tk.WORD)
        self.port_input.grid(row=5, column=0, columnspan=2, pady=5)
        
        # 地区输入
        ttk.Label(self.main_frame, text="地区（每行一个）：").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.region_input = scrolledtext.ScrolledText(self.main_frame, height=3, width=80, wrap=tk.WORD)
        self.region_input.grid(row=7, column=0, columnspan=2, pady=5)

    def create_buttons(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        # 生成节点按钮
        self.generate_button = ttk.Button(button_frame, text="生成节点", command=self.generate_nodes)
        self.generate_button.grid(row=0, column=0, padx=5)
        
        # 复制节点按钮
        self.copy_button = ttk.Button(button_frame, text="复制节点", command=self.copy_nodes)
        self.copy_button.grid(row=0, column=1, padx=5)
        
        # 下载文件按钮
        self.save_button = ttk.Button(button_frame, text="下载文件", command=self.open_file_location)
        self.save_button.grid(row=0, column=2, padx=5)

    def create_result_area(self):
        """创建结果显示区域"""
        ttk.Label(self.main_frame, text="生成结果：").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.result_display = scrolledtext.ScrolledText(self.main_frame, height=10, width=80, wrap=tk.WORD)
        self.result_display.grid(row=10, column=0, columnspan=2, pady=5)

    def copy_nodes(self):
        """复制节点到剪贴板"""
        result_text = self.result_display.get(1.0, tk.END).strip()
        if result_text:
            pyperclip.copy(result_text)
            messagebox.showinfo("成功", "节点已复制到剪贴板！")
        else:
            messagebox.showwarning("警告", "没有可复制的节点！")

    def open_file_location(self):
        """打开文件所在位置"""
        if os.path.exists(self.generator.output_file):
            os.startfile(os.path.dirname(os.path.abspath(self.generator.output_file)))
        else:
            messagebox.showwarning("警告", "文件尚未生成！")

    def generate_nodes(self):
        """生成节点"""
        # 获取当前输入的配置
        config = {
            "ip_list": [ip.strip() for ip in self.ip_input.get(1.0, tk.END).strip().split("\n") if ip.strip()],
            "port_list": [port.strip() for port in self.port_input.get(1.0, tk.END).strip().split("\n") if port.strip()],
            "regions": [region.strip() for region in self.region_input.get(1.0, tk.END).strip().split("\n") if region.strip()]
        }
        
        # 检查是否有输入
        if not config["ip_list"] or not config["port_list"] or not config["regions"]:
            messagebox.showerror("错误", "请确保已输入IP、端口和地区！")
            return
        
        template = self.template_input.get(1.0, tk.END).strip()
        if not template:
            messagebox.showerror("错误", "请输入模板节点！")
            return
        
        self.generator.set_template(template)
        
        # 直接传递当前配置给 generate_nodes
        generated_nodes = self.generator.generate_nodes(config)  # 修改这里，传入配置
        self.generator.save_nodes(generated_nodes)
        
        # 显示结果
        result_text = f"已成功生成 {len(generated_nodes)} 个节点！\n"
        result_text += f"节点已保存到 {self.generator.output_file}\n\n"
        result_text += "生成的节点：\n" + "\n".join(generated_nodes)
        
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, result_text)
        
        messagebox.showinfo("成功", f"已生成 {len(generated_nodes)} 个节点！")

    def load_existing_config(self):
        """加载现有配置到输入框 - 现在保持为空"""
        pass  # 不执行任何操作，保持输入框为空

    def save_config(self):
        """保存配置到文件"""
        config = {
            "ip_list": [ip.strip() for ip in self.ip_input.get(1.0, tk.END).strip().split("\n") if ip.strip()],
            "port_list": [port.strip() for port in self.port_input.get(1.0, tk.END).strip().split("\n") if port.strip()],
            "regions": [region.strip() for region in self.region_input.get(1.0, tk.END).strip().split("\n") if region.strip()]
        }
        
        with open(self.generator.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        messagebox.showinfo("成功", "配置已保存！")

class NodeGenerator:
    def __init__(self):
        self.template_node = ""
        self.config_file = "node_config.json"
        self.output_file = "generated_nodes.txt"
        
    def load_config(self) -> Dict:
        """加载配置文件"""
        # 返回空配置
        return {
            "ip_list": [],
            "port_list": [],
            "regions": []
        }

    def set_template(self, node_string: str):
        """设置模板节点"""
        self.template_node = node_string

    def generate_nodes(self, config: Dict) -> List[str]:
        """生成新的节点列表"""
        generated_nodes = []
        
        # 获取最短长度，确保一一对应
        min_length = min(len(config["ip_list"]), 
                        len(config["port_list"]), 
                        len(config["regions"]))
        
        for i in range(min_length):
            ip = config["ip_list"][i]
            port = config["port_list"][i]
            region = config["regions"][i]
            
            # 分割节点字符串在 # 处
            base_part, name_part = self.template_node.split('#', 1) if '#' in self.template_node else (self.template_node, '')
            
            # 替换IP和端口
            new_node = re.sub(r'@.*?:', f'@{ip}:', base_part)
            new_node = re.sub(r':\d+\?', f':{port}?', new_node)
            
            # 添加新的节点名称（格式：地区 YouTubexiaoer886）
            new_node = f"{new_node}#{region} YouTubexiaoer886"
            
            generated_nodes.append(new_node)
        
        return generated_nodes

    def save_nodes(self, nodes: List[str]):
        """保存生成的节点到文件"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for node in nodes:
                f.write(node + '\n')

def main():
    root = tk.Tk()
    app = NodeGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
