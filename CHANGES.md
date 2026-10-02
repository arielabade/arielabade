# Registro de alterações do perfil

Reorganização do perfil público para posicionamento em vagas de **Analista de Dados pleno/sênior**,
**Cientista de Dados pleno/sênior** e **ML Engineer pleno**, com foco em marketing, growth e lógica
de negócios.

Data: 2026-10-02 · Executado via `gh` CLI.

**Nenhum repositório foi deletado.** Todas as ações abaixo são reversíveis, e o comando de reversão
está na última coluna.

---

## 1. Diagnóstico dos repositórios públicos

Estado antes da mudança: 12 repositórios públicos, 42 privados.

| Repositório | Linguagem | Tam. | Classificação | Justificativa | Reversão |
| --- | --- | --- | --- | --- | --- |
| `arielabade` | — | 649KB | **MANTER E MELHORAR** | Repositório de perfil; é a primeira coisa que um recrutador lê. | — |
| `carbon` | Jupyter | 7.2MB | **MANTER E MELHORAR** | ML de verdade (BI-LSTM, baselines controlados, paper aceito) — sustenta a candidatura a ML Engineer. | — |
| `mandacaru` | — | 4.5MB | **MANTER E MELHORAR** | Produto real de extração de documentos, com documentação de engenharia; mostra entrega ponta a ponta. | — |
| `visppy-cv` | — | 13.7MB | **MANTER E MELHORAR** | Produto com reconhecimento externo (Centelha SE III); mostra visão de produto além do notebook. | — |
| `echo-womens-health-research-analytics` | Jupyter | 7.5MB | **MANTER** | Rigor estatístico e metodologia de pesquisa; fora do tema de marketing, por isso não é fixado. | — |
| `abade` | HTML | 24KB | **MANTER** | Vira o portfólio público via GitHub Pages. | — |
| `tracking-attribution-lab` | — | 2KB | **ARQUIVAR** | Só documentação e SQL genérico, sem implementação; o tema é coberto com dados reais em `unit-economics-olist` e `ab-testing-toolkit`. | `gh repo unarchive arielabade/tracking-attribution-lab` |
| `marketing-analytics-portfolio` | Python | 4KB | **ARQUIVAR** | Helpers de KPI sobre dados sintéticos; superado por `unit-economics-olist`, que roda sobre dados reais. | `gh repo unarchive arielabade/marketing-analytics-portfolio` |
| `paid-media-budget-optimizer` | Python | 4KB | **ARQUIVAR** | Protótipo baseado em regras com dados sintéticos; superado por `marketing-mix-modeling`, que otimiza orçamento com modelo estatístico. | `gh repo unarchive arielabade/paid-media-budget-optimizer` |
| `spatial-analytics-dashboard` | Python | 3KB | **TORNAR PRIVADO** | Stub sem dashboard e fora do tema marketing/growth; dilui o posicionamento. | `gh repo edit arielabade/spatial-analytics-dashboard --visibility public` |
| `visppy-cv-lab` | Python | 3KB | **TORNAR PRIVADO** | Stub de modelo de eventos; `visppy-cv` já cobre o produto com muito mais substância. | `gh repo edit arielabade/visppy-cv-lab --visibility public` |
| `miscellaneous` | Jupyter | 3.8MB | **TORNAR PRIVADO** | Exercícios de graduação; para vaga pleno/sênior, trabalha contra o posicionamento. | `gh repo edit arielabade/miscellaneous --visibility public` |

### Critério usado

Arquivar manteve público o que é **coerente com o tema** mas foi superado por trabalho melhor —
serve como registro histórico. Tornar privado foi aplicado ao que é **fora do tema** ou **sinaliza
nível júnior**, porque esses pesam contra na triagem.

Repositórios arquivados continuam visíveis e somente leitura. Repositórios privados saem do perfil
público mas não são perdidos.

---

## 2. Alterações de conteúdo em repositórios mantidos

| Repositório | Alteração |
| --- | --- |
| `visppy-cv` | Removida a referência a `visppy-cv-lab`, que passou a privado e deixaria um link quebrado. |
| `carbon` | Topics adicionados: `deep-learning`, `tensorflow`, `keras`, `sequence-modeling`, `python`. |
| `mandacaru` | Topics adicionados: `document-ai`, `information-extraction`, `nlp`, `python`, `product-engineering`. |
| `echo-womens-health-research-analytics` | Topics adicionados: `statistics`, `python`, `survey-analysis`, `scientific-computing`. |
| `abade` | Topics adicionados e **GitHub Pages ativado**: https://arielabade.github.io/abade/ |

---

## 3. Projetos novos criados

Seis projetos novos, cada um com dados reais e públicos, README em inglês na estrutura padrão
(business problem → key results → data → approach → business metrics → limitations → how to run),
testes e `INTERVIEW_NOTES.md` em português.

| Repositório | Problema de negócio | Dados |
| --- | --- | --- |
| `unit-economics-olist` | CAC, LTV, payback e margem por canal | Olist (real) + gasto de mídia simulado, declarado |
| `clv-cohort-prediction` | Previsão de LTV e retenção por coorte | Olist (real) |
| `lead-scoring-api` | Priorização de leads por propensão | Bank Marketing, UCI (real) |
| `marketing-mix-modeling` | ROI por canal e alocação de orçamento | Simulado com processo gerador conhecido, declarado |
| `churn-cost-sensitive` | Limiar de retenção por valor esperado | Telco IBM (real) |
| `ab-testing-toolkit` | Dimensionamento e leitura de experimentos | Simulado para validação estatística, declarado |

> O dataset de funil de marketing da Olist (MQL + closed deals) exigiria credencial do Kaggle e não
> tem mirror público. `lead-scoring-api` usa o Bank Marketing (UCI), que é um funil de marketing real
> e reproduzível sem login.

---

## Como reverter tudo

```bash
gh repo unarchive arielabade/tracking-attribution-lab
gh repo unarchive arielabade/marketing-analytics-portfolio
gh repo unarchive arielabade/paid-media-budget-optimizer
gh repo edit arielabade/spatial-analytics-dashboard --visibility public
gh repo edit arielabade/visppy-cv-lab --visibility public
gh repo edit arielabade/miscellaneous --visibility public
```
