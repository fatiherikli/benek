# coding=utf-8
# 29 11 2018 MIT Licensed
# All the cats around the the world.
# 〄
PAGE_TEMPLATE = '''
<style>
  body {
    margin: 0;
    font-size: 3em;
  }

  div {
    float: left;
    transform: rotate(-293deg);
  }
</style>
%(content)s
'''

DIV_TEMPLATE = '<div style="%(attr)s: %(value)s">&#12292;</div>'

LINE_BREAK = '''
<div style="clear: both"></div>
'''

def model(r=255, g=255, b=255):
  return {
    'r': r,
    'g': g,
    'b': b,
  }

def invert(r=255, g=255, b=255):
  return {
    'r': 255 - r,
    'g': 255 - g,
    'b': 255 - b,
  }


def identity(color):
  return color

DEFAULT = model
INVERT = invert

def benek(color, modulator, printer):
  placeholdr = 0
  red = color['r'] / 255.0
  green = color['g'] / 255.0
  blue = color['b'] / 255.0

  hue, luminosity, saturation = modulator(red, green, blue)

  return printer(hue * 255, saturation * 100, luminosity * 100)

def as_hsl(h, s, l):
  MODULUS = '%'
  return 'hsl(%(h)s, %(s)s, %(l)s);' % {
    'h': h,
    's': str(s) + MODULUS,
    'l': str(l) + MODULUS,
  }

def render(model, modulator):
  return DIV_TEMPLATE % {
    'attr': 'color',
    'value': benek(model, modulator, as_hsl),
  }


def am_i_blind(modulator, args):
  renders = [
    render(
      model(
        r=channel + args.red,
        g=channel + args.green,
        b=channel + args.blue
      ),
      modulator
    ) for channel in range(255)
  ]

  return PAGE_TEMPLATE % {
    'content': '\n'.join(renders),
  }


if __name__ == '__main__':
  import argparse
  import colorsys

  parser = argparse.ArgumentParser()
  parser.add_argument('red', help="channel red", type=int)
  parser.add_argument('green', help="channel green", type=int)
  parser.add_argument('blue', help="channel blue", type=int)
  args = parser.parse_args()

  print(PAGE_TEMPLATE % {
    'content': am_i_blind(
      colorsys.rgb_to_hsv,
      args
    )
  })
