import cv2
import numpy as np
import os
from typing import Tuple, List, Optional, Union

__all__ = [
    # IO
    'abrir_imagem', 'salvar_imagem',

    # Transformações geométricas
    'rotacionar', 'redimensionar', 'cortar', 'transladar', 'espelhar',
    'warp_perspectiva', 'remap',

    # Filtros e denoise
    'aplicar_filtro', 'desfocar', 'mediana', 'bilateral', 'remover_ruido',

    # Ajustes de brilho/contraste/gamma
    'ajustar_brilho_contraste', 'ajustar_gamma', 'clahe',

    # Conversões de canal / cores
    'converter_canal', 'bgr_to_rgb', 'rgb_to_bgr', 'converter_para_gray',

    # Detecção e bordas
    'detectar_bordas', 'detectar_contornos', 'desenhar_contornos',
    'detectar_circulos', 'detectar_retangulos',

    # Morfologia
    'morfologia', 'erodir', 'dilatar', 'abrir_morf', 'fechar_morf',

    # Equalização / histograma
    'equalizar_histograma', 'equalizar_color', 'histograma', 'equalizar_clahe',

    # Segmentação
    'thresholding', 'kmeans_segmentacao', 'grabcut_remover_fundo',

    # Efeitos artísticos
    'cartoonize', 'pencil_sketch', 'oil_painting',

    # Faces / detecção
    'detectar_faces', 'desenhar_bbox',

    # Blending / overlay
    'alpha_blend', 'overlay_image', 'overlay_text',

    # Utilitários
    'resize_max', 'ensure_color', 'to_bytes'
]

def abrir_imagem(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagem não encontrada: {path}")
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise IOError(f"Falha ao abrir imagem: {path}")
    return img


def salvar_imagem(img: np.ndarray, path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    ok = cv2.imwrite(path, img)
    if not ok:
        raise IOError(f"Falha ao salvar imagem: {path}")


def rotacionar(img: np.ndarray, graus: float, escala: float = 1.0, center: Optional[Tuple[float,float]] = None,
               keep_size: bool = True, border_mode=cv2.BORDER_REFLECT) -> np.ndarray:
    (h, w) = img.shape[:2]
    if center is None:
        center = (w / 2.0, h / 2.0)
    M = cv2.getRotationMatrix2D(center, graus, escala)
    if keep_size:
        return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=border_mode)
    else:
        cos = abs(M[0, 0]); sin = abs(M[0, 1])
        nw = int((h * sin) + (w * cos))
        nh = int((h * cos) + (w * sin))
        M[0, 2] += (nw / 2) - center[0]
        M[1, 2] += (nh / 2) - center[1]
        return cv2.warpAffine(img, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=border_mode)


def redimensionar(img: np.ndarray, largura: int = None, altura: int = None, fx: float = None, fy: float = None,
                  interpolation=cv2.INTER_AREA) -> np.ndarray:
    if largura is not None and altura is not None:
        return cv2.resize(img, (largura, altura), interpolation=interpolation)
    if fx is not None or fy is not None:
        fx = 1.0 if fx is None else fx
        fy = 1.0 if fy is None else fy
        return cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=interpolation)
    raise ValueError("Forneça largura/altura ou fx/fy.")


def resize_max(img: np.ndarray, max_size: int) -> np.ndarray:
    h, w = img.shape[:2]
    if max(h, w) <= max_size:
        return img
    scale = max_size / float(max(h, w))
    return redimensionar(img, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)


