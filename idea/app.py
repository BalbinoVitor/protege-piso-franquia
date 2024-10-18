import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import pandas as pd

# Caminho dos templates e arquivos estáticos
TEMPLATE_PATH = 'templates/index_template.html'
STATIC_PATH = 'templates'
OUTPUT_BASE_PATH = 'output'

class TagFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Preenchimento de Tags Dinâmicas")

        # Criação da interface
        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.root, padding="10")
        form_frame.grid(row=0, column=0, sticky="NSEW")

        # Botão para carregar Excel
        ttk.Button(form_frame, text="Selecionar Arquivo Excel", 
                   command=self.select_excel_file).grid(row=0, column=0, pady=10)

    def select_excel_file(self):
        """Seleciona um arquivo Excel contendo os dados."""
        excel_path = filedialog.askopenfilename(
            title="Selecione o Arquivo Excel",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        if excel_path:
            try:
                self.process_excel(excel_path)
                messagebox.showinfo("Sucesso", "Sites gerados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao processar Excel: {str(e)}")

    def process_excel(self, excel_path):
        """Lê o Excel e gera os sites com base em cada linha."""
        try:
            df = pd.read_excel(excel_path)
            df.columns = df.columns.str.strip()  # Remove espaços em branco dos nomes das colunas
            
            # Itera sobre cada linha do DataFrame
            for _, row in df.iterrows():
                data = row.to_dict()
                self.generate_site(data)

        except Exception as e:
            raise RuntimeError(f"Erro ao ler o arquivo Excel: {str(e)}")

    def generate_site(self, data):
        """Gera um site para cada linha do Excel."""
        try:
            cidade = data.get('CIDADE', '').strip()
            if not cidade:
                raise ValueError("Nome da cidade não pode estar vazio.")

            cidade_path = os.path.join(OUTPUT_BASE_PATH, cidade)
            os.makedirs(cidade_path, exist_ok=True)

            self.copy_static_files(cidade_path)

            with open(TEMPLATE_PATH, 'r', encoding='utf-8') as file:
                html_content = file.read()

            for key, value in data.items():
                if key not in ['CADRS COM IMAGENS', 'RECOMENDADO']:
                    html_content = html_content.replace(f'{{{{{key}}}}}', str(value))

            # Processar o arquivo recomendado
            if data.get('RECOMENDADO'):
                recommended_file = os.path.basename(data['RECOMENDADO'].strip())
                src_recommended = os.path.join(STATIC_PATH, 'images', recommended_file)

                if os.path.isfile(src_recommended):
                    dst_recommended = os.path.join(cidade_path, 'images', recommended_file)
                    if os.path.abspath(src_recommended) != os.path.abspath(dst_recommended):
                        shutil.copy2(src_recommended, dst_recommended)

                if recommended_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    media_html = f'<img src="images/{recommended_file}" alt="Recomendado" class="imagem-quem-somos">'
                elif recommended_file.lower().endswith(('.mp4', '.webm', '.ogg')):
                    media_html = f'''
                    <video controls class="video-quem-somos" style="width:100%; max-width:600px;">
                        <source src="images/{recommended_file}" type="video/mp4">
                        Seu navegador não suporta o elemento de vídeo.
                    </video>
                    '''
                else:
                    media_html = '<!-- Arquivo recomendado não suportado -->'

                html_content = html_content.replace('{{RECOMENDADO}}', media_html)

            # Gera os cards de imagens
            cards_html = ''
            if data.get('CADRS COM IMAGENS'):
                cadrs = data['CADRS COM IMAGENS']
                
                # Garantir que cadrs seja tratado como string
                if isinstance(cadrs, float):
                    cadrs = ''  # Se for um float, consideramos como vazio
                elif not isinstance(cadrs, str):
                    raise ValueError("CADRS COM IMAGENS deve ser uma string.")

                image_files = [img.strip() for img in cadrs.split(',') if img.strip()]
                for image_name in image_files:
                    src_image = os.path.join(STATIC_PATH, 'images', image_name)
                    dst_image = os.path.join(cidade_path, 'images', image_name)

                    if os.path.isfile(src_image):
                        if os.path.abspath(src_image) != os.path.abspath(dst_image):
                            shutil.copy2(src_image, dst_image)

                        card = f'''
                        <div class="card">
                            <img src="images/{image_name}" alt="Imagem da obra" class="card-image">
                        </div>
                        '''
                        cards_html += card
                    else:
                        raise FileNotFoundError(f"Imagem não encontrada: {src_image}")

            html_content = html_content.replace('{{CADRS COM IMAGENS}}', cards_html)

            # Salva o HTML final na pasta da cidade
            output_html_path = os.path.join(cidade_path, 'index.html')
            with open(output_html_path, 'w', encoding='utf-8') as file:
                file.write(html_content)

        except Exception as e:
            raise RuntimeError(f"Erro ao gerar site para {cidade}: {str(e)}")

    def copy_static_files(self, cidade_path):
        """Copia os arquivos estáticos para a pasta da cidade."""
        static_dirs = ['images', 'fonts', 'index.js', 'styles.css']
        for item in static_dirs:
            src = os.path.join(STATIC_PATH, item)
            dst = os.path.join(cidade_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif os.path.isfile(src):
                if os.path.abspath(src) != os.path.abspath(dst):
                    shutil.copy2(src, dst)

# Inicializa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TagFormApp(root)
    root.mainloop()
