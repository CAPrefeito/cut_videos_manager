from moviepy.editor import *
import PySimpleGUI as sg


class VideoYoutube:

    LIB_CODEC = 'libx264'

    def __init__(self, *args, **kwargs):
        self.nome_video_original = kwargs.get("nome_arquivo")
        self.nome_novo_video = kwargs.get("nome_novo_video", "video_cortado.mp4")
        self.inicio_corte = self._convert_em_segundos(kwargs.get("inicio_corte"))
        self.final_corte = self._convert_em_segundos(kwargs.get("final_corte"))
        self.thumbnail = kwargs.get("thumbnail", None)
        self.video_encerramento = kwargs.get("video_encerramento", None)

    @staticmethod
    def _convert_em_segundos(valor):
        try:
            split_valor = str(valor).split(":")
            if len(split_valor) < 2 or len(split_valor) > 3:
                print(f'ERROR: INPUT tempo inválido: {valor}.')
            if len(split_valor) == 2:
                segundos = (int(split_valor[0]) * 60) + int(split_valor[1])
                return segundos
            else:
                horas = int(split_valor[0]) * 3600
                minutos = (int(split_valor[1]) * 60) + int(split_valor[2])
                segundos = horas + minutos
                return segundos
        except Exception as e:
            print(f'ERROR: Ao converter a variável em segundos. e {e}')

    def cortar_video(self):
        try:
            clips = []
            self.validacao_valores_tempo()
            video = VideoFileClip(self.nome_video_original)
            video_cortado = video.subclip(self.inicio_corte, self.final_corte)
            if self.thumbnail:
                clip_foto_capa = ImageClip(self.thumbnail).set_duration(5)
                clips.append(clip_foto_capa)
            clips.append(video_cortado)
            if self.video_encerramento:
                video_encerramento = VideoFileClip(self.video_encerramento)
                clips.append(video_encerramento)
            if len(clips) > 1:
                video_clip = concatenate_videoclips(clips, method='compose')
                video_clip.write_videofile(self.nome_novo_video, codec=self.LIB_CODEC)
            else:
                video_cortado.write_videofile(self.nome_novo_video, codec=self.LIB_CODEC)
            response = f'SUCESSO ao salvar o novo video {self.nome_novo_video}'
            return response
        except Exception as e:
            print(f'ERROR: Ao salvar o novo video {self.nome_novo_video}. e {e}')

    def validacao_valores_tempo(self):
        if self.final_corte <= self.inicio_corte:
            print('ERROR: Valor do tempo FINAL é inválido.')
        return True


class TelaPython:

    SIZE_LABEL = 25
    SIZE_INPUT = 50
    SIZE_OUTPUT_X = 80
    SIZE_OUTPUT_Y = 10

    def __init__(self):
        # Layout
        layout = [
            [sg.Text('Nome do vídeo original: *', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='nome_arquivo')],
            [sg.Text('Tempo INICIAL do corte: *', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='inicio_corte')],
            [sg.Text('Tempo FINAL do corte: *', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='final_corte')],
            [sg.Text('Nome do novo vídeo: *', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='nome_novo_video')],
            [sg.Text('Foto capa:', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='foto_capa')],
            [sg.Text('Vídeo encerramento:', size=(self.SIZE_LABEL, 0)), sg.Input(size=(self.SIZE_INPUT, 0), key='video_encerramento')],
            [sg.Button('Cortar o vídeo')],
            [sg.Output(size=(self.SIZE_OUTPUT_X, self.SIZE_OUTPUT_Y), key='output')],
            [sg.Text('* Campos obrigatórios.', size=(self.SIZE_LABEL, 0))]
        ]
        # Janela
        self.janela = sg.Window('Cortar o vídeo').layout(layout)
        self.nome_arquivo = ''
        self.inicio_corte = ''
        self.final_corte = ''
        self.nome_novo_video = ''
        self.foto_capa = ''
        self.video_encerramento = ''
        self.validacao = True

    def iniciar(self):
        while True:
            self.button, self.values = self.janela.Read()
            self.janela.FindElement(key='output').Update('')
            self.nome_arquivo = self.values['nome_arquivo']
            self.inicio_corte = self.values['inicio_corte']
            self.final_corte = self.values['final_corte']
            self.nome_novo_video = self.values['nome_novo_video']
            self.foto_capa = self.values['foto_capa'] if 'foto_capa' in self.values else None
            self.video_encerramento = self.values['video_encerramento'] if 'video_encerramento' in self.values else None
            print(f'nome_arquivo:  {self.nome_arquivo}')
            print(f'inicio_corte:  {self.inicio_corte}')
            print(f'final_corte:  {self.final_corte}')
            print(f'nome_novo_video:  {self.nome_novo_video}')
            self.janela.Refresh()
            self.validacao_inputs()
            self.executar()

    def validacao_inputs(self):
        print('Iniciando validações dos dados de entrada ...')
        self.janela.Refresh()
        if not self.nome_arquivo or not self.nome_novo_video or not self.inicio_corte or not self.final_corte:
            msg_error = 'ERROR: Campos obrigatórios não preenchidos.'
            print(msg_error)
            self.validacao = False
            return
        if '.' not in self.nome_arquivo or '.' not in self.nome_novo_video:
            msg_error = 'ERROR: Nome dos arquivos sem a extensão. Favor verificar ...'
            print(msg_error)
            self.validacao = False
            return 
        print('Nomes dos arquivos: OK')
        if ':' not in self.inicio_corte or ':' not in self.final_corte:
            msg_error = 'ERROR: O formato do tempo está inválido. Exemplo: 01:30'
            print(msg_error)
            self.validacao = False
            return 
        print('Tempos dos cortes: OK')
        self.janela.Refresh()

    def executar(self):
        if not self.validacao:
            return
        print(f'Iniciando o corte do vídeo ...')
        self.janela.Refresh()
        args = {
            'nome_arquivo': self.nome_arquivo,
            'nome_novo_video': self.nome_novo_video,
            'inicio_corte': self.inicio_corte,
            'final_corte': self.final_corte,
            'thumbnail': self.foto_capa,
            'video_encerramento': self.video_encerramento
        }
        video = VideoYoutube(**args)
        response = video.cortar_video()
        print(f'{response}')
        self.janela.Refresh()


if __name__ == '__main__':
    tela = TelaPython()
    tela.iniciar()
