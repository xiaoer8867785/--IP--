import re
from urllib.parse import urlparse, parse_qs, quote
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 60)
    print("                    VLESS节点生成器")
    print("=" * 60)
    print("\n作者: 科技共享")
    print("版本: 1.0.0\n")
    print("-" * 60)

def parse_vless_url(vless_url):
    try:
        raw = vless_url.replace('vless://', '')
        uuid = raw.split('@')[0]
        remaining = raw.split('@')[1]
        address_part = remaining.split('?')[0]
        params_part = remaining.split('?')[1] if '?' in remaining else ''
        ip = address_part.split(':')[0]
        port = address_part.split(':')[1].split('?')[0]
        name = remaining.split('#')[1] if '#' in remaining else ''
        params = params_part.split('#')[0] if '#' in params_part else params_part
        return {
            'uuid': uuid,
            'ip': ip,
            'port': port,
            'params': params,
            'name': name
        }
    except Exception as e:
        print("\n错误：节点格式不正确！请检查输入的节点URL。")
        return None

def generate_vless_urls(base_url, ips, ports, locations):
    components = parse_vless_url(base_url)
    if not components:
        return []
    
    generated_urls = []
    # 使用最小长度，确保一一对应
    min_length = min(len(ips), len(ports), len(locations))
    
    # 一一对应生成节点
    for i in range(min_length):
        new_url = f"vless://{components['uuid']}@{ips[i]}:{ports[i]}"
        if components['params']:
            new_url += f"?{components['params']}"
        # 在属地后面添加"YouTube科技共享"
        location_with_suffix = f"{locations[i]}-YouTube科技共享"
        new_url += f"#{quote(location_with_suffix)}"
        generated_urls.append(new_url)
    
    return generated_urls

def save_to_file(urls):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"vless_nodes_{timestamp}.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        return filename
    except Exception as e:
        print(f"\n错误：保存文件时出错 - {str(e)}")
        return None

def main():
    clear_screen()
    print_header()
    
    base_url = input("请输入基础VLESS节点URL：\n")
    
    print("\n请输入IP地址列表（每行一个，输入空行结束）：")
    ips = []
    while True:
        ip = input()
        if not ip:
            break
        ips.append(ip.strip())
    
    print("\n请输入端口列表（每行一个，输入空行结束）：")
    ports = []
    while True:
        port = input()
        if not port:
            break
        ports.append(port.strip())
    
    print("\n请输入属地/名称列表（每行一个，输入空行结束）：")
    locations = []
    while True:
        location = input()
        if not location:
            break
        locations.append(location.strip())
    
    if not ips or not ports or not locations:
        print("\n错误：IP、端口和属地/名称列表不能为空！")
        input("\n按回车键退出...")
        return
    
    print("\n正在生成节点...")
    new_urls = generate_vless_urls(base_url, ips, ports, locations)
    
    if new_urls:
        filename = save_to_file(new_urls)
        print(f"\n成功生成 {len(new_urls)} 个节点！")
        if filename:
            print(f"节点已保存到文件：{filename}")
        
        print("\n预览生成的节点：")
        print("-" * 60)
        for url in new_urls:
            print(url)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
