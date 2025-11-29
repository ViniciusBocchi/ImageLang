from typing import Any, List, Tuple, Optional

class ASTNode:
    def __init__(self, type: str, **kwargs: Any):
        self.type = type
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        attrs = {k: v for k, v in self.__dict__.items() if k != 'type'}
        return f"ASTNode({self.type}, {attrs})"


class ParserError(Exception):
    pass


class TokenProxy:
    def __init__(self, t):
        self.type = t.type
        self.value = t.value
        self.line = t.line
        self.col = t.col

    def __repr__(self):
        return f"Token({self.type},{self.value})"


class Parser:
    def __init__(self, tokens: List):
        self.tokens = tokens
        self.i = 0
        self.cur = TokenProxy(tokens[0])

    def advance(self):
        self.i += 1
        if self.i < len(self.tokens):
            self.cur = TokenProxy(self.tokens[self.i])

    def eat(self, *expected):
        for e in expected:
            if self.cur.type == e or self.cur.value == e:
                tok = self.cur
                self.advance()
                return tok
        raise ParserError(f"Esperado {expected}, encontrado {self.cur}")

    def _peek_is(self, *expected):
        return any(self.cur.type == e or self.cur.value == e for e in expected)

    def _parse_ident(self):
        tok = self.eat('IDENT')
        return tok.value

    def _parse_string(self):
        tok = self.eat('STRING')
        return tok.value

    def _parse_number(self) -> float:
        tok = self.eat('NUMBER')
        v = tok.value
        return float(v) if ('.' in v) else int(v)

    def _parse_int(self) -> int:
        n = self._parse_number()
        return int(n)

    def _parse_optional_keyword_number(self, kw: str, default=None):
        if self._peek_is(kw.upper(), kw):
            self.eat(self.cur.type)
            return self._parse_number()
        return default

    def _parse_coord_pair(self) -> Tuple[int,int]:
        x = self._parse_int()
        self.eat('COMMA', ',')
        y = self._parse_int()
        return (x, y)

    def _parse_four_ints(self) -> Tuple[int,int,int,int]:
        a = self._parse_int(); self.eat('COMMA', ',')
        b = self._parse_int(); self.eat('COMMA', ',')
        c = self._parse_int(); self.eat('COMMA', ',')
        d = self._parse_int()
        return (a,b,c,d)

    def _parse_color(self) -> Tuple[int,int,int]:
        r = self._parse_int(); self.eat('COMMA', ',')
        g = self._parse_int(); self.eat('COMMA', ',')
        b = self._parse_int()
        return (r,g,b)

    def parse(self):
        stmts = []
        while self.cur.type != 'EOF':
            t = self.cur.type
            v = self.cur.value.lower() if isinstance(self.cur.value, str) else self.cur.value

            if t == 'ABRIR_IMAGEM' or v == 'abrir_imagem':
                stmts.append(self.parse_abrir())
            elif t == 'SALVAR_IMAGEM' or v == 'salvar_imagem':
                stmts.append(self.parse_salvar())
            elif t == 'ROTACIONAR' or v == 'rotacionar':
                stmts.append(self.parse_rotacionar())
            elif t == 'REDIMENSIONAR' or v == 'redimensionar':
                stmts.append(self.parse_redimensionar())
            elif t == 'CORTAR' or v == 'cortar':
                stmts.append(self.parse_cortar())
            elif t == 'APLICAR_FILTRO' or v == 'aplicar_filtro':
                stmts.append(self.parse_aplicar_filtro())
            elif t == 'ADICIONAR_TEXTO' or v == 'adicionar_texto' or v == 'overlay_text':
                stmts.append(self.parse_adicionar_texto())
            elif t == 'SOBREPOR' or v == 'sobrepor' or v == 'overlay_image':
                stmts.append(self.parse_sobrepor())
            elif t == 'TRANSLADAR' or v == 'transladar':
                stmts.append(self.parse_transladar())
            elif t == 'ESPELHAR' or v == 'espelhar':
                stmts.append(self.parse_espelhar())
            elif t == 'WARP_PERSPECTIVA' or v == 'warp_perspectiva':
                stmts.append(self.parse_warp_perspectiva())
            elif t == 'REMAP' or v == 'remap':
                stmts.append(self.parse_remap())
            elif t == 'DESFOCAR' or v == 'desfocar':
                stmts.append(self.parse_desfocar())
            elif t == 'MEDIANA' or v == 'mediana':
                stmts.append(self.parse_mediana())
            elif t == 'BILATERAL' or v == 'bilateral':
                stmts.append(self.parse_bilateral())
            elif t == 'REMOVER_RUIDO' or v == 'remover_ruido':
                stmts.append(self.parse_remover_ruido())
            elif t == 'AJUSTAR_BRILHO_CONTRASTE' or v == 'ajustar_brilho_contraste':
                stmts.append(self.parse_ajustar_brilho_contraste())
            elif t == 'AJUSTAR_GAMMA' or v == 'ajustar_gamma':
                stmts.append(self.parse_ajustar_gamma())
            elif t == 'CLAHE' or v == 'clahe':
                stmts.append(self.parse_clahe())
            elif t == 'CONVERTER_CANAL' or v == 'converter_canal':
                stmts.append(self.parse_converter_canal())
            elif v in ('bgr_to_rgb','rgb_to_bgr','converter_para_gray'):
                stmts.append(self.parse_simple_conversion())
            elif t == 'DETECTAR_BORDAS' or v == 'detectar_bordas':
                stmts.append(self.parse_detectar_bordas())
            elif t == 'DETECTAR_CONTORNOS' or v == 'detectar_contornos':
                stmts.append(self.parse_detectar_contornos())
            elif t == 'DESENHAR_CONTORNOS' or v == 'desenhar_contornos':
                stmts.append(self.parse_desenhar_contornos())
            elif t == 'DETECTAR_CIRCUlOS' or v == 'detectar_circulos' or v == 'detectar_circulos':
                stmts.append(self.parse_detectar_circulos())
            elif t == 'DETECTAR_RETANGULOS' or v == 'detectar_retangulos':
                stmts.append(self.parse_detectar_retangulos())
            elif t == 'MORFOLOGIA' or v == 'morfologia':
                stmts.append(self.parse_morfologia())
            elif v in ('erodir','dilatar','abrir_morf','fechar_morf'):
                stmts.append(self.parse_morfologia_shorthand())
            elif t == 'EQUALIZAR_HISTOGRAMA' or v == 'equalizar_histograma':
                stmts.append(self.parse_equalizar_histograma())
            elif t == 'EQUALIZAR_COLOR' or v == 'equalizar_color':
                stmts.append(self.parse_equalizar_color())
            elif t == 'HISTOGRAMA' or v == 'histograma':
                stmts.append(self.parse_histograma())
            elif t == 'EQUALIZAR_CLAHE' or v == 'equalizar_clahe':
                stmts.append(self.parse_equalizar_clahe())
            elif t == 'THRESHOLDING' or v == 'thresholding':
                stmts.append(self.parse_thresholding())
            elif t == 'KMEANS_SEGMENTACAO' or v == 'kmeans_segmentacao':
                stmts.append(self.parse_kmeans_segmentacao())
            elif t == 'GRABCUT_REMOVER_FUNDO' or v == 'grabcut_remover_fundo':
                stmts.append(self.parse_grabcut_remover_fundo())
            elif t == 'CARTOONIZE' or v == 'cartoonize':
                stmts.append(self.parse_cartoonize())
            elif t == 'PENCIL_SKETCH' or v == 'pencil_sketch':
                stmts.append(self.parse_pencil_sketch())
            elif t == 'OIL_PAINTING' or v == 'oil_painting':
                stmts.append(self.parse_oil_painting())
            elif t == 'DETECTAR_FACES' or v == 'detectar_faces':
                stmts.append(self.parse_detectar_faces())
            elif t == 'DESENHAR_BBOX' or v == 'desenhar_bbox':
                stmts.append(self.parse_desenhar_bbox())
            elif t == 'ALPHA_BLEND' or v == 'alpha_blend':
                stmts.append(self.parse_alpha_blend())
            elif t == 'OVERLAY_IMAGE' or v == 'overlay_image':
                stmts.append(self.parse_overlay_image())
            elif t == 'OVERLAY_TEXT' or v == 'overlay_text':
                stmts.append(self.parse_overlay_text())
            elif t == 'RESIZE_MAX' or v == 'resize_max':
                stmts.append(self.parse_resize_max())
            elif t == 'ENSURE_COLOR' or v == 'ensure_color':
                stmts.append(self.parse_ensure_color())
            elif t == 'TO_BYTES' or v == 'to_bytes':
                stmts.append(self.parse_to_bytes())
            else:
                raise ParserError(f"Comando desconhecido: {self.cur}")
        return ASTNode('Program', statements=stmts)

    def parse_abrir(self):
        self.eat('ABRIR_IMAGEM', 'abrir_imagem')
        path = self._parse_string()
        self.eat('COMO', 'como')
        idt = self._parse_ident()
        self.eat('SEMICOLON', ';')
        return ASTNode('Abrir', path=path, id=idt)

    def parse_salvar(self):
        self.eat('SALVAR_IMAGEM', 'salvar_imagem')
        idt = self._parse_ident()
        if self._peek_is('EM','em'):
            self.eat(self.cur.type)
        path = self._parse_string()
        self.eat('SEMICOLON',';')
        return ASTNode('Salvar', id=idt, path=path)

    def parse_rotacionar(self):
        self.eat('ROTACIONAR','rotacionar')
        src = self._parse_ident()
        if self._peek_is('POR','por'):
            self.eat(self.cur.type)
        graus = self._parse_number()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Rotacionar', src=src, graus=float(graus), dst=dst)

    def parse_redimensionar(self):
        self.eat('REDIMENSIONAR','redimensionar')
        src = self._parse_ident()
        if self._peek_is('PARA','para'):
            self.eat(self.cur.type)
            w_tok = self.eat('NUMBER'); 
            if self._peek_is('SYMBOL') and str(self.cur.value).lower()=='x':
                self.eat('SYMBOL')
            else:
                self.eat('SYMBOL','x','X')
            h_tok = self.eat('NUMBER')
            w = int(w_tok.value); h = int(h_tok.value)
            self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
            return ASTNode('Redimensionar', src=src, w=w, h=h, dst=dst)
        else:
            if self._peek_is('POR','por'):
                self.eat(self.cur.type)
            fx = self._parse_number()
            fy = self._parse_number()
            self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
            return ASTNode('Redimensionar', src=src, fx=float(fx), fy=float(fy), dst=dst)

    def parse_cortar(self):
        self.eat('CORTAR','cortar')
        src = self._parse_ident()
        if self._peek_is('PARA','para'):
            self.eat(self.cur.type)
        x = self._parse_int(); self.eat('COMMA',',')
        y = self._parse_int(); self.eat('COMMA',',')
        w = self._parse_int(); self.eat('COMMA',',')
        h = self._parse_int()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Cortar', src=src, x=int(x), y=int(y), w=int(w), h=int(h), dst=dst)

    def parse_aplicar_filtro(self):
        self.eat('APLICAR_FILTRO','aplicar_filtro')
        src = self._parse_ident()
        self.eat('FILTRO','filtro')
        nome = self._parse_string()
        raio = None
        if self._peek_is('RAIO','raio'):
            self.eat(self.cur.type)
            raio = int(self._parse_number())
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('AplicarFiltro', src=src, filtro=nome, raio=raio, dst=dst)

    def parse_adicionar_texto(self):
        self.eat('ADICIONAR_TEXTO','adicionar_texto','overlay_text')
        src = self._parse_ident()
        self.eat('TEXTO','texto')
        txt = self._parse_string()
        self.eat('EM','em')
        x = self._parse_int(); self.eat('COMMA',',')
        y = self._parse_int()
        self.eat('TAMANHO','tamanho')
        t = self._parse_number()
        self.eat('COR','cor')
        r = self._parse_int(); self.eat('COMMA',',')
        g = self._parse_int(); self.eat('COMMA',',')
        b = self._parse_int()
        self.eat('ESPESSURA','espessura')
        e = self._parse_int()
        self.eat('SEMICOLON',';')
        return ASTNode('AdicionarTexto', src=src, texto=txt, x=int(x), y=int(y),
                       tamanho=float(t), cor=(int(r),int(g),int(b)), espessura=int(e))

    def parse_sobrepor(self):
        self.eat('SOBREPOR','sobrepor','overlay_image')
        base = self._parse_ident()
        if self._peek_is('COM','com'):
            self.eat(self.cur.type)
        overlay = self._parse_ident()
        if self._peek_is('EM','em'):
            self.eat(self.cur.type)
        x = self._parse_int(); self.eat('COMMA',',')
        y = self._parse_int()
        alpha = 1.0
        if self._peek_is('ALPHA','alpha'):
            self.eat(self.cur.type)
            alpha = float(self._parse_number())
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Sobrepor', base=base, overlay=overlay, x=int(x), y=int(y), alpha=float(alpha), dst=dst)

    def parse_transladar(self):
        self.eat('TRANSLADAR','transladar')
        src = self._parse_ident()
        if self._peek_is('POR','por'):
            self.eat(self.cur.type)
        dx = self._parse_int(); self.eat('COMMA',',')
        dy = self._parse_int()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Transladar', src=src, dx=int(dx), dy=int(dy), dst=dst)

    def parse_espelhar(self):
        self.eat('ESPELHAR','espelhar')
        src = self._parse_ident()
        if self._peek_is('HORIZONTAL','horizontal'):
            eixo = 'horizontal'; self.eat(self.cur.type)
        elif self._peek_is('VERTICAL','vertical'):
            eixo = 'vertical'; self.eat(self.cur.type)
        elif self._peek_is('BOTH','both'):
            eixo = 'both'; self.eat(self.cur.type)
        else:
            raise ParserError("espelhar: esperado 'horizontal','vertical' ou 'both'")
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Espelhar', src=src, eixo=eixo, dst=dst)

    def parse_warp_perspectiva(self):
        self.eat('WARP_PERSPECTIVA','warp_perspectiva')
        src = self._parse_ident()
        if self._peek_is('PARA','para'):
            self.eat(self.cur.type)
        pts = []
        for i in range(4):
            xi = self._parse_int(); self.eat('COMMA',',')
            yi = self._parse_int()
            pts.append((int(xi), int(yi)))
            if i < 3:
                if self._peek_is('COMMA',','):
                    self.eat(self.cur.type)
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('WarpPerspectiva', src=src, src_pts=pts, dst=dst)

    def parse_remap(self):
        self.eat('REMAP','remap')
        src = self._parse_ident()
        mapx = self._parse_ident()
        mapy = self._parse_ident()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Remap', src=src, map_x=mapx, map_y=mapy, dst=dst)

    def parse_desfocar(self):
        self.eat('DESFOCAR','desfocar')
        src = self._parse_ident()
        k = self._parse_int()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Desfocar', src=src, k=int(k), dst=dst)

    def parse_mediana(self):
        self.eat('MEDIANA','mediana')
        src = self._parse_ident()
        k = self._parse_int()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Mediana', src=src, k=int(k), dst=dst)

    def parse_bilateral(self):
        self.eat('BILATERAL','bilateral')
        src = self._parse_ident()
        d = self._parse_int()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('Bilateral', src=src, d=int(d), dst=dst)

    def parse_remover_ruido(self):
        self.eat('REMOVER_RUIDO','remover_ruido')
        src = self._parse_ident()
        h = 10.0
        if self._peek_is('NUMBER'):
            h = self._parse_number()
        self.eat('COMO','como')
        dst = self._parse_ident()
        self.eat('SEMICOLON',';')
        return ASTNode('RemoverRuido', src=src, h=float(h), dst=dst)


    def parse_ajustar_brilho_contraste(self):
        self.eat('AJUSTAR_BRILHO_CONTRASTE','ajustar_brilho_contraste')
        src = self._parse_ident()
        brilho = 0.0; contraste = 1.0
        if self._peek_is('BRILHO','brilho'):
            self.eat(self.cur.type); brilho = float(self._parse_number())
        if self._peek_is('CONTRASTE','contraste'):
            self.eat(self.cur.type); contraste = float(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('AjustarBrilhoContraste', src=src, brilho=float(brilho), contraste=float(contraste), dst=dst)

    def parse_ajustar_gamma(self):
        self.eat('AJUSTAR_GAMMA')
        src = self._parse_ident()  
        self.eat('GAMMA')
        gamma = float(self._parse_number())
        self.eat('COMO')
        dst = self._parse_ident()
        self.eat('SEMICOLON')
    
        return ASTNode(
            type='AjustarGamma',
            src=src,
            gamma=gamma,
            dst=dst
        )


    def parse_clahe(self):
        self.eat('CLAHE','clahe')
        src = self._parse_ident()
        clip = 2.0; tile = (8,8)
        if self._peek_is('CLIP','clip'):
            self.eat(self.cur.type); clip = float(self._parse_number())
        if self._peek_is('TILE','tile'):
            self.eat(self.cur.type)
            a = self._parse_int(); self.eat('COMMA',','); b = self._parse_int()
            tile = (int(a),int(b))
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('Clahe', src=src, clipLimit=float(clip), tileGridSize=tile, dst=dst)


    def parse_converter_canal(self):
        self.eat('CONVERTER_CANAL','converter_canal')
        src = self._parse_ident()
        code = self._parse_string()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('ConverterCanal', src=src, codigo=code, dst=dst)

    def parse_simple_conversion(self):
        func = self.cur.value.lower()
        self.eat(self.cur.type)
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        mapping = {
            'bgr_to_rgb': 'BgrToRgb',
            'rgb_to_bgr': 'RgbToBgr',
            'converter_para_gray': 'ConverterParaGray'
        }
        return ASTNode(mapping.get(func, 'Converter'), src=src, dst=dst)


    def parse_detectar_bordas(self):
        self.eat('DETECTAR_BORDAS','detectar_bordas')
        src = self._parse_ident()
        metodo = 'canny'; th1=100; th2=200; aper=3
        if self._peek_is('METODO','metodo'):
            self.eat(self.cur.type); metodo = self._parse_string()
        if self._peek_is('THRESHOLD1','threshold1'):
            self.eat(self.cur.type); th1 = self._parse_number()
        if self._peek_is('THRESHOLD2','threshold2'):
            self.eat(self.cur.type); th2 = self._parse_number()
        if self._peek_is('APERTURE','aperture'):
            self.eat(self.cur.type); aper = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DetectarBordas', src=src, metodo=metodo, threshold1=float(th1), threshold2=float(th2), apertureSize=int(aper), dst=dst)

    def parse_detectar_contornos(self):
        self.eat('DETECTAR_CONTORNOS','detectar_contornos')
        src = self._parse_ident()
        min_area = 0
        if self._peek_is('MIN_AREA','min_area','min_area'):
            self.eat(self.cur.type); min_area = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DetectarContornos', src=src, min_area=int(min_area), dst=dst)

    def parse_desenhar_contornos(self):
        self.eat('DESENHAR_CONTORNOS','desenhar_contornos')
        src = self._parse_ident()
        contours = self._parse_ident()
        color = (0,255,0); thickness = 2
        if self._peek_is('COR','cor'):
            self.eat(self.cur.type); color = self._parse_color()
        if self._peek_is('ESPESSURA','espessura'):
            self.eat(self.cur.type); thickness = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DesenharContornos', src=src, contours=contours, color=color, thickness=int(thickness), dst=dst)

    def parse_detectar_circulos(self):
        self.eat('DETECTAR_CIRCUlOS','detectar_circulos','detectar_circulos')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DetectarCirculos', src=src, dst=dst)

    def parse_detectar_retangulos(self):
        self.eat('DETECTAR_RETANGULOS','detectar_retangulos')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DetectarRetangulos', src=src, dst=dst)


    def parse_morfologia(self):
        self.eat('MORFOLOGIA','morfologia')
        src = self._parse_ident()
        op = None; ksize = (3,3); iterations = 1; shape='rect'
        if self._peek_is('OPERACAO','operacao'):
            self.eat(self.cur.type)
            op = self._parse_string()
        if self._peek_is('KSIZE','ksize'):
            self.eat(self.cur.type)
            k = self._parse_int()
            ksize = (int(k), int(k))
        if self._peek_is('ITERATIONS','iterations','iter'):
            self.eat(self.cur.type)
            iterations = int(self._parse_number())
        if self._peek_is('SHAPE','shape'):
            self.eat(self.cur.type); shape = self._parse_string()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('Morfologia', src=src, operacao=op, ksize=ksize, iterations=int(iterations), shape=shape, dst=dst)

    def parse_morfologia_shorthand(self):
        func = self.cur.value.lower()
        self.eat(self.cur.type)
        src = self._parse_ident()
        ksize = (3,3)
        if self._peek_is('KSIZE','ksize'):
            self.eat(self.cur.type)
            k = self._parse_int()
            ksize = (int(k),int(k))
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        mapping = {'erodir':'Erodir','dilatar':'Dilatar','abrir_morf':'AbrirMorf','fechar_morf':'FecharMorf'}
        return ASTNode(mapping.get(func, 'MorfologiaShorthand'), src=src, ksize=ksize, dst=dst)

    def parse_equalizar_histograma(self):
        self.eat('EQUALIZAR_HISTOGRAMA','equalizar_histograma')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('EqualizarHistograma', src=src, dst=dst)

    def parse_equalizar_color(self):
        self.eat('EQUALIZAR_COLOR','equalizar_color')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('EqualizarColor', src=src, dst=dst)

    def parse_histograma(self):
        self.eat('HISTOGRAMA','histograma')
        src = self._parse_ident()
        channel = 0
        if self._peek_is('CANAL','canal'):
            self.eat(self.cur.type); channel = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('Histograma', src=src, channel=int(channel), dst=dst)

    def parse_equalizar_clahe(self):
        self.eat('EQUALIZAR_CLAHE','equalizar_clahe')
        src = self._parse_ident()
        clip = 2.0; tile=(8,8)
        if self._peek_is('CLIP','clip'):
            self.eat(self.cur.type); clip = float(self._parse_number())
        if self._peek_is('TILE','tile'):
            self.eat(self.cur.type); a=self._parse_int(); self.eat('COMMA',','); b=self._parse_int(); tile=(int(a),int(b))
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('EqualizarClahe', src=src, clipLimit=float(clip), tileGridSize=tile, dst=dst)

    def parse_thresholding(self):
        self.eat('THRESHOLDING','thresholding')
        src = self._parse_ident()
        metodo='otsu'; thresh=128; maxval=255; tipo='binary'
        if self._peek_is('METODO','metodo'):
            self.eat(self.cur.type); metodo = self._parse_string()
        if self._peek_is('THRESH','thresh'):
            self.eat(self.cur.type); thresh = int(self._parse_number())
        if self._peek_is('TIPO','tipo'):
            self.eat(self.cur.type); tipo = self._parse_string()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('Thresholding', src=src, metodo=metodo, thresh=int(thresh), tipo=tipo, dst=dst)

    def parse_kmeans_segmentacao(self):
        self.eat('KMEANS_SEGMENTACAO','kmeans_segmentacao')
        src = self._parse_ident()
        k = 2
        if self._peek_is('K','k'):
            self.eat(self.cur.type); k = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('KMeansSegmentacao', src=src, k=int(k), dst=dst)

    def parse_grabcut_remover_fundo(self):
        self.eat('GRABCUT_REMOVER_FUNDO','grabcut_remover_fundo')
        src = self._parse_ident()
        rect = (0,0,0,0)
        if self._peek_is('RECT','rect'):
            self.eat(self.cur.type); rect = self._parse_four_ints()
        iterCount = 5
        if self._peek_is('ITER','iter','iterCount'):
            self.eat(self.cur.type); iterCount = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('GrabcutRemoverFundo', src=src, rect=rect, iterCount=int(iterCount), dst=dst)

    def parse_cartoonize(self):
        self.eat('CARTOONIZE','cartoonize')
        src = self._parse_ident()
        downscale = 2; bilateral_iter = 5; edge_thresh = 100
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('Cartoonize', src=src, downscale=int(downscale), bilateral_iter=int(bilateral_iter), edge_thresh=int(edge_thresh), dst=dst)

    def parse_pencil_sketch(self):
        self.eat('PENCIL_SKETCH','pencil_sketch')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('PencilSketch', src=src, dst=dst)

    def parse_oil_painting(self):
        self.eat('OIL_PAINTING','oil_painting')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('OilPainting', src=src, dst=dst)

    def parse_detectar_faces(self):
        self.eat('DETECTAR_FACES','detectar_faces')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DetectarFaces', src=src, dst=dst)

    def parse_desenhar_bbox(self):
        self.eat('DESENHAR_BBOX','desenhar_bbox')
        src = self._parse_ident()
        bboxes = self._parse_ident()
        color = (0,255,0); thickness=2
        if self._peek_is('COR','cor'):
            self.eat(self.cur.type); color = self._parse_color()
        if self._peek_is('ESPESSURA','espessura'):
            self.eat(self.cur.type); thickness = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('DesenharBBox', src=src, bboxes=bboxes, color=color, thickness=int(thickness), dst=dst)

    def parse_alpha_blend(self):
        self.eat('ALPHA_BLEND','alpha_blend')
        fg = self._parse_ident()
        if self._peek_is('COM','com'):
            self.eat(self.cur.type)
        bg = self._parse_ident()
        alpha = 0.5
        if self._peek_is('ALPHA','alpha'):
            self.eat(self.cur.type); alpha = float(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('AlphaBlend', fg=fg, bg=bg, alpha=float(alpha), dst=dst)

    def parse_overlay_image(self):
        self.eat('OVERLAY_IMAGE','overlay_image')
        base = self._parse_ident()
        if self._peek_is('COM','com'):
            self.eat(self.cur.type)
        overlay = self._parse_ident()
        if self._peek_is('EM','em'):
            self.eat(self.cur.type)
        x = self._parse_int(); self.eat('COMMA',','); y = self._parse_int()
        alpha = 1.0
        if self._peek_is('ALPHA','alpha'):
            self.eat(self.cur.type); alpha = float(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('OverlayImage', base=base, overlay=overlay, x=int(x), y=int(y), alpha=float(alpha), dst=dst)

    def parse_overlay_text(self):
        self.eat('OVERLAY_TEXT','overlay_text','adicionar_texto')
        src = self._parse_ident()
        text = self._parse_string()
        self.eat('EM','em')
        x = self._parse_int(); self.eat('COMMA',','); y = self._parse_int()
        font_scale = 1.0; color=(255,255,255); thickness=2; bgcolor=None
        if self._peek_is('FONT','font'):
            self.eat(self.cur.type); font_scale = float(self._parse_number())
        if self._peek_is('COR','cor'):
            self.eat(self.cur.type); color = self._parse_color()
        if self._peek_is('ESPESSURA','espessura'):
            self.eat(self.cur.type); thickness = int(self._parse_number())
        if self._peek_is('BGCOLOR','bgcolor','bg'):
            self.eat(self.cur.type); bgcolor = self._parse_color()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('OverlayText', src=src, text=text, pos=(int(x),int(y)), font_scale=float(font_scale),
                       color=color, thickness=int(thickness), bgcolor=bgcolor, dst=dst)


    def parse_resize_max(self):
        self.eat('RESIZE_MAX','resize_max')
        src = self._parse_ident()
        max_size = int(self._parse_number())
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('ResizeMax', src=src, max_size=int(max_size), dst=dst)

    def parse_ensure_color(self):
        self.eat('ENSURE_COLOR','ensure_color')
        src = self._parse_ident()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('EnsureColor', src=src, dst=dst)

    def parse_to_bytes(self):
        self.eat('TO_BYTES','to_bytes')
        src = self._parse_ident()
        ext = '.png'
        if self._peek_is('EXT','ext'):
            self.eat(self.cur.type); ext = self._parse_string()
        self.eat('COMO','como'); dst = self._parse_ident(); self.eat('SEMICOLON',';')
        return ASTNode('ToBytes', src=src, ext=ext, dst=dst)


def parse(tokens):
    p = Parser(tokens)
    return p.parse()
