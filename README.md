# Django_ProjectMVISIA
**Pipeline - Processo Seletivo MVISIA 08/2021**

Foi desenvolvida uma solução que permite ao usuário a configuração de uma câmera e aplicação de operações simples nas imagens obtidas da câmera por meio de um pipeline de processameto. A interface web possui as opções de **Camera Stream**, inicializando a câmera; **Capturar | Resgatar Frame**, capturando ou resgatando o frame capturando da câmera stream. A partir do frame capturado é possível aplicar as operações **Subtrair Background**, subtraindo do frame capturado por meio do stream um frame obtido ao clicar nesta opção; **Detectar Face e Idade Aparente**, solução implementada como desafio extra, detectando uma face, como sugerido e em adicional, estimando uma idade aparente; **Recortar Imagem**,a partir dos pontos (x,y) e (dx,dy) realiza um crop na imagem capturada e **Binarizar Imagem**, que realiza a binarização da imagem com base nos parâmetros r,g,b e k.



## Configuração Inicial - Instalação de dependências
> **Django:** pip install django

> **Django Crispy Forms:** pip install django-crispy-forms 

> **Numpy:** pip install numpy

> **Imutils:** pip install imutils

> **OpenCV:** pip install opencv-python

>  **Tensorflow** pip install tensorflow


## Executando o Projeto

Dentro do diretório Django_ProjectMVISIA executar:

>  python ./manage.py runserver

Em seguida acessar:
>  http://127.0.0.1:8000/ ou http://localhost:8000/
