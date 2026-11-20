import os 
import time

from helpers import retorna_reservas

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError, expect




load_dotenv()


usuario_sei = os.getenv("SEI_USUARIO")
senha_sei = os.getenv("SEI_SENHA")


with sync_playwright() as pw:
    navegador = pw.chromium.launch(headless=False)
    contexto = navegador.new_context()

    pagina_1 = contexto.new_page()

    pagina_1.goto("https://sei.pentagonoedu.com.br")

    #FAZENDO LOGIN
    pagina_1.get_by_role("textbox", name="Usuário").fill(usuario_sei)
    pagina_1.get_by_role("textbox", name="Senha").fill(senha_sei)
    pagina_1.get_by_role("link", name="Entrar").click()

    
    ##VERIFICANDO SE TEM ANUNCIO 
    try: 

        botao_anuncio = pagina_1.get_by_role("link", name="Entendi")
        botao_anuncio.wait_for(state="visible", timeout=3000)
        botao_anuncio.click()

    except TimeoutError:
        print("[DEBUG] Pop-up não apareceu.")
        pass
    
    #INDO PARA PÁGINA DE OCORRENCIA DIRETAMENTE PELA URL 
    pagina_1.goto("https://sei.pentagonoedu.com.br/visaoAdministrativo/patrimonio/ocorrenciaPatrimonioForm.xhtml")


    


    ##INSERINDO     DADOS    DA      PLANILHA (LÓGICA)

    lista_reservas = retorna_reservas()
    posicao_reserva = 0 

    while posicao_reserva <= len(lista_reservas) - 1:




        ##SELECIONANDO TIPO OCORRENCIA
        pagina_1.locator('[id="form:tipoOcorrencia"]').select_option("RESERVA_LOCAL")
        
        ##INSERINDO MOTIVO DA RESERVA 
        pagina_1.locator('textarea[name="form:j_idt270"]').click()
        pagina_1.locator('textarea[name="form:j_idt270"]').fill( list(lista_reservas[posicao_reserva].values())[2] )

        ##INSERINDO NOME DO PROFESSOR
        pagina_1.locator('[id="form:consultasolicitanteEmprestimo:consultasolicitanteEmprestimo"]').click()
        pagina_1.locator('[id="formFuncionario:valorConsultaFuncionario"]').click()
        pagina_1.locator('[id="formFuncionario:valorConsultaFuncionario"]').fill( list(lista_reservas[posicao_reserva].values())[0] )

        pagina_1.locator('[id="formFuncionario:btnConsultarFuncionario"]').click()

        

        #VERIFICANDO SE O BANCO DE DADOS CARREGOU ALGUM PROFESSOR E SELECIONANDO ELE
        check_professor_retornado = pagina_1.locator('[id="formFuncionario:funcionarioVOs:0:j_idt121:j_idt121"]')
        expect(check_professor_retornado).to_be_visible(timeout=15000)
        check_professor_retornado.click()
        


        #LOCAL (SALA)
        pagina_1.locator('[id="form:consultaDadosLocalReservado:consultaDadosLocalReservado"]').click()
        pagina_1.locator('[id="formLocalReservado:valorConsultaLocal"]').click()
        pagina_1.locator('[id="formLocalReservado:valorConsultaLocal"]').fill(list(lista_reservas[posicao_reserva].values())[3])

        pagina_1.locator('[id="formLocalReservado:btnConsultarlocalArmazenamentoVOs"]').click()

        check_sala_encontrada = pagina_1.locator('[id="formLocalReservado:localAReservarVOs:0:j_idt189:j_idt189"]')
        expect(check_sala_encontrada).to_be_visible(timeout=15000)
        check_sala_encontrada.click()



        #DATA
        pagina_1.locator('[id="form:dataReserva:dataReserva"]').click()
        pagina_1.locator('[id="form:dataReserva:dataReserva"]').fill("23/11/2026")



        #HORA
        pagina_1.locator('[id="form:horaInicio"]').click()
        pagina_1.locator('[id="form:horaInicio"]').fill("19:00")

        pagina_1.locator('input[name="form:horaFim"]').click()
        pagina_1.locator('input[name="form:horaFim"]').fill("21:50")



        #SALVAR
        pagina_1.get_by_role("link", name="Gravar").click()
        pagina_1.get_by_role("link", name="Novo").click()

        posicao_reserva += 1

    time.sleep(10)
    contexto.close()
    navegador.close()