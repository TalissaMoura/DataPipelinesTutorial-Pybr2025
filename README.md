# Testes automatizados para data pipelines 

Imagine que você é dono(a) de uma cafeteria super movimentada ☕. Tudo parece calmo… mas será que está *mesmo*?  
Será que houve uma queda estranha nas vendas? O cartão parou de funcionar no horário de pico? E aquele blend especial — está vendendo como pão quente ou acumulando poeira na prateleira?

Neste tutorial, vamos escrever testes para garantir que os dados da sua cafeteria estejam sempre fresquinhos e prontos para a análise. Usaremos as bibliotecas **Great Expectations** e **Pytest** para construir testes que validem a qualidade dos dados de vendas em tempo quase real.

Suponha que você quer saber como está a saúde do seu negócio e disso surgiram as seguintes questões:

- **Estamos vendendo café conforme o esperado hoje?** Ou estamos deixando oportunidades escaparem pelo ralo (ou pela máquina de café)?
- **Há algo de errado com os métodos de pagamento?** Uma queda súbita nas transações pode ser sinal de problema técnico… ou só de que todo mundo esqueceu a carteira em casa.
- **Quais cafés estão bombando?** Conseguimos atender à demanda ou estamos prestes a ter uma revolta de clientes sem seu latte matinal?

Mas calma — antes de responder essas perguntas, precisamos entender **o que medir**.  
“Vendas conforme o esperado” pode significar:  
- Quantidade e valor total dentro de uma faixa razoável?  
- Os tipos diferentes de café (expresso, latte, mocha…) estão tendo uma quantidade de vendas similar ou muito diferentes? Existe algum café vendendo muito mais que outros? é esperado que isso aconteça?  
- Consistência nos métodos de pagamento (cartão, PIX, troco de emergência)?

Com base nisso, definimos algumas métricas-chave para monitorar **a cada hora**:
- Quantidade e valor médio das vendas;
- Vendas por tipo de café e qual café é o mais popular;

Vamos usar o dataset [**Coffee Sales**](https://www.kaggle.com/datasets/navjotkaushal/coffee-sales-dataset) como base e exibir tudo em um **dashboard interativo feito com Streamlit**. Assim, seu cliente só precisa olhar a tela — e confiar que os números ali são tão confiáveis quanto seu barista favorito.

Afinal, se os dados falham… o café pode até estar quente, mas o negócio esfria rápido. ☕🔥

