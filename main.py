import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
from faker import Faker
import os
import random
import textwrap

# Configurações
input_xml_path = 'paths.xml'  # Caminho do arquivo XML
input_image_path = 'danfe_model.png'  # Caminho da imagem modelo
output_image_dir = 'output_images/'
output_labels_dir = 'output_labels/'
font_path = 'LiberationSans-Regular.ttf'  # Caminho para a fonte usada nos textos
num_images = 300  # Quantidade de imagens a serem geradas

# Gerador de dados aleatórios
fake = Faker('pt_BR')

# Limitação de tamanho para evitar sobreposição
def limitar_tamanho_texto(texto, max_length):
    if len(texto) > max_length:
        return texto[:max_length - 3] + '...'
    return texto

# Limitação de números para não quebrar o layout
def limitar_tamanho_numero(numero, casas_decimais=3, max_length=10):
    numero_formatado = f"{numero:.{casas_decimais}f}"
    if len(numero_formatado) > max_length:
        return limitar_tamanho_texto(numero_formatado, max_length)
    return numero_formatado

# Ajusta a fonte dependendo do espaço disponível
def ajustar_fonte(texto, draw, max_width, font_size=18):
    font = ImageFont.truetype(font_path, font_size)
    while draw.textbbox((0, 0), texto, font=font)[2] > max_width and font_size > 8:
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
    return font

# Função para garantir que o texto do endereço caiba em uma linha
def limitar_texto_largura(texto, draw, max_width, font):
    while draw.textbbox((0, 0), texto, font=font)[2] > max_width and len(texto) > 0:
        texto = texto[:-1]  # Remove o último caractere até caber na largura disponível
    return texto

# Função para apagar a área anterior
def apagar_area(draw, xmin, ymin, xmax, ymax, background_color="white"):
    draw.rectangle([xmin, ymin, xmax, ymax], fill=background_color)

# Função para gerar o texto dos dados adicionais
def gerar_dados_adicionais(fake):
    empresa = fake.company()
    cnpj = fake.cnpj()
    inscricao_estadual = str(random.randint(100000000, 999999999))
    rua = fake.street_name()
    numero = str(random.randint(1, 9999))
    complemento = fake.word()
    bairro = fake.bairro()
    cidade = fake.city()
    cep = fake.postcode()
    estado = fake.state_abbr()
    nota_fiscal = str(random.randint(100000, 999999))
    data_emissao = fake.date_object().strftime("%d/%m/%Y")
    serie = str(random.randint(1, 9))
    valor_tributos = f"{random.uniform(100, 1000):.2f}"
    difal_destino = f"{random.uniform(1, 20):.2f}"
    fcp = f"{random.uniform(0, 5):.2f}"
    difal_origem = f"{random.uniform(0, 10):.2f}"

    return f"Enviado diretamente do depósito temporário - operador logístico: {empresa}, Cnpj: {cnpj}, Inscricao Estadual: {inscricao_estadual}, saindo do endereço: {rua}, Numero: {numero}, Complemento: {complemento}, Bairro: {bairro}, Cidade: {cidade}, Cep: {cep}, Estado: {estado}, País: BR. Nota fiscal de retorno simbólico n {nota_fiscal}, emitida em {data_emissao}, serie {serie}. Valor aproximado dos tributos (IBPT) R$ {valor_tributos}. Valores totais do ICMS Interestadual: DIFAL da UF destino R${difal_destino} + FCP R${fcp}; DIFAL da UF Origem R${difal_origem}."

# Função para ajustar o texto à caixa com tamanho de fonte controlado apenas para 'nfe_dados_adicionais'
def ajustar_texto_caixa(texto, draw, max_width, max_height, font_path, font_size_escolhido):
    font_size = font_size_escolhido
    font = ImageFont.truetype(font_path, font_size)
    lines = textwrap.wrap(texto, width=int(max_width / (font_size * 0.6)))  # Estimativa inicial

    while font_size > 20:
        total_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
        if total_height <= max_height and len(lines) * font.getbbox(lines[0])[2] <= max_width:
            break
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        lines = textwrap.wrap(texto, width=int(max_width / (font_size * 0.6)))

    return font, lines

