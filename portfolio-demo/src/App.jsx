import status from "./status.json";
import LivePovDemo from "./LivePovDemo.jsx";

function Badge({ value }) {
  const cls = value.replace(/\s+/g, "-").toLowerCase();
  return <span className={`badge badge-${cls}`}>{value}</span>;
}

const problems = [
  ["Manual releases", "Releasing a new version means copying files and starting the app by hand."],
  ["Server-specific settings", "The app relies on settings stored on one particular computer."],
  ["Environment drift", "The test version and the real version can slowly become different."],
  ["Unclear health", "The team cannot quickly tell if the app is ready for people to use."],
  ["Manual rollback", "When an update fails, going back to the old version takes several manual steps."],
  ["Manual scaling", "Supporting more users may mean setting up another server by hand."],
];

const criteria = [
  ["Repeatability", "Can someone else run the app without knowing secret steps?", "Versioned configuration and deployment files."],
  ["Health visibility", "Can the platform tell if the app is working and ready?", "/health, /ready, and OpenShift probes."],
  ["Separate settings", "Can settings change without editing the app itself?", "DATABASE_URL, environment variables, ConfigMap, and Secret references."],
  ["Standard deployment", "Are release steps written as code instead of kept in someone’s memory?", "Dockerfile and OpenShift manifests."],
  ["Repeatable environment", "Can the platform setup be recreated from written instructions?", "Terraform configuration."],
  ["Safe way back", "If an update fails, is there a clear path back to the last version?", "OpenShift rollout and rollback design. Live rollback was not executed."],
];

