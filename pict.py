import base64
def handle_gif_to_py(picture_name):
    open_gif = open("%s.gif"%picture_name, 'rb')
    b64str = base64.b64encode(open_gif.read())
    open_gif.close()
    write_data = 'img = "%s"'% b64str.decode()
    f = open('%s.py' % picture_name, 'w+')
    f.write(write_data)
    f.close()
if __name__=='__main__':
    picture = ['waiting']
    for picture_position in picture:
        handle_gif_to_py(picture_position)