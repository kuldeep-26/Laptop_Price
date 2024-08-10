from flask import Flask,render_template,url_for,request

import joblib
model = joblib.load('./models/randomforest_model.lb')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route("/prediction", methods=['GET','POST'])
def prediction():
    if request.method == "POST":
        # Input values
        brand = request.form['brand']
        brands = ['Acer', 'Asus', 'Dell', 'HP', 'Lenovo', 'MSI', 'Avita']
        brand_flags = [1 if brand == b else 0 for b in brands]

        weight = request.form['weight']
        category = ['ThinNline' , 'Gaming']
        weight_flags = [1 if weight == cat else 0 for cat in category]

        p_brand = request.form['p_brand']
        gpus = ['Intel', 'M1']
        gpu_flags = [1 if p_brand == g else 0 for g in gpus]

        ram = request.form['ram']
        ram_systems = ['4 Gb','8 Gb','32 Gb']
        ram_flags = [1 if ram == r else 0 for r in ram_systems]

        p_name = request.form['p_name']
        cpus = ['Core i3', 'Core i5', 'Core i7', 'Core i9', 'Ryzen r3', 'Ryzen 5', 'Ryzen 7', 'Ryzen 9', 'M1', 'Pentium Quad']
        cpu_flags = [1 if p_name == c else 0 for c in cpus]

        opsys = request.form['opsys']
        os_systems = [ 'Mac', 'Windows']
        os_flags = [1 if opsys == os else 0 for os in os_systems]

        p_gen = request.form['p_gen']
        gen_systems = ['12th', '11th', '9th', '8th', '7th' , '4th', 'Not Available']
        gen_flags = [1 if p_gen == os else 0 for os in gen_systems]
            
        os_bit = request.form['os_bit']
        op_bit = 1 if os_bit == '64 Bit' else 0

        ssd = request.form['ssd']
        ssd_systems = ['128 GB','256 GB','512 GB','1024 GB','2048 GB','3072 GB']
        ssd_flags = [1 if ssd == s else 0 for s in ssd_systems]

        screen_type = request.form['screen_type']
        touchscreen = 1 if screen_type == 'Yes' else 0

        unseen_data = [op_bit,touchscreen] + brand_flags +  weight_flags + gpu_flags + ram_flags + cpu_flags + os_flags + gen_flags + ssd_flags

        prediction = model.predict([unseen_data])[0]
        prediction = round(prediction,2)
            
        return render_template('output.html', prediction=prediction,
                               op_bit = '64-bit' if op_bit == 1 else '32-bit',
                               touchscreen = 'Yes' if touchscreen == 1 else 'No',
                               brand_flags = brand,
                               weight_flags = weight,
                               gpu_flags = p_brand,
                               ram_flags = ram,
                               cpu_flags = p_name,
                               os_flags = opsys,
                               gen_flags = p_gen,
                               ssd_flags = ssd,
                               )  # Pass the prediction to the template

if __name__ == "__main__":
    app.run(debug=True)