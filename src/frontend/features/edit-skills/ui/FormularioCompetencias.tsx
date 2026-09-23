import { useState, type KeyboardEvent } from "react";

import "./FormularioCompetencias.css";

import {
  adicionarHabilidade,
  HARD_SKILLS_SUGERIDAS,
  removerHabilidade,
  SOFT_SKILLS_SUGERIDAS,
  type Habilidades,
  type TipoHabilidade
} from "../model/habilidades";

/**
 * Define os valores iniciais e o callback opcional de persistência da tela.
 */
export interface FormularioCompetenciasProps {
  habilidadesIniciais?: Habilidades;
  onSalvar?: (habilidades: Habilidades) => void;
}

const VALORES_INICIAIS: Habilidades = {
  hardSkills: [],
  softSkills: []
};

/**
 * Renderiza a tela de cadastro de competências técnicas e comportamentais.
 *
 * Mantém o estado de edição local, transforma o texto do input em uma tag
 * quando Enter é pressionado e permite remover ou selecionar competências.
 * A persistência fica atrás do callback opcional para que a feature não dependa
 * diretamente de HTTP ou de uma implementação de backend ainda inexistente.
 */
export function FormularioCompetencias({
  habilidadesIniciais = VALORES_INICIAIS,
  onSalvar
}: FormularioCompetenciasProps) {
  const [hardSkills, setHardSkills] = useState(habilidadesIniciais.hardSkills);
  const [softSkills, setSoftSkills] = useState(habilidadesIniciais.softSkills);
  const [inputHardSkill, setInputHardSkill] = useState("");
  const [inputSoftSkill, setInputSoftSkill] = useState("");

  /**
   * Adiciona uma competência à categoria escolhida e limpa seu input.
   */
  function adicionarSkill(tipo: TipoHabilidade, habilidade: string): void {
    if (tipo === "hard") {
      setHardSkills((atuais) => adicionarHabilidade(atuais, habilidade));
      setInputHardSkill("");
      return;
    }

    setSoftSkills((atuais) => adicionarHabilidade(atuais, habilidade));
    setInputSoftSkill("");
  }

  /**
   * Remove uma competência da categoria escolhida.
   */
  function removerSkill(tipo: TipoHabilidade, habilidade: string): void {
    if (tipo === "hard") {
      setHardSkills((atuais) => removerHabilidade(atuais, habilidade));
      return;
    }

    setSoftSkills((atuais) => removerHabilidade(atuais, habilidade));
  }

  /**
   * Converte o conteúdo do input em uma competência quando Enter é pressionado.
   */
  function lidarComTecla(
    evento: KeyboardEvent<HTMLInputElement>,
    tipo: TipoHabilidade
  ): void {
    if (evento.key !== "Enter") {
      return;
    }

    evento.preventDefault();

    const habilidade = tipo === "hard" ? inputHardSkill : inputSoftSkill;
    adicionarSkill(tipo, habilidade);
  }

  /**
   * Encaminha as competências atuais ao consumidor da feature.
   */
  function salvar(): void {
    onSalvar?.({
      hardSkills,
      softSkills
    });
  }

  return (
    <form className="skills-form" onSubmit={(evento) => {
      evento.preventDefault();
      salvar();
    }}>
      <section aria-labelledby="hard-skills-titulo" className="skills-section">
        <div className="skills-section__heading">
          <h2 id="hard-skills-titulo">Hard Skills</h2>
          <p>Competências técnicas e conhecimentos específicos da sua área.</p>
        </div>

        <label htmlFor="hard-skill-input">Adicionar competência técnica</label>
        <input
          id="hard-skill-input"
          name="hardSkill"
          type="text"
          value={inputHardSkill}
          onChange={(evento) => setInputHardSkill(evento.target.value)}
          onKeyDown={(evento) => lidarComTecla(evento, "hard")}
          placeholder="Digite uma competência e pressione Enter"
        />

        <div
          aria-label="Hard Skills selecionadas"
          className="skills-chips"
        >
          {hardSkills.map((habilidade) => (
            <span className="skill-chip" key={habilidade}>
              <span>{habilidade}</span>
              <button
                aria-label={`Remover ${habilidade}`}
                className="skill-chip__remove"
                type="button"
                onClick={() => removerSkill("hard", habilidade)}
              >
                ×
              </button>
            </span>
          ))}
        </div>

        <div className="skills-suggestions">
          <h3>Sugestões de Hard Skills</h3>
          <div className="skills-suggestions__list">
            {HARD_SKILLS_SUGERIDAS.map((habilidade) => (
              <button
                className="skill-suggestion"
                disabled={hardSkills.includes(habilidade)}
                key={habilidade}
                type="button"
                onClick={() => adicionarSkill("hard", habilidade)}
              >
                {habilidade}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section aria-labelledby="soft-skills-titulo" className="skills-section">
        <div className="skills-section__heading">
          <h2 id="soft-skills-titulo">Soft Skills</h2>
          <p>Competências comportamentais e habilidades interpessoais.</p>
        </div>

        <label htmlFor="soft-skill-input">
          Adicionar competência comportamental
        </label>
        <input
          id="soft-skill-input"
          name="softSkill"
          type="text"
          value={inputSoftSkill}
          onChange={(evento) => setInputSoftSkill(evento.target.value)}
          onKeyDown={(evento) => lidarComTecla(evento, "soft")}
          placeholder="Digite uma competência e pressione Enter"
        />

        <div
          aria-label="Soft Skills selecionadas"
          className="skills-chips"
        >
          {softSkills.map((habilidade) => (
            <span className="skill-chip" key={habilidade}>
              <span>{habilidade}</span>
              <button
                aria-label={`Remover ${habilidade}`}
                className="skill-chip__remove"
                type="button"
                onClick={() => removerSkill("soft", habilidade)}
              >
                ×
              </button>
            </span>
          ))}
        </div>

        <div className="skills-suggestions">
          <h3>Sugestões de Soft Skills</h3>
          <div className="skills-suggestions__list">
            {SOFT_SKILLS_SUGERIDAS.map((habilidade) => (
              <button
                className="skill-suggestion"
                disabled={softSkills.includes(habilidade)}
                key={habilidade}
                type="button"
                onClick={() => adicionarSkill("soft", habilidade)}
              >
                {habilidade}
              </button>
            ))}
          </div>
        </div>
      </section>

      <button type="submit">Salvar competências</button>
    </form>
  );
}
