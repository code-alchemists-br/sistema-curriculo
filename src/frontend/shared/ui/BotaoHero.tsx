import {
  useEffect,
  useRef,
  type ButtonHTMLAttributes,
  type ReactNode,
} from "react";

import "./BotaoHero.css";

export interface BotaoHeroProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  wrapperClassName?: string;
  mostrarIcone?: boolean;
}

/**
 * Botão interativo com o mesmo design e iluminação dinâmica da seção Hero.
 *
 * Inclui vazamento de luz nas bordas (efeito Huly), brilho interno reativo
 * ao ponteiro do mouse, tipografia estilizada e seta direcional SVG.
 */
export function BotaoHero({
  children,
  className = "",
  wrapperClassName = "",
  mostrarIcone = true,
  disabled,
  ...props
}: BotaoHeroProps) {
  const buttonRef = useRef<HTMLButtonElement | null>(null);
  const lightEffectRef = useRef<HTMLDivElement | null>(null);
  const rightOuterGlowRef = useRef<HTMLDivElement | null>(null);
  const leftOuterGlowRef = useRef<HTMLDivElement | null>(null);
  const leaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    function getRightSidePosition() {
      if (!buttonRef.current) return 120;
      return buttonRef.current.offsetWidth - 110;
    }

    const timer = setTimeout(() => {
      const lightEffect = lightEffectRef.current;
      const rightOuterGlow = rightOuterGlowRef.current;
      const leftOuterGlow = leftOuterGlowRef.current;
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
    if (disabled) return;
    if (leaveTimeoutRef.current) clearTimeout(leaveTimeoutRef.current);
    if (lightEffectRef.current)
      lightEffectRef.current.style.transition = "transform 0.1s ease-out";
    if (rightOuterGlowRef.current)
      rightOuterGlowRef.current.style.transition = "opacity 0.2s ease";
    if (leftOuterGlowRef.current)
      leftOuterGlowRef.current.style.transition = "opacity 0.2s ease";
  }

  function handleMouseMove(e: React.MouseEvent<HTMLButtonElement>) {
    if (disabled) return;
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
    if (disabled) return;
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
    <div
      className={`botao-hero-wrapper ${wrapperClassName}`.trim()}
      data-testid="botao-hero-wrapper"
    >
      <div
        ref={rightOuterGlowRef}
        aria-hidden="true"
        className="botao-hero__border-light-blur"
      >
        <div className="botao-hero__border-light" />
      </div>
      <div
        ref={leftOuterGlowRef}
        aria-hidden="true"
        className="botao-hero__border-light-blur flipped"
      >
        <div className="botao-hero__border-light" />
      </div>

      <button
        ref={buttonRef}
        className={`botao-hero__interactive ${className}`.trim()}
        disabled={disabled}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onMouseMove={handleMouseMove}
        {...props}
      >
        <div
          ref={lightEffectRef}
          aria-hidden="true"
          className="botao-hero__light-effect"
        >
          <div className="botao-hero__core-glow" />
          <div className="botao-hero__wider-blur" />
        </div>

        <span className="botao-hero__text">{children}</span>

        {mostrarIcone && (
          <svg
            aria-hidden="true"
            className="botao-hero__icon"
            fill="none"
            viewBox="0 0 17 9"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              clipRule="evenodd"
              d="m12.495 0 4.495 4.495-4.495 4.495-.99-.99 2.805-2.805H0v-1.4h14.31L11.505.99z"
              fill="currentColor"
              fillRule="evenodd"
            />
          </svg>
        )}
      </button>
    </div>
  );
}
