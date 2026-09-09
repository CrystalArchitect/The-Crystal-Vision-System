import './globals.css';

export const metadata = {
  title: 'The Library — The Living Archive of TerAustralis',
  description:
    'The canonical source of truth and memory for TerAustralis Incognita. Reads open to all humans and AI systems; writes consent-governed. Every entry carries provenance.'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <div className="wrap">
          <nav className="nav">
            <a className="brand" href="/">
              THE <span>LIBRARY</span>
            </a>
            <div className="links">
              <a href="/search">Search</a>
              <a href="/api/entries">API</a>
              <a href="/steward">Steward</a>
            </div>
          </nav>
          {children}
          <div className="footer">
            The Library · The Living Archive of TerAustralis Incognita · MemoryCore is the vault
            beneath · Evidence before conclusion · Consent before influence · Reads open to humans
            &amp; AI · ABN 70 741 068 059
          </div>
        </div>
      </body>
    </html>
  );
}
