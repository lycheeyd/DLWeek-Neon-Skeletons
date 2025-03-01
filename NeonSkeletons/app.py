from flask import Flask, render_template, request, redirect, url_for, flash
import os
import kaggle

app = Flask(__name__)
app.secret_key = 'your_secret_key'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('submit.html', methods=['POST'])
def submit():
    if request.method == 'POST':
        file = request.files['formFileLg']
        if file:
            # Save the file locally
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Upload the file to Kaggle
            try:
                kaggle.api.dataset_create_new(
                    folder='uploads',
                    convert_to_csv=False,
                    dir_mode='tar',
                    public=True,
                    quiet=False
                )

                # Clean up the local file
                os.remove(file_path)

                flash('File uploaded successfully!', 'success')

            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'danger')

            return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)