def cortar(img: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    h_img, w_img = img.shape[:2]
    x = max(0, int(x)); y = max(0, int(y))
    x2 = min(w_img, x + int(w))
    y2 = min(h_img, y + int(h))
    return img[y:y2, x:x2].copy()


def transladar(img: np.ndarray, dx: int, dy: int, border_mode=cv2.BORDER_REFLECT) -> np.ndarray:
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    h, w = img.shape[:2]
    return cv2.warpAffine(img, M, (w, h), borderMode=border_mode)


def espelhar(img: np.ndarray, eixo: str = 'horizontal') -> np.ndarray:
    if eixo == 'horizontal':
        return cv2.flip(img, 1)
    if eixo == 'vertical':
        return cv2.flip(img, 0)
    if eixo == 'both':
        return cv2.flip(img, -1)
    raise ValueError("eixo deve ser 'horizontal', 'vertical' ou 'both'.")


def warp_perspectiva(img: np.ndarray, src_pts: np.ndarray, dst_pts: np.ndarray, dsize: Tuple[int,int]) -> np.ndarray:
    M = cv2.getPerspectiveTransform(np.float32(src_pts), np.float32(dst_pts))
    return cv2.warpPerspective(img, M, dsize, flags=cv2.INTER_LINEAR)


def remap(img: np.ndarray, map_x: np.ndarray, map_y: np.ndarray, interpolation=cv2.INTER_LINEAR) -> np.ndarray:
    return cv2.remap(img, map_x, map_y, interpolation)


def aplicar_filtro(img: np.ndarray, nome: str, raio: int = 3, **kwargs) -> np.ndarray:
    nome = nome.lower()
    if 'gauss' in nome or 'gaussiano' in nome:
        k = int(raio) if raio and raio>0 else 3
        if k % 2 == 0: k += 1
        sigmaX = kwargs.get('sigmaX', 0)
        return cv2.GaussianBlur(img, (k, k), sigmaX)
    if 'median' in nome or 'mediana' in nome:
        k = int(raio) if raio and raio>0 else 3
        if k % 2 == 0: k += 1
        return cv2.medianBlur(img, k)
    if 'bilateral' in nome:
        d = kwargs.get('d', int(raio))
        sigmaColor = kwargs.get('sigmaColor', 75)
        sigmaSpace = kwargs.get('sigmaSpace', 75)
        return cv2.bilateralFilter(img, d if d>0 else 9, sigmaColor, sigmaSpace)
    if 'laplacian' in nome:
        gray = converter_para_gray(img)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap = cv2.convertScaleAbs(lap)
        return cv2.cvtColor(lap, cv2.COLOR_GRAY2BGR) if img.ndim==3 else lap
    if 'sobel' in nome:
        gray = converter_para_gray(img)
        ksize = kwargs.get('ksize', 3)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        mag = cv2.magnitude(sx, sy)
        mag = cv2.convertScaleAbs(mag)
        return cv2.cvtColor(mag, cv2.COLOR_GRAY2BGR) if img.ndim==3 else mag
    if 'sharpen' in nome or 'unsharp' in nome:
        blur = cv2.GaussianBlur(img, (0,0), float(kwargs.get('sigma',1.0)))
        amount = float(kwargs.get('amount', 1.0))
        res = cv2.addWeighted(img, 1 + amount, blur, -amount, 0)
        return np.clip(res, 0, 255).astype('uint8')
    if 'emboss' in nome:
        kernel = np.array([[ -2, -1, 0],
                           [ -1,  1, 1],
                           [  0,  1, 2]])
        embossed = cv2.filter2D(img, -1, kernel) + 128
        return np.clip(embossed, 0, 255).astype('uint8')
    return img


def desfocar(img: np.ndarray, k: int = 5):
    if k % 2 == 0: k += 1
    return cv2.GaussianBlur(img, (k, k), 0)


def mediana(img: np.ndarray, k: int = 3):
    if k % 2 == 0: k += 1
    return cv2.medianBlur(img, k)


def bilateral(img: np.ndarray, d: int = 9, sigmaColor: int = 75, sigmaSpace: int = 75):
    return cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)


def remover_ruido(img: np.ndarray, h: float = 10.0, templateWindowSize: int = 7, searchWindowSize: int = 21):
    if img.ndim == 3 and img.shape[2] == 3:
        return cv2.fastNlMeansDenoisingColored(img, None, h, h, templateWindowSize, searchWindowSize)
    else:
        return cv2.fastNlMeansDenoising(img, None, h, templateWindowSize, searchWindowSize)


def ajustar_brilho_contraste(img: np.ndarray, brilho: float = 0.0, contraste: float = 1.0) -> np.ndarray:
    img_float = img.astype('float32')
    img_float = img_float * float(contraste) + float(brilho)
    img_float = np.clip(img_float, 0, 255)
    return img_float.astype('uint8')


