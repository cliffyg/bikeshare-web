from bikeshare import app
debug = False
if __name__ == '__main__':
    if debug:
        app.run(host='127.0.0.1', port=8089, debug=True)
    else:
        app.run(host='0.0.0.0', port=8089, debug=False)

