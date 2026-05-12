// ===== Supabase Client =====
const SUPABASE_URL = 'https://your-project.supabase.co';
const SUPABASE_KEY = 'your-anon-key';

let supabase = null;
try {
  if (window.supabase && SUPABASE_URL !== 'https://your-project.supabase.co') {
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  }
} catch (e) {
  console.warn('Supabase not available, using sample data');
}

// ===== Sample Publications Data =====
const samplePublications = [
  {
    id: 1,
    title: 'A Novel Approach to Large Language Model Fine-tuning with Adaptive Regularization',
    authors: 'Wang, X., Zhang, Y., Li, M.',
    highlight_author: 'Wang, X.',
    journal: 'Nature Machine Intelligence',
    year: 2025,
    jcr_quartile: 'Q1',
    doi: '10.1038/s42256-025-00001-0',
    arxiv: '2501.00001',
  },
  {
    id: 2,
    title: 'Multi-Modal Understanding in Open-Domain Question Answering Systems',
    authors: 'Wang, X., Chen, H., Liu, J., Wu, K.',
    highlight_author: 'Wang, X.',
    journal: 'IEEE Transactions on Pattern Analysis and Machine Intelligence',
    year: 2025,
    jcr_quartile: 'Q1',
    doi: '10.1109/TPAMI.2025.00001',
  },
  {
    id: 3,
    title: 'Efficient Graph Neural Networks for Large-Scale Knowledge Graph Reasoning',
    authors: 'Wang, X., Zhou, T., Huang, R.',
    highlight_author: 'Wang, X.',
    journal: 'NeurIPS 2024',
    year: 2024,
    jcr_quartile: 'Q1',
    arxiv: '2412.00001',
  },
  {
    id: 4,
    title: 'Self-Supervised Representation Learning for Biomedical Entity Linking',
    authors: 'Li, S., Wang, X., Zhao, P., Chen, W.',
    highlight_author: 'Wang, X.',
    journal: 'Bioinformatics',
    year: 2025,
    jcr_quartile: 'Q2',
    doi: '10.1093/bioinformatics/btae001',
  },
  {
    id: 5,
    title: 'A Survey of Prompt Engineering Strategies for Foundation Models',
    authors: 'Wang, X., Kim, D., Patel, R., Garcia, M.',
    highlight_author: 'Wang, X.',
    journal: 'ACM Computing Surveys',
    year: 2024,
    jcr_quartile: 'Q1',
    doi: '10.1145/3600000',
  },
  {
    id: 6,
    title: 'Cross-Lingual Transfer Learning with Minimal Supervision',
    authors: 'Wang, X., Tanaka, H.',
    highlight_author: 'Wang, X.',
    journal: 'ACL 2024',
    year: 2024,
    jcr_quartile: 'Q1',
    arxiv: '2406.00001',
  },
  {
    id: 7,
    title: 'Data Augmentation Techniques for Low-Resource Neural Machine Translation',
    authors: 'Chen, L., Wang, X., Yang, F.',
    highlight_author: 'Wang, X.',
    journal: 'Machine Translation',
    year: 2023,
    jcr_quartile: 'Q3',
    doi: '10.1007/s10590-023-00001-0',
  },
  {
    id: 8,
    title: 'Benchmarking Robustness of Vision-Language Models under Distribution Shift',
    authors: 'Wang, X., Park, S., Anderson, T.',
    highlight_author: 'Wang, X.',
    journal: 'CVPR 2024',
    year: 2024,
    jcr_quartile: 'Q1',
    arxiv: '2403.00001',
  },
];

// ===== DOM Elements =====
const pubList = document.getElementById('pub-list');
const statCards = document.querySelectorAll('.stat-card');
const filterBtns = document.querySelectorAll('.filter-btn');

// ===== Counter Animation =====
function easeOutExpo(t) {
  return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
}

function animateCounter(element, target, duration = 1500) {
  const start = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easedProgress = easeOutExpo(progress);

    const current = Math.floor(start + (target - start) * easedProgress);
    element.textContent = current.toLocaleString();

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = target.toLocaleString();
    }
  }

  requestAnimationFrame(update);
}

function replayAnimation(card) {
  const numberEl = card.querySelector('.stat-number');
  const target = parseInt(card.getAttribute('data-target'), 10);

  // Add ripple effect
  const ripple = document.createElement('span');
  ripple.className = 'ripple';
  card.appendChild(ripple);

  ripple.addEventListener('animationend', () => {
    ripple.remove();
  });

  // Reset and replay
  numberEl.textContent = '0';
  animateCounter(numberEl, target);
}

