from flask import Flask, render_template_string
from captcha.image import ImageCaptcha
import io
import base64
import random
import string

app = Flask(__name__)

def generate_random_code(length=5):
    """生成隨機的驗證碼"""
    characters = string.ascii_letters + string.digits  # 包含字母和數字
    return ''.join(random.choices(characters, k=length))  # 隨機選擇5個字符

@app.route('/')
def index():
    # 生成隨機的驗證碼字符
    code = generate_random_code(5)

    # 使用captcha庫生成圖片
    image_captcha = ImageCaptcha()
    image = image_captcha.generate_image(code)
    
    # 將圖片保存到內存中
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # 將圖片數據轉換為 Base64 編碼
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    # 返回HTML頁面顯示圖片和答案
    html_content = f'''
        <html>
            <body>
                <h2>驗證碼圖片</h2>
                <img src="data:image/png;base64,{img_base64}" alt="captcha">
                <h3>解答: {code}</h3>
            </body>
        </html>
    '''
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
