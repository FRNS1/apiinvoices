from app import create_app

app = create_app()

### IP público da api: 52.67.209.166
if __name__ == "__main__":
    app.run(host='172.31.43.25', port=5000, debug=True)