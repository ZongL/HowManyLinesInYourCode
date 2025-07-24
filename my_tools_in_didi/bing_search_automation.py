import pyautogui
import time
import random
import subprocess
import os
import requests
import psutil
import pyperclip
from PIL import Image, ImageGrab

# pyautogui设置
pyautogui.FAILSAFE = True  # 鼠标移到屏幕左上角时停止程序
pyautogui.PAUSE = 0.5  # 操作间默认暂停时间

def check_network_connection():
    """检查网络连接"""
    try:
        response = requests.get('https://www.bing.com', timeout=10)
        return response.status_code == 200
    except:
        return False

def is_edge_running():
    """检查Edge浏览器是否正在运行"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'msedge.exe' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def open_edge_browser():
    """打开Edge浏览器"""
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    if is_edge_running():
        print("Edge浏览器已在运行")
        return True
    
    edge_path = None
    for path in edge_paths:
        if os.path.exists(path):
            edge_path = path
            break
    
    if not edge_path:
        print("找不到Edge浏览器安装路径")
        return False
    
    try:
        subprocess.Popen([edge_path])
        print("正在启动Edge浏览器...")
        time.sleep(3)  # 等待浏览器启动
        return True
    except Exception as e:
        print(f"启动Edge浏览器失败: {e}")
        return False

def wait_for_element(image_path, timeout=10, confidence=0.8):
    """等待屏幕上出现指定图像元素"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                return pyautogui.center(location)
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)
    return None

def click_element(image_path, timeout=10, confidence=0.8):
    """点击屏幕上的指定图像元素"""
    location = wait_for_element(image_path, timeout, confidence)
    if location:
        pyautogui.click(location)
        return True
    return False

def input_chinese_text(text):
    """使用剪贴板输入中文文本，避免输入法问题"""
    # 保存当前剪贴板内容
    try:
        old_clipboard = pyperclip.paste()
    except:
        old_clipboard = ""
    
    # 将文本复制到剪贴板
    pyperclip.copy(text)
    time.sleep(0.1)
    
    # 使用Ctrl+V粘贴
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # 恢复原剪贴板内容
    try:
        pyperclip.copy(old_clipboard)
    except:
        pass

def navigate_to_bing():
    """导航到Bing搜索页面"""
    print("导航到Bing...")
    
    # 点击地址栏 (使用Ctrl+L快捷键)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(1)
    
    # 输入Bing网址
    #human_like_typing("https://www.bing.com")
    pyautogui.write("https://www.bing.com")
    time.sleep(1)
    
    # 按回车
    pyautogui.press('enter')
    time.sleep(3)  # 等待页面加载

def search_on_bing(query):
    """在Bing上搜索指定查询"""
    print(f"搜索: {query}")
    
    # 点击搜索框 (尝试多种方式定位)
    search_clicked = False
    
    # # 方法1: 使用Tab键导航到搜索框
    # pyautogui.press('tab')
    # time.sleep(0.5)
    
    # # 方法2: 点击页面中央区域然后按Tab
    # if not search_clicked:
    #     screen_width, screen_height = pyautogui.size()
    #     pyautogui.click(screen_width // 2, screen_height // 3)
    #     time.sleep(0.5)
    #     pyautogui.press('tab')
    #     time.sleep(0.5)
    
    # # 清空搜索框
    # pyautogui.hotkey('ctrl', 'a')
    # time.sleep(0.3)
    
    # 输入搜索查询
    input_chinese_text(query)
    time.sleep(random.uniform(0.8, 2.0))
    
    # 按回车搜索
    pyautogui.press('enter')
    time.sleep(random.uniform(3, 5))  # 等待搜索结果加载

def human_like_scroll():
    """模拟人类滚动页面行为"""
    scroll_times = random.randint(2, 5)
    for _ in range(scroll_times):
        scroll_amount = random.randint(3, 8)
        pyautogui.scroll(-scroll_amount)  # 向下滚动
        time.sleep(random.uniform(0.5, 1.5))
    
    # 30%的概率回到页面顶部
    if random.random() < 0.3:
        pyautogui.press('home')
        time.sleep(random.uniform(1, 2))

def random_mouse_movement():
    """随机鼠标移动，模拟真实用户行为"""
    screen_width, screen_height = pyautogui.size()
    x = random.randint(100, screen_width - 100)
    y = random.randint(100, screen_height - 100)
    
    # 平滑移动鼠标
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))
    time.sleep(random.uniform(0.2, 0.8))

