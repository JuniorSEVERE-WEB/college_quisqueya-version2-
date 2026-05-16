/**
 * Écran "Connexion impossible" plein écran à afficher quand une page
 * de contenu n'arrive pas à charger ses données depuis le backend.
 *
 * Props :
 *   - message    (string)   — texte secondaire affiché sous le titre.
 *   - title      (string)   — titre principal (par défaut "Connexion impossible").
 *   - onRetry    (function) — callback du bouton "Réessayer". Par défaut, recharge la page.
 *   - retryLabel (string)   — texte du bouton (par défaut "Réessayer").
 */
export function ConnectionError({
  message = "Vérifiez votre connexion internet et réessayez.",
  title = "Connexion impossible",
  onRetry,
  retryLabel = "Réessayer",
}) {
  const handleRetry = () => {
    if (typeof onRetry === "function") {
      onRetry();
    } else {
      window.location.reload();
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-light-bg px-4">
      <div className="flex flex-col items-center gap-5 text-center max-w-sm">
        <div className="w-16 h-16 rounded-full bg-navy/8 flex items-center justify-center">
          <svg
            className="w-8 h-8 text-navy/40"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={1.5}
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
            />
          </svg>
        </div>
        <div>
          <p className="text-navy font-bold text-lg mb-1">{title}</p>
          <p className="text-sm text-[#666] leading-relaxed">{message}</p>
        </div>
        <button
          onClick={handleRetry}
          className="px-6 py-2.5 bg-navy text-white text-sm font-semibold rounded-full hover:bg-navy/80 transition-colors duration-200"
        >
          {retryLabel}
        </button>
      </div>
    </div>
  );
}
