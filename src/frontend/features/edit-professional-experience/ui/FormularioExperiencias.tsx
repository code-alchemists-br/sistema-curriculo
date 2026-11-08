import { useEffect, useState, type FormEvent } from "react";

import {
  LIMITES_EXPERIENCIA,
  criarExperienciaVazia,
  obterDataAtualIso,
  ordenarPorDataDecrescente,
  restringirAno4Digitos,
  validarListaExperiencias,
  type ErrosExperiencia,
  type Experiencia,
} from "../model/experiencias";
import "./FormularioExperiencias.css";

/** Define os valores iniciais e os callbacks do formulário. */
export interface FormularioExperienciasProps {
  aoAlterarProgresso?: (progresso: number) => void;
  experienciasIniciais?: Experiencia[];
  onSalvar?: (experiencias: Experiencia[]) => void;
  onVoltar?: () => void;
  /** Notifica alterações nas experiências para preservação de estado. */
  aoAlterarExperiencias?: (experiencias: Experiencia[]) => void;
}

/**
 * Renderiza e controla o formulário de cadastro de experiências profissionais.
 *
 * O componente mantém um array de experiências no estado local, permite
 * adicionar e remover entradas dinamicamente, desabilita o campo Fim quando
 * "Emprego atual" está marcado, e ordena as experiências cronologicamente
 * antes de chamar o callback de persistência.
 */
