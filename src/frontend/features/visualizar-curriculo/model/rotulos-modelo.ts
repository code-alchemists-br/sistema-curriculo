/**
 * Nome de exibição de cada modelo de currículo, pela chave do catálogo.
 *
 * - O que faz: traduz a chave técnica do modelo ("ats-simples") no nome
 *   mostrado ao estudante ("ATS simples").
 * - Como faz: mapa fixo, consultado pelas páginas que exibem o modelo.
 * - Qual finalidade atende: manter um único lugar para os nomes dos modelos,
 *   usado na visualização do currículo e no perfil.
 */
export const ROTULOS_MODELO_CURRICULO: Readonly<Record<string, string>> = {
  classico: "Profissional clássico",
  compacto: "Compacto",
  "ats-simples": "ATS simples",
  criativo: "Criativo",
  moderno: "Moderno",
  academico: "Acadêmico",
  "primeiro-emprego": "Primeiro emprego",
};
