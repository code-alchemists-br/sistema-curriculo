import type { SugestaoVaga } from "../../../entities/vaga";
import type { ClienteDecisoesRecomendacao } from "./cliente-decisoes-recomendacao";
import {
  adaptarRespostaGrupo2,
  type ClienteVagasGrupo2,
  type CriteriosPesquisaVagas,
} from "./cliente-vagas-grupo2";

export const RESPOSTA_MATCHES_DEMONSTRACAO = {
  curriculo_id: "curriculo-demo-01",
  matches: [
    {
      rank: 1,
      job: {
        id: "vaga-demo-01",
        company: "TechLab Soluções Digitais",
        title: "Desenvolvedor(a) Frontend Júnior",
        description:
          "Atuação no desenvolvimento e evolução de interfaces web acessíveis e responsivas, utilizando React, TypeScript e padrões de usabilidade modernos.",
        keywords: ["Frontend", "Design System", "Acessibilidade Web"],
        location: {
          city: "São Paulo",
          state: "SP",
        },
        work_arrangement: "HYBRID",
        seniority_level: "JUNIOR",
        skills: [
          "React",
          "TypeScript",
          "HTML5 Semântico & CSS3",
          "Git & GitHub",
          "Boas práticas de acessibilidade (WCAG)",
        ],
        salary: {
          min: 3500,
          max: 4500,
        },
        currency: "BRL",
        job_url: "https://carreiras.techlab.com.br/vagas/frontend-jr",
        publication_date: "2026-11-01T04:11:59.870Z",
      },
      score: 96,
      embedding_model: "text-embedding-3-small",
      algorithm_version: "1.0.0",
    },
    {
      rank: 2,
      job: {
        id: "vaga-demo-02",
        company: "Inovação & Sistemas Cloud",
        title: "Estágio em Engenharia de Software",
        description:
          "Oportunidade para estudantes participarem ativamente de equipes ágeis na criação de dashboards interativos, componentes reutilizáveis e integração de APIs.",
        keywords: ["Estágio TI", "Cloud", "APIs REST"],
        location: {
          country: "Brasil",
        },
        work_arrangement: "REMOTE",
        seniority_level: "INTERN",
        skills: [
          "JavaScript / TypeScript",
          "Lógica de Programação",
          "Testes Automatizados",
          "Trabalho em Equipe",
        ],
        salary: {
          bolsa: 1800,
        },
        currency: "BRL",
        job_url: "https://inovacao.cloud/estagio-software",
        publication_date: "2026-10-29T14:30:00.000Z",
      },
      score: 89,
      embedding_model: "text-embedding-3-small",
      algorithm_version: "1.0.0",
    },
    {
      rank: 3,
      job: {
        id: "vaga-demo-03",
        company: "Alquimia Dados & Tecnologia",
        title: "Desenvolvedor(a) Full Stack Júnior",
        description:
          "Integração de serviços RESTful em Python/Node.js com frontends dinâmicos em React, participando de code reviews e deploys contínuos.",
        keywords: ["Full Stack", "Microsserviços"],
        location: {
          city: "Campinas",
          state: "SP",
        },
        work_arrangement: "ONSITE",
        seniority_level: "JUNIOR",
        skills: [
          "React",
          "Python ou Node.js",
          "Bancos de Dados SQL",
          "Conceitos de Docker",
        ],
        salary: {
          min: 0,
          max: 0,
        },
        currency: "BRL",
        job_url: "https://alquimiatech.com.br/vagas/fullstack",
        publication_date: null,
      },
      score: 82,
      embedding_model: "text-embedding-3-small",
      algorithm_version: "1.0.0",
    },
    {
      rank: 4,
      job: {
        id: "vaga-demo-04",
        title: "Desenvolvedor(a) Web",
        description:
          "Manutenção evolutiva e criação de novas landing pages e módulos web para o portal corporativo.",
        job_url: "https://oportunidades.exemplo.com/vagas/web-geral",
      },
      score: 74,
      embedding_model: "text-embedding-3-small",
      algorithm_version: "1.0.0",
    },
  ],
};

export const VAGAS_DEMONSTRACAO: SugestaoVaga[] = adaptarRespostaGrupo2(
  RESPOSTA_MATCHES_DEMONSTRACAO,
);

export function criarClienteVagasDemonstracao(
  vagasIniciais: SugestaoVaga[] = VAGAS_DEMONSTRACAO,
): ClienteVagasGrupo2 {
  return {
    async listarSugestoes(
      criterios: CriteriosPesquisaVagas,
    ): Promise<SugestaoVaga[]> {
      const termoLimpo = criterios.termo.trim().toLowerCase();
      if (!termoLimpo) {
        return vagasIniciais;
      }
      return vagasIniciais.filter(({ vaga }) => {
        const noTitulo = vaga.titulo.toLowerCase().includes(termoLimpo);
        const naEmpresa = vaga.empresa.toLowerCase().includes(termoLimpo);
        const naDescricao = vaga.descricao.toLowerCase().includes(termoLimpo);
        const nosRequisitos = vaga.requisitos.some((req) =>
          req.toLowerCase().includes(termoLimpo),
        );
        const nasPalavrasChave = vaga.palavrasChave?.some((kw) =>
          kw.toLowerCase().includes(termoLimpo),
        );
        const naModalidade = vaga.modalidade
          ?.toLowerCase()
          .includes(termoLimpo);
        const naLocalizacao = vaga.localizacao
          ?.toLowerCase()
          .includes(termoLimpo);
        const naSenioridade = vaga.nivelSenioridade
          ?.toLowerCase()
          .includes(termoLimpo);
        return Boolean(
          noTitulo ||
          naEmpresa ||
          naDescricao ||
          nosRequisitos ||
          nasPalavrasChave ||
          naModalidade ||
          naLocalizacao ||
          naSenioridade,
        );
      });
    },
  };
}

export function criarClienteDecisoesDemonstracao(): ClienteDecisoesRecomendacao {
  return {
    async salvarDecisao(): Promise<void> {
      await new Promise((resolve) => setTimeout(resolve, 300));
    },
  };
}
