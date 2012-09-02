#!/usr/bin/env python

import argparse
import struct

# Appendix A.
LABEL_EXTENSION_INTRODUCER = 0x21
LABEL_GRAPHIC_CONTROL_EXTENSION = 0xf9
LABEL_IMAGE_DESCRIPTOR = 0x2c
LABEL_TRAILER = 0x3b

def copy_data_sub_blocks(source, result):
    # 15. Data sub-blocks
    block_size = read_byte(source)
    while block_size != 0:
        data = source.read(block_size)
        result.write(chr(block_size))
        result.write(data)
        block_size = read_byte(source)

    # terminbal block
    result.write(chr(0))

def copy_image(source, result):
    # 20. Image descriptor
    (image_left_position,
     image_top_position,
     image_width,
     image_height,
     fields) = copy_struct('HHHHB', source, result)

    local_color_table_flag = fields & 0x80
    local_color_table_size = fields & 0x7

    # 21. Local color table
    if local_color_table_flag:
        local_color_table = source.read(6 << local_color_table_size)
        result.write(local_color_table)

    # 22. Table based image data
    lzw_code_size = source.read(1)
    result.write(lzw_code_size)
    copy_data_sub_blocks(source, result)

def unpack(format, file):
    size = struct.calcsize(format)
    data = file.read(size)
    if len(data) < size:
        raise Exception('Unexpected EOF')
    return struct.unpack(format, data)

def copy_struct(format, source, result):
     size = struct.calcsize(format)
     data = source.read(size)
     if len(data) < size:
          raise Exception('Unexpected EOF')
     result.write(data)
     return struct.unpack(format, data)

def read_byte(file):
    data = file.read(1)
    if not len(data):
        raise Exception('Unexpected EOF')
    return ord(data)

def copy_gif_header(source, result):
     # header
     (signature,
      version) = copy_struct('3s3s', source, result)
     if signature != 'GIF':
        raise Exception('Not a GIF stream')

     # 18. Logical screen descriptor
     (logical_screen_width,
      logical_screen_height,
      fields,
      background_color_index,
      pixel_aspect_ratio) = copy_struct('HHBBB', source, result)
     global_color_table_flag = fields & 0x80
     global_color_table_size = fields & 0x7

     # 19. Global color table
     if global_color_table_flag:
          global_color_table = source.read(6 << global_color_table_size) 
          result.write(global_color_table)

def add_wav_block(source, result, wav_block):
     block_added = False;

     copy_gif_header(source, result)

     block_type = read_byte(source)
     while block_type != LABEL_TRAILER:
          if block_type == LABEL_IMAGE_DESCRIPTOR:
               # write wav block before first image block
               if not block_added:
                    result.write(wav_block)
                    block_added = True
               #copy image block
               result.write(chr(block_type))
               copy_image(source, result)
          elif block_type == LABEL_EXTENSION_INTRODUCER:
               # copy extension blocks
               extension_block_type = read_byte(source)
               result.write(chr(block_type))
               result.write(chr(extension_block_type))
               copy_data_sub_blocks(source, result)

          block_type = read_byte(source)    

     # gif trailer
     result.write(chr(LABEL_TRAILER))     
     
     source.close()
     result.close()
    

def get_wav_block(file):
     # read wave file data
     (signature,
      size,
      format) = unpack('4sI4s', file)
     if signature != 'RIFF':
        raise Exception('Not a RIFF file')
     if format != 'WAVE':
        raise Exception('Not a WAVE file')
     data = file.read(size - 4)

     # block header
     wave_block_header = struct.pack('BBB8sBBB', 0x21, 0xff, 11, 'RIFFWAVE', 0, 0, 0)
     data_subblocks = [wave_block_header];

     # data subblocks
     for i in range(0, len(data) // 255):
          data_subblocks.append(chr(0xff))
          data_subblocks.append(data[i*255:(i + 1)*255])
     if (len(data) % 255) > 0:
          rest = len(data) % 255
          data_subblocks.append(chr(rest))
          data_subblocks.append(data[-rest:])          

     #bloack terminator
     data_subblocks.append(chr(0))

     return ''.join(data_subblocks) 

parser = argparse.ArgumentParser(description='Adding sound to gif')
parser.add_argument('source.gif', type=argparse.FileType('rb'))
parser.add_argument('source.wav', type=argparse.FileType('rb'))
parser.add_argument('result.gif', type=argparse.FileType('wb'))
args = vars(parser.parse_args())

wav_block = get_wav_block(args['source.wav'])
add_wav_block(args['source.gif'], args['result.gif'], wav_block)


