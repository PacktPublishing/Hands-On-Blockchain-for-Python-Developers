from os.path import isdir, exists
from os import mkdir
from tools.identicon import render_identicon


def render_avatar(code):
    code = int(code, 16)
    img_filename = 'images/%08x.png' % code
    if exists(img_filename):
        return img_filename
    img = render_identicon(code, 24)
    if not isdir('images'):
        mkdir('images')
    img.save(img_filename, 'PNG')
    return img_filename
