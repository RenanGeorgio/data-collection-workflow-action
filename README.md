# Workflow Execution via GitHub Action

Este repositorio representa o seguinte workflow - 
![image](https://user-images.githubusercontent.com/19303690/130244375-693e0ea2-7d71-4a07-87da-e8dc3332885f.png)

 - O GoogleNews Observer pesquisa e busca artigos de notícias do Google com determinada consulta
 - Em seguida, o TextSplitter divide o artigo em pequenos pedaços para que o Classification Analyzer possa processá-lo facilmente
 - Em seguida, o Classification Analyzer classifica os pedaços em determinados rótulos usando [HuggingFace zero shot models](https://huggingface.co/models?pipeline_tag=zero-shot-classification)
 - Em seguida, o Inference Aggregator agrega a saída de classificação para cada bloco e calcula a inferência final com base em determinada função de agregação
 - E, finalmente, o Slack Informer envia o resultado para um determinado canal do Slack usando API

Screenshot do resutado final -
- Artigo completo
![image](https://user-images.githubusercontent.com/19303690/130246209-91490dfa-3350-4a1e-a502-97e05000d937.png)
- Resultado final da classificação aplciada sobre o artigo
![image](https://user-images.githubusercontent.com/19303690/130246280-e6941719-abda-42e2-a993-a26e08cc38ef.png)


# Referencia
- Update github [action.yml](https://github.com/obsei/demo-workflow-action/blob/main/.github/workflows/action.yml) along with required environment variables (For example scheduling at regular time or based on some event refer [link](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#on) for more detail)

Este [link](https://github.com/obsei/obsei#how-to-use) pode ajudá-lo a coletar credenciais de observadores (Facebook, Twitter etc) e informantes (Slack, Zendesk etc).
