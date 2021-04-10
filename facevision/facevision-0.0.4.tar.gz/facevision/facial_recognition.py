import time

import cv2
import glob
import os 
from deepface import DeepFace


class FaceRecognition(object):
    """
    Classe que representa o pipeline do sistema de reconhecimento facial: 
            1 - Extração e Detecção de Faces  
            2 - Alinhamento de Faces 
            3 - Representação 
            4 - Reconhecimento Facial

    
    Methods
    ------- 
         - cascade: retorna um detector de faces HaarCascade
         - extract_cam: extração de frames do usuário pela webcam 
         - waiting_recognition: carreganmento da detecção de faces 
         - recognition: inferência utilizando deepface 
         - execute: execução de todo o pipeline de Reconhecimento facial 
    

    """

    def __init__(self, user_name: str, password: str, db_images: str, frames_dir: str, cascade_path: str,
                 number_frames: int, image_format: str):

        """
        Construtor da classe com os atributos globais compartilhados entre os métodos.

        -------------

        Atributos: 
                    - user_name: nome do usuário de acesso
                    - password: senha do usuário
                    - db_images: banco de imagens do usuário 
                    - cascade_path: caminho do arquivo "xml" do HaarCascade 
                    - number_frames: número de frames a serem extraídos
                    - image_format: formato do salvamento do frame

        """

        self.user_name = user_name
        self.password = password
        self.db_images = db_images
        self.frames_dir = frames_dir
        self.cascade_path = cascade_path
        self.number_frames = number_frames
        self.image_format = image_format

    def cascade(self):
        """
         Instânciar o detector de faces HaarCascade.  

            Parâmetros(__init__): 
                                - cascade_path: caminho do arquivo "xml" do HaarCascade 

            Retorno: instância do detector (objeto cv2) 
            """
        cascade_detector = cv2.CascadeClassifier(self.cascade_path)
        return cascade_detector

    def extract_cam(self):

        """
        Faz Extração de frames da webcam do usuário, e salva estes frames no diretório referente ao nome do usuário. 

            Parâmetros (__init__):
                        - user_name: nome do usuário de acesso
                        - image_format: formato de salvamento do frame
                        - number_frames: número de frames a serem recortados pela webcam 
                        - frames_dir: diretório para salvar os frames 

            Retorno: None 

        """

        time_start = time.time()
        cap = cv2.VideoCapture(0)
        count = 0
        print('Extraindo frames .... \n\n')
        while cap.isOpened():

            ret, frame = cap.read()
            cv2.imwrite(f"{self.frames_dir}/{self.user_name}/{self.user_name}_{count + 1}.{self.image_format}", frame)
            count = count + 1

            if (count > (self.number_frames - 1)):
                time_end = time.time()
                cap.release()

                print("Extração de frames concluída.\n%d frames extraidos" % count)
                print("Levou cerca de %d segundos para conversão." % (time_end - time_start))
                print(f"Frames salvos em: frames/{self.user_name}")
                break

        cv2.destroyAllWindows()

    def waiting_recognition(self):

        """
        Faz o carregamento do reconhecimento facial. 

        Retorno: None 

        """

        webcam = cv2.VideoCapture(0)
        faceCascade = self.cascade()

        while True:

            ret, frames = webcam.read()

            # HaarCascade detecção
            gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            cv2.putText(frames,
                        "Aperte a tecla 'C' para continuar",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255),
                        2,
                        cv2.LINE_4)

            # desenhar boxes no vídeo 
            for (x, y, w, h) in faces:
                cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(frames, 'Carregando reconhecimento.... ', (x - 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # mostrar resultado no frame 
            cv2.imshow('Video', frames)

            if cv2.waitKey(1) == ord('c'):
                break

    def recognition(self):

        """
        Aplicação do DeepFace utilizando o a rede "VGG-Face" para inferência. 

            Parâmetros(__init__): 
                        - user_name: nome do usuário de acesso
                        - image_format: formato de salvamento do frame
                        - frames_dir: diretório para salvar os frames 

            Retorno: um dicionário com métricas da inferência. 

        """

        # frame salvo 
        imagem_camera = f"{self.frames_dir}/{self.user_name}/{self.user_name}_120.{self.image_format}"

        face_result = DeepFace.verify(self.db_images, imagem_camera, model_name="VGG-Face", distance_metric="cosine",
                                      detector_backend="mtcnn")
        print("Imagem verificada: ", face_result["verified"])

        return face_result

    def excute(self):

        """
        Execução de todo o pipeline de Reconhecimento facial. 

            Parâmetros(__init__): 
                                 - user_name: nome do usuário de acesso
            
            Retorno: None

        """

        # carregando reconhecimento
        self.waiting_recognition()
        # extração de frames 
        self.extract_cam()
        # reconhecimento facial 
        face_result = self.recognition()

        # HaarCascade 
        faceCascade = self.cascade()

        # acessar webcam  
        webcam = cv2.VideoCapture(0)

        while True:

            ret, frame = webcam.read()

            if face_result["verified"] == True:

                # HaarCascade detecção
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                # desenhar boxes no vídeo
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, 'Usuario identificado: ' + self.user_name, (x - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # mostrar resultado no frame 
                cv2.imshow('Video', frame)


            else:
                # HaarCascade detecção
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                # desenhar boxes no vídeo
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, 'Acesso negado!', (x - 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # mostrar resultado no frame 
                cv2.imshow('Video', frame)

            # encerrar execução 
            if cv2.waitKey(1) == ord('q'):
                break

        webcam.release()
        cv2.destroyAllWindows()

        files = glob.glob(f'{self.frames_dir}/{self.user_name}/*{self.image_format}')
        for f in files:
            os.remove(f)
