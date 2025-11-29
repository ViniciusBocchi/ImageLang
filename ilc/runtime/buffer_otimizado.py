from typing import Union

class BufferOtimizado:
    def __init__(self, data: Union[str, bytes, None] = None):
        if data is None:
            data = ""
        if isinstance(data, bytes):
            self._texto = data.decode('utf-8', errors='replace')
        else:
            self._texto = str(data)

        self._pos = 0
        self._tamanho = len(self._texto)

    def proximo_caractere(self) -> int:
        if self._pos >= self._tamanho:
            return -1
        ch = self._texto[self._pos]
        self._pos += 1
        return ord(ch)

    def espiar_caractere(self, offset: int = 0) -> int:
        idx = self._pos + offset
        if idx >= self._tamanho or idx < 0:
            return -1
        return ord(self._texto[idx])

    def retroceder(self, steps: int = 1):
        self._pos = max(0, self._pos - int(steps))

    def acabou(self) -> bool:
        return self._pos >= self._tamanho

    def posicao(self) -> int:
        return self._pos

    def tamanho(self) -> int:
        return self._tamanho
