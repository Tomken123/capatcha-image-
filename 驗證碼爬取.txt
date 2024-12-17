import os
import re
import base64
import requests
from bs4 import BeautifulSoup
import time  # 引入 time 模組來設置刷新間隔

# 設定參數
NUM_IMAGES = 500  # 要下載的圖片數量     
DOWNLOAD_DIR = "網路爬蟲project2"  # 保存圖片的目錄
TARGET_URL = "http://127.0.0.1:5000/"  # 目標網站的 URL
REFRESH_INTERVAL = 5  # 頁面刷新間隔，秒

# 確保圖片保存的目錄存在
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# 抓取並保存圖片，並自動刷新頁面
def fetch_and_save_images(url, total_images):
    """抓取頁面、保存圖片並自動刷新，直到達到總數"""
    image_count = 0  # 已下載的圖片數量

    while image_count < total_images:
        print(f"Fetching page {url}...")
        page_content = get_page(url)

        if page_content:
            print("Extracting and saving images...")
            # 解析 HTML 並提取圖片 URL 或 Base64 編碼
            image_count = save_images_from_page(page_content, total_images - image_count, image_count)
            print(f"{image_count} images saved so far.")
        else:
            print("Failed to fetch page content. Retrying...")

        if image_count < total_images:
            print(f"Refreshing the page in {REFRESH_INTERVAL} seconds...")
            time.sleep(REFRESH_INTERVAL)  # 等待刷新時間
            print(f"Refreshing page {url}...")

    print(f"Downloaded {image_count} images successfully!")

# 抓取網頁內容
def get_page(url):
    """用於抓取頁面內容"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# 提取並保存圖片
def save_images_from_page(html_content, num_images, image_count):
    """從 HTML 中提取圖片並保存到本地"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 先找出所有圖片標籤
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        # 提取圖片的 src 屬性
        img_src = img_tag.get('src', '')
        if not img_src:
            continue
        
        if img_src.startswith('data:image'):  # Base64 圖片
            # 保存 Base64 編碼的圖片
            image_count = save_base64_image(img_src, num_images, image_count)
        else:  # 外部圖片 URL
            # 保存圖片 URL
            image_count = save_image_from_url(img_src, num_images, image_count)

        if image_count >= num_images:
            break
    
    return image_count

# 保存 Base64 編碼圖片
def save_base64_image(base64_data, num_images, image_count):
    """保存 Base64 編碼的圖片"""
    try:
        # 解碼 Base64
        base64_data = base64_data.split(',', 1)[1]  # 去掉 "data:image/png;base64," 這部分
        image_data = base64.b64decode(base64_data)

        # 保存圖片到本地
        filename = os.path.join(DOWNLOAD_DIR, f"網路爬蟲project2_{image_count + 1}.png")
        with open(filename, 'wb') as f:
            f.write(image_data)

        print(f"Saved Base64 Image: {filename}")
        image_count += 1
    except Exception as e:
        print(f"Error saving Base64 image: {e}")

    return image_count

# 保存圖片 URL
def save_image_from_url(image_url, num_images, image_count):
    """下載並保存圖片 URL 指向的圖片"""
    try:
        # 下載圖片
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # 設定保存路徑
        filename = os.path.join(DOWNLOAD_DIR, f"網路爬蟲project2_{image_count + 1}.png")

        # 保存圖片到本地
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Saved Image from URL: {filename}")
        image_count += 1
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from URL {image_url}: {e}")

    return image_count

# 主程式
if __name__ == "__main__":
    print("Starting the automated image download process...")
    fetch_and_save_images(TARGET_URL, NUM_IMAGES)
    print("Process completed.")
