from flask import Flask, render_template, request
from scraper import scrape_website

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        urls = request.form['urls'].split(',')  # Assuming URLs are comma-separated
        selector = request.form['selector']
        scraped_data = []
        errors = []

        for url in urls:
            url = url.strip()  # Remove leading/trailing whitespace
            try:
                data = scrape_website(url, selector)
                scraped_data.append((url, data))
            except Exception as e:
                errors.append((url, str(e)))

        return render_template('index1.html', data=scraped_data, errors=errors, selector=selector)

    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001)