import { useEffect, useRef, useState } from "react";

import "./CabecalhoPublico.css";

export interface CabecalhoPublicoProps {
  onNavegarCadastro?: () => void;
  onNavegarLogin?: () => void;
  onNavegarInicio?: () => void;
  onNavegarVagas?: () => void;
  onNavegarPerfil?: () => void;
  textoBotaoRetorno?: string;
  onRetorno?: () => void;
}

export function CabecalhoPublico({
  onNavegarCadastro,
  onNavegarLogin,
  onNavegarInicio,
  onNavegarVagas,
  onNavegarPerfil,
  textoBotaoRetorno,
  onRetorno,
}: CabecalhoPublicoProps) {
  const [menuAberto, setMenuAberto] = useState(false);
  const menuWrapperRef = useRef<HTMLDivElement | null>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (!menuAberto) return;

    function aoClicarFora(event: MouseEvent) {
      if (
        menuWrapperRef.current &&
        !menuWrapperRef.current.contains(event.target as Node)
      ) {
        setMenuAberto(false);
      }
    }

    function aoPressionarTecla(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setMenuAberto(false);
        triggerRef.current?.focus();
      }
    }

    document.addEventListener("mousedown", aoClicarFora);
    document.addEventListener("keydown", aoPressionarTecla);
    return () => {
      document.removeEventListener("mousedown", aoClicarFora);
      document.removeEventListener("keydown", aoPressionarTecla);
    };
  }, [menuAberto]);

  function acionarOpcaoMenu(callback?: () => void) {
    setMenuAberto(false);
    callback?.();
  }

  return (
    <header className="cabecalho-publico" aria-label="Navegação principal">
      <div className="cabecalho-publico__container">
        <div className="cabecalho-publico__brand">
          <button
            type="button"
            className="cabecalho-publico__logo-btn"
            onClick={onNavegarInicio}
            aria-label="LIMINAL - Voltar para o início"
          >
            LIMINAL
          </button>
        </div>

        <nav
          className="cabecalho-publico__actions"
          aria-label="Acesso e cadastro"
        >
          {textoBotaoRetorno ? (
            <button
              type="button"
              className="cabecalho-publico__btn-retorno"
              onClick={onRetorno ?? onNavegarInicio}
            >
              {textoBotaoRetorno}
            </button>
          ) : (
            <>
              <button
                type="button"
                className="cabecalho-publico__btn-login"
                onClick={onNavegarLogin}
              >
                Fazer login
              </button>
              <button
                type="button"
                className="cabecalho-publico__btn-criar-conta"
                onClick={onNavegarCadastro}
              >
                Criar conta
              </button>

              <span className="cabecalho-publico__divisor" aria-hidden="true" />

              <div
                className="cabecalho-publico__menu-wrapper"
                ref={menuWrapperRef}
              >
                <button
                  ref={triggerRef}
                  type="button"
                  className={`cabecalho-publico__menu-trigger${
                    menuAberto ? " cabecalho-publico__menu-trigger--ativo" : ""
                  }`}
                  aria-label="Menu de navegação e perfil"
                  aria-expanded={menuAberto}
                  aria-haspopup="menu"
                  onClick={() => setMenuAberto((anterior) => !anterior)}
                >
                  <svg
                    className="cabecalho-publico__menu-icone-linhas"
                    viewBox="0 0 18 14"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    aria-hidden="true"
                  >
                    <path
                      d="M1 1.75H17M1 7H17M1 12.25H17"
                      stroke="currentColor"
                      strokeWidth="1.6"
                      strokeLinecap="round"
                    />
                  </svg>
                  <span
                    className="cabecalho-publico__menu-avatar"
                    aria-hidden="true"
                  >
                    <svg
                      viewBox="0 0 16 16"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <circle
                        cx="8"
                        cy="5.25"
                        r="2.75"
                        stroke="currentColor"
                        strokeWidth="1.4"
                      />
                      <path
                        d="M3 13.5C3.6 11.1 5.5 9.75 8 9.75C10.5 9.75 12.4 11.1 13 13.5"
                        stroke="currentColor"
                        strokeWidth="1.4"
                        strokeLinecap="round"
                      />
                    </svg>
                  </span>
                </button>

                {menuAberto && (
                  <div
                    className="cabecalho-publico__menu-dropdown"
                    role="menu"
                    aria-label="Opções rápidas"
                  >
                    <button
                      type="button"
                      role="menuitem"
                      className="cabecalho-publico__menu-item"
                      onClick={() => acionarOpcaoMenu(onNavegarPerfil)}
                    >
                      <svg
                        className="cabecalho-publico__menu-item-icone"
                        viewBox="0 0 20 20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                      >
                        <circle
                          cx="10"
                          cy="6.5"
                          r="3.25"
                          stroke="currentColor"
                          strokeWidth="1.5"
                        />
                        <path
                          d="M4 16.5C4.8 13.6 7.1 12 10 12C12.9 12 15.2 13.6 16 16.5"
                          stroke="currentColor"
                          strokeWidth="1.5"
                          strokeLinecap="round"
                        />
                      </svg>
                      <span>Meu perfil</span>
                    </button>

                    <button
                      type="button"
                      role="menuitem"
                      className="cabecalho-publico__menu-item"
                      onClick={() => acionarOpcaoMenu(onNavegarVagas)}
                    >
                      <svg
                        className="cabecalho-publico__menu-item-icone"
                        viewBox="0 0 20 20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                      >
                        <rect
                          x="2.75"
                          y="6"
                          width="14.5"
                          height="10.5"
                          rx="2.25"
                          stroke="currentColor"
                          strokeWidth="1.5"
                        />
                        <path
                          d="M7 6V4.75C7 3.7835 7.7835 3 8.75 3H11.25C12.2165 3 13 3.7835 13 4.75V6"
                          stroke="currentColor"
                          strokeWidth="1.5"
                        />
                        <path
                          d="M2.75 10.5H17.25"
                          stroke="currentColor"
                          strokeWidth="1.4"
                        />
                      </svg>
                      <span>Vagas</span>
                    </button>
                  </div>
                )}
              </div>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
