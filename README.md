# Finance-NLP

## Présentation du projet

**Que disent les analystes sur certaines compagnie côtés en bourse ? Est-ce positif ou négatif ? À quel point ?**

Afin de le savoir, nous pouvons analyser certains réseaux sociaux et nouvelles. Par exemple, l'annonce du départ d'un CEO peut entrainer le prix de l'action à la baisse. Cependant, si le CEO ne performait deja pas bien, le marché peut le prendre comme une bonne nouvelle. Il est donc important de nuancer l'analyse de nouvelle avec du contexte. 


Les sources d'informations peuvent être :

- DataMinr
- Bloomberg (nous avons accès à des postes bloomberg grâce à HEC Montreal)


Par exemple, DataMinr a fourni à ses utilisateurs, sur ses terminaux, des alertes spécifiques aux actions et des nouvelles concernant Dell qui peuvent avoir une incidence sur le marché.


## Différences entre l'analyse de sentiment 'classique' et 'financière'

L'analyse des sentiments financiers est différente de l'analyse des sentiments de routine. Elle est différente à la fois dans son domaine et dans son objectif. Dans l'analyse de sentiment ordinaire, l'objectif est de trouver si l'information est intrinsèquement positive ou non. Cependant, dans l'analyse du sentiment financier basée sur le NLP, l'objectif est de voir si le marché va réagir à la nouvelle et si le cours de l'action va baisser ou augmenter.


## Quel modèle de NLP pré entrainé à notre disposition ?

BioBERT, un modèle de représentation du langage biomédical pré-entraîné pour l'exploration de textes biomédicaux, s'est avéré très utile pour les soins de santé et les chercheurs travaillent maintenant à l'adaptation de BERT dans le domaine financier. FinBERT est l'un de ces modèles développés pour le secteur des services financiers. FinBERT fonctionne sur un ensemble de données qui contient des nouvelles financières de Reuters. Pour attribuer le sentiment, une banque de phrases a été utilisée. Elle se compose d'environ 4 000 phrases étiquetées par différentes personnes issues du monde des affaires ou de la finance. 

Dans l'analyse habituelle des sentiments, une déclaration positive implique une émotion positive. Mais dans la banque de phrases financières, un sentiment négatif implique que le cours de l'action de l'entreprise peut chuter à cause de la nouvelle publiée. FinBERT a donné de bons résultats avec une précision de 0,97 et un F1 de 0,95, ce qui est nettement supérieur aux autres outils disponibles. La bibliothèque FinBERT est ouverte sur GitHub avec les données pertinentes. Ce modèle linguistique robuste pour la classification du sentiment économique peut être utilisé à différentes fins.