def ajustar_gamma(img: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    if gamma <= 0:
        raise ValueError("gamma deve ser > 0")
    inv = 1.0 / gamma
    table = (np.arange(256) / 255.0) ** inv * 255.0
    table = np.clip(table, 0, 255).astype('uint8')
    return cv2.LUT(img, table)


def clahe(img: np.ndarray, clipLimit: float = 2.0, tileGridSize: Tuple[int,int] = (8,8)) -> np.ndarray:
    if img.ndim == 3 and img.shape[2] == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        return clahe.apply(img)


def equalizar_clahe(img: np.ndarray, clipLimit: float = 2.0, tileGridSize: Tuple[int,int] = (8,8)):
    return clahe(img, clipLimit=clipLimit, tileGridSize=tileGridSize)


def converter_canal(img: np.ndarray, codigo: str) -> np.ndarray:
    code = getattr(cv2, 'COLOR_' + codigo, None)
    if code is None:
        raise ValueError(f'Código de conversão desconhecido: {codigo}')
    return cv2.cvtColor(img, code)


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def converter_para_gray(img: np.ndarray) -> np.ndarray:
    if img.ndim == 2:
        return img
    if img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def ensure_color(img: np.ndarray) -> np.ndarray:
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img


def detectar_bordas(img: np.ndarray, metodo: str = 'canny', threshold1: float = 100.0,
                    threshold2: float = 200.0, apertureSize: int = 3) -> np.ndarray:
    gray = converter_para_gray(img)
    metodo = metodo.lower()
    if metodo == 'canny':
        edges = cv2.Canny(gray, int(threshold1), int(threshold2), apertureSize=apertureSize)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    if metodo == 'laplacian':
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap = cv2.convertScaleAbs(lap)
        return cv2.cvtColor(lap, cv2.COLOR_GRAY2BGR)
    if metodo == 'sobel':
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=apertureSize)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=apertureSize)
        mag = cv2.magnitude(sx, sy)
        mag = cv2.convertScaleAbs(mag)
        return cv2.cvtColor(mag, cv2.COLOR_GRAY2BGR)
    raise ValueError("metodo deve ser 'canny', 'laplacian' ou 'sobel'.")


def detectar_contornos(img: np.ndarray, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE,
                       min_area: int = 0) -> List[np.ndarray]:
    gray = converter_para_gray(img)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(th, mode, method)
    if min_area > 0:
        contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    return contours


def desenhar_contornos(img: np.ndarray, contours: List[np.ndarray], color: Tuple[int,int,int]=(0,255,0), thickness: int=2):
    out = ensure_color(img).copy()
    cv2.drawContours(out, contours, -1, color, thickness)
    return out


def detectar_circulos(img: np.ndarray, dp: float = 1.2, minDist: float = 20,
                      param1: float = 50, param2: float = 30, minRadius: int = 0, maxRadius: int = 0) -> Optional[np.ndarray]:
    gray = converter_para_gray(img)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    return None if circles is None else np.uint16(np.around(circles))


def detectar_retangulos(img: np.ndarray, epsilon_ratio: float = 0.02, min_area: int = 1000) -> List[np.ndarray]:
    contours = detectar_contornos(img, min_area=min_area)
    rects = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon_ratio * peri, True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            rects.append(approx)
    return rects


def morfologia(img: np.ndarray, operacao: str, ksize: Tuple[int,int]=(3,3), iterations: int=1, shape: str='rect') -> np.ndarray:
    op = operacao.lower()
    shape_map = {'rect': cv2.MORPH_RECT, 'ellipse': cv2.MORPH_ELLIPSE, 'cross': cv2.MORPH_CROSS}
    if shape not in shape_map:
        raise ValueError("shape deve ser 'rect', 'ellipse' ou 'cross'")
    kernel = cv2.getStructuringElement(shape_map[shape], ksize)
    if op == 'erode':
        return cv2.erode(img, kernel, iterations=iterations)
    if op == 'dilate':
        return cv2.dilate(img, kernel, iterations=iterations)
    if op == 'open':
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    if op == 'close':
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    if op == 'gradient':
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
    if op == 'tophat':
        return cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel, iterations=iterations)
    if op == 'blackhat':
        return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
    raise ValueError("Operação morfológica desconhecida.")


def erodir(img: np.ndarray, ksize: Tuple[int,int]=(3,3), iterations: int=1, shape: str='rect'):
    return morfologia(img, 'erode', ksize, iterations, shape)


def dilatar(img: np.ndarray, ksize: Tuple[int,int]=(3,3), iterations: int=1, shape: str='rect'):
    return morfologia(img, 'dilate', ksize, iterations, shape)


def abrir_morf(img: np.ndarray, ksize: Tuple[int,int]=(3,3), iterations: int=1, shape: str='rect'):
    return morfologia(img, 'open', ksize, iterations, shape)