def click_random_search_result():
    """随机点击一个搜索结果"""
    try:
        # 滚动到页面中部查看更多结果
        pyautogui.scroll(-3)
        time.sleep(1)
        
        # 随机移动鼠标并可能点击
        if random.random() < 0.6:  # 60%的概率点击搜索结果
            screen_width, screen_height = pyautogui.size()
            
            # 在搜索结果区域随机点击
            x = random.randint(screen_width // 4, 3 * screen_width // 4)
            y = random.randint(screen_height // 3, 2 * screen_height // 3)
            
            pyautogui.click(x, y)
            print(f"点击了搜索结果区域: ({x}, {y})")
            
            # 在新页面停留
            time.sleep(random.uniform(3, 8))
            
            # 在新页面随机滚动
            human_like_scroll()
            
            # 返回搜索结果页
            pyautogui.hotkey('alt', 'left')  # 浏览器后退
            time.sleep(random.uniform(2, 4))
            return True
    except Exception as e:
        print(f"点击搜索结果时出错: {e}")
    return False

def perform_bing_searches(search_queries):
    """执行Bing搜索，模拟人类行为"""
    # 导航到Bing主页
    #navigate_to_bing()
    
    # 随机在主页停留
    time.sleep(random.uniform(2, 4))
    random_mouse_movement()
    
    for i, query in enumerate(search_queries, 1):
        try:
            print(f"\n开始第{i}次搜索: {query}")
            navigate_to_bing()
            # 执行搜索
            search_on_bing(query)
            
            # 随机滚动查看结果
            human_like_scroll()
            
            # 随机鼠标移动
            random_mouse_movement()
            
            # 随机点击搜索结果
            #click_random_search_result()
            
            # 两次搜索之间的随机间隔
            if i < len(search_queries):
                delay = random.uniform(3, 6)
                print(f"等待 {delay:.2f} 秒后进行下一次搜索...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"第{i}次搜索 '{query}' 时出错: {e}")
            # 尝试返回Bing主页
            try:
                navigate_to_bing()
            except:
                pass

def fetch_hot_topics(url):
    """从外部API获取热门话题"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Parse the JSON response
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    # 从外部API获取热门话题作为搜索关键词
    url = "https://api-hot.imsyy.top/douyin"
    
    print("正在获取热门话题...")
    hot_topics = fetch_hot_topics(url)
    
    if hot_topics:
        try:
            # Extract titles and put them into the questions array
            search_queries = [item['title'] for item in hot_topics['data']]
            print(f"获取到 {len(search_queries)} 个热门话题")
        except (KeyError, TypeError) as e:
            print(f"解析数据时出错: {e}")
            print("使用备用搜索关键词...")
            # 备用搜索关键词列表
            search_queries = [
                "Python编程教程",
                "机器学习算法",
                "Web开发框架",
                "数据结构与算法",
                "人工智能应用",
                "云计算技术",
                "网络安全防护",
                "移动应用开发",
                "数据库设计",
                "软件工程实践"
            ]
    else:
        print("无法获取热门话题数据，使用备用搜索关键词...")
        # 备用搜索关键词列表
        search_queries = [
            "Python编程教程",
            "机器学习算法",
            "Web开发框架",
            "数据结构与算法",
            "人工智能应用",
            "云计算技术",
            "网络安全防护",
            "移动应用开发",
            "数据库设计",
            "软件工程实践"
        ]
    
    try:
        # 首先检查网络连接
        print("检查网络连接...")
        if not check_network_connection():
            print("网络连接失败！请检查网络设置。")
            return
        print("网络连接正常")
        
        # 打开Edge浏览器
        print("正在打开Edge浏览器...")
        if not open_edge_browser():
            print("无法打开Edge浏览器！")
            return
        
        print("Edge浏览器已启动")
        print("程序将在5秒后开始自动搜索...")
        print("注意: 如需紧急停止程序，请将鼠标移动到屏幕左上角")
        time.sleep(5)
        
        # 执行搜索
        print("开始执行Bing搜索...")
        perform_bing_searches(search_queries)
        print("\n所有搜索完成！")
        
    except pyautogui.FailSafeException:
        print("\n程序被用户紧急停止（鼠标移到屏幕左上角）")
    except KeyboardInterrupt:
        print("\n程序被用户中断（Ctrl+C）")
    except Exception as e:
        print(f"程序执行出错: {e}")
        print("可能的解决方案:")
        print("1. 检查网络连接")
        print("2. 确保Edge浏览器已安装")
        print("3. 确保屏幕分辨率适合自动化操作")
        print("4. 检查是否有其他程序阻止鼠标键盘操作")

if __name__ == "__main__":
    main()
    
