from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Kode ini adalah poin masuk (entry point) untuk aplikasi Flask.
# `create_app()` adalah fungsi yang digunakan untuk menciptakan instance aplikasi Flask dengan konfigurasi yang ditetapkan.