export default function App() {
  return (
    <main className="page">
      <header className="hero">
        <h1>Hybrid Cloud Modernization Proof-of-Value</h1>
        <p className="subtitle">
          Keep the working order app. Fix the messy way it runs.
        </p>
        <p className="lede">
          A fictional company has an app that accepts customer orders. The app
          does its job, but every update takes too much manual work. This project
          shows how to make releases safer and more consistent without rebuilding
          the whole app.
        </p>
        <div className="hero-flow" aria-label="Modernization summary">
          <div><small>Starting point</small><strong>Working app</strong><span>Messy release process</span></div>
          <span className="hero-arrow" aria-hidden="true">→</span>
          <div><small>Modernized result</small><strong>Same working app</strong><span>Clear, repeatable process</span></div>
        </div>
        <div className="summary-chips">
          <span><b>01</b><strong>Orders still work</strong>The customer experience stays the same.</span>
          <span><b>02</b><strong>Updates become safer</strong>The app is easier to check and recover.</span>
          <span><b>03</b><strong>Change happens in steps</strong>The existing ERP can stay where it is.</span>
        </div>
      </header>

      <section className="intro-section">
        <p className="section-kicker">What is this project?</p>
        <h2>The app is useful. Updating it is the hard part.</h2>
        <p className="section-intro">
          Customers can already create and view orders. That part works. The
          problem is everything around the app: starting it, changing its
          settings, checking if it is healthy, and fixing a bad update.
        </p>
        <aside className="analogy">
          <strong>The recipe works. The kitchen is messy.</strong>
          <span>Instead of rewriting the recipe, this project modernizes the kitchen.</span>
        </aside>
      </section>

      <section>
        <p className="section-kicker">The problem in normal English</p>
        <h2>Small tasks take too many manual steps</h2>
        <div className="problem-grid">
          {problems.map(([term, text]) => (
            <article key={term}>
              <p>{text}</p>
              <small>{term}</small>
            </article>
          ))}
        </div>
      </section>

      <section>
        <p className="section-kicker">What are the options?</p>
        <h2>There are three reasonable choices</h2>
        <div className="cards strategy-cards">
          <article>
            <small>Rehost / lift-and-shift</small>
            <h3>Move it without changing much</h3>
            <p>Put the same app on a new server. This is quick, but the old release problems come along with it.</p>
          </article>
          <article className="selected">
            <span className="selection-label">Selected for this PoV</span>
            <small>Replatform</small>
            <h3>Keep the app, modernize how it runs</h3>
            <p>Keep the useful code. Improve how the app is packaged, configured, checked, updated, and restored.</p>
          </article>
          <article>
            <small>Refactor</small>
            <h3>Rewrite larger parts of the application</h3>
            <p>Rebuild major parts of the app. This can help later, but it takes more time and adds risk that was not needed yet.</p>
          </article>
        </div>
        <aside className="why-box">
          <strong>Why replatform?</strong>
          <span>The order features already work. The first step should fix the release process, not replace useful code.</span>
        </aside>
      </section>

      <LivePovDemo />

      <section>
        <p className="section-kicker">Before vs after</p>
        <h2>Same app. A much clearer release process.</h2>
        <div className="before-after">
          <article>
            <small>Before</small>
            <h3>How a release used to work</h3>
            <ol>
              <li>Copy application files.</li>
              <li>Change configuration manually.</li>
              <li>Start the application manually.</li>
              <li>Check whether it seems to work.</li>
              <li>Diagnose problems manually.</li>
              <li>Restore old files if something breaks.</li>
            </ol>
            <p className="technical-line">Technical model: direct Flask process and host-local SQLite.</p>
          </article>
          <article className="after-card">
            <small>After</small>
            <h3>How the modernized model works</h3>
            <ol>
              <li>The application is packaged consistently.</li>
              <li>Environment settings are supplied separately.</li>
              <li>The release steps are written down as code.</li>
              <li>The platform checks if the app works and is ready.</li>
              <li>Updates happen in a controlled order.</li>
              <li>The platform has a defined way to restore an older version.</li>
            </ol>
            <p className="technical-line">Docker · ConfigMap / Secret · OpenShift Deployment · liveness/readiness probes · rolling update · rollback</p>
          </article>
        </div>
        <p className="conclusion">The business logic did not need a full rewrite. The operating process became more repeatable.</p>
      </section>

      <section>
        <p className="section-kicker">The technology roles</p>
        <h2>Three tools, three simple jobs</h2>
        <div className="cards technology-cards">
          <article>
            <span className="tech-icon" aria-hidden="true">D</span>
            <h3>Docker</h3>
            <p>Packs the app and what it needs into one consistent package.</p>
            <p><strong>Why it helps:</strong> The same package can be used in different places.</p>
            <p className="technical-line">Dockerfile implemented. GitHub Actions tested the image BUILD. That is not an OpenShift deployment.</p>
          </article>
          <article>
            <span className="tech-icon openshift-icon" aria-hidden="true">O</span>
            <h3>Red Hat OpenShift</h3>
            <p>Runs the packaged app and watches over it.</p>
            <p><strong>Why it helps:</strong> It can check the app, manage updates, and limit how many resources it uses.</p>
            <p className="technical-line">Deployment, Service, Route, ConfigMap, Secret references, probes, and a NetworkPolicy baseline.</p>
          </article>
          <article>
            <span className="tech-icon terraform-icon" aria-hidden="true">T</span>
            <h3>Terraform</h3>
            <p>Writes the environment setup as code.</p>
            <p><strong>Why it helps:</strong> The setup can be reviewed and recreated instead of remembered.</p>
            <p className="technical-line">GitHub Actions tested terraform fmt, init, and validate. That is not terraform plan or apply.</p>
          </article>
        </div>
      </section>

      <section>
        <p className="section-kicker">Hybrid cloud</p>
        <h2>Why keep part of the system on-site?</h2>
        <p className="section-intro">
          “Hybrid cloud” means some parts can use a modern cloud platform while
          other parts stay in the company’s own building or data center. Here,
          the Order Intake app can move first. The older ERP system can stay
          on-site and connect through a clear boundary.
        </p>
        <div className="architecture" aria-label="Hybrid cloud target architecture">
          <div className="arch-node customer-node"><small>People using the app</small><strong>Customers</strong></div>
          <span className="down-arrow" aria-hidden="true">↓</span>
          <div className="arch-node route-node"><small>Secure front door</small><strong>OpenShift entry point</strong><span>Technical term: Route</span></div>
          <span className="down-arrow" aria-hidden="true">↓</span>
          <div className="arch-node service-node"><small>The part being modernized</small><strong>Order Intake Service</strong><span>Target: 1 replica for this SQLite PoV</span></div>
          <div className="dependency-grid">
            <div className="arch-node"><small>Stores order data</small><strong>Data storage</strong><span>SQLite now · shared database later</span></div>
            <div className="arch-node"><small>Connects to the existing system</small><strong>Integration boundary</strong><span>→ On-site ERP</span></div>
          </div>
        </div>
        <p className="conclusion">This lets the company modernize one part of the system without forcing a risky all-at-once migration.</p>
        <details>
          <summary>Technical details and limitations</summary>
          <ul>
            <li>OpenShift Route is the entry point that sends traffic to the application.</li>
            <li>The target uses <code>replicas: 1</code> because SQLite is local storage.</li>
            <li>SQLite on <code>emptyDir</code> is PoV-only, not highly available, and pod replacement may lose data.</li>
            <li>Horizontal scaling requires an external shared database.</li>
            <li>Database modernization is outside this PoV.</li>
            <li>This is a target architecture. OpenShift deployment was not executed.</li>
            <li>IBM Cloud is not claimed.</li>
          </ul>
        </details>
      </section>

      <section>
        <p className="section-kicker">Discovery</p>
        <h2>Do not treat guesses like facts</h2>
        <p className="section-intro">Before choosing technology, we need to know what is true. This case study separates confirmed details, temporary assumptions, and questions that a real customer must answer.</p>
        <div className="cards discovery-cards">
          <article>
            <span className="discovery-number">1</span>
            <h3>What we know</h3>
            <p>Flask handles order intake. SQLite is stored on a host. The ERP stays on-premises. A failed start blocks new order capture.</p>
          </article>
          <article>
            <span className="discovery-number">2</span>
            <h3>What we assumed for this PoV</h3>
            <p>The API is internal. SQLite is enough for this small demonstration. An entry point and automatic checks are a useful first step.</p>
          </article>
          <article>
            <span className="discovery-number">3</span>
            <h3>What a customer must confirm</h3>
            <p>Who can sign in, where data may live, how the ERP connects, who owns the system, and how quickly it must recover.</p>
          </article>
        </div>
        <details>
          <summary>More discovery questions</summary>
          <p><strong>Business:</strong> What process depends on this app? What happens after a failed release? How often does it deploy? What downtime is acceptable? Which systems cannot move?</p>
          <p><strong>Technical:</strong> Which runtime, authentication, network, secret store, observability tools, integrations, and recovery targets are required?</p>
        </details>
      </section>

      <section>
        <p className="section-kicker">Success criteria</p>
        <h2>How do we know this is actually better?</h2>
        <div className="criteria-list">
          {criteria.map(([name, plain, evidence]) => (
            <article key={name}>
              <h3>{name}</h3>
              <p>{plain}</p>
              <small><strong>Evidence:</strong> {evidence}</small>
            </article>
          ))}
        </div>
      </section>

      <section>
        <p className="section-kicker">Validation status</p>
        <h2>What was built, tested, or only designed?</h2>
        <p>These labels make the evidence clear. “Not executed” stays visible so this page never claims more than the project proved.</p>
        <div className="status-key">
          <div><Badge value="IMPLEMENTED" /><span>The code or configuration exists.</span></div>
          <div><Badge value="TESTED" /><span>I actually ran a test or validation for it.</span></div>
          <div><Badge value="TESTED IN CI" /><span>GitHub Actions ran the check. A Docker image build is not an OpenShift deploy. Terraform validate is not plan or apply.</span></div>
          <div><Badge value="ARCHITECTED" /><span>The design is documented, but the real runtime was not built or connected.</span></div>
          <div><Badge value="NOT EXECUTED" /><span>The artifact may exist, but I have not run it in that environment.</span></div>
        </div>
        <p className="note">{status.note}</p>
        <div className="table-wrap">
          <table>
            <thead><tr><th>Item</th><th>Status</th></tr></thead>
            <tbody>
              {status.items.map((row) => (
                <tr key={row.name}><td>{row.name}</td><td><Badge value={row.status} /></td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <details>
          <summary>Technical artifact inventory</summary>
          <ul>
            <li>Legacy and modernized Flask applications</li>
            <li>Dockerfile and <code>.dockerignore</code></li>
            <li>OpenShift Deployment, Service, ConfigMap, Secret template, NetworkPolicy baseline, and <code>route.openshift.io/v1</code> Route</li>
            <li>Terraform Kubernetes provider, namespace, quotas, limits, configuration, and service account</li>
            <li>Automated tests, validation scripts, and GitHub Actions workflow</li>
          </ul>
        </details>
      </section>
    </main>
  );
}
