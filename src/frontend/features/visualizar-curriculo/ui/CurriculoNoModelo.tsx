import type { ComponentType } from "react";

import type { PreviaCurriculo } from "../../../entities/curriculo";
import { ModeloAcademico } from "./ModeloAcademico";
import { ModeloAtsSimples } from "./ModeloAtsSimples";
import { ModeloClassico } from "./ModeloClassico";
import { ModeloCompacto } from "./ModeloCompacto";
import { ModeloCriativo } from "./ModeloCriativo";
import { ModeloModerno } from "./ModeloModerno";
import { ModeloPrimeiroEmprego } from "./ModeloPrimeiroEmprego";

const MODELOS: Readonly<
  Record<string, ComponentType<{ previa: PreviaCurriculo }>>
> = {
  classico: ModeloClassico,
  compacto: ModeloCompacto,
  "ats-simples": ModeloAtsSimples,
  criativo: ModeloCriativo,
  moderno: ModeloModerno,
  academico: ModeloAcademico,
  "primeiro-emprego": ModeloPrimeiroEmprego,
};

/** Props do currículo renderizado em um modelo do catálogo. */
export interface CurriculoNoModeloProps {
  previa: PreviaCurriculo;
  /** Chave do modelo (ex.: "moderno"); chaves desconhecidas usam o clássico. */
  modelo: string;
}

/**
 * Renderiza a prévia do currículo no modelo visual escolhido.
 *
 * - O que faz: escolhe o componente do catálogo pela chave do modelo e repassa a prévia.
 * - Como faz: consulta um mapa chave → componente, com o modelo clássico como padrão.
 * - Qual finalidade atende: permite que páginas diferentes (visualização e perfil)
 *   mostrem o mesmo currículo sem repetir o catálogo de modelos.
 */
export function CurriculoNoModelo({ previa, modelo }: CurriculoNoModeloProps) {
  const Modelo = MODELOS[modelo] ?? ModeloClassico;
  return <Modelo previa={previa} />;
}