def fechar_morf(img: np.ndarray, ksize: Tuple[int,int]=(3,3), iterations: int=1, shape: str='rect'):
    return morfologia(img, 'close', ksize, iterations, shape)


def equalizar_histograma(img: np.ndarray) -> np.ndarray:
    if img.ndim == 3 and img.shape[2] == 3:
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        return cv2.equalizeHist(img)


def equalizar_color(img: np.ndarray) -> np.ndarray:
    if img.ndim == 3 and img.shape[2] == 3:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img


def histograma(img: np.ndarray, channel: int = 0, mask: Optional[np.ndarray] = None, bins: int = 256):
    if img.ndim == 3:
        ch = img[:, :, channel]
    else:
        ch = img
    hist = cv2.calcHist([ch], [0], mask, [bins], [0, 256])
    return hist.flatten()


def equalizar_clahe(img: np.ndarray, clipLimit: float = 2.0, tileGridSize=(8,8)):
    return clahe(img, clipLimit=clipLimit, tileGridSize=tileGridSize)


def thresholding(img: np.ndarray, metodo: str = 'otsu', thresh: int = 128, maxval: int = 255,
                 tipo: str = 'binary') -> np.ndarray:
    gray = converter_para_gray(img)
    metodo = metodo.lower()
    if metodo == 'otsu':
        _, th = cv2.threshold(gray, 0, maxval, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return th
    if metodo == 'binary':
        tipo_map = {'binary': cv2.THRESH_BINARY, 'binary_inv': cv2.THRESH_BINARY_INV}
        t = tipo_map.get(tipo, cv2.THRESH_BINARY)
        _, th = cv2.threshold(gray, thresh, maxval, t)
        return th
    if metodo == 'adaptive':
        adaptive = kwargs = {}
        method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        return cv2.adaptiveThreshold(gray, maxval, method, cv2.THRESH_BINARY, 11, 2)
    raise ValueError("metodo deve ser 'otsu', 'binary' ou 'adaptive'.")


def kmeans_segmentacao(img: np.ndarray, k: int = 2, attempts: int = 10, criteria=None) -> np.ndarray:
    if criteria is None:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    Z = img.reshape((-1, 3)).astype(np.float32)
    _, labels, centers = cv2.kmeans(Z, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((img.shape))


def grabcut_remover_fundo(img: np.ndarray, rect: Tuple[int,int,int,int], iterCount: int = 5) -> np.ndarray:
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65), np.float64)
    fgdModel = np.zeros((1,65), np.float64)
    x, y, w, h = rect
    cv2.grabCut(img, mask, (x, y, w, h), bgdModel, fgdModel, iterCount, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
    result = img * mask2[:, :, np.newaxis]
    return result


def cartoonize(img: np.ndarray, downscale: int = 2, bilateral_iter: int = 5, edge_thresh: int = 100) -> np.ndarray:
    img_color = img.copy()
    for _ in range(downscale):
        img_color = cv2.pyrDown(img_color)
    for _ in range(bilateral_iter):
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)
    for _ in range(downscale):
        img_color = cv2.pyrUp(img_color)
    img_gray = converter_para_gray(img)
    img_blur = cv2.medianBlur(img_gray, 7)
    edges = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(img_color, edges_colored)
    return cartoon


