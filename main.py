import os 
from dotenv import load_dotenv


from playwright.sync_api import sync_playwright, TimeoutError, expect

import time


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


    ##SELECIONANDO TIPO OCORRENCIA
    pagina_1.locator('[id="form:tipoOcorrencia"]').select_option("RESERVA_LOCAL")

    ##INSERINDO MOTIVO DA RESERVA 
    pagina_1.locator('textarea[name="form:j_idt270"]').click()
    pagina_1.locator('textarea[name="form:j_idt270"]').fill("Motivo Reserva")

    ##INSERINDO NOME DO PROFESSOR
    pagina_1.locator('[id="form:consultasolicitanteEmprestimo:consultasolicitanteEmprestimo"]').click()
    pagina_1.locator('[id="formFuncionario:valorConsultaFuncionario"]').click()
    pagina_1.locator('[id="formFuncionario:valorConsultaFuncionario"]').fill("Maycon Douglas")

    pagina_1.locator('[id="formFuncionario:btnConsultarFuncionario"]').click()

    

    #VERIFICANDO SE O BANCO DE DADOS CARREGOU ALGUM PROFESSOR E SELECIONANDO ELE
    check_professor_retornado = pagina_1.locator('[id="formFuncionario:funcionarioVOs:0:j_idt121:j_idt121"]')
    expect(check_professor_retornado).to_be_visible(timeout=15000)
    check_professor_retornado.click()
    


    #LOCAL (SALA)
    pagina_1.locator('[id="form:consultaDadosLocalReservado:consultaDadosLocalReservado"]').click()
    pagina_1.locator('[id="formLocalReservado:valorConsultaLocal"]').click()
    pagina_1.locator('[id="formLocalReservado:valorConsultaLocal"]').fill("204")

    pagina_1.locator('[id="formLocalReservado:btnConsultarlocalArmazenamentoVOs"]').click()

    check_sala_encontrada = pagina_1.locator('[id="formLocalReservado:localAReservarVOs:0:j_idt189:j_idt189"]')
    expect(check_sala_encontrada).to_be_visible(timeout=15000)
    check_sala_encontrada.click()



    #DATA
    pagina_1.locator('[id="form:dataReserva:dataReserva"]').click()
    pagina_1.locator('[id="form:dataReserva:dataReserva"]').fill("12/11/2026")



    #HORA
    pagina_1.locator('[id="form:horaInicio"]').click()
    pagina_1.locator('[id="form:horaInicio"]').fill("18:00")

    pagina_1.locator('input[name="form:horaFim"]').click()
    pagina_1.locator('input[name="form:horaFim"]').fill("19:00")



    #SALVAR
    pagina_1.get_by_role("link", name="Gravar").click()

    time.sleep(15)
    contexto.close()
    navegador.close()