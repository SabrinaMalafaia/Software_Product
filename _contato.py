from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import _rotas


def enviar_email_contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        # Envia e-mail para o destinatário
        msg = Message(f'Além do Pedal - {assunto}',
                      recipients=['rpa.malafaia@gmail.com'])
        msg.html = f'''
        <h2>Detalhes do Contato:</h2>
        <p><strong>Nome:</strong> {nome}</p>
        <p><strong>E-mail:</strong> {email}</p>
        <p><strong>Telefone:</strong> {telefone}</p>
        <p><strong>Assunto:</strong> {assunto}</p>
        <p><strong>Mensagem:</strong> {mensagem}</p>
        '''
        _rotas.mail.send(msg)

        # Envia e-mail de resposta para o remetente
        msg_reply = Message('Além do Pedal',
                            recipients=[email])
        msg_reply.body = '''
        Obrigado por entrar em contato conosco.

        Nossa equipe retornará o contato em breve.

        
        Atenciosamente,
        Equipe Além do Pedal
        '''
        _rotas.mail.send(msg_reply)