def pencil_sketch(img: np.ndarray, sigma_s: int = 60, sigma_r: float = 0.07, shade_factor: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
    gray, color = cv2.pencilSketch(img, sigma_s=sigma_s, sigma_r=sigma_r, shade_factor=shade_factor)
    return gray, color


def oil_painting(img: np.ndarray, size: int = 7, dynRatio: int = 1) -> np.ndarray:
    try:
        return cv2.xphoto.oilPainting(img, size, dynRatio)
    except Exception:
        return cv2.stylization(img, sigma_s=60, sigma_r=0.6)


def detectar_faces(img: np.ndarray, scaleFactor: float = 1.1, minNeighbors: int = 5, minSize: Tuple[int,int]=(30,30),
                   cascade_path: Optional[str] = None) -> List[Tuple[int,int,int,int]]:
    if cascade_path is None:
        cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
    if not os.path.exists(cascade_path):
        raise FileNotFoundError(f"Haarcascade não encontrada: {cascade_path}")
    detector = cv2.CascadeClassifier(cascade_path)
    gray = converter_para_gray(img)
    faces = detector.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    return [(int(x), int(y), int(w), int(h)) for (x, y, w, h) in faces]


def desenhar_bbox(img: np.ndarray, bboxes: List[Tuple[int,int,int,int]], color: Tuple[int,int,int]=(0,255,0),
                  thickness: int = 2, labels: Optional[List[str]] = None) -> np.ndarray:
    out = ensure_color(img).copy()
    for i, (x, y, w, h) in enumerate(bboxes):
        cv2.rectangle(out, (x, y), (x + w, y + h), color, thickness)
        if labels and i < len(labels):
            cv2.putText(out, labels[i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return out


def alpha_blend(fg: np.ndarray, bg: np.ndarray, alpha: float = 0.5) -> np.ndarray:
    if fg.shape[:2] != bg.shape[:2]:
        bg = redimensionar(bg, largura=fg.shape[1], altura=fg.shape[0])
    fg = fg.astype('float32'); bg = bg.astype('float32')
    out = fg * alpha + bg * (1 - alpha)
    return np.clip(out, 0, 255).astype('uint8')


def overlay_image(base: np.ndarray, overlay: np.ndarray, x: int, y: int, alpha: float = 1.0) -> np.ndarray:
    out = ensure_color(base).copy()
    h, w = overlay.shape[:2]
    if overlay.ndim == 3 and overlay.shape[2] == 4:
        alpha_mask = overlay[:, :, 3] / 255.0
        for c in range(3):
            y1 = y; y2 = y + h; x1 = x; x2 = x + w
            if y1<0 or x1<0 or y2>out.shape[0] or x2>out.shape[1]:
                y1c = max(0, -y); x1c = max(0, -x)
                y1 = max(0, y); x1 = max(0, x)
                y2 = min(out.shape[0], y + h); x2 = min(out.shape[1], x + w)
                alpha_mask = alpha_mask[y1c:y1c + (y2-y1), x1c:x1c + (x2-x1)]
                overlay_crop = overlay[y1c:y1c + (y2-y1), x1c:x1c + (x2-x1), c]
                out[y1:y2, x1:x2, c] = (overlay_crop * alpha_mask * alpha + out[y1:y2, x1:x2, c] * (1 - alpha_mask * alpha))
            else:
                overlay_crop = overlay[:, :, c]
                out[y:y+h, x:x+w, c] = (overlay_crop * alpha_mask * alpha + out[y:y+h, x:x+w, c] * (1 - alpha_mask * alpha))
        return out.astype('uint8')
    else:
        h_b = min(out.shape[0] - y, h)
        w_b = min(out.shape[1] - x, w)
        if h_b <= 0 or w_b <= 0:
            return out
        roi = out[y:y+h_b, x:x+w_b]
        overlay_crop = overlay[0:h_b, 0:w_b]
        blended = cv2.addWeighted(overlay_crop.astype('uint8'), alpha, roi.astype('uint8'), 1-alpha, 0)
        out[y:y+h_b, x:x+w_b] = blended
        return out


def overlay_text(img: np.ndarray, text: str, pos: Tuple[int,int], font_scale: float = 1.0, color: Tuple[int,int,int]=(255,255,255),
                 thickness: int = 2, bgcolor: Optional[Tuple[int,int,int]] = None) -> np.ndarray:
    out = ensure_color(img).copy()
    x, y = pos
    (tw, th), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    if bgcolor is not None:
        cv2.rectangle(out, (x, y - th - baseline), (x + tw, y + baseline), bgcolor, -1)
    cv2.putText(out, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)
    return out


def to_bytes(img: np.ndarray, ext: str = '.png') -> bytes:
    ext = ext if ext.startswith('.') else f'.{ext}'
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise IOError("Falha ao codificar imagem para bytes")
    return buf.tobytes()


def matching_template(img: np.ndarray, template: np.ndarray, method=cv2.TM_CCOEFF_NORMED):
    gray = converter_para_gray(img)
    tpl = converter_para_gray(template)
    res = cv2.matchTemplate(gray, tpl, method)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
        top_left = minLoc
    else:
        top_left = maxLoc
    h, w = tpl.shape[:2]
    return {'res': res, 'top_left': top_left, 'bottom_right': (top_left[0] + w, top_left[1] + h),
            'minVal': minVal, 'maxVal': maxVal}

