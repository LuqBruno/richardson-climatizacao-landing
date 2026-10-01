"""Codifica os PNGs de blender/renders/frames em vídeos para a web (FFmpeg embutido no Blender).

Uso: blender -b --factory-startup -P blender/encode_video.py
Saída em public/scene: richardson-instalacao-{1280,800}.{webm,mp4}
"""
import os

import bpy

ROOT = os.path.dirname(os.path.abspath(__file__))
FRAMES = os.path.join(ROOT, 'renders', 'frames')
OUT = os.path.join(os.path.dirname(ROOT), 'public', 'scene')
os.makedirs(OUT, exist_ok=True)

files = sorted(f for f in os.listdir(FRAMES) if f.endswith('.png'))
sc = bpy.context.scene
sc.render.fps = 30
sc.frame_start = 1
sc.frame_end = len(files)
sc.render.resolution_x, sc.render.resolution_y = 1280, 1024  # antes de criar a faixa
sc.sequence_editor_create()
seqs = sc.sequence_editor.strips if hasattr(sc.sequence_editor, 'strips') else sc.sequence_editor.sequences
strip = seqs.new_image('frames', os.path.join(FRAMES, files[0]), 1, 1)
for f in files[1:]:
    strip.elements.append(f)
strip.frame_final_duration = len(files)
sc.view_settings.view_transform = 'Standard'  # os PNGs já estão com AgX aplicado
sc.render.use_sequencer = True
try:
    sc.render.image_settings.media_type = 'VIDEO'
except AttributeError:
    pass
sc.render.image_settings.file_format = 'FFMPEG'

for width, height, crf in ((1280, 1024, 'HIGH'), (800, 640, 'MEDIUM')):
    sc.render.resolution_x, sc.render.resolution_y = width, height
    sc.render.resolution_percentage = 100
    # a escala da faixa não acompanha a resolução: ajusta para os quadros de 1280 px
    strip.transform.scale_x = strip.transform.scale_y = width / 1280
    strip.transform.offset_x = strip.transform.offset_y = 0
    for container, codec, ext in (('WEBM', 'WEBM', 'webm'), ('MPEG4', 'H264', 'mp4')):
        ff = sc.render.ffmpeg
        ff.format = container
        ff.codec = codec
        ff.constant_rate_factor = crf
        ff.ffmpeg_preset = 'BEST'
        ff.gopsize = 30
        ff.audio_codec = 'NONE'
        sc.render.filepath = os.path.join(OUT, f'richardson-instalacao-{width}.{ext}')
        sc.render.use_file_extension = False
        bpy.ops.render.render(animation=True)
        print('ok', sc.render.filepath, os.path.getsize(sc.render.filepath))