export function FormularioExperiencias({
  aoAlterarProgresso,
  experienciasIniciais = [criarExperienciaVazia()],
  onSalvar,
  onVoltar,
  aoAlterarExperiencias,
}: FormularioExperienciasProps) {
  const dataMaximaHoje = obterDataAtualIso();
  const [experiencias, setExperiencias] =
    useState<Experiencia[]>(experienciasIniciais);
  const [erros, setErros] = useState<Record<number, ErrosExperiencia>>({});
  const [mensagem, setMensagem] = useState<string | null>(null);
  const [experienciaRemovida, setExperienciaRemovida] = useState<{
    item: Experiencia;
    indice: number;
  } | null>(null);
  const [experienciasLimpas, setExperienciasLimpas] = useState<
    Experiencia[] | null
  >(null);

  useEffect(() => {
    if (experienciasLimpas) {
      const timer = setTimeout(() => {
        setExperienciasLimpas(null);
      }, 7000);
      return () => clearTimeout(timer);
    }
  }, [experienciasLimpas]);

  useEffect(() => {
    if (experienciaRemovida) {
      const timer = setTimeout(() => {
        setExperienciaRemovida(null);
      }, 7000);
      return () => clearTimeout(timer);
    }
  }, [experienciaRemovida]);

  useEffect(() => {
    aoAlterarExperiencias?.(experiencias);
  }, [experiencias, aoAlterarExperiencias]);

  /** Calcula e notifica o progresso da etapa atual */
  useEffect(() => {
    if (!aoAlterarProgresso) return;
    if (experiencias.length === 0) {
      aoAlterarProgresso(100);
      return;
    }

    let totalObrigatorios = 0;
    let preenchidos = 0;

    experiencias.forEach((exp) => {
      totalObrigatorios += 4;
      if (exp.empresa.trim().length > 0) preenchidos += 1;
      if (exp.cargo.trim().length > 0) preenchidos += 1;
      if (exp.inicio.trim().length > 0) preenchidos += 1;
      if (exp.descricao.trim().length > 0) preenchidos += 1;

      if (!exp.empregoAtual) {
        totalObrigatorios += 1;
        if (exp.fim.trim().length > 0) preenchidos += 1;
      }
    });

    const porcentagem =
      totalObrigatorios > 0
        ? Math.round((preenchidos / totalObrigatorios) * 100)
        : 100;

    aoAlterarProgresso(porcentagem);
  }, [experiencias, aoAlterarProgresso]);

  /** Atualiza um campo de texto de uma experiência pela sua posição. */
  function atualizarCampo(
    indice: number,
    campo: keyof Omit<Experiencia, "empregoAtual">,
    valor: string,
  ): void {
    const valorTratado =
      campo === "inicio" || campo === "fim"
        ? restringirAno4Digitos(valor)
        : valor;
    setExperiencias((atuais) =>
      atuais.map((exp, i) =>
        i === indice ? { ...exp, [campo]: valorTratado } : exp,
      ),
    );
    limparErroDoCampo(indice, campo as keyof ErrosExperiencia);
  }

  /** Alterna o checkbox de emprego atual e limpa o campo Fim quando ativado. */
  function alternarEmpregoAtual(indice: number): void {
    setExperiencias((atuais) =>
      atuais.map((exp, i) => {
        if (i !== indice) return exp;
        const novoValor = !exp.empregoAtual;
        return {
          ...exp,
          empregoAtual: novoValor,
          fim: novoValor ? "" : exp.fim,
        };
      }),
    );
    limparErroDoCampo(indice, "fim");
  }

  /** Remove o erro de um campo específico de uma experiência. */
  function limparErroDoCampo(
    indice: number,
    campo: keyof ErrosExperiencia,
  ): void {
    setErros((atuais) => {
      const errosExp = { ...atuais[indice] };
      delete errosExp[campo];
      const novoMapa = { ...atuais };

      if (Object.keys(errosExp).length === 0) {
        delete novoMapa[indice];
      } else {
        novoMapa[indice] = errosExp;
      }

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Inclui uma nova entrada vazia no final da lista. */
  function adicionarExperiencia(): void {
    setExperiencias((atuais) => [...atuais, criarExperienciaVazia()]);
  }

  /** Remove uma experiência pela sua posição no array com suporte a desfazer. */
  function removerExperiencia(indice: number): void {
    const item = experiencias[indice];
    if (
      item &&
      (item.empresa.trim() || item.cargo.trim() || item.descricao.trim())
    ) {
      setExperienciaRemovida({ item, indice });
    } else {
      setExperienciaRemovida(null);
    }

    setExperiencias((atuais) => atuais.filter((_, i) => i !== indice));
    setErros((atuais) => {
      const novoMapa: Record<number, ErrosExperiencia> = {};

      Object.entries(atuais).forEach(([chave, valor]) => {
        const indiceOriginal = Number(chave);
        if (indiceOriginal < indice) {
          novoMapa[indiceOriginal] = valor;
        } else if (indiceOriginal > indice) {
          novoMapa[indiceOriginal - 1] = valor;
        }
      });

      return novoMapa;
    });
    setMensagem(null);
  }

  /** Restaura a última experiência removida na mesma posição. */
  function desfazerRemocao(): void {
    if (!experienciaRemovida) return;
    setExperiencias((atuais) => {
      const copia = [...atuais];
      copia.splice(experienciaRemovida.indice, 0, experienciaRemovida.item);
      return copia;
    });
    setExperienciaRemovida(null);
  }

  /** Remove todas as experiências da lista com suporte a desfazer. */
  function limparTodasExperiencias(): void {
    const temDados = experiencias.some(
      (e) => e.empresa.trim() || e.cargo.trim() || e.descricao.trim(),
    );
    if (temDados) {
      setExperienciasLimpas(experiencias);
    } else {
      setExperienciasLimpas(null);
    }
    setExperiencias([]);
    setErros({});
    setMensagem(null);
  }

  /** Restaura a lista de experiências que havia sido limpa em massa. */
  function desfazerLimpezaExperiencias(): void {
    if (!experienciasLimpas) return;
    setExperiencias(experienciasLimpas);
    setExperienciasLimpas(null);
  }

  /**
   * Valida, ordena cronologicamente e comunica o status de envio do formulário.
   */
  function enviarFormulario(evento: FormEvent<HTMLFormElement>): void {
    evento.preventDefault();

    if (experiencias.length === 0) {
      onSalvar?.([]);
      setMensagem("Experiências salvas com sucesso.");
      return;
    }

    const novosErros = validarListaExperiencias(experiencias);

    if (Object.keys(novosErros).length > 0) {
      setErros(novosErros);
      setMensagem("Há pendências que precisam ser corrigidas antes de salvar.");
      return;
    }

    const experienciasNormalizadas = experiencias.map((exp) => ({
      empresa: exp.empresa.trim(),
      cargo: exp.cargo.trim(),
      inicio: exp.inicio,
      fim: exp.fim,
      empregoAtual: exp.empregoAtual,
      descricao: exp.descricao.trim(),
    }));

    const experienciasOrdenadas = ordenarPorDataDecrescente(
      experienciasNormalizadas,
    );
    onSalvar?.(experienciasOrdenadas);
    setMensagem("Experiências salvas com sucesso.");
  }

  return (
    <form
      className="formulario-experiencias"
      noValidate
      onSubmit={enviarFormulario}
    >
      {experiencias.length === 0 && (
        <div className="experiencias-vazio" role="status">
          <p className="experiencias-vazio__texto">
            Nenhuma experiência profissional cadastrada.
          </p>
          <p className="experiencias-vazio__subtexto">
            Se você não possui experiência profissional formal ou busca o
            primeiro emprego, pode avançar para a próxima etapa.
          </p>
        </div>
      )}

      {experiencias.map((exp, indice) => {
        const errosExp = erros[indice];
        const prefixo = `exp-${indice}`;

        return (
          <fieldset aria-label={`Experiência ${indice + 1}`} key={prefixo}>
            <legend className="sr-only">Experiência {indice + 1}</legend>

            {experiencias.length > 1 && (
              <div className="experiencia-header">
                <span className="experiencia-header__titulo">
                  Experiência {indice + 1}
                </span>
                <button
                  aria-label={`Remover experiência ${indice + 1}`}
                  className="btn-remover-experiencia"
                  onClick={() => removerExperiencia(indice)}
                  type="button"
                >
                  Remover
                </button>
              </div>
            )}

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-empresa`}
              >
                Nome da empresa
              </label>
              <input
                aria-describedby={
                  errosExp?.empresa !== undefined
                    ? `${prefixo}-empresa-erro`
                    : undefined
                }
                aria-invalid={
                  errosExp?.empresa !== undefined ? true : undefined
                }
                id={`${prefixo}-empresa`}
                maxLength={LIMITES_EXPERIENCIA.empresaMax}
                onChange={(e) =>
                  atualizarCampo(indice, "empresa", e.target.value)
                }
                placeholder="Ex.: Google, Microsoft, FATEC..."
                required
                type="text"
                value={exp.empresa}
              />
              {errosExp?.empresa !== undefined && (
                <p className="field__error" id={`${prefixo}-empresa-erro`}>
                  {errosExp.empresa}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-cargo`}
              >
                Cargo
              </label>
              <input
                aria-describedby={
                  errosExp?.cargo !== undefined
                    ? `${prefixo}-cargo-erro`
                    : undefined
                }
                aria-invalid={errosExp?.cargo !== undefined ? true : undefined}
                id={`${prefixo}-cargo`}
                maxLength={LIMITES_EXPERIENCIA.cargoMax}
                onChange={(e) =>
                  atualizarCampo(indice, "cargo", e.target.value)
                }
                placeholder="Ex.: Desenvolvedor Frontend Jr"
                required
                type="text"
                value={exp.cargo}
              />
              {errosExp?.cargo !== undefined && (
                <p className="field__error" id={`${prefixo}-cargo-erro`}>
                  {errosExp.cargo}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-inicio`}
              >
                Início
              </label>
              <input
                aria-describedby={
                  errosExp?.inicio !== undefined
                    ? `${prefixo}-inicio-erro`
                    : undefined
                }
                aria-invalid={errosExp?.inicio !== undefined ? true : undefined}
                id={`${prefixo}-inicio`}
                max={dataMaximaHoje}
                onChange={(e) =>
                  atualizarCampo(indice, "inicio", e.target.value)
                }
                required
                type="date"
                value={exp.inicio}
              />
              {errosExp?.inicio !== undefined && (
                <p className="field__error" id={`${prefixo}-inicio-erro`}>
                  {errosExp.inicio}
                </p>
              )}
            </div>

            <div className="field">
              <label
                className={`titulo-campo ${!exp.empregoAtual ? "titulo-campo--obrigatorio" : ""}`}
                htmlFor={`${prefixo}-fim`}
              >
                Fim
              </label>
              <input
                aria-describedby={
                  errosExp?.fim !== undefined
                    ? `${prefixo}-fim-erro`
                    : undefined
                }
                aria-invalid={errosExp?.fim !== undefined ? true : undefined}
                disabled={exp.empregoAtual}
                id={`${prefixo}-fim`}
                max={dataMaximaHoje}
                min={exp.inicio || undefined}
                onChange={(e) => atualizarCampo(indice, "fim", e.target.value)}
                required={!exp.empregoAtual}
                type="date"
                value={exp.fim}
              />
              {errosExp?.fim !== undefined && (
                <p className="field__error" id={`${prefixo}-fim-erro`}>
                  {errosExp.fim}
                </p>
              )}
            </div>

            <div className="field-checkbox">
              <label
                className="label-checkbox"
                htmlFor={`${prefixo}-emprego-atual`}
              >
                <input
                  checked={exp.empregoAtual}
                  id={`${prefixo}-emprego-atual`}
                  onChange={() => alternarEmpregoAtual(indice)}
                  type="checkbox"
                />
                Emprego atual
              </label>
            </div>

            <div className="field">
              <label
                className="titulo-campo titulo-campo--obrigatorio"
                htmlFor={`${prefixo}-descricao`}
              >
                Descrição das atividades
              </label>
              <textarea
                aria-describedby={
                  errosExp?.descricao !== undefined
                    ? `${prefixo}-descricao-erro`
                    : undefined
                }
                aria-invalid={
                  errosExp?.descricao !== undefined ? true : undefined
                }
                id={`${prefixo}-descricao`}
                maxLength={LIMITES_EXPERIENCIA.descricaoMax}
                onChange={(e) =>
                  atualizarCampo(indice, "descricao", e.target.value)
                }
                placeholder="Principais responsabilidades, projetos e tecnologias utilizadas..."
                required
                rows={4}
                value={exp.descricao}
              />
              {(() => {
                const totalDescricao = exp.descricao.length;
                const limite = LIMITES_EXPERIENCIA.descricaoMax;
                const classeModificadora =
                  totalDescricao >= limite
                    ? "formulario-experiencias__contador-caracteres--limite"
                    : totalDescricao >= limite * 0.8
                      ? "formulario-experiencias__contador-caracteres--alerta"
                      : "";

                return (
                  <div
                    aria-live="polite"
                    className={`formulario-experiencias__contador-caracteres ${classeModificadora}`.trim()}
                    id={`${prefixo}-descricao-contador`}
                  >
                    {totalDescricao}/{limite} caracteres
                  </div>
                );
              })()}
              {errosExp?.descricao !== undefined && (
                <p className="field__error" id={`${prefixo}-descricao-erro`}>
                  {errosExp.descricao}
                </p>
              )}
            </div>
          </fieldset>
        );
      })}

      {experienciaRemovida && (
        <div className="alerta-desfazer" role="status">
          <span>
            Experiência{" "}
            {experienciaRemovida.item.empresa
              ? `em "${experienciaRemovida.item.empresa}"`
              : ""}{" "}
            removida.
          </span>
          <button
            aria-label="Desfazer remoção da experiência"
            className="btn-desfazer"
            onClick={desfazerRemocao}
            type="button"
          >
            Desfazer
          </button>
        </div>
      )}

      <button
        className="btn-adicionar-experiencia"
        onClick={adicionarExperiencia}
        type="button"
      >
        + Adicionar experiência
      </button>

      {mensagem !== null && (
        <p
          className="form-message"
          role={mensagem.includes("sucesso") ? "status" : "alert"}
        >
          {mensagem}
        </p>
      )}

      <div className="botoes-navegacao">
        {onVoltar && (
          <button
            type="button"
            className="btn-voltar"
            onClick={onVoltar}
            aria-label="Voltar para a etapa anterior"
          >
            Voltar
          </button>
        )}
        <button
          aria-label="Salvar experiências"
          className="btn-proximo"
          type="submit"
        >
          Próximo
        </button>
      </div>

      {experienciasLimpas && (
        <div className="alerta-desfazer" role="status">
          <span>Experiências removidas.</span>
          <button
            aria-label="Desfazer remoção de todas as experiências"
            className="btn-desfazer"
            onClick={desfazerLimpezaExperiencias}
            type="button"
          >
            Desfazer
          </button>
        </div>
      )}

      {experiencias.length > 0 && (
        <button
          className="btn-limpar-experiencias"
          onClick={limparTodasExperiencias}
          type="button"
        >
          Não possuo experiência profissional
        </button>
      )}
    </form>
  );
}
