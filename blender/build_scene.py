"""Richardson Climatização — cena do hero (split de parede genérico, sem marca).

Uso (na pasta do projeto):
  blender -b -P blender/build_scene.py -- build            # gera blender/richardson-split.blend
  blender -b -P blender/build_scene.py -- still [frame]    # PNG 1600x1280 (padrão: último quadro)
  blender -b -P blender/build_scene.py -- anim             # PNGs 1280x1024 em blender/renders/frames
  blender -b -P blender/build_scene.py -- eevee [frame]    # prévia rasterizada (comparação realtime)
  blender -b -P blender/build_scene.py -- glb              # blender/export/richardson-split.glb

Unidades em metros. Parede no plano XZ (y = 0); o aparelho cresce para +y.
Materiais são procedurais (sem texturas externas).
"""
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['build']
MODE = ARGS[0]
FPS = 30
END = 150  # 5 s

# Dimensões plausíveis de um hi-wall residencial (aprox. 9.000–12.000 BTU/h)
W = 0.82
EDGE = 0.018

# ---------------------------------------------------------------- utilidades

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb(hexstr):
    h = hexstr.lstrip('#')
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, 1.0)


def fillet(points, radii, seg=10):
    """Polígono 2D (y, z) com cantos arredondados."""
    n = len(points)
    out = []
    for i, p in enumerate(points):
        p = Vector(p)
        r = radii[i]
        a = Vector(points[i - 1])
        b = Vector(points[(i + 1) % n])
        if r <= 0:
            out.append(p)
            continue
        u = (a - p).normalized()
        v = (b - p).normalized()
        theta = math.acos(max(-1, min(1, u.dot(v))))
        d = r / math.tan(theta / 2)
        t1 = p + u * d
        t2 = p + v * d
        bis = (u + v).normalized()
        c = p + bis * (r / math.sin(theta / 2))
        a1 = math.atan2(t1.y - c.y, t1.x - c.x)
        a2 = math.atan2(t2.y - c.y, t2.x - c.x)
        da = a2 - a1
        while da > math.pi:
            da -= 2 * math.pi
        while da < -math.pi:
            da += 2 * math.pi
        for k in range(seg + 1):
            ang = a1 + da * k / seg
            out.append(Vector((c.x + r * math.cos(ang), c.y + r * math.sin(ang))))
    return out


def resample(poly, step=0.003):
    """Subdivide arestas longas (perfil denso para seleção e normais)."""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        k = max(1, int((b - a).length / step))
        for j in range(k):
            out.append(a + (b - a) * (j / k))
    return out


def orientation(poly):
    area = 0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        area += a.x * b.y - b.x * a.y
    return 1 if area > 0 else -1


def normals(poly, closed=True):
    """Normais externas por vértice (média das arestas vizinhas)."""
    s = orientation(poly) if closed else -1
    res = []
    n = len(poly)
    for i in range(n):
        prev = poly[i - 1] if (closed or i > 0) else poly[i]
        nxt = poly[(i + 1) % n] if (closed or i < n - 1) else poly[i]
        t = (nxt - prev).normalized()
        res.append(Vector((t.y, -t.x)) * s)
    return res