# Campos que serão alterados com tamanho controlado para caber em seus espaços
campos_alterados = {
    'remet_enderec': lambda: limitar_tamanho_texto(f"{fake.street_name()}, {random.randint(1, 9999)}, {fake.bairro()}", 50),
    'chave_acesso': lambda: limitar_tamanho_texto(''.join([str(random.randint(0, 9)) for _ in range(44)]), 44),
    'nfe_numero': lambda: limitar_tamanho_texto(f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}", 11),
    'insc_estadual': lambda: limitar_tamanho_texto(str(random.randint(100000000, 999999999)), 12),
    'remet_cpfcnpj': lambda: limitar_tamanho_texto(fake.cnpj(), 18),
    'dest_nome': lambda: limitar_tamanho_texto(fake.name(), 25),
    'dest_cnpjcpf': lambda: limitar_tamanho_texto(fake.cpf(), 14),
    'data_emissao': lambda: fake.date(),
    'dest_enderec': lambda: limitar_tamanho_texto(f"{fake.street_name()}, {random.randint(1, 9999)}, {fake.bairro()}", 50),
    'dest_bairro': lambda: limitar_tamanho_texto(fake.street_name(), 25),
    'dest_cep': lambda: limitar_tamanho_texto(fake.postcode(), 9),
    'data_entradasaida': lambda: fake.date(),
    'remet_municipio': lambda: limitar_tamanho_texto(fake.city().replace("\n", ""), 20),
    'remet_estado': lambda: limitar_tamanho_texto(fake.state_abbr(), 2),
    'nfe_hr_saida': lambda: fake.time(),
    'transp_valor_frete': lambda: limitar_tamanho_numero(random.uniform(100, 1000), casas_decimais=2, max_length=8),
    'nfe_valor_total_nota': lambda: limitar_tamanho_numero(random.uniform(500, 5000), casas_decimais=2, max_length=10),
    'nfe_valor_total_produtos': lambda: limitar_tamanho_numero(random.uniform(500, 5000), casas_decimais=2, max_length=10),
    'transp_nome': lambda: limitar_tamanho_texto(fake.company(), 30),
    'transp_tipo': lambda: limitar_tamanho_texto(fake.word(), 10),
    'transp_cnpj': lambda: limitar_tamanho_texto(fake.cnpj(), 18),
    'transp_endereco': lambda: limitar_tamanho_texto(f"{fake.street_name()}, {random.randint(1, 9999)}, {fake.bairro()}", 50),
    'transp_municipio': lambda: limitar_tamanho_texto(fake.city(), 20),
    'transp_estado': lambda: limitar_tamanho_texto(fake.state_abbr(), 2),
    'transp_inscr_est': lambda: limitar_tamanho_texto(str(random.randint(100000000, 999999999)), 12),
    'transp_qtd': lambda: limitar_tamanho_numero(random.uniform(1, 50), casas_decimais=3, max_length=7),
    'transp_peso_bruto': lambda: limitar_tamanho_numero(random.uniform(100, 500), casas_decimais=2, max_length=8) + " kg",
    'transp_peso_liquido': lambda: limitar_tamanho_numero(random.uniform(100, 500), casas_decimais=2, max_length=8) + " kg",
    'prod_cod': lambda: limitar_tamanho_texto(f"PRD{random.randint(1000, 9999)}", 10),
    'prod_nome': lambda: limitar_tamanho_texto(fake.word(), 15),
    'prod_cfop': lambda: limitar_tamanho_texto(str(random.randint(1000, 9999)), 4),
    'prod_ncm': lambda: limitar_tamanho_texto(str(random.randint(10000000, 99999999)), 8),
    'prod_cst': lambda: limitar_tamanho_texto(str(random.randint(100, 999)), 3),
    'prod_tipo_unit': lambda: limitar_tamanho_texto(random.choice(['unid', 'kg', 'g']), 5),
    'prod_qtd': lambda: str(random.randint(1, 50)),
    'prod_vlr_unit': lambda: limitar_tamanho_numero(random.uniform(10, 100), casas_decimais=2, max_length=8),
    'prod_valr_total': lambda: limitar_tamanho_numero(random.uniform(500, 5000), casas_decimais=2, max_length=10),
    'prod_b_calc_icms': lambda: limitar_tamanho_numero(random.uniform(500, 5000), casas_decimais=2, max_length=10),
    'prod_valr_icms': lambda: limitar_tamanho_numero(random.uniform(100, 500), casas_decimais=2, max_length=8),
    'nfe_dados_adicionais': lambda: gerar_dados_adicionais(fake),
    'nome_empresa': lambda: limitar_tamanho_texto(fake.company(), 25)
}

# Função para gerar novas imagens e labels com controle específico de fonte para nfe_dados_adicionais
def gerar_nova_imagem_e_labels(xml_path, image_path, output_img_dir, output_lbl_dir, campos_alterados, num_images, tamanho_fonte_dados_adicionais):
    for i in range(num_images):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        for obj in root.findall('object'):
            campo = obj.find('name').text
            if campo in campos_alterados:
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)

                novo_valor = campos_alterados[campo]()
                max_width = xmax - xmin
                max_height = ymax - ymin

                apagar_area(draw, xmin, ymin, xmax, ymax)

                if campo == 'nfe_dados_adicionais':
                    # Usar tamanho de fonte escolhido para os dados adicionais
                    font, lines = ajustar_texto_caixa(novo_valor, draw, max_width, max_height, font_path, tamanho_fonte_dados_adicionais)
                    y_text = ymin
                    for line in lines:
                        draw.text((xmin, y_text), line, font=font, fill='black')
                        y_text += font.getbbox(line)[3] - font.getbbox(line)[1]
                else:
                    # Ajustar a fonte normalmente para os outros campos
                    font = ajustar_fonte(novo_valor, draw, max_width)
                    novo_valor = limitar_texto_largura(novo_valor, draw, max_width, font)
                    draw.text((xmin, ymin), novo_valor, font=font, fill='black')

        nova_imagem_path = os.path.join(output_img_dir, f"nota_fiscal_{random.randint(1000,9999)}.png")
        image.save(nova_imagem_path)

        novo_label_path = os.path.join(output_lbl_dir, f"nota_fiscal_{random.randint(1000,9999)}.txt")
        # Aqui você deve gerar o arquivo de anotação no formato YOLO

        print(f"Imagem gerada: {nova_imagem_path}")
        print(f"Arquivo de anotação gerado: {novo_label_path}")

# Gerar novas imagens e labels com controle de fonte para nfe_dados_adicionais
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

# Defina o tamanho da fonte para nfe_dados_adicionais
tamanho_fonte_dados_adicionais = 14  # Aqui você controla o tamanho da fonte dos dados adicionais

gerar_nova_imagem_e_labels(input_xml_path, input_image_path, output_image_dir, output_labels_dir, campos_alterados, num_images, tamanho_fonte_dados_adicionais)