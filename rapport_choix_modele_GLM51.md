**HIREBOX DATA**

**Rapport de Choix du Modèle**

Modèle sélectionné : zai-org/GLM-5.1

Avril 2026

# **1. Contexte du projet**
Le projet HireBox Data vise à automatiser la génération de questions d'entretien personnalisées à partir du contenu d'un CV de candidat. Pour chaque CV soumis, le système doit analyser les expériences, compétences et formations mentionnées, puis produire une question pertinente et ciblée, permettant d'approfondir un point précis du parcours du candidat.

Ce rapport documente le processus de sélection du modèle de langage (LLM) retenu pour accomplir cette tâche, en explicitant les critères d'évaluation et les raisons du choix de GLM-5.1 de la société Z.ai.

# **2. Critères de sélection**
Le choix du modèle a été guidé par les critères suivants, par ordre de priorité :

- Compréhension profonde de textes longs et structurés (CV multi-sections)
- Capacité à extraire des informations clés et à les mettre en relation
- Qualité et pertinence de la génération de texte en contexte conversationnel
- Performances mesurées sur des benchmarks de raisonnement et de compréhension
- Disponibilité via API et facilité d'intégration dans un pipeline Python/HuggingFace
- Licence ouverte permettant un usage dans un projet d'équipe

# **3. Présentation du modèle GLM-5.1**
GLM-5.1 est le modèle phare de nouvelle génération de Z.ai, développé pour l'ingénierie agentique. Il s'agit d'un modèle à architecture MoE (Mixture of Experts) de 754 milliards de paramètres, publié sous licence MIT sur HuggingFace. Il succède à GLM-5 avec des améliorations significatives sur les tâches longue durée, la résolution de problèmes ambigus et l'utilisation d'outils.

## **3.1 Caractéristiques techniques**
- Architecture : GLM MoE DSA (Mixture of Experts avec Dynamic Sparse Attention)
- Taille : 754 milliards de paramètres (BF16 / F32)
- Langues : Anglais et Chinois (multilingue de fait)
- Licence : MIT — usage libre, y compris commercial
- Disponible via : API Z.ai, SGLang, vLLM, Transformers HuggingFace
- Publication : Février 2026 — modèle récent et maintenu activement

## **3.2 Capacités spécifiques pertinentes pour HireBox**
GLM-5.1 a été conçu pour maintenir une performance élevée sur des tâches complexes et longues. Cette caractéristique est directement utile pour notre cas d'usage : un CV peut contenir de nombreuses sections (expériences, formations, projets, compétences) et le modèle doit en extraire un élément saillant pour formuler une question pertinente.

Le modèle se distingue notamment par sa capacité à décomposer des problèmes complexes, à relire son raisonnement et à réviser sa stratégie — ce qui se traduit par des réponses plus précises et contextualisées dans notre pipeline.

# **4. Analyse des performances — Benchmark**
Le tableau ci-dessous présente les résultats de GLM-5.1 comparés aux principaux modèles concurrents sur les benchmarks officiels publiés par Z.ai. Les scores en surbrillance (★) indiquent les domaines où GLM-5.1 atteint la 1ère place.

|**Benchmark**|**GLM-5.1**|**GLM-5**|**DeepSeek-V3.2**|**Kimi K2.5**|**Claude Opus 4.6**|**GPT-5.4**|
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
|HLE|**31.0**|30\.5|25\.1|31\.5|36\.7|39\.8|
|HLE (avec outils)|**52.3**|50\.4|40\.8|51\.8|53\.1|52\.1|
|SWE-Bench Pro|**58.4 ★**|55\.1|-|53\.8|57\.3|57\.7|
|GPQA-Diamond|**86.2**|86\.0|82\.4|87\.6|91\.3|92\.0|
|CyberGym|**68.7 ★**|48\.3|17\.3|41\.3|66\.6|-|
|BrowseComp|**68.0 ★**|62\.0|51\.4|60\.6|-|-|

*Source : https://huggingface.co/zai-org/GLM-5.1#benchmark*

## **4.1 Points forts relevés**
- SWE-Bench Pro (58.4) : 1ère place mondiale — mesure la résolution de problèmes de code réels dans des dépôts entiers, ce qui valide la capacité du modèle à raisonner sur des documents complexes et structurés.
- CyberGym (68.7) : 1ère place — aptitude à résoudre des problèmes inédits nécessitant du raisonnement multi-étapes, directement transposable à l'analyse d'un CV varié.
- BrowseComp (68.0) : 1ère place — excellente capacité de recherche et d'extraction d'informations dans des documents, ce qui correspond précisément à la lecture d'un CV.
- HLE avec outils (52.3) : score très compétitif face aux meilleurs modèles du marché (Claude Opus : 53.1, GPT-5.4 : 52.1), confirmant que GLM-5.1 rivalise avec les modèles propriétaires les plus puissants.

## **4.2 Nuances et limites**
- Sur les benchmarks de mathématiques pures (AIME, HMMT), GLM-5.1 est compétitif mais ne domine pas. Ces benchmarks ne sont pas prioritaires pour notre cas d'usage.
- Sur HLE sans outils (31.0) et GPQA-Diamond (86.2), le modèle est légèrement en retrait face à Gemini ou GPT-5.4. Cependant, notre application ne nécessite pas ce niveau de raisonnement scientifique expert.

# **5. Justification du choix**
Au regard des critères définis en section 2, GLM-5.1 s'impose comme le meilleur choix pour les raisons suivantes :

## **5.1 Adéquation avec le cas d'usage**
La génération d'une question à partir d'un CV est une tâche de compréhension et d'extraction de contenu textuel structuré, suivie d'une génération de texte contextualisée. GLM-5.1 excelle précisément sur ces dimensions (BrowseComp, SWE-Bench Pro, CyberGym), ce qui en fait un choix naturel.
## **5.2 Performance de niveau état de l'art**
GLM-5.1 rivalise avec Claude Opus 4.6 et GPT-5.4 — deux des modèles propriétaires les plus performants au monde — sur les benchmarks les plus pertinents pour notre projet. Il obtient même la 1ère place sur plusieurs d'entre eux, à un coût d'utilisation moindre.
## **5.3 Accessibilité et intégration**
Le modèle est disponible directement sur HuggingFace et compatible avec les bibliothèques standard de l'écosystème Python (transformers, vLLM, SGLang). Son intégration dans notre pipeline de données est donc fluide et ne nécessite pas d'infrastructure propriétaire.
## **5.4 Licence ouverte**
La licence MIT de GLM-5.1 garantit une liberté totale d'utilisation, de modification et de déploiement, sans restriction commerciale. C'est un avantage déterminant pour un projet d'équipe en cours de développement.

# **6. Conclusion**
*GLM-5.1 est le modèle le mieux adapté au projet HireBox Data. Il combine des performances de niveau état de l'art sur les tâches de compréhension de documents et de génération contextuelle, une architecture ouverte et accessible, et une licence libre. Il constitue un choix solide, fondé sur des benchmarks objectifs, pour alimenter notre système de génération de questions personnalisées à partir de CV.*


**Références**

[1] GLM-5.1 Model Card — https://huggingface.co/zai-org/GLM-5.1

[2] GLM-5 Technical Report — https://arxiv.org/abs/2602.15763

[3] Z.ai Blog — GLM-5.1 — https://z.ai/blog/glm-5.1
HireBox Data — Rapport de choix du modèle