// Click handler for stat cards
statCards.forEach(card => {
  card.addEventListener('click', () => {
    replayAnimation(card);
  });
});

// ===== Intersection Observer for Auto-Animation =====
let hasAnimated = false;

const statsObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !hasAnimated) {
        hasAnimated = true;
        statCards.forEach(card => {
          const numberEl = card.querySelector('.stat-number');
          const target = parseInt(card.getAttribute('data-target'), 10);
          // Stagger the animations
          const delay = Array.from(statCards).indexOf(card) * 120;
          setTimeout(() => {
            animateCounter(numberEl, target);
          }, delay);
        });
        statsObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.4 }
);

const statsSection = document.getElementById('stats');
if (statsSection) {
  statsObserver.observe(statsSection);
}

// ===== Publications Rendering =====
function createPubCard(pub) {
  const jcrClass = pub.jcr_quartile ? `jcr-${pub.jcr_quartile.toLowerCase()}` : '';
  const jcrLabel = pub.jcr_quartile ? `JCR ${pub.jcr_quartile}` : '';

  // Use shimmer variant for Q1 for extra visual flair
  const jcrTagClass = pub.jcr_quartile === 'Q1' ? 'jcr-q1-shimmer' : jcrClass;

  const authorsHtml = pub.authors.replace(
    pub.highlight_author || '',
    `<span class="highlight">${pub.highlight_author || ''}</span>`
  );

  let linksHtml = '';
  if (pub.doi) {
    linksHtml += `<a href="https://doi.org/${pub.doi}" class="pub-link" target="_blank" rel="noopener">DOI</a>`;
  }
  if (pub.arxiv) {
    linksHtml += `<a href="https://arxiv.org/abs/${pub.arxiv}" class="pub-link" target="_blank" rel="noopener">arXiv</a>`;
  }

  return `
    <div class="pub-card" data-jcr="${pub.jcr_quartile || ''}">
      <div class="pub-card-header">
        <div class="pub-title">
          <a href="${pub.doi ? `https://doi.org/${pub.doi}` : '#'}" target="_blank" rel="noopener">${pub.title}</a>
        </div>
        ${jcrLabel ? `<span class="jcr-tag ${jcrTagClass}">${jcrLabel}</span>` : ''}
      </div>
      <div class="pub-authors">${authorsHtml}</div>
      <div class="pub-meta">
        <span class="pub-journal">${pub.journal}</span>
        <span>${pub.year}</span>
      </div>
      ${linksHtml ? `<div class="pub-links">${linksHtml}</div>` : ''}
    </div>
  `;
}

function renderPublications(publications) {
  if (!pubList) return;

  if (!publications || publications.length === 0) {
    pubList.innerHTML = '<div class="empty">No publications yet.</div>';
    return;
  }

  pubList.innerHTML = publications.map(createPubCard).join('');
}

// ===== Filter Functionality =====
let currentFilter = 'all';

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.getAttribute('data-filter');

    const cards = pubList.querySelectorAll('.pub-card');
    cards.forEach(card => {
      if (currentFilter === 'all' || card.getAttribute('data-jcr') === currentFilter) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
});

// ===== Data Fetching =====
async function fetchPublications() {
  // Try Supabase first
  if (supabase) {
    try {
      const { data, error } = await supabase
        .from('publications')
        .select('*')
        .order('year', { ascending: false });

      if (error) throw error;
      if (data && data.length > 0) {
        return data;
      }
    } catch (e) {
      console.warn('Supabase fetch failed, using sample data:', e.message);
    }
  }

  // Fallback to sample data
  return samplePublications;
}

async function loadPublications() {
  if (!pubList) return;

  pubList.innerHTML = '<div class="loading">Loading publications...</div>';

  try {
    const publications = await fetchPublications();
    renderPublications(publications);

    // Update stats counters with real data
    updateStats(publications);
  } catch (e) {
    pubList.innerHTML = '<div class="error">Failed to load publications. Please try again later.</div>';
    console.error('Error loading publications:', e);
  }
}

function updateStats(publications) {
  const jcrQ1Count = publications.filter(p => p.jcr_quartile === 'Q1').length;

  // Update the JCR Q1 counter target
  const jcrCard = document.querySelector('[data-target]');
  const jcrQ1Card = document.getElementById('counter-jcrq1')?.parentElement;
  if (jcrQ1Card) {
    jcrQ1Card.setAttribute('data-target', jcrQ1Count);
  }

  // Update publication count
  const pubCard = document.getElementById('counter-publications')?.parentElement;
  if (pubCard) {
    pubCard.setAttribute('data-target', publications.length);
  }
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
  loadPublications();
});