def extrude_profile(name, poly, x0, x1, material=None, smooth=True):
    """Extruda um polígono (y, z) ao longo de x."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    ring0 = [bm.verts.new((x0, p.x, p.y)) for p in poly]
    ring1 = [bm.verts.new((x1, p.x, p.y)) for p in poly]
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((ring0[i], ring0[j], ring1[j], ring1[i]))
    bm.faces.new(list(reversed(ring0)))
    bm.faces.new(ring1)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    for f in me.polygons:
        f.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if material:
        me.materials.append(material)
    return ob


def box(name, size, loc, material=None, bevel=0.0, segs=3):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    bpy.context.scene.collection.objects.link(ob)
    if material:
        me.materials.append(material)
    if bevel:
        m = ob.modifiers.new('Bevel', 'BEVEL')
        m.width = bevel
        m.segments = segs
        m.harden_normals = True
        for f in me.polygons:
            f.use_smooth = True
    return ob


def empty(name, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    ob.location = loc
    ob.empty_display_size = 0.1
    bpy.context.scene.collection.objects.link(ob)
    return ob


def fcurves_of(idblock):
    ad = idblock.animation_data
    act = ad.action
    try:
        return list(act.fcurves)
    except AttributeError:
        from bpy_extras import anim_utils
        return list(anim_utils.action_get_channelbag_for_slot(act, ad.action_slot).fcurves)


def animate(owner, path, keys, interp='SINE', easing='EASE_IN_OUT', idblock=None, index=-1):
    """keys = [(frame, value), ...]; interpolação aplicada a todos os segmentos."""
    for frame, value in keys:
        if index >= 0:
            getattr(owner, path)[index] = value
        else:
            setattr(owner, path, value)
        owner.keyframe_insert(path, frame=frame, index=index)
    idb = idblock or owner
    frames = {k[0] for k in keys}
    for fc in fcurves_of(idb):
        if not fc.data_path.endswith(path):
            continue
        for kp in fc.keyframe_points:
            if int(round(kp.co.x)) in frames:
                kp.interpolation = interp
                kp.easing = easing


# ---------------------------------------------------------------- materiais

def principled(name, color, rough, metallic=0.0, coat=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = srgb(color)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Specular IOR Level'].default_value = spec
    if coat:
        b.inputs['Coat Weight'].default_value = coat
        b.inputs['Coat Roughness'].default_value = 0.12
    return m


def add_rough_variation(m, lo, hi, scale=38.0):
    """Variação sutil de rugosidade (plástico injetado)."""
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 6
    mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['To Min'].default_value = lo
    mr.inputs['To Max'].default_value = hi
    nt.links.new(noise.outputs['Fac'], mr.inputs['Value'])
    nt.links.new(mr.outputs['Result'], b.inputs['Roughness'])
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.025
    bump.inputs['Distance'].default_value = 0.0004
    n2 = nt.nodes.new('ShaderNodeTexNoise')
    n2.inputs['Scale'].default_value = 900
    nt.links.new(n2.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])


def wall_material():
    m = principled('Parede', '#b9c3cf', 0.88, spec=0.3)
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 260
    noise.inputs['Detail'].default_value = 8
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.06
    bump.inputs['Distance'].default_value = 0.0008
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    # Leve variação tonal para a parede não parecer um fundo digital chapado
    big = nt.nodes.new('ShaderNodeTexNoise')
    big.inputs['Scale'].default_value = 3.0
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = srgb('#b3becb')
    ramp.color_ramp.elements[1].color = srgb('#bec8d4')
    nt.links.new(big.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    return m


def airflow_material():
    m = bpy.data.materials.new('FluxoDeAr')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    mix = nt.nodes.new('ShaderNodeMixShader')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = srgb('#cfe9ff')
    em.inputs['Strength'].default_value = 2.1
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['UV'], sep.inputs[0])
    info = nt.nodes.new('ShaderNodeObjectInfo')

    head = nt.nodes.new('ShaderNodeValue')
    head.name = 'Head'
    head.outputs[0].default_value = 0.0
    master = nt.nodes.new('ShaderNodeValue')
    master.name = 'Master'
    master.outputs[0].default_value = 0.0

    def math(op, a, b=None, clamp=False):
        n = nt.nodes.new('ShaderNodeMath')
        n.operation = op
        n.use_clamp = clamp
        for i, v in enumerate((a, b)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                nt.links.new(v, n.inputs[i])
        return n.outputs[0]

    u, v = sep.outputs['X'], sep.outputs['Y']
    h = math('SUBTRACT', head.outputs[0], math('MULTIPLY', info.outputs['Random'], 0.18))
    # revelação: 1 atrás da "cabeça", 0 à frente
    reveal = math('SUBTRACT', 1.0, math('DIVIDE', math('SUBTRACT', u, h), 0.18), clamp=True)
    reveal = math('MINIMUM', reveal, 1.0)
    tail = math('POWER', math('SUBTRACT', 1.0, u), 1.7)
    start = nt.nodes.new('ShaderNodeMapRange')
    start.interpolation_type = 'SMOOTHSTEP'
    start.inputs['From Max'].default_value = 0.14
    nt.links.new(u, start.inputs['Value'])
    across = math('SUBTRACT', 1.0, math('POWER', math('ABSOLUTE', math('SUBTRACT', math('MULTIPLY', v, 2.0), 1.0)), 2.0))
    alpha = math('MULTIPLY', master.outputs[0], reveal)
    alpha = math('MULTIPLY', alpha, tail)
    alpha = math('MULTIPLY', alpha, start.outputs['Result'])
    alpha = math('MULTIPLY', alpha, across)
    alpha = math('MULTIPLY', alpha, 0.62, clamp=True)
    nt.links.new(alpha, mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs['Surface'])
    try:
        m.surface_render_method = 'BLENDED'
    except AttributeError:
        pass
    return m, head, master


# ---------------------------------------------------------------- cena

def build():
    reset()
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.frame_start = 1
    sc.frame_end = END

    body_mat = principled('Plastico_Corpo', '#f1f1ee', 0.34, spec=0.5)
    add_rough_variation(body_mat, 0.28, 0.40)
    panel_mat = principled('Plastico_Painel', '#f6f6f3', 0.16, coat=0.25)
    add_rough_variation(panel_mat, 0.12, 0.2, scale=22)
    vane_mat = principled('Plastico_Defletores', '#e4e5e2', 0.45)
    cavity_mat = principled('Saida_Interna', '#33373c', 0.6)
    display_mat = principled('Visor', '#0e1114', 0.06, coat=1.0)
    led_mat = principled('LED', '#0e1114', 0.2)
    led_b = led_mat.node_tree.nodes['Principled BSDF']
    led_b.inputs['Emission Color'].default_value = srgb('#7fd3ff')
    led_b.inputs['Emission Strength'].default_value = 0.0
    steel_mat = principled('Aco_Galvanizado', '#b9bec3', 0.38, metallic=1.0)
    add_rough_variation(steel_mat, 0.3, 0.48, scale=60)
    steel_b = steel_mat.node_tree.nodes['Principled BSDF']
    steel_b.inputs['Alpha'].default_value = 0.0
    try:
        steel_mat.surface_render_method = 'DITHERED'
    except AttributeError:
        pass
    wall_mat = wall_material()
    ceil_mat = principled('Teto', '#cfd6de', 0.9, spec=0.25)
    air_mat, air_head, air_master = airflow_material()

    # ---- parede e teto (ambiente)
    me = bpy.data.meshes.new('Parede')
    me.from_pydata([(-3, 0, -2.5), (3, 0, -2.5), (3, 0, 0.56), (-3, 0, 0.56)], [], [(0, 1, 2, 3)])
    wall = bpy.data.objects.new('Parede', me)
    sc.collection.objects.link(wall)
    me.materials.append(wall_mat)
    me = bpy.data.meshes.new('Teto')
    me.from_pydata([(-3, 0, 0.56), (3, 0, 0.56), (3, 4, 0.56), (-3, 4, 0.56)], [], [(0, 1, 2, 3)])
    ceil = bpy.data.objects.new('Teto', me)
    sc.collection.objects.link(ceil)
    ceil.visible_shadow = False  # o sol entra por uma janela lateral fora de quadro
    me.materials.append(ceil_mat)

    # ---- suporte de fixação (chapa galvanizada simplificada)
    plate = box('Suporte', (0.58, 0.0022, 0.185), (0, 0.0016, 0.152), steel_mat, bevel=0.0015, segs=2)
    cut = box('Suporte_Furos', (0.05, 0.02, 0.012), (-0.24, 0.0, 0.11))
    arr = cut.modifiers.new('X', 'ARRAY')
    arr.count = 7
    arr.use_relative_offset = False
    arr.use_constant_offset = True
    arr.constant_offset_displace = (0.08, 0, 0)
    arr2 = cut.modifiers.new('Z', 'ARRAY')
    arr2.count = 4
    arr2.use_relative_offset = False
    arr2.use_constant_offset = True
    arr2.constant_offset_displace = (0, 0, 0.034)
    cut.hide_render = True
    cut.hide_viewport = True
    bo = plate.modifiers.new('Furos', 'BOOLEAN')
    bo.object = cut
    bo.operation = 'DIFFERENCE'
    plate.modifiers.move(plate.modifiers.find('Furos'), 0)
    tabs = []
    for x in (-0.2, 0.2):
        t = box(f'Suporte_Gancho_{x:+.1f}', (0.05, 0.012, 0.004), (x, 0.007, 0.244), steel_mat, bevel=0.001, segs=2)
        tabs.append(t)
        t.parent = plate
        t.location = (x, 0.0055, 0.092)

    # ---- aparelho
    rig = empty('Aparelho')

    corners = [(0.0, 0.040), (0.0, 0.280), (0.150, 0.280), (0.207, 0.200),
               (0.196, 0.090), (0.120, 0.022), (0.030, 0.0)]
    radii = [0.004, 0.004, 0.034, 0.12, 0.026, 0.012, 0.02]
    prof = resample(fillet(corners, radii, seg=12))
    body = extrude_profile('Corpo', prof, -W / 2, W / 2, body_mat)
    bev = body.modifiers.new('Bevel', 'BEVEL')
    bev.width = EDGE
    bev.segments = 7
    bev.limit_method = 'ANGLE'
    bev.angle_limit = math.radians(40)
    bev.harden_normals = True
    body.data.materials.append(cavity_mat)

    # Saída de ar: cavidade na face inclinada inferior
    E, F = Vector(corners[4]), Vector(corners[5])
    slant = (F - E)
    sdir = slant.normalized()
    snorm = Vector((-sdir.y, sdir.x))  # aponta para fora/baixo
    if snorm.x < 0:  # x do vetor 2D = profundidade (y no mundo)
        snorm = -snorm
    e1 = E + slant * 0.16
    f1 = F - slant * 0.06
    depth = 0.032
    cav_poly = [e1 + snorm * 0.02, f1 + snorm * 0.02, f1 - snorm * depth, e1 - snorm * depth]
    cutter = extrude_profile('Saida_Corte', cav_poly, -W / 2 + 0.034, W / 2 - 0.034, cavity_mat, smooth=False)
    cutter.hide_render = True
    cutter.hide_viewport = True
    bo = body.modifiers.new('Saida', 'BOOLEAN')
    bo.object = cutter
    bo.operation = 'DIFFERENCE'
    try:
        bo.solver = 'EXACT'
        bo.material_mode = 'TRANSFER'
    except Exception:
        pass

    # Defletores verticais dentro da saída
    vin = 0.003
    vane_poly = [e1 - snorm * 0.009 + sdir * vin, f1 - snorm * 0.009 - sdir * vin,
                 f1 - snorm * (depth - 0.002) - sdir * vin, e1 - snorm * (depth - 0.002) + sdir * vin]
    vane = extrude_profile('Defletor', vane_poly, -W / 2 + 0.05, -W / 2 + 0.0512, vane_mat, smooth=False)
    va = vane.modifiers.new('Array', 'ARRAY')
    va.count = 36
    va.use_relative_offset = False
    va.use_constant_offset = True
    va.constant_offset_displace = ((W - 0.1) / 35, 0, 0)

    # Painel frontal: casca sobre a curva frontal, com junta visível
    nrm = normals(prof)
    front_idx = [i for i, p in enumerate(prof) if p.x > 0.13 and 0.104 < p.y < 0.268]
    outer = [prof[i] + nrm[i] * 0.0034 for i in front_idx]
    inner = [prof[i] - nrm[i] * 0.0015 for i in front_idx]
    panel = extrude_profile('Painel_Frontal', outer + list(reversed(inner)), -W / 2 + 0.011, W / 2 - 0.011, panel_mat)
    pb = panel.modifiers.new('Bevel', 'BEVEL')
    pb.width = 0.0016
    pb.segments = 3
    pb.limit_method = 'ANGLE'
    pb.angle_limit = math.radians(50)
    pb.harden_normals = True

    # Aleta (louver): cobre a saída; pivô na borda superior
    l0 = E + slant * 0.12
    l1 = F - slant * 0.03
    mid = (l0 + l1) / 2 + snorm * 0.004
    pivot_pt = l1 - slant * 0.18 + snorm * 0.003  # eixo próximo à borda traseira
    lp = []
    for t in [i / 10 for i in range(11)]:
        # curva quadrática l0 -> mid -> l1, relativa ao pivô
        q = (1 - t) ** 2 * l0 + 2 * (1 - t) * t * mid + t ** 2 * l1
        lp.append(q + snorm * 0.0035 - pivot_pt)
    ln = normals(lp, closed=False)
    lpoly = [p + n * 0.0013 for p, n in zip(lp, ln)] + [p - n * 0.0013 for p, n in reversed(list(zip(lp, ln)))]
    louver = extrude_profile('Aleta', lpoly, -W / 2 + 0.03, W / 2 - 0.03, panel_mat)
    lb = louver.modifiers.new('Bevel', 'BEVEL')
    lb.width = 0.0012
    lb.segments = 2
    lb.harden_normals = True
    pivot = empty('Aleta_Pivo', (0, pivot_pt.x, pivot_pt.y))
    louver.parent = pivot

    # Visor e LED (sem marca)
    def front_y(z):
        pts = sorted(outer, key=lambda p: p.y)
        for a, b in zip(pts, pts[1:]):
            if a.y <= z <= b.y:
                t = (z - a.y) / (b.y - a.y)
                return a.x + (b.x - a.x) * t
        return outer[0].x
    zd = 0.128
    display = box('Visor', (0.064, 0.004, 0.016), (0.255, front_y(zd) + 0.0008, zd), display_mat, bevel=0.0035, segs=4)
    led = box('LED', (0.004, 0.002, 0.004), (0.236, front_y(zd) + 0.0031, zd), led_mat, bevel=0.0012, segs=2)

    for ob in (body, vane, panel, pivot, display, led):
        ob.parent = rig

    # ---- fluxo de ar (fitas translúcidas)
    cam_loc = Vector((-0.52, 1.62, -0.30))
    air = []
    xs = [-0.29, -0.19, -0.095, 0.0, 0.095, 0.19, 0.29]
    for i, x0 in enumerate(xs):
        me = bpy.data.meshes.new(f'Fluxo_{i}')
        verts, faces, uvs = [], [], []
        N = 48
        for k in range(N + 1):
            t = k / N
            x = x0 * (1 + 0.35 * t)
            y = 0.17 + 0.62 * t
            z = 0.035 - 0.30 * t - 0.12 * t * t + 0.008 * math.sin(7 * t + i)
            p = Vector((x, y, z))
            t2 = min(1, t + 1 / N)
            q = Vector((x0 * (1 + 0.35 * t2), 0.17 + 0.62 * t2, 0.035 - 0.30 * t2 - 0.12 * t2 * t2 + 0.008 * math.sin(7 * t2 + i)))
            tan = (q - p).normalized() if k < N else tan
            side = tan.cross((cam_loc - p).normalized()).normalized()
            w = 0.010 * (1 + 2.2 * t)
            verts += [p - side * w, p + side * w]
            uvs += [(t, 0), (t, 1)]
            if k:
                a = 2 * (k - 1)
                faces.append((a, a + 1, a + 3, a + 2))
        me.from_pydata(verts, [], faces)
        uvl = me.uv_layers.new(name='UVMap')
        for poly in me.polygons:
            for li in poly.loop_indices:
                uvl.data[li].uv = uvs[me.loops[li].vertex_index]
        ob = bpy.data.objects.new(f'Fluxo_{i}', me)
        sc.collection.objects.link(ob)
        me.materials.append(air_mat)
        ob.parent = rig
        try:
            ob.visible_shadow = False
        except AttributeError:
            pass
        air.append(ob)

    # ---- iluminação
    world = bpy.data.worlds.new('Mundo')
    sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = srgb('#d9e2ee')
    bg.inputs['Strength'].default_value = 0.3

    def area(name, loc, target, size, size_y, energy, color):
        ld = bpy.data.lights.new(name, 'AREA')
        ld.shape = 'RECTANGLE'
        ld.size = size
        ld.size_y = size_y
        ld.energy = energy
        ld.color = color
        ob = bpy.data.objects.new(name, ld)
        ob.location = loc
        sc.collection.objects.link(ob)
        d = Vector(target) - Vector(loc)
        ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        return ob

    area('Luz_Principal', (-1.15, 1.25, 0.75), (0.05, 0.1, 0.12), 1.1, 0.7, 95, (1.0, 0.955, 0.9))
    area('Luz_Preenchimento', (1.6, 1.9, -0.4), (0.0, 0.1, 0.05), 2.2, 1.4, 38, (0.88, 0.93, 1.0))
    area('Luz_Recorte', (0.4, 0.55, 0.53), (0.0, 0.12, 0.25), 0.9, 0.2, 9, (1.0, 1.0, 1.0))

    # ---- câmera
    cd = bpy.data.cameras.new('Camera')
    cd.lens = 52
    cd.sensor_width = 36
    cam = bpy.data.objects.new('Camera', cd)
    cam.location = cam_loc
    sc.collection.objects.link(cam)
    tgt = empty('Alvo', (0.03, 0.08, 0.07))
    con = cam.constraints.new('TRACK_TO')
    con.target = tgt
    con.track_axis = 'TRACK_NEGATIVE_Z'
    con.up_axis = 'UP_Y'
    cd.dof.use_dof = False
    sc.camera = cam

    # ---- animação (30 fps, 150 quadros)
    # 1. suporte aparece
    animate(steel_b.inputs['Alpha'], 'default_value', [(1, 0.0), (16, 1.0)], 'SINE', 'EASE_OUT', idblock=steel_mat.node_tree)
    animate(plate, 'location', [(1, 0.018), (18, 0.0016)], 'CUBIC', 'EASE_OUT', index=1)
    # 2. aparelho se aproxima (vem de cima e da frente)
    animate(rig, 'location', [(12, 0.42), (60, 0.012)], 'CUBIC', 'EASE_OUT', index=1)
    animate(rig, 'location', [(12, 0.36), (60, 0.012), (74, 0.0)], 'CUBIC', 'EASE_OUT', index=2)
    animate(rig, 'location', [(12, 0.10), (60, 0.0)], 'CUBIC', 'EASE_OUT', index=0)
    animate(rig, 'rotation_euler', [(12, math.radians(-7)), (60, 0.0)], 'CUBIC', 'EASE_OUT', index=0)
    animate(rig, 'rotation_euler', [(12, math.radians(9)), (60, 0.0)], 'CUBIC', 'EASE_OUT', index=2)
    # 3. encaixe: últimos 12 mm de profundidade e descida nos ganchos
    animate(rig, 'location', [(60, 0.012), (74, 0.0)], 'CUBIC', 'EASE_IN_OUT', index=1)
    # 4. aleta abre
    pivot.rotation_euler = (0, 0, 0)
    animate(pivot, 'rotation_euler', [(80, 0.0), (104, math.radians(-42))], 'SINE', 'EASE_IN_OUT', index=0)
    # LED acende
    animate(led_b.inputs['Emission Strength'], 'default_value', [(84, 0.0), (96, 3.0)], 'SINE', 'EASE_IN_OUT', idblock=led_mat.node_tree)
    # 5. indicação de fluxo de ar
    animate(air_head.outputs[0], 'default_value', [(94, 0.0), (140, 1.25)], 'SINE', 'EASE_OUT', idblock=air_mat.node_tree)
    animate(air_master.outputs[0], 'default_value', [(94, 0.0), (120, 1.0)], 'SINE', 'EASE_OUT', idblock=air_mat.node_tree)

    sc.frame_set(END)

    # ---- render
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 96
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.02
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = 'OPTIX'
    except Exception:
        pass
    sc.cycles.max_bounces = 8
    sc.cycles.transparent_max_bounces = 16
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = 0.45
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, 'richardson-split.blend'))
    return sc


def use_gpu(sc):
    prefs = bpy.context.preferences.addons['cycles'].preferences
    for kind in ('OPTIX', 'CUDA'):
        try:
            prefs.compute_device_type = kind
            prefs.get_devices()
            ok = False
            for d in prefs.devices:
                d.use = d.type == kind
                ok = ok or d.use
            if ok:
                sc.cycles.device = 'GPU'
                print('GPU:', kind)
                return
        except Exception as e:
            print('GPU', kind, e)
    print('Renderizando na CPU')


def main():
    sc = build()
    if MODE == 'build':
        return
    use_gpu(sc)
    if MODE in ('still', 'eevee'):
        frame = int(ARGS[1]) if len(ARGS) > 1 else END
        sc.frame_set(frame)
        sc.render.resolution_x, sc.render.resolution_y = 1600, 1280
        if MODE == 'eevee':
            sc.render.engine = 'BLENDER_EEVEE'
            sc.render.filepath = os.path.join(ROOT, 'renders', f'eevee-{frame:03d}.png')
        else:
            sc.cycles.samples = int(ARGS[2]) if len(ARGS) > 2 else 256
            sc.render.filepath = os.path.join(ROOT, 'renders', f'still-{frame:03d}.png')
        bpy.ops.render.render(write_still=True)
    elif MODE == 'anim':
        sc.render.resolution_x, sc.render.resolution_y = 1280, 1024
        sc.cycles.samples = 64
        if len(ARGS) > 1:
            sc.frame_start, sc.frame_end = int(ARGS[1]), int(ARGS[2])
        sc.render.filepath = os.path.join(ROOT, 'renders', 'frames', 'f_')
        bpy.ops.render.render(animation=True)
    elif MODE == 'glb':
        for ob in list(sc.objects):
            if ob.name.startswith(('Caixilho', 'Fluxo_')) or ob.type == 'LIGHT':
                bpy.data.objects.remove(ob)
        bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, 'export', 'richardson-split.glb'),
                                  export_format='GLB', export_apply=True, export_animations=True,
                                  export_cameras=True, export_draco_mesh_compression_enable=True)


main()
