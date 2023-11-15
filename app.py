from flask import Flask, render_template, request
import torch
from PIL import Image
from io import BytesIO
from diffusers import AutoPipelineForImage2Image
import base64
import os
from diffusers.utils import load_image
import hex2text as hex2text
import img2banner as img2banner

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images/uploads/'
SAVED_FOLDER = 'static/images/saved/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pipeline = AutoPipelineForImage2Image.from_pretrained(
    "kandinsky-community/kandinsky-2-2-decoder", torch_dtype=torch.float16, use_safetensors=True
).to("cuda")
pipeline.enable_model_cpu_offload()
pipeline.enable_xformers_memory_efficient_attention()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/task1',methods=['POST'])
def task1():
    if len(request.form['image_url']) != 0:
        url = request.form['image_url']
        init_image = load_image(url)
    else:
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        init_image = Image.open(UPLOAD_FOLDER+ f.filename)

    hex_color = request.values.get("hex_code")
    text_color = hex2text.get_color_name(hex_color)
    prompt = request.values.get("promt")
    prompt =  text_color + " color, " + prompt
    
    image = pipeline(prompt, image=init_image, strength=0.4).images[0]
    image.save(SAVED_FOLDER + 'image.jpg')
    
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_tag = '<img src="data:image/png;base64,{}" alt="Processed Image">'.format(img_str)

    return render_template('task1.html', img_tag=img_tag)

@app.route('/task2', methods=['GET', 'POST'])
def task2():
    if request.method == 'POST':
        f2 = request.files['file2']
        f2.save(os.path.join(app.config['UPLOAD_FOLDER'], f2.filename))
        punchline = request.form.get('punch_line')
        button_text = request.form.get('button_text')
        button_color = request.form.get('hex_code2')
        output_path = SAVED_FOLDER+'output.png'
        
        img2banner.create_dynamic_ad_template(SAVED_FOLDER+'image.jpg', UPLOAD_FOLDER+ f2.filename, 
                                              button_color, punchline, button_text, output_path)
        
        image2= Image.open(output_path).convert('RGBA')
        
        buffered2 = BytesIO()
        image2.save(buffered2, format="PNG")
        img_str = base64.b64encode(buffered2.getvalue()).decode()
        img_tag2 = '<img src="data:image/png;base64,{}" alt="Processed Image">'.format(img_str)

        return render_template('task2.html',img_tag2 = img_tag2)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    