from typing import Any
from ilc.runtime import il_runtime


class ToPython:
    def __init__(self, ast):
        self.ast = ast

    def generate(self) -> str:
        lines = []
        lines.append("from ilc.runtime import il_runtime")
        lines.append("")
        lines.append("def main():")
        for stmt in self.ast.statements:
            for l in self._stmt_to_lines(stmt):
                lines.append("    " + l)
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    main()")
        return "\n".join(lines)

    def _py(self, v: Any) -> str: # Python Literal
       if v is None:
           return "None"
    
       if isinstance(v, str):
           if v.isidentifier():
               return v
           return repr(v)
    
       if isinstance(v, bool):
           return "True" if v else "False"
    
       if isinstance(v, (int, float)):
           return str(v)
    
       if isinstance(v, (list, tuple)):
           inner = ", ".join(self._py(x) for x in v)
           if isinstance(v, tuple):
               return f"({inner}{',' if len(v)==1 else ''})"
           return f"[{inner}]"
    
       return repr(v)


    def _call(self, func_name: str, **kwargs) -> str: # Chamada para o IL_RUNTIME
        args = []
        for k, v in kwargs.items():
            if v is None:
                continue
            args.append(f"{k}={self._py(v)}")
        return f"il_runtime.{func_name}({', '.join(args)})"

    def _stmt_to_lines(self, node):
        t = node.type
        fn = getattr(self, f"_gen_{t}", None)
        if fn is None:
            return [self._gen_generic(node)]
        return fn(node)

    def _gen_generic(self, node):
        func = node.type
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', func)
        snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        kwargs = {k: getattr(node, k) for k in node.__dict__ if k != "type"}
        return self._call(snake, **kwargs)

    def _gen_Abrir(self, node):
        line = f"{node.id} = {self._call('abrir_imagem', path=node.path)}"
        return [line]

    def _gen_Salvar(self, node):
        return [self._call('salvar_imagem', img=node.id, path=node.path)]

    def _gen_Rotacionar(self, node):
        return [f"{node.dst} = {self._call('rotacionar', img=node.src, graus=node.graus)}"]

    def _gen_Redimensionar(self, node):
        if hasattr(node, "w") and hasattr(node, "h"):
            return [f"{node.dst} = {self._call('redimensionar', img=node.src, largura=node.w, altura=node.h)}"]
        else:
            return [f"{node.dst} = {self._call('redimensionar', img=node.src, fx=node.fx, fy=node.fy)}"]

    def _gen_Cortar(self, node):
        return [f"{node.dst} = {self._call('cortar', img=node.src, x=node.x, y=node.y, w=node.w, h=node.h)}"]

    def _gen_AplicarFiltro(self, node):
        if getattr(node, "raio", None) is None:
            return [f"{node.dst} = {self._call('aplicar_filtro', img=node.src, nome=node.filtro)}"]
        else:
            return [f"{node.dst} = {self._call('aplicar_filtro', img=node.src, nome=node.filtro, raio=node.raio)}"]

    def _gen_Desfocar(self, node):
        return [f"{node.dst} = {self._call('desfocar', img=node.src, k=node.k)}"]

    def _gen_Mediana(self, node):
        return [f"{node.dst} = {self._call('mediana', img=node.src, k=node.k)}"]

    def _gen_Bilateral(self, node):
        return [f"{node.dst} = {self._call('bilateral', img=node.src, d=node.d)}"]

    def _gen_RemoverRuido(self, node):
        return [f"{node.dst} = {self._call('remover_ruido', img=node.src, h=node.h)}"]

    def _gen_AjustarBrilhoContraste(self, node):
        return [f"{node.dst} = {self._call('ajustar_brilho_contraste', img=node.src, brilho=node.brilho, contraste=node.contraste)}"]

    def _gen_AjustarGamma(self, node):
        return [f"{node.dst} = {self._call('ajustar_gamma', img=node.src, gamma=node.gamma)}"]

    def _gen_Clahe(self, node):
        return [f"{node.dst} = {self._call('clahe', img=node.src, clipLimit=node.clipLimit, tileGridSize=node.tileGridSize)}"]

    def _gen_ConverterCanal(self, node):
        return [f"{node.dst} = {self._call('converter_canal', img=node.src, codigo=node.codigo)}"]

    def _gen_BgrToRgb(self, node):
        return [f"{node.dst} = {self._call('bgr_to_rgb', img=node.src)}"]

    def _gen_RgbToBgr(self, node):
        return [f"{node.dst} = {self._call('rgb_to_bgr', img=node.src)}"]

    def _gen_ConverterParaGray(self, node):
        return [f"{node.dst} = {self._call('converter_para_gray', img=node.src)}"]

    def _gen_DetectarBordas(self, node):
        return [f"{node.dst} = {self._call('detectar_bordas', img=node.src, metodo=node.metodo, threshold1=node.threshold1, threshold2=node.threshold2, apertureSize=node.apertureSize)}"]

    def _gen_DetectarContornos(self, node):
        return [f"{node.dst} = {self._call('detectar_contornos', img=node.src, min_area=node.min_area)}"]

    def _gen_DesenharContornos(self, node):
        return [f"{node.dst} = {self._call('desenhar_contornos', img=node.src, contours=node.contours, color=node.color, thickness=node.thickness)}"]

    def _gen_DetectarCirculos(self, node):
        return [f"{node.dst} = {self._call('detectar_circulos', img=node.src)}"]

    def _gen_DetectarRetangulos(self, node):
        return [f"{node.dst} = {self._call('detectar_retangulos', img=node.src)}"]

    def _gen_Morfologia(self, node):
        return [f"{node.dst} = {self._call('morfologia', img=node.src, operacao=node.operacao, ksize=node.ksize, iterations=node.iterations, shape=node.shape)}"]

    def _gen_Erodir(self, node):
        return [f"{node.dst} = {self._call('erodir', img=node.src, ksize=node.ksize)}"]

    def _gen_Dilatar(self, node):
        return [f"{node.dst} = {self._call('dilatar', img=node.src, ksize=node.ksize)}"]

    def _gen_AbrirMorf(self, node):
        return [f"{node.dst} = {self._call('abrir_morf', img=node.src, ksize=node.ksize)}"]

    def _gen_FecharMorf(self, node):
        return [f"{node.dst} = {self._call('fechar_morf', img=node.src, ksize=node.ksize)}"]

    def _gen_EqualizarHistograma(self, node):
        return [f"{node.dst} = {self._call('equalizar_histograma', img=node.src)}"]

    def _gen_EqualizarColor(self, node):
        return [f"{node.dst} = {self._call('equalizar_color', img=node.src)}"]

    def _gen_Histograma(self, node):
        return [f"{node.dst} = {self._call('histograma', img=node.src, channel=node.channel)}"]

    def _gen_EqualizarClahe(self, node):
        return [f"{node.dst} = {self._call('equalizar_clahe', img=node.src, clipLimit=node.clipLimit, tileGridSize=node.tileGridSize)}"]

    def _gen_Thresholding(self, node):
        return [f"{node.dst} = {self._call('thresholding', img=node.src, metodo=node.metodo, thresh=node.thresh, tipo=node.tipo)}"]

    def _gen_KMeansSegmentacao(self, node):
        return [f"{node.dst} = {self._call('kmeans_segmentacao', img=node.src, k=node.k)}"]

    def _gen_GrabcutRemoverFundo(self, node):
        return [f"{node.dst} = {self._call('grabcut_remover_fundo', img=node.src, rect=node.rect, iterCount=node.iterCount)}"]

    def _gen_Cartoonize(self, node):
        return [f"{node.dst} = {self._call('cartoonize', img=node.src, downscale=node.downscale, bilateral_iter=node.bilateral_iter, edge_thresh=node.edge_thresh)}"]

    def _gen_PencilSketch(self, node):
        return [f"{node.dst}_gray, {node.dst}_color = {self._call('pencil_sketch', img=node.src)}"]

    def _gen_OilPainting(self, node):
        return [f"{node.dst} = {self._call('oil_painting', img=node.src)}"]

    def _gen_DetectarFaces(self, node):
        return [f"{node.dst} = {self._call('detectar_faces', img=node.src)}"]

    def _gen_DesenharBBox(self, node):
        return [f"{node.dst} = {self._call('desenhar_bbox', img=node.src, bboxes=node.bboxes, color=node.color, thickness=node.thickness)}"]

    def _gen_AlphaBlend(self, node):
        return [f"{node.dst} = {self._call('alpha_blend', fg=node.fg, bg=node.bg, alpha=node.alpha)}"]

    def _gen_OverlayImage(self, node):
        return [f"{node.dst} = {self._call('overlay_image', base=node.base, overlay=node.overlay, x=node.x, y=node.y, alpha=node.alpha)}"]

    def _gen_OverlayText(self, node):
        return [f"{node.dst} = {self._call('overlay_text', img=node.src, text=node.text, pos=node.pos, font_scale=node.font_scale, color=node.color, thickness=node.thickness, bgcolor=node.bgcolor)}"]

    def _gen_ResizeMax(self, node):
        return [f"{node.dst} = {self._call('resize_max', img=node.src, max_size=node.max_size)}"]

    def _gen_EnsureColor(self, node):
        return [f"{node.dst} = {self._call('ensure_color', img=node.src)}"]

    def _gen_ToBytes(self, node):
        return [f"{node.dst} = {self._call('to_bytes', img=node.src, ext=node.ext)}"]

    def _gen_Remap(self, node):
        return [f"{node.dst} = {self._call('remap', img=node.src, map_x=node.map_x, map_y=node.map_y)}"]

    def _gen_Transladar(self, node):
        return [f"{node.dst} = {self._call('transladar', img=node.src, dx=node.dx, dy=node.dy)}"]

    def _gen_Espelhar(self, node):
        return [f"{node.dst} = {self._call('espelhar', img=node.src, eixo=node.eixo)}"]

    def _gen_WarpPerspectiva(self, node):
        return [f"{node.dst} = {self._call('warp_perspectiva', img=node.src, src_pts=node.src_pts, dst_pts=node.src_pts, dsize=node.dst if hasattr(node,'dsize') else None)}"]
