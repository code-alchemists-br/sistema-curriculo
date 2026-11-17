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

export function Destaques() {
  const [visivel, setVisivel] = useState(
    () => typeof IntersectionObserver === "undefined",
  );
  const secaoRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const elemento = secaoRef.current;
    if (!elemento || typeof IntersectionObserver === "undefined") return;

    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (entrada.isIntersecting) {
          setVisivel(true);
          observador.disconnect();
        }
      },
      { threshold: 0.15 },
    );

    observador.observe(elemento);

    return () => {
      observador.disconnect();
    };
  }, []);

  return (
    <section
      aria-labelledby="destaques-title"
      className={`destaques-section ${visivel ? "destaques-section--visivel" : ""}`}
      ref={secaoRef}
    >
      <div className="destaques-section__container">
        <h2 className="destaques-section__title" id="destaques-title">
          <span className="destaques-section__title-destaque">
            CONSTRUÍMOS A PONTE ENTRE O SEU TALENTO E A SUA PRÓXIMA ENTREVISTA
            —{" "}
          </span>
          <span className="destaques-section__title-suave">
            DO PRIMEIRO SEMESTRE AO DIPLOMA.
          </span>
        </h2>

        <div
          aria-label="Principais métricas da plataforma"
          className="destaques-section__grid"
          role="list"
        >
          {METRICAS_PADRAO.map((item) => (
            <div
              className="destaques-section__card"
              key={item.id}
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
