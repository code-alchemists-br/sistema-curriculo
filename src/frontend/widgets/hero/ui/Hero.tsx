import { useEffect, useRef } from "react";

import imagemHero from "../../../shared/assets/images/imagem_hero.webp";
import "./Hero.css";

export interface HeroProps {
  onCriarCurriculo?: () => void;
}

export function Hero({ onCriarCurriculo }: HeroProps) {
  const buttonRef = useRef<HTMLButtonElement | null>(null);
  const lightEffectRef = useRef<HTMLDivElement | null>(null);
  const rightOuterGlowRef = useRef<HTMLDivElement | null>(null);
  const leftOuterGlowRef = useRef<HTMLDivElement | null>(null);
  const leaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const button = buttonRef.current;
    const lightEffect = lightEffectRef.current;
    const rightOuterGlow = rightOuterGlowRef.current;
    const leftOuterGlow = leftOuterGlowRef.current;

    if (!button || !lightEffect || !rightOuterGlow || !leftOuterGlow) return;

    function getRightSidePosition() {
      return (button?.offsetWidth ?? 240) - 110;
    }

    const timer = setTimeout(() => {
      if (lightEffect) {
        lightEffect.style.transform = `translateX(${getRightSidePosition()}px) translateZ(0px)`;
      }
      if (rightOuterGlow) rightOuterGlow.style.opacity = "1";
      if (leftOuterGlow) leftOuterGlow.style.opacity = "0";
    }, 50);

    return () => {
      clearTimeout(timer);
      if (leaveTimeoutRef.current) clearTimeout(leaveTimeoutRef.current);
    };
  }, []);

  function handleMouseEnter() {
    if (leaveTimeoutRef.current) clearTimeout(leaveTimeoutRef.current);
    if (lightEffectRef.current)
      lightEffectRef.current.style.transition = "transform 0.1s ease-out";
    if (rightOuterGlowRef.current)
      rightOuterGlowRef.current.style.transition = "opacity 0.2s ease";
    if (leftOuterGlowRef.current)
      leftOuterGlowRef.current.style.transition = "opacity 0.2s ease";
  }

  function handleMouseMove(e: React.MouseEvent<HTMLButtonElement>) {
    const button = buttonRef.current;
    const lightEffect = lightEffectRef.current;
    const rightOuterGlow = rightOuterGlowRef.current;
    const leftOuterGlow = leftOuterGlowRef.current;

    if (!button || !lightEffect || !rightOuterGlow || !leftOuterGlow) return;

    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const lightX = x - 100;
    lightEffect.style.transform = `translateX(${lightX}px) translateZ(0px)`;

    const ratio = x / rect.width;
    const rightOpacity = Math.max(0, (ratio - 0.5) * 2);
    const leftOpacity = Math.max(0, (0.5 - ratio) * 2);

    rightOuterGlow.style.opacity = rightOpacity.toString();
    leftOuterGlow.style.opacity = leftOpacity.toString();
  }

  function handleMouseLeave() {
    const button = buttonRef.current;
    const lightEffect = lightEffectRef.current;
    const rightOuterGlow = rightOuterGlowRef.current;
    const leftOuterGlow = leftOuterGlowRef.current;

    leaveTimeoutRef.current = setTimeout(() => {
      if (!button || !lightEffect || !rightOuterGlow || !leftOuterGlow) return;
      const rightPos = button.offsetWidth - 110;
      lightEffect.style.transition = "transform 0.5s ease";
      lightEffect.style.transform = `translateX(${rightPos}px) translateZ(0px)`;

      rightOuterGlow.style.transition = "opacity 0.5s ease";
      leftOuterGlow.style.transition = "opacity 0.5s ease";
      rightOuterGlow.style.opacity = "1";
      leftOuterGlow.style.opacity = "0";
    }, 1500);
  }

  return (
    <section className="hero-section" aria-labelledby="hero-title">
      <div className="hero-section__container">
        <div className="hero-section__content">
          <h1 id="hero-title" className="hero-section__title">
            O currículo que abre portas
          </h1>

          <p className="hero-section__subtitle">
            Você já aprendeu muita coisa na faculdade. A LIMINAL ajuda você a
            organizar seus projetos, cursos e habilidades em um currículo limpo,
            bonito e que os recrutadores realmente leem.
          </p>

          <div className="hero-section__actions">
            <div className="button-wrapper">
              {/* Outer light leaks (efeito Huly) */}
              <div
                ref={rightOuterGlowRef}
                className="border-button-light-blur"
                id="right-outer-glow"
              >
                <div className="border-button-light" />
              </div>
              <div
                ref={leftOuterGlowRef}
                className="border-button-light-blur flipped"
                id="left-outer-glow"
              >
                <div className="border-button-light" />
              </div>

              {/* Botão interativo */}
              <button
                ref={buttonRef}
                type="button"
                id="interactive-button"
                className="interactive-button"
                aria-label="CRIAR CURRÍCULO →"
                onClick={onCriarCurriculo}
                onMouseEnter={handleMouseEnter}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
              >
                {/* Glow interno reativo */}
                <div
                  ref={lightEffectRef}
                  id="light-effect"
                  className="light-effect"
                >
                  <div className="core-glow" />
                  <div className="wider-blur" />
                </div>

                <span className="button-text">CRIAR CURRÍCULO</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 17 9"
                  className="button-icon"
                  aria-hidden="true"
                >
                  <path
                    fill="currentColor"
                    fillRule="evenodd"
                    d="m12.495 0 4.495 4.495-4.495 4.495-.99-.99 2.805-2.805H0v-1.4h14.31L11.505.99z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="hero-section__visual">
        <img
          src={imagemHero}
          alt="Demonstração visual do currículo gerado pela plataforma LIMINAL com dados e tecnologias estruturadas"
          className="hero-section__image"
          loading="eager"
        />
      </div>

      <div className="hero-section__wave" aria-hidden="true">
        <svg
          viewBox="0 0 1440 80"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="none"
        >
          <path
            d="M0,65 C400,15 1040,15 1440,65 L1440,80 L0,80 Z"
            fill="#050505"
          />
        </svg>
      </div>
    </section>
  );
}
