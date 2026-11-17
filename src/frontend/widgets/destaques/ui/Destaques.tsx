import { useEffect, useRef, useState } from "react";

import "./Destaques.css";

export interface MetricaItem {
  id: string;
  valor: string;
  descricaoLinha1: string;
  descricaoLinha2: string;
}

const METRICAS_PADRAO: MetricaItem[] = [
  {
    id: "tempo",
    valor: "< 10 min",
    descricaoLinha1: "Do cadastro ao currículo",
    descricaoLinha2: "pronto",
  },
  {
    id: "custo",
    valor: "100%",
    descricaoLinha1: "Gratuito e sem",
    descricaoLinha2: "pegadinhas",
  },
  {
    id: "formatos",
    valor: "2 formatos",
    descricaoLinha1: "Prontos para envio:",
    descricaoLinha2: "PDF e Word",
  },
];

function obterVisibilidadeInicial(): boolean {
  if (typeof window === "undefined") {
    return false;
  }
  const suportaObserver = typeof window.IntersectionObserver === "function";
  const prefereReducaoMovimento =
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  return !suportaObserver || prefereReducaoMovimento;
}

export function Destaques() {
  const [visivel, setVisivel] = useState(obterVisibilidadeInicial);
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (visivel) {
      return;
    }

    const elemento = containerRef.current;
    if (!elemento) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry?.isIntersecting) {
          setVisivel(true);
          observer.disconnect();
        }
      },
      {
        threshold: 0.1,
        rootMargin: "0px 0px -60px 0px",
      },
    );

    observer.observe(elemento);

    return () => {
      observer.disconnect();
    };
  }, [visivel]);

  return (
    <section
      className={`destaques-section ${visivel ? "destaques-section--visivel" : ""}`.trim()}
      aria-labelledby="destaques-title"
    >
      <div ref={containerRef} className="destaques-section__container">
        <h2 id="destaques-title" className="destaques-section__title">
          <span className="destaques-section__title-destaque">
            CONSTRUÍMOS A PONTE ENTRE O SEU TALENTO E A SUA PRÓXIMA ENTREVISTA
            —{" "}
          </span>
          <span className="destaques-section__title-suave">
            DO PRIMEIRO SEMESTRE AO DIPLOMA.
          </span>
        </h2>

        <div
          className="destaques-section__grid"
          role="list"
          aria-label="Principais métricas da plataforma"
        >
          {METRICAS_PADRAO.map((item) => (
            <div
              key={item.id}
              className="destaques-section__card"
              role="listitem"
            >
              <div className="destaques-section__valor">{item.valor}</div>
              <p className="destaques-section__descricao">
                {item.descricaoLinha1}
                <br />
                {item.descricaoLinha2}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
