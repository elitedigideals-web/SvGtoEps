from flask import Flask, request, send_file, render_template
import cairosvg
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return {'error': 'File නැත'}, 400
    
    file = request.files['file']
    if not file.filename.endswith('.svg'):
        return {'error': 'SVG file ඕනේ'}, 400
    
    width = int(request.form.get('width', 5000))
    height = int(request.form.get('height', 5000))
    
    svg_data = file.read()
    eps_data = cairosvg.svg2eps(
        bytestring=svg_data,
        output_width=width,
        output_height=height
    )
    
    out_name = file.filename.replace('.svg', '.eps')
    return send_file(
        io.BytesIO(eps_data),
        mimetype='application/postscript',
        as_attachment=True,
        download_name=out_name
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

@app.route('/manifest.json')
def manifest():
    return render_template('manifest.json'), 200, {'Content-Type': 'application/json'}

@app.route('/sw.js')
def sw():
    return render_template('sw.js'), 200, {'Content-Type': 'application/javascript'